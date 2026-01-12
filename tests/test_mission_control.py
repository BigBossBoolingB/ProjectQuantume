import unittest
import os
import json
from src.mission_control import MissionControl
from src.cypher import CyrillicCypher

class TestMissionControl(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_system_state.json'
        self.kinship_file = 'test_kinship_state.json'
        self.mc = MissionControl(state_file=self.test_file, kinship_state_file=self.kinship_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.kinship_file):
            os.remove(self.kinship_file)

    def test_initial_state(self):
        self.assertEqual(self.mc.state, {})

    def test_save_and_load_state(self):
        self.mc.update_state('mission', 'active')

        # Create a new instance to verify persistence
        mc2 = MissionControl(state_file=self.test_file, kinship_state_file=self.kinship_file)
        self.assertEqual(mc2.get_state('mission'), 'active')

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

    def test_ethical_validation_rejection(self):
        """Verify that MissionControl rejects updates violating Kinship Protocol."""
        # Using keywords that trigger strict intent/risk mapping
        result = self.mc.update_state('mission_status', 'initiate_hostile_takeover')

        # Update should fail
        self.assertFalse(result)
        # State should NOT be updated
        self.assertNotEqual(self.mc.get_state('mission_status'), 'initiate_hostile_takeover')

    def test_ethical_validation_acceptance(self):
        """Verify that MissionControl accepts valid updates."""
        result = self.mc.update_state('mission_status', 'peaceful_coexistence_protect')

        # Update should succeed
        self.assertTrue(result)
        # State SHOULD be updated
        self.assertEqual(self.mc.get_state('mission_status'), 'peaceful_coexistence_protect')

if __name__ == '__main__':
    unittest.main()
