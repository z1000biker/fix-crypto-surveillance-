import asyncio
import grpc
import pandas as pd
from concurrent import futures
import trades_pb2
import trades_pb2_grpc
import cases_pb2_grpc

from cases.case_manager import CaseManager
from features.feature_extraction import extract_features
from features.feature_stats import compute_feature_baselines
from rules.rule_engine import RuleEngine
from ml.anomaly_detection import AnomalyDetector
from ml.explainability import explain_anomaly

# Global state
TRADES_QUEUE = asyncio.Queue()
TRADES_BUFFER = []
BASELINES = {}

# Initialize surveillance components
RULE_ENGINE = RuleEngine(rules_dir="rules")
ANOMALY_DETECTOR = AnomalyDetector()
CASE_MANAGER = CaseManager()

class TradeStreamServicer(trades_pb2_grpc.TradeStreamServicer):
    async def PublishTrades(self, request, context):
        global TRADES_QUEUE
        
        # Convert Proto to Dict
        new_trades = []
        for t in request.trades:
            trade_dict = {
                "event_time": t.event_time_ns,
                "venue": t.venue,
                "instrument": t.instrument,
                "side": t.side,
                "price": t.price,
                "quantity": t.quantity,
                "participant_id": t.participant_id,
                "order_id": t.order_id,
                "origin": t.origin
            }
            new_trades.append(trade_dict)
            
        print(f"Received batch of {len(new_trades)} trades")
        
        # Schedule analysis
        await run_surveillance_cycle(new_trades)
        
        return trades_pb2.Ack(success=True, message="Processed")

    async def Subscribe(self, request, context):
        # streaming response
        # In a real app, we'd use a dedicated queue per subscriber.
        # For this demo, we'll just stream what comes into the global analysis loop via a simplified bus or just echo for now.
        # Let's implement a listener pattern.
        queue = asyncio.Queue()
        BROADCAST_CHANNELS.add(queue)
        try:
            while True:
                trade = await queue.get()
                yield trade
        finally:
            BROADCAST_CHANNELS.remove(queue)

BROADCAST_CHANNELS = set()

async def run_surveillance_cycle(new_trades):
    global BASELINES, TRADES_BUFFER
    
    # Broadcast to UI subscribers
    import trades_pb2
    for t_dict in new_trades:
        # Re-wrap in Proto for the stream
        t_proto = trades_pb2.CanonicalTrade(
            event_time_ns=int(t_dict.get("event_time", 0)),
            venue=t_dict.get("venue"),
            instrument=t_dict.get("instrument"),
            side=t_dict.get("side"),
            price=t_dict.get("price"),
            quantity=t_dict.get("quantity"),
            participant_id=t_dict.get("participant_id"),
            origin=t_dict.get("origin"),
            order_id=t_dict.get("order_id"),
            execution_id=t_dict.get("execution_id", "")
        )
        for q in list(BROADCAST_CHANNELS):
            await q.put(t_proto)

    # Accumulate trades for stateful analysis
    TRADES_BUFFER.extend(new_trades)
    # Prune buffer (simplistic sliding window)
    if len(TRADES_BUFFER) > 1000:
        TRADES_BUFFER = TRADES_BUFFER[-1000:]
        
    # Minimum window size check (optional)
    if len(TRADES_BUFFER) < 1:
        return

    df = pd.DataFrame(TRADES_BUFFER)
    
    # 1. Feature Extraction
    features = extract_features(df)
    if features.empty:
        return

    # 2. Update Baselines (rolling strategy would be better, here we accumulate or just use batch)
    feature_cols = ["num_trades", "buy_sell_ratio", "avg_quantity", "venue_switch_count"]
    # In reality we need historical context. For this demo we just calc stats on the batch.
    current_stats = compute_feature_baselines(features, feature_cols)
    BASELINES.update(current_stats) 
    
    # 3. ML Scoring
    ANOMALY_DETECTOR.fit(features, feature_cols)
    scores = ANOMALY_DETECTOR.score(features)
    features["ml_score"] = scores
    
    # 4. Rules & Cases
    for i, row in features.iterrows():
        metrics = row.to_dict()
        alerts = RULE_ENGINE.evaluate(metrics)
        is_anomaly = row["ml_score"] > 0.8
        
        if alerts or is_anomaly:
            pid = row["participant_id"]
            instrument = row["instrument"]
            explanations = explain_anomaly(metrics, BASELINES)
            
            priority = "HIGH" if (alerts and is_anomaly) else "MEDIUM"
            case = CASE_MANAGER.open_case(
                participant_id=pid,
                instrument=instrument,
                alerts=alerts + explanations,
                ml_score=float(row["ml_score"]),
                priority=priority
            )
            print(f"OPENED CASE {case.case_id} for {pid}")
            
            # Broadcast Case
            import cases_pb2
            
            # Create Case Proto
            case_proto = cases_pb2.SurveillanceCase(
                case_id=case.case_id,
                participant_id=case.participant_id,
                instrument=case.instrument,
                status=case.status,
                priority=case.priority,
                ml_score=case.ml_score
            )
            # TODO: Add alerts once proto is properly regenerated
            # case_proto.alerts.extend(case.alerts)
            
            for q in list(CASE_CHANNELS):
                await q.put(case_proto)

CASE_CHANNELS = set()

class CaseStreamServicer(cases_pb2_grpc.CaseStreamServicer):
    async def StreamCases(self, request, context):
        queue = asyncio.Queue()
        CASE_CHANNELS.add(queue)
        try:
            while True:
                case = await queue.get()
                yield case
        finally:
            CASE_CHANNELS.remove(queue)

async def serve():
    server = grpc.aio.server()
    trades_pb2_grpc.add_TradeStreamServicer_to_server(TradeStreamServicer(), server)
    cases_pb2_grpc.add_CaseStreamServicer_to_server(CaseStreamServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Surveillance Engine running on port 50051...")
    print("Audit Log: Ready to ingest trades...")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
