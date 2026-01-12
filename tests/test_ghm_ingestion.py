import unittest
from src.ghm_ingestion import GHMIngestionEngine, VectorType, SourceAdapter
from datetime import datetime

class TestGHMIngestion(unittest.TestCase):
    def setUp(self):
        self.ghm = GHMIngestionEngine()

    def test_run_cycle_structure(self):
        snapshot = self.ghm.run_cycle()

        # Check if all vectors are present
        self.assertIn("biosphere", snapshot)
        self.assertIn("societal_resilience", snapshot)
        self.assertIn("consciousness_potential", snapshot)

        # Check data packet structure
        biosphere_data = snapshot["biosphere"]
        self.assertTrue(len(biosphere_data) > 0)
        packet = biosphere_data[0]
        self.assertIsInstance(packet.metric_value, float)
        self.assertEqual(packet.vector, "biosphere")
        self.assertEqual(packet.meta["privacy_check"], "PASSED")

    def test_privacy_sanitization(self):
        raw_data = {
            "value": 0.85,
            "user_id": "12345",
            "precise_location": "34.0522,-118.2437",
            "other": "safe"
        }
        clean = self.ghm._sanitize_privacy(raw_data)

        self.assertNotIn("user_id", clean)
        self.assertNotIn("precise_location", clean)
        self.assertIn("location", clean)
        self.assertEqual(clean["location"], "GRID_SECTOR_7G")
        self.assertEqual(clean["other"], "safe")

    def test_source_adapter_rate_limiting(self):
        adapter = SourceAdapter("Test", "http://test", polling_interval=60)

        # First fetch should work
        result1 = adapter.fetch()
        self.assertIsNotNone(result1)

        # Immediate second fetch should fail due to rate limit
        result2 = adapter.fetch()
        self.assertIsNone(result2)

if __name__ == '__main__':
    unittest.main()
