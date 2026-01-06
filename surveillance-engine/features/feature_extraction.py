import pandas as pd
import numpy as np
from typing import List, Dict, Any

def extract_features(trades_df: pd.DataFrame, window="5min") -> pd.DataFrame:
    """
    Aggregates raw trades into per-participant behavioral feature vectors.
    """
    if trades_df.empty:
        return pd.DataFrame()

    # Ensure event_time is datetime
    if not pd.api.types.is_datetime64_any_dtype(trades_df["event_time"]):
        trades_df["event_time"] = pd.to_datetime(trades_df["event_time"])

    # Group by Participant + Instrument + Time Window
    grouped = (
        trades_df
        .set_index("event_time")
        .groupby([
            "participant_id",
            "instrument",
            pd.Grouper(freq=window)
        ])
    )

    def calculate_metrics(x):
        # Metrics:
        # 1. Cancel Ratio: (Count of CANCELs) / (Count of EXECUTIONs + CANCELs)
        # 2. Avg Quantity
        # 3. Max Quantity
        # 4. Venue Switching (count of unique venues)
        # 5. Quantity Percentile (of this batch vs 'market' history - simplified to within-batch for now or static threshold)
        
        cancels = x[x["side"] == "CANCEL"]
        executions = x[x["side"].isin(["BUY", "SELL"])]
        
        cancel_count = len(cancels)
        execution_count = len(executions)
        total_events = cancel_count + execution_count
        
        cancel_ratio = cancel_count / total_events if total_events > 0 else 0.0
        
        avg_qty = executions["quantity"].mean() if execution_count > 0 else 0.0
        # Fix: max_qty should look at ALL events (including Cancels) to detect large spoof orders
        max_qty = x["quantity"].max() if len(x) > 0 else 0.0
        
        # Quantity Percentile:
        # For this rule engine, we want to know if *this* participant's trades are in the 95th percentile
        # of "normal" size.
        # Since we don't have a full history DB loaded here, we compare max_qty against a hardcoded "market norm" 
        # or the batch's distribution.
        # Let's say "Normal" max is ~1.0 BTC. If > 5.0, that's 99th percentile.
        # We'll map max_qty to a simplified percentile score (0-100).
        # < 1.0 = 50
        # 1.0 - 5.0 = 75 - 90
        # > 5.0 = 99
        qty_percentile = 50.0
        if max_qty > 1.0: qty_percentile = 80.0
        if max_qty > 5.0: qty_percentile = 99.0
        
        buy_count = len(x[x["side"] == "BUY"])
        sell_count = len(x[x["side"] == "SELL"])
        buy_sell_ratio = buy_count / max(sell_count, 1)

        unique_venues = x["venue"].nunique()
        
        # Wash Trading Detection Metrics:
        # 1. self_trade_ratio: If buy/sell are perfectly balanced, suspicious
        # 2. wash_volume_ratio: If quantities are repetitive/identical, suspicious
        
        # Simple heuristic: if buy_sell_ratio is close to 1.0 and quantities are uniform
        balanced = abs(buy_sell_ratio - 1.0) < 0.2  # Within 20% of perfect balance
        
        # Check for repetitive quantities (wash trading often uses same size)
        if len(executions) > 0:
            qty_std = executions["quantity"].std()
            qty_mean = executions["quantity"].mean()
            qty_cv = qty_std / qty_mean if qty_mean > 0 else 0  # Coefficient of variation
            uniform_quantities = qty_cv < 0.1  # Low variance = suspicious uniformity
        else:
            uniform_quantities = False
        
        self_trade_ratio = 0.5 if (balanced and uniform_quantities) else 0.0
        wash_volume_ratio = 0.5 if (balanced and execution_count >= 4) else 0.0
        
        return pd.Series({
            "num_trades": execution_count,
            "buy_sell_ratio": buy_sell_ratio,
            "avg_quantity": avg_qty,
            "max_quantity": max_qty,
            "venue_switch_count": unique_venues,
            "cancel_ratio": cancel_ratio,
            "quantity_percentile": qty_percentile,
            "self_trade_ratio": self_trade_ratio,
            "wash_volume_ratio": wash_volume_ratio
        })

    features = grouped.apply(calculate_metrics, include_groups=False)
    return features.reset_index()
