from dataclasses import dataclass
import pandas as pd

@dataclass
class FeatureStats:
    mean: float
    std: float
    p95: float

def compute_feature_baselines(features_df: pd.DataFrame, feature_cols: list) -> dict[str, FeatureStats]:
    """
    Computes market baselines (Mean, Std, P95) for explainability.
    """
    baselines = {}
    for col in feature_cols:
        if col in features_df.columns:
            baselines[col] = FeatureStats(
                mean=float(features_df[col].mean()),
                std=float(features_df[col].std()),
                p95=float(features_df[col].quantile(0.95))
            )
    return baselines
