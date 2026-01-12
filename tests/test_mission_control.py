import unittest
import json
import os
import tempfile
from src.mission_control import MissionControl

class TestMissionControl(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.state_file = os.path.join(self.test_dir.name, "system_state.json")
        self.initial_state = {
            "system_state": {
                "meta": {
                    "timestamp": "2026-01-11T18:59:40-07:00",
                    "status": "ACTIVE_EXECUTION"
                },
                "physical_infrastructure": {
                    "faraday_cage": {"status": "CERTIFIED_SOVEREIGN"}
                }
            }
        }
        with open(self.state_file, 'w') as f:
            json.dump(self.initial_state, f)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_load_state(self):
        mc = MissionControl(self.state_file)
        self.assertEqual(mc.get_status(), "ACTIVE_EXECUTION")

    def test_update_status(self):
        mc = MissionControl(self.state_file)
        mc.update_status("DORMANT")
        self.assertEqual(mc.get_status(), "DORMANT")

        # Verify persistence
        mc2 = MissionControl(self.state_file)
        self.assertEqual(mc2.get_status(), "DORMANT")

    def test_get_infrastructure(self):
        mc = MissionControl(self.state_file)
        infra = mc.get_infrastructure_status()
        self.assertEqual(infra["faraday_cage"]["status"], "CERTIFIED_SOVEREIGN")

if __name__ == '__main__':
    unittest.main()
