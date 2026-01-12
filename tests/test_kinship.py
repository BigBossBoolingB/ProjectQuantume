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
        self.assertIn("violates Collaboration Principle", msg)

    def test_risk_rejection(self):
        """Test that high risk actions are rejected when debt is high."""
        # Debt starts at 1.0. Tolerance = 0.1 - (1.0*0.05) = 0.05
        # Risk 0.1 should be rejected
        approved, msg, debt = self.kinship.verify_action(
            "High Risk Action",
            KinshipLevel.HUMAN_KIND,
            ActionIntent.OPTIMIZE,
            potential_risk_to_human_kin=0.1
        )
        self.assertFalse(approved)
        self.assertIn("Potential risk", msg)

    def test_human_contribution_increases_debt(self):
        """Test that acknowledging contribution increases debt."""
        start_debt = 0.5
        self.kinship.gratitude_debt = start_debt

        new_debt = self.kinship.acknowledge_human_contribution("code_fix", 0.1)
        self.assertGreater(new_debt, start_debt)

if __name__ == '__main__':
    unittest.main()
