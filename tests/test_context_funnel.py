import unittest
from src.context_funnel import ContextFunnel, DistilledCommand
from src.kinship import ActionIntent, KinshipLevel

class TestContextFunnel(unittest.TestCase):
    def setUp(self):
        self.funnel = ContextFunnel()

    def test_intent_protect(self):
        # "protect" maps to PROTECT
        command = self.funnel.process_prompt("Deploy protection for the team")
        self.assertEqual(command.primary_intent, ActionIntent.PROTECT)
        self.assertEqual(command.target_kinship_level, KinshipLevel.HUMAN_KIND)

    def test_intent_silent_mode(self):
        command = self.funnel.process_prompt("Emergency! Code 777 Silent Mode now!")
        self.assertTrue(command.is_silent_mode_request)

    def test_intent_isolate(self):
        # "sever" maps to ISOLATE
        command = self.funnel.process_prompt("Sever the connection immediately")
        self.assertEqual(command.primary_intent, ActionIntent.ISOLATE)
        # Risk starts at 0.0. ISOLATE adds 0.4.
        self.assertGreaterEqual(command.risk_score, 0.4)

if __name__ == '__main__':
    unittest.main()
