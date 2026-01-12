import unittest
import os
import json
from src.mission_control import MissionControl
from src.cypher import CyrillicCypher

class TestMissionControl(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_system_state.json'
        self.mc = MissionControl(state_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_initial_state(self):
        self.assertEqual(self.mc.state, {})

    def test_save_and_load_state(self):
        self.mc.update_state('mission', 'active')

        # Create a new instance to verify persistence
        mc2 = MissionControl(state_file=self.test_file)
        self.assertEqual(mc2.get_state('mission'), 'active')

    def test_update_state(self):
        self.mc.update_state('fuel', 100)
        self.assertEqual(self.mc.get_state('fuel'), 100)

    def test_encrypted_storage(self):
        """Verify that the file on disk is actually encrypted (not plain JSON)."""
        self.mc.update_state('secret', 'sovereign_code')

        with open(self.test_file, 'r') as f:
            content = f.read()

        # Content should NOT look like the plain JSON
        self.assertNotIn('"secret": "sovereign_code"', content)

        # But it should be decryptable
        cypher = CyrillicCypher()
        decrypted = cypher.decrypt(content)
        self.assertIn('"secret": "sovereign_code"', decrypted)

if __name__ == '__main__':
    unittest.main()
