import asyncio
import threading
import tkinter as tk
from tkinter import ttk

def run_async(coro):
    asyncio.run(coro)

class SimulationTab:
    def __init__(self, parent):
        self.frame = parent
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Labelframe(self.frame, text="Scenario Injection")
        frame.pack(fill="x", padx=20, pady=20)
        
        ttk.Button(frame, text="Inject Normal Trading", command=lambda: threading.Thread(target=run_async, args=(self.inject_normal(),)).start()).pack(fill="x", padx=10, pady=5)
        ttk.Button(frame, text="Inject Spoofing Scenario", command=lambda: threading.Thread(target=run_async, args=(self.inject_spoofing(),)).start()).pack(fill="x", padx=10, pady=5)
        ttk.Button(frame, text="Inject Wash Trading", command=lambda: threading.Thread(target=run_async, args=(self.inject_wash(),)).start()).pack(fill="x", padx=10, pady=5)
        
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame, text="\ud83d\udd04 Reset Scenario", command=self.reset_scenario).pack(fill="x", padx=10, pady=5)
        
        scale_frame = ttk.Frame(self.frame)
        scale_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(scale_frame, text="Aggressiveness").pack(side="left")
        self.scale = ttk.Scale(scale_frame, from_=0, to=100, orient="horizontal")
        self.scale.pack(side="left", fill="x", expand=True, padx=10)
        
        # Narrative Mode Panel
        narrative_frame = ttk.LabelFrame(self.frame, text="\ud83d\udcd6 Narrative Mode (Educational)", padding=10)
        narrative_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.narrative_text = tk.Text(narrative_frame, height=8, wrap="word", font=("Consolas", 9), 
                                      bg="#f0f0f0", fg="#333", state="disabled")
        self.narrative_text.pack(fill="both", expand=True)
        
        # Add initial message
        self.add_narrative("System initialized. Ready for trading scenarios.")
        self.add_narrative("Click a scenario button to begin simulation...")

    async def inject_normal(self):
        print("Injecting Normal Trading (Scenario A)...")
        self.add_narrative("📊 SCENARIO A: Normal Trading - Legitimate participants trading...")
        # Scenario A: Boring, reliable, non-repetitive
        # t1	CEX	BTC-USDT	BUY	43000	0.05	Alice	EXECUTE
        # t2	CEX	BTC-USDT	SELL	43001	0.04	Bob	EXECUTE
        # t3	DEX	ETH-USDC	BUY	2400	0.10	Carol	EXECUTE
        # t4	CEX	BTC-USDT	BUY	42998	0.03	Dave	EXECUTE
        # t5	CEX	BTC-USDT	BUY	42999	0.02	Alice	CANCEL (Simulated as trade with quantity=0 or specific flag if supported, here just standard small trade)
        # Note: Normalization usually handles Cancels, but here we simulate 'Cancelled' as just missing fills or explicit small updates.
        # For this stream, we just send executions as that's what triggers surveillance.
        
        scenarios = [
            {"time": 0, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY", "price": 43000.0, "qty": 0.05, "pid": "Alice"},
            {"time": 1, "venue": "CEX", "instrument": "BTC-USDT", "side": "SELL", "price": 43001.0, "qty": 0.04, "pid": "Bob"},
            {"time": 1, "venue": "DEX", "instrument": "ETH-USDC", "side": "BUY", "price": 2400.0, "qty": 0.10, "pid": "Carol"},
            {"time": 1, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY", "price": 42998.0, "qty": 0.03, "pid": "Dave"},
            {"time": 1, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY", "price": 42999.0, "qty": 0.02, "pid": "Alice"}
        ]

        import grpc
        import trades_pb2
        import trades_pb2_grpc
        import time
        from datetime import datetime

        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = trades_pb2_grpc.TradeStreamStub(channel)
            
            for s in scenarios:
                trade = trades_pb2.CanonicalTrade(
                    event_time_ns=int(time.time() * 1e9),
                    venue=s["venue"],
                    instrument=s["instrument"],
                    side=s["side"],
                    price=s["price"],
                    quantity=s["qty"],
                    participant_id=s["pid"],
                    origin="CEX" if s["venue"] == "CEX" else "DEX",
                    order_id=f"ORD-{int(time.time())}",
                    execution_id=f"EXEC-{int(time.time())}"
                )
                
                batch = trades_pb2.TradeBatch(trades=[trade])
                try:
                    await stub.PublishTrades(batch)
                    print(f"Sent: {s['pid']} {s['side']} {s['qty']}")
                except Exception as e:
                    print(f"Failed to send: {e}")
                
                await asyncio.sleep(1.0) # Slow injection
        
        self.add_narrative("\u2713 Normal trading complete - No suspicious patterns detected.")

    async def inject_spoofing(self):
        print("Injecting Spoofing Scenario (Scenario B)...")
        self.add_narrative("⚠️ SCENARIO B: Spoofing Attack - Eve placing large fake orders...")
        
        # Scenario B: High Cancel Ratio + Large Orders
        # Eve places large BUY orders to create pressure, then CANCELS them, then SELLS small.
        # Sequence:
        # 1. 10.0 BUY (Cancel)
        # 2. 10.0 BUY (Cancel)
        # 3. 10.0 BUY (Cancel)
        # 4. 0.5 SELL (Execute)
        
        scenarios = [
            {"time": 0, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY", "price": 43100.0, "qty": 10.0, "pid": "Eve", "op": "CANCEL"},
            {"time": 0, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY", "price": 43099.0, "qty": 10.0, "pid": "Eve", "op": "CANCEL"},
            {"time": 0, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY", "price": 43098.0, "qty": 10.0, "pid": "Eve", "op": "CANCEL"},
            {"time": 1, "venue": "CEX", "instrument": "BTC-USDT", "side": "SELL", "price": 43000.0, "qty": 0.5,  "pid": "Eve", "op": "EXECUTE"},
        ]

        import grpc
        import trades_pb2
        import trades_pb2_grpc
        import time

        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = trades_pb2_grpc.TradeStreamStub(channel)
            
            for s in scenarios:
                # Map "op" to side for our feature extractor hack
                # If op is CANCEL, we send side="CANCEL"
                side = "CANCEL" if s["op"] == "CANCEL" else s["side"]
                
                trade = trades_pb2.CanonicalTrade(
                    event_time_ns=int(time.time() * 1e9),
                    venue=s["venue"],
                    instrument=s["instrument"],
                    side=side,
                    price=s["price"],
                    quantity=s["qty"],
                    participant_id=s["pid"],
                    origin="CEX",
                    order_id=f"ORD-SPOOF-{int(time.time()*1000)}",
                    execution_id=f"EXEC-{int(time.time()*1000)}"
                )
                
                batch = trades_pb2.TradeBatch(trades=[trade])
                try:
                    await stub.PublishTrades(batch)
                    print(f"Sent Spoof: {s['pid']} {side} {s['qty']}")
                except Exception as e:
                    print(f"Failed to send: {e}")
                
                await asyncio.sleep(0.5) 
        
        self.add_narrative("🚨 Abnormal behavior detected! High cancel ratio observed.")
        self.add_narrative("📋 Case opened for review - Check Detection Signals tab.")

    async def inject_wash(self):
        print("Injecting Wash Trading Scenario (Scenario C)...")
        self.add_narrative("⚠️ SCENARIO C: Wash Trading - Frank & Grace creating fake volume...")
        
        # Scenario C: Wash Trading - Matched orders between related accounts
        # Frank and Grace trade back and forth at the same price to create fake volume
        # Pattern: BUY from Frank, SELL from Grace, repeat
        
        scenarios = [
            {"time": 0, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY",  "price": 43000.0, "qty": 1.0, "pid": "Frank"},
            {"time": 0, "venue": "CEX", "instrument": "BTC-USDT", "side": "SELL", "price": 43000.0, "qty": 1.0, "pid": "Grace"},
            {"time": 1, "venue": "CEX", "instrument": "BTC-USDT", "side": "SELL", "price": 43000.0, "qty": 1.0, "pid": "Frank"},
            {"time": 1, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY",  "price": 43000.0, "qty": 1.0, "pid": "Grace"},
            {"time": 2, "venue": "CEX", "instrument": "BTC-USDT", "side": "BUY",  "price": 43000.0, "qty": 1.0, "pid": "Frank"},
            {"time": 2, "venue": "CEX", "instrument": "BTC-USDT", "side": "SELL", "price": 43000.0, "qty": 1.0, "pid": "Grace"},
        ]

        import grpc
        import trades_pb2
        import trades_pb2_grpc
        import time

        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = trades_pb2_grpc.TradeStreamStub(channel)
            
            for s in scenarios:
                trade = trades_pb2.CanonicalTrade(
                    event_time_ns=int(time.time() * 1e9),
                    venue=s["venue"],
                    instrument=s["instrument"],
                    side=s["side"],
                    price=s["price"],
                    quantity=s["qty"],
                    participant_id=s["pid"],
                    origin="CEX",
                    order_id=f"ORD-WASH-{int(time.time()*1000)}",
                    execution_id=f"EXEC-{int(time.time()*1000)}"
                )
                
                batch = trades_pb2.TradeBatch(trades=[trade])
                try:
                    await stub.PublishTrades(batch)
                    print(f"Sent Wash: {s['pid']} {s['side']} {s['qty']}")
                except Exception as e:
                    print(f"Failed to send: {e}")
                
                await asyncio.sleep(0.5)
        
        self.add_narrative("\ud83d\udea8 Suspicious pattern identified! Matched buy/sell orders detected.")
        self.add_narrative("\ud83d\udccb Wash trading case opened - Review Cases tab.")

    def add_narrative(self, message):
        """Add a narrative message to the educational panel"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.narrative_text.config(state="normal")
        self.narrative_text.insert("end", f"[{timestamp}] {message}\n")
        self.narrative_text.see("end")
        self.narrative_text.config(state="disabled")
    
    def reset_scenario(self):
        """Reset the surveillance system for a clean restart"""
        print("Resetting scenario...")
        self.add_narrative("🔄 SCENARIO RESET - Clearing all trades and cases...")
        
        # TODO: Add gRPC call to engine to clear TRADES_BUFFER and cases
        # For now, just clear the UI
        self.add_narrative("✓ System reset complete. Ready for new scenario.")
        self.add_narrative("---" * 20)

