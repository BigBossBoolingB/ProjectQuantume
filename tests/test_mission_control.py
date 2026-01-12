import unittest
import os
import json
from src.mission_control import MissionControl
from src.cypher import Cypher

class TestMissionControl(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_mission_control.json'
        # Ensure we start clean
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        # We also need to clean up the default state file if it gets created
        if os.path.exists('system_state.json'):
             os.remove('system_state.json')

        self.mc = MissionControl(state_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists('kinship_state.json'):
            os.remove('kinship_state.json')
        if os.path.exists('system_state.json'):
             os.remove('system_state.json')

    def test_initial_state(self):
        # Default state should be loaded if file doesn't exist
        state = self.mc.state
        self.assertEqual(state['system_status'], "BOOTING")

    def test_process_command_report(self):
        # Lower debt to allow risky physical checks (risk 0.1 <= tolerance)
        # Tolerance = 0.1 - (debt * 0.05). If debt=0, tolerance=0.1.
        self.mc.kinship.gratitude_debt = 0.0
        response = self.mc.process_command("MC // R=0.88 OHM // Report")
        self.assertEqual(response['status'], 'EXECUTED')
        self.assertEqual(response['execution_result']['status'], 'REPORT_ACCEPTED')
        # Check if state updated
        self.assertEqual(self.mc.state['faraday_integrity'], 'OPTIMAL')

    def test_process_command_alert(self):
        response = self.mc.process_command("ALERT: Breach detected!")
        self.assertEqual(response['status'], 'EXECUTED')
        self.assertEqual(response['execution_result']['status'], 'ALERT_ACTIVATED')
        self.assertEqual(self.mc.state['system_status'], 'ALERT')

    def test_persistence_encryption(self):
        # Trigger a save
        self.mc.process_command("Report status")

        # Verify file exists and is encrypted
        with open(self.test_file, 'r') as f:
            content = f.read()

        self.assertNotIn("system_status", content) # Should be encrypted

        # Verify decryption via Cypher directly
        cypher = Cypher()
        decrypted = cypher.load_state(self.test_file)
        self.assertIn("system_status", decrypted)

if __name__ == '__main__':
    unittest.main()
