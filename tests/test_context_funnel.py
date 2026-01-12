import unittest
from src.context_funnel import ContextFunnel

class TestContextFunnel(unittest.TestCase):
    def setUp(self):
        self.funnel = ContextFunnel()

    def test_chunking(self):
        text = "Hello world, this is a test. Another chunk."
        chunks = self.funnel._chunk_input(text)
        self.assertEqual(len(chunks), 3)
        self.assertIn("Hello world", chunks)

    def test_intent_modify(self):
        result = self.funnel.process_input("Please update the status")
        self.assertEqual(result['primary_intent'], "modify_state")

    def test_intent_query(self):
        result = self.funnel.process_input("Check status report")
        self.assertEqual(result['primary_intent'], "query_status")

if __name__ == '__main__':
    unittest.main()
