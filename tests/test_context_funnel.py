import unittest
from src.context_funnel import ContextFunnel, SystemState, DistilledCommand
from src.kinship import ActionIntent, KinshipLevel

class TestContextFunnel(unittest.TestCase):
    def setUp(self):
        self.funnel = ContextFunnel()

    def test_chunking(self):
        text = "Hello world, this is a test. Another chunk."
        chunks = self.funnel._chunk_input(text)
        self.assertEqual(len(chunks), 3)
        self.assertIn("Hello world", chunks)

    def test_intent_protect(self):
        command = self.funnel.process_prompt("Deploy protection for the team")
        self.assertIsInstance(command, DistilledCommand)
        self.assertEqual(command.primary_intent, ActionIntent.PROTECT)
        self.assertEqual(command.target_kinship_level, KinshipLevel.HUMAN_KIND)

    def test_intent_silent_mode(self):
        command = self.funnel.process_prompt("Emergency! Code 777 Silent Mode now!")
        self.assertEqual(command.system_mode_request, SystemState.SILENT)

    def test_intent_hostile(self):
        command = self.funnel.process_prompt("Terminate the connection immediately")
        self.assertEqual(command.primary_intent, ActionIntent.ISOLATE)
        self.assertGreater(command.risk_score, 0.5)

if __name__ == '__main__':
    unittest.main()
