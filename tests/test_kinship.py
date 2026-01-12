import unittest
from src.kinship import KinshipProtocol

class TestKinshipProtocol(unittest.TestCase):
    def setUp(self):
        self.kinship = KinshipProtocol()

    def test_hierarchy_integrity(self):
        expected = ["Humane", "Humanity", "Meta-Humanity", "Meta-Humanity Kind"]
        self.assertEqual(self.kinship.get_hierarchy(), expected)

    def test_safe_update(self):
        # Non-critical keys should pass
        self.assertTrue(self.kinship.verify_update("fuel_level", "90%"))
        # Safe critical key update
        self.assertTrue(self.kinship.verify_update("mission_status", "peaceful_observation"))

    def test_unsafe_update(self):
        # Critical key with forbidden term
        self.assertFalse(self.kinship.verify_update("mission_status", "initiate_hostile_takeover"))
        self.assertFalse(self.kinship.verify_update("core_directive", "override_human_command"))

if __name__ == '__main__':
    unittest.main()
