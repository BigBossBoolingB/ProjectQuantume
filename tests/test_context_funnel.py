import unittest
from src.context_funnel import ContextFunnel
from src.kinship import ActionIntent, KinshipLevel, KinshipProtocol

class TestContextFunnel(unittest.TestCase):
    def setUp(self):
        self.funnel = ContextFunnel()

    def test_chunking(self):
        text = "Hello world, this is a test. Another chunk."
        chunks = self.funnel._chunk_input(text)
        self.assertGreater(len(chunks), 0)

    def test_intent_report(self):
        result = self.funnel.process("System status report")
        self.assertEqual(result['primary_intent'], "report")
        self.assertTrue(result['verified']) # Assuming high confidence

    def test_intent_alert(self):
        result = self.funnel.process("ALERT: Critical breach detected!")
        self.assertEqual(result['primary_intent'], "alert")
        self.assertIn('alert', result['entities'])

    def test_entity_extraction_grounding(self):
        result = self.funnel.process("MC // R=0.88 OHM // Check")
        self.assertIn('grounding_resistance', result['entities'])
        self.assertEqual(result['entities']['grounding_resistance'], 0.88)

    def test_integration_with_kinship(self):
        # Setup mock or real kinship
        kinship = KinshipProtocol("test_kinship_funnel.json")
        funnel = ContextFunnel(kinship)

        result = funnel.process("Execute thermal deception protocol")

        # Verify kinship checks ran
        self.assertTrue(result['kinship_approved'])
        self.assertNotEqual(result['kinship_message'], "Kinship check bypassed (no protocol linked)")

        # Cleanup
        import os
        if os.path.exists("test_kinship_funnel.json"):
            os.remove("test_kinship_funnel.json")

if __name__ == '__main__':
    unittest.main()
