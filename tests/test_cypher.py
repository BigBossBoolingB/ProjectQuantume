import unittest
import os
import json
from src.cypher import CyrillicCypher

class TestCyrillicCypher(unittest.TestCase):
    def setUp(self):
        self.cypher = CyrillicCypher()

    def test_encrypt_decrypt_string(self):
        original_text = "test_string"
        encrypted = self.cypher.encrypt(original_text)
        decrypted = self.cypher.decrypt(encrypted)

        self.assertNotEqual(original_text, encrypted)
        self.assertEqual(original_text, decrypted)

    def test_encrypt_decrypt_dict(self):
        original_data = {"key": "value", "number": 123}
        encrypted = self.cypher.encrypt(original_data)
        decrypted = self.cypher.decrypt(encrypted)

        self.assertIsInstance(encrypted, str)
        self.assertEqual(original_data, decrypted)

if __name__ == '__main__':
    unittest.main()
