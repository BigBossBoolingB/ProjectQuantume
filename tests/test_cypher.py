import unittest
import os
import json
from src.cypher import Cypher

class TestCypher(unittest.TestCase):
    def setUp(self):
        self.cypher = Cypher()
        self.test_file = "test_cypher_state.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_encrypt_decrypt(self):
        original_text = '{"mission": "active"}'
        encrypted = self.cypher.encrypt(original_text)
        decrypted = self.cypher.decrypt(encrypted)

        self.assertNotEqual(original_text, encrypted)
        self.assertEqual(original_text, decrypted)

    def test_empty_string(self):
        encrypted = self.cypher.encrypt("")
        decrypted = self.cypher.decrypt(encrypted)
        self.assertEqual("", decrypted)

    def test_save_and_load_state(self):
        data = {"key": "value", "number": 123}
        self.cypher.save_state(data, self.test_file)

        # Verify file exists and is not plain json
        with open(self.test_file, 'r') as f:
            content = f.read()
        self.assertNotIn("key", content)

        # Verify load
        loaded_data = self.cypher.load_state(self.test_file)
        self.assertEqual(loaded_data, data)

if __name__ == '__main__':
    unittest.main()
