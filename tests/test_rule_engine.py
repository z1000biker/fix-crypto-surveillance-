"""
Unit tests for the Rule Engine
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'surveillance-engine'))

from rules.rule_engine import RuleEngine


class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.rule_engine = RuleEngine(rules_dir="surveillance-engine/rules")
    
    def test_spoofing_detection_high_cancel_ratio(self):
        """Test spoofing detection with high cancel ratio"""
        metrics = {
            "cancel_ratio": 0.8,
            "quantity_percentile": 96,
            "participant_id": "TestTrader",
            "instrument": "BTC-USDT"
        }
        
        alerts = self.rule_engine.evaluate(metrics)
        self.assertTrue(len(alerts) > 0)
        self.assertTrue(any("SPOOFING" in alert for alert in alerts))
    
    def test_wash_trading_detection(self):
        """Test wash trading detection"""
        metrics = {
            "self_trade_ratio": 0.5,
            "wash_volume_ratio": 0.5,
            "participant_id": "TestTrader",
            "instrument": "BTC-USDT"
        }
        
        alerts = self.rule_engine.evaluate(metrics)
        self.assertTrue(len(alerts) > 0)
        self.assertTrue(any("WASH_TRADING" in alert for alert in alerts))
    
    def test_normal_trading_no_alerts(self):
        """Test that normal trading doesn't trigger alerts"""
        metrics = {
            "cancel_ratio": 0.1,
            "quantity_percentile": 50,
            "self_trade_ratio": 0.0,
            "wash_volume_ratio": 0.0,
            "participant_id": "NormalTrader",
            "instrument": "BTC-USDT"
        }
        
        alerts = self.rule_engine.evaluate(metrics)
        self.assertEqual(len(alerts), 0)


if __name__ == '__main__':
    unittest.main()
