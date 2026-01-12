import unittest
from src.mission_control import MissionControl
from src.glass_bridge import GlassBridge, CyrillicCypher
import tempfile
import json
import os

class TestGlassBridge(unittest.TestCase):
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

        self.mc = MissionControl(self.state_file)
        self.bridge = GlassBridge(self.mc)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_otdr_verification_success(self):
        result = self.bridge.perform_otdr_test()
        self.assertTrue(result["success"])
        self.assertLess(result["signal_loss_db"], 0.5)
        self.assertTrue(self.bridge.integrity_verified)

    def test_otdr_verification_fail_if_dormant(self):
        self.mc.update_status("DORMANT")
        # Re-init bridge or just call method? Method checks mc status dynamically.
        result = self.bridge.perform_otdr_test()
        self.assertFalse(result["success"])
        self.assertFalse(self.bridge.integrity_verified)

    def test_handshake_flow(self):
        # Fail before integrity check
        self.assertFalse(self.bridge.initialize_handshake())

        # Pass integrity check
        self.bridge.perform_otdr_test()
        self.assertTrue(self.bridge.initialize_handshake())
        self.assertTrue(self.bridge.connection_active)

    def test_cypher_encryption(self):
        data = {"mission": "secret"}
        enc = CyrillicCypher.encrypt(data)
        self.assertTrue(enc.startswith("CYRILLIC_ENC:"))
        self.assertTrue(CyrillicCypher.is_sanitized(enc))

    def test_transmit_payload(self):
        data = {"target": "warehouse_alpha"}

        # Should fail if not connected
        result = self.bridge.transmit_secure_payload(data)
        self.assertFalse(result["success"])

        # Connect
        self.bridge.perform_otdr_test()
        self.bridge.initialize_handshake()

        # Should succeed
        result = self.bridge.transmit_secure_payload(data)
        self.assertTrue(result["success"])
        self.assertEqual(result["protocol"], "CYRILLIC_HANDSHAKE_V1")

if __name__ == '__main__':
    unittest.main()
