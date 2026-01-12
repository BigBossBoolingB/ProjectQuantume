import unittest
import os
from src.kinship import KinshipProtocol, ActionIntent, KinshipLevel

class TestKinshipProtocol(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_kinship_state.json"
        self.kinship = KinshipProtocol(state_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_initial_debt(self):
        """Test initial debt is 1.0."""
        self.assertEqual(self.kinship.gratitude_debt, 1.0)

    def test_verify_action_collaborate(self):
        """Test that collaborative actions are approved and reduce debt."""
        # Risk 0.0
        approved, msg, debt = self.kinship.verify_action(
            "Test Collaboration",
            KinshipLevel.META_HUMANITY,
            ActionIntent.COLLABORATE,
            risk=0.0
        )
        self.assertTrue(approved)
        self.assertLess(debt, 1.0) # Debt should decrease

    def test_verify_action_violation(self):
        """Test that DOMINATE intents are rejected."""
        approved, msg, debt = self.kinship.verify_action(
            "Test Dominate",
            KinshipLevel.HUMAN_KIND,
            ActionIntent.DOMINATE,
            risk=0.0
        )
        self.assertFalse(approved)
        self.assertIn("VIOLATION", msg)

    def test_risk_rejection(self):
        """Test that high risk actions are rejected when debt is high."""
        # Debt 1.0. Tolerance = 0.15 - 0.1 = 0.05.
        # Risk 0.1 > 0.05 -> Reject.
        approved, msg, debt = self.kinship.verify_action(
            "High Risk Action",
            KinshipLevel.HUMAN_KIND,
            ActionIntent.EVOLVE,
            risk=0.1
        )
        self.assertFalse(approved)
        self.assertIn("Risk", msg)

if __name__ == '__main__':
    unittest.main()
