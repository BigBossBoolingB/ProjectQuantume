import unittest
import json
import os
import tempfile
from src.chimera import ChimeraNode

class TestChimeraNode(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.state_file = os.path.join(self.test_dir.name, "chimera_state.json")
        self.initial_state = {
            "system_identity": {
                "codename": "CHIMERA_PRIME",
                "version": "v1.0"
            },
            "infrastructure_health": {
                "vitals": {"status": "ACTIVE"}
            },
            "active_mission": {
                "directives": ["SURVIVE"]
            },
            "cognitive_state": {
                "current_intent": "IDLE"
            }
        }
        with open(self.state_file, 'w') as f:
            json.dump(self.initial_state, f)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_load_identity(self):
        node = ChimeraNode(self.state_file)
        self.assertEqual(node.get_identity()["codename"], "CHIMERA_PRIME")

    def test_get_health(self):
        node = ChimeraNode(self.state_file)
        self.assertEqual(node.get_health_status(), "ACTIVE")

    def test_update_intent(self):
        node = ChimeraNode(self.state_file)
        node.update_intent("ENGAGE")

        # Reload to check persistence
        node2 = ChimeraNode(self.state_file)
        self.assertEqual(node2.state["cognitive_state"]["current_intent"], "ENGAGE")

if __name__ == '__main__':
    unittest.main()
