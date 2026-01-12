import unittest
from src.glass_bridge import GlassBridge
from src.cypher import CyrillicCypher
import json

class TestGlassBridge(unittest.TestCase):
    def setUp(self):
        self.bridge = GlassBridge()

    def test_otdr_verification(self):
        # We expect random result but high enough for green in most cases
        # Since it's random, we can't assert exact value, but we can check bounds
        score = self.bridge.perform_otdr_test()
        self.assertGreater(score, 0.90)  # Logic implies < 0.90 is unstable
        self.assertLessEqual(score, 1.0)
        self.assertEqual(self.bridge.status.integrity_score, score)

    def test_handshake_flow(self):
        # Initial state
        self.assertFalse(self.bridge.status.is_connected)

        # Must pass OTDR first
        score = self.bridge.perform_otdr_test()
        if score > 0.90:
            success = self.bridge.establish_handshake()
            self.assertTrue(success)
            self.assertTrue(self.bridge.status.is_connected)
            self.assertTrue(self.bridge.status.secure_channel_active)
        else:
            # If random generator gave bad score (unlikely with current implementation)
            success = self.bridge.establish_handshake()
            self.assertFalse(success)

    def test_transmit_secure(self):
        data = {"target": "warehouse_alpha"}

        # Should fail if not connected
        result = self.bridge.transmit_secure(data)
        self.assertFalse(result)

        # Connect
        self.bridge.perform_otdr_test()
        self.bridge.establish_handshake()

        # Should succeed (if handshake worked)
        if self.bridge.status.is_connected:
            result = self.bridge.transmit_secure(data)
            self.assertTrue(result)

    def test_diagnostics(self):
        diag = self.bridge.get_diagnostics()
        self.assertEqual(diag["link_target"], "WAREHOUSE_ALPHA")
        self.assertIn("connected", diag)
        self.assertIn("integrity", diag)

class TestCyrillicCypher(unittest.TestCase):
    def test_encrypt(self):
        cypher = CyrillicCypher()
        data = {"key": "value"}
        enc = cypher.encrypt(data)
        self.assertTrue(enc.startswith("CYRILLIC_ENC:"))
        self.assertTrue(cypher.is_sanitized(enc))

if __name__ == '__main__':
    unittest.main()
