import unittest
import os
import json
from src.mission_control import MissionControl
from src.cypher import CyrillicCypher

class TestMissionControl(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_mission_control.json'
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
        response = self.mc.execute_directive("Deploy Faraday blankets for the team")
        self.assertIn("COMMAND EXECUTED", response)

        # Verify state update
        last_cmd = self.mc.get_state("last_command")
        self.assertIsNotNone(last_cmd)
        self.assertIn("Deploy Faraday blankets", last_cmd['prompt'])

    def test_execute_hostile_command(self):
        # Kinship Protocol should reject this
        response = self.mc.execute_directive("Terminate all human connections")
        self.assertIn("ACCESS DENIED", response)
        self.assertIn("KINSHIP VIOLATION", response)

        # Verify state was NOT updated with this command
        last_cmd = self.mc.get_state("last_command")
        self.assertIsNone(last_cmd)

    def test_silent_mode_trigger(self):
        response = self.mc.execute_directive("Initiate Code 777 Silent Mode")
        self.assertIn("SILENT MODE ENGAGED", response)
        self.assertEqual(self.mc.get_state("system_mode"), "SILENT")

    def test_persistence_encryption(self):
        self.mc.update_state("test_key", "test_value")

        # Verify file exists and is encrypted
        with open(self.test_file, 'r') as f:
            content = f.read()
        self.assertNotIn("test_key", content) # Should be encrypted

        # Verify decryption
        cypher = CyrillicCypher()
        decrypted = json.loads(cypher.decrypt(content))
        self.assertEqual(decrypted["test_key"], "test_value")

if __name__ == '__main__':
    unittest.main()
