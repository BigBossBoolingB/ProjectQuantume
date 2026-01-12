import unittest
from src.cypher import CyrillicCypher

class TestCyrillicCypher(unittest.TestCase):
    def setUp(self):
        self.cypher = CyrillicCypher()

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

if __name__ == '__main__':
    unittest.main()
