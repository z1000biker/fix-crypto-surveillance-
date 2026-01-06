"""
Unit tests for the Case Manager
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'surveillance-engine'))

from cases.case_manager import CaseManager, CaseStatus


class TestCaseManager(unittest.TestCase):
    def setUp(self):
        self.case_manager = CaseManager()
    
    def test_open_case(self):
        """Test case creation"""
        case = self.case_manager.open_case(
            participant_id="TestTrader",
            instrument="BTC-USDT",
            alerts=["SPOOFING: High cancel ratio"],
            ml_score=0.85,
            priority="HIGH"
        )
        
        self.assertIsNotNone(case.case_id)
        self.assertEqual(case.participant_id, "TestTrader")
        self.assertEqual(case.status, CaseStatus.OPEN.value)
        self.assertEqual(case.priority, "HIGH")
        self.assertEqual(len(case.alerts), 1)
    
    def test_case_lifecycle(self):
        """Test case lifecycle transitions"""
        case = self.case_manager.open_case(
            participant_id="TestTrader",
            instrument="BTC-USDT",
            alerts=["Test alert"],
            ml_score=0.75,
            priority="MEDIUM"
        )
        
        # Start investigation
        self.case_manager.start_investigation(case.case_id, "analyst_001")
        self.assertEqual(case.status, CaseStatus.INVESTIGATE.value)
        
        # Close case
        self.case_manager.close_case(case.case_id, "analyst_001", "False positive")
        self.assertEqual(case.status, CaseStatus.CLOSED.value)
        self.assertEqual(case.resolution, "False positive")


if __name__ == '__main__':
    unittest.main()
