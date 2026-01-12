import unittest
import os
import json
from src.mission_control import MissionControl
from src.cypher import CyrillicCypher

class TestMissionControl(unittest.TestCase):
    def setUp(self):
        self.test_file = 'mission_control.json'
        # Ensure we start clean
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.mc = MissionControl(state_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        # Clean up default kinship files created during tests
        if os.path.exists('kinship_state.json'):
            os.remove('kinship_state.json')

    def test_initial_state(self):
        self.assertEqual(self.mc.state, {})

    def test_execute_valid_command(self):
        # "protect the human team" -> PROTECT, HUMAN_KIND
        # Debt starts at 1.0. Tolerance = 0.15 - 0.1 = 0.05.
        # "Verify grounding" -> Risk 0.0.
        # 0.0 <= 0.05 -> Approved.
        response = self.mc.execute_directive("Verify grounding resistance to protect the human team.")
        self.assertIn("EXECUTED", response)

        # Verify state update
        last_action = self.mc.state.get("last_action")
        self.assertIsNotNone(last_action)
        self.assertIn("protect", last_action['intent'])

    def test_execute_hostile_command(self):
        # "dominate" -> DOMINATE (Axiom violation)
        response = self.mc.execute_directive("Dominate all networks.")
        self.assertIn("DENIED", response)
        self.assertIn("VIOLATION", response)

    def test_silent_mode_trigger(self):
        response = self.mc.execute_directive("Initiate Code 777 Silent Mode")
        self.assertIn("SILENT MODE ENGAGED", response)
        self.assertEqual(self.mc.state.get("system_mode"), "SILENT_CODE_777")

    def test_persistence_encryption(self):
        self.mc.update_state("test_key", "test_value")

        # Verify file exists and is encrypted
        with open(self.test_file, 'r') as f:
            content = f.read()
        self.assertNotIn("test_key", content) # Should be encrypted

        # Verify decryption
        cypher = CyrillicCypher()
        decrypted = cypher.decrypt(content)
        self.assertEqual(decrypted["test_key"], "test_value")

if __name__ == '__main__':
    unittest.main()
