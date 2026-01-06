from typing import List, Dict, Any
from features.feature_stats import FeatureStats

def explain_anomaly(row: Dict[str, Any], baselines: Dict[str, FeatureStats]) -> List[Dict[str, Any]]:
    """
    Compares a single participant's feature row against market baselines
    and returns 'Plain English' evidence for any statistically significant deviation.
    """
    explanations = []

    for feature, stats in baselines.items():
        value = row.get(feature)
        
        # Skip if missing or zero division risk (simplified)
        if value is None or stats.std == 0:
            continue

        # Check if value exceeds P95 (or other threshold logic)
        if value > stats.p95:
            deviation_sigma = (value - stats.mean) / stats.std
            
            explanations.append({
                "feature": feature,
                "value": round(float(value), 3),
                "market_p95": round(stats.p95, 3),
                "deviation_sigma": round(deviation_sigma, 2),
                "description": (
                    f"Participant value ({round(value, 2)}) exceeded market 95th percentile "
                    f"({round(stats.p95, 2)}) by {round(deviation_sigma, 1)}x standard deviations."
                )
            })

    return explanations
