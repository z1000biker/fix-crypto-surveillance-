import tkinter as tk
from tkinter import ttk
import threading
import asyncio
from tabs.trade_stream import TradeStreamTab
from tabs.detection_signals import DetectionSignalsTab
from tabs.cases import CasesTab
from tabs.case_details import CaseDetailsTab
from tabs.simulation import SimulationTab

class SurveillanceLabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Market Surveillance Lab")
        self.geometry("1200x800")
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        self.create_tabs()
        
    def create_tabs(self):
        self.trade_tab = self.make_tab("Trade Stream")
        self.signal_tab = self.make_tab("Detection Signals")
        self.cases_tab = self.make_tab("Cases")
        self.detail_tab = self.make_tab("Case Details")
        self.sim_tab = self.make_tab("Simulation Control")
        
        self.trade_stream = TradeStreamTab(self.trade_tab)
        self.detection_signals = DetectionSignalsTab(self.signal_tab)
        self.cases_view = CasesTab(self.cases_tab, app=self)
        self.case_details_view = CaseDetailsTab(self.detail_tab)
        self.simulation_control = SimulationTab(self.sim_tab)

        # Start background subscribers
        threading.Thread(target=self.start_subscriber_thread, daemon=True).start()
        threading.Thread(target=self.start_case_subscriber, daemon=True).start()

    def start_subscriber_thread(self):
        asyncio.run(self.subscribe_to_trades())

    def start_case_subscriber(self):
        asyncio.run(self.subscribe_to_cases())

    async def subscribe_to_cases(self):
        import grpc
        import cases_pb2
        import cases_pb2_grpc
        import trades_pb2 # for Empty
        
        print("Connecting to Case Stream...")
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = cases_pb2_grpc.CaseStreamStub(channel)
            try:
                while True:
                    try:
                        async for case in stub.StreamCases(trades_pb2.Empty()):
                            # Map to UI model
                            case_data = {
                                "id": case.case_id,
                                "participant": case.participant_id,
                                "priority": case.priority,
                                "score": f"{case.ml_score:.2f}",
                                "status": case.status,
                                "instrument": case.instrument
                                # TODO: Add alerts once proto is fixed
                                # "alerts": list(case.alerts)
                            }
                            
                            # Update Cases Tab
                            self.after(0, lambda d=case_data: self.cases_view.add_case(d))
                            
                            # Update Detection Signals (Alerts)
                            # Infer rule type from priority and score
                            if case.priority == "HIGH":
                                rule = "SPOOFING"
                            elif case.ml_score > 0.8:
                                rule = "ANOMALY (ML)"
                            else:
                                rule = "WASH_TRADING"
                            
                            signal_data = {
                                "time": "Now",
                                "rule": rule,
                                "symbol": case.instrument,
                                "participant": case.participant_id
                            }
                            # Store rule type in case_data for investigation view
                            case_data["rule_type"] = rule
                            
                            self.after(0, lambda d=signal_data: self.detection_signals.add_signal(d))
                            
                    except grpc.RpcError as e:
                        print(f"Case Stream disconnected: {e}")
                        await asyncio.sleep(5)
            except asyncio.CancelledError:
                pass


    async def subscribe_to_trades(self):
        import grpc
        import trades_pb2
        import trades_pb2_grpc
        
        print("Connecting to Trade Stream...")
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = trades_pb2_grpc.TradeStreamStub(channel)
            try:
                # Retry loop
                while True:
                    try:
                        print("Subscribing...")
                        async for trade in stub.Subscribe(trades_pb2.Empty()):
                            # Convert to dict for UI
                            data = {
                                "time": trade.event_time_ns, # Raw for now
                                "venue": trade.venue,
                                "instrument": trade.instrument,
                                "side": trade.side,
                                "price": f"{trade.price:.2f}",
                                "qty": f"{trade.quantity:.4f}",
                                "participant": trade.participant_id
                            }
                            # Schedule UI update on main thread
                            self.after(0, lambda d=data: self.trade_stream.add_trade(d))
                    except grpc.RpcError as e:
                        print(f"Stream disconnected: {e}. Retrying in 2s...")
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"Subscriber error: {e}")
                        await asyncio.sleep(2)
            except asyncio.CancelledError:
                pass

    def make_tab(self, name):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name)
        return frame

if __name__ == "__main__":
    app = SurveillanceLabApp()
    app.mainloop()
