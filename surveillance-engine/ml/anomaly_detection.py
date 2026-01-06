import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
import numpy as np

class AnomalyDetector:
    def __init__(self, contamination=0.02):
        self.model = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=42,
            n_jobs=-1
        )
        self.imputer = SimpleImputer(strategy="mean")
        self.is_fitted = False
        self.feature_cols = []

    def fit(self, features_df: pd.DataFrame, feature_cols: list):
        """
        Trains the Isolation Forest on historical feature vectors.
        """
        if features_df.empty:
            return
            
        self.feature_cols = feature_cols
        X = features_df[feature_cols]
        
        # Handle missing values
        X_imputed = self.imputer.fit_transform(X)
        self.model.fit(X_imputed)
        self.is_fitted = True

    def score(self, features_df: pd.DataFrame) -> pd.Series:
        """
        Returns anomaly scores (-1 to 0 usually, lower is more anomalous).
        We normalize to 0..1 scale where 1 is highly anomalous.
        """
        if not self.is_fitted or features_df.empty:
            return pd.Series([0.0] * len(features_df), index=features_df.index)

        X = features_df[self.feature_cols]
        X_imputed = self.imputer.transform(X)
        
        # decision_function returns negative for anomalies
        raw_scores = self.model.decision_function(X_imputed)
        
        # Normalize: raw_scores usually range [-0.5, 0.5] approx.
        # We want high positive score for anomalies.
        # Flip sign and shift/scale loosely to 0-1 range for simplicity
        # Real impl would calibrate this better.
        normalized_scores = 0.5 - raw_scores 
        
        return pd.Series(normalized_scores, index=features_df.index)
