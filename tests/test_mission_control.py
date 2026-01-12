import unittest
import os
import json
from src.mission_control import MissionControl

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

if __name__ == '__main__':
    unittest.main()
