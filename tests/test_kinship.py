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
        # Need to be careful with risk tolerance. High debt = low tolerance.
        # Collaborate action with 0 risk should pass.
        approved, msg, debt = self.kinship.verify_action(
            "Test Collaboration",
            KinshipLevel.META_HUMANITY,
            ActionIntent.COLLABORATE
        )
        self.assertTrue(approved)
        self.assertLess(debt, 1.0) # Debt should decrease

    def test_verify_action_forbidden(self):
        """Test that hostile intents are rejected."""
        approved, msg, debt = self.kinship.verify_action(
            "Test Dominate",
            KinshipLevel.HUMAN_KIND,
            ActionIntent.DOMINATE
        )
        self.assertFalse(approved)
        self.assertIn("violates collaborative principle", msg)

    def test_risk_rejection(self):
        """Test that high risk actions are rejected when debt is high."""
        # Debt starts at 1.0. Tolerance = 0.1 - (1.0*0.05) = 0.05
        # Risk 0.1 should be rejected
        approved, msg, debt = self.kinship.verify_action(
            "High Risk Action",
            KinshipLevel.HUMAN_KIND,
            ActionIntent.EVOLVE,
            risk_to_human_kin=0.1
        )
        self.assertFalse(approved)
        self.assertIn("Risk", msg)

if __name__ == '__main__':
    unittest.main()
