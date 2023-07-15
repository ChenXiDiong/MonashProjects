import unittest
from unittest.mock import Mock
from pokemon_base import PokemonBase, GlitchMon
from pokemon import Charmander, MissingNo

#setting up a mock Abstract Base Class for testing methods
class MockPokemonBase(PokemonBase):
    def name(self):
        return None
    
    def get_poke_type(self):
        return None

    def attack(self):
        return None
    
    def defence(self):
        return None

    def speed(self):
        return None

    def attacked_dmg(self):
        return None

class TestPokemonBase(unittest.TestCase):
    def test_set_hp(self):
        pb = MockPokemonBase()
        pb.set_hp(5)
        self.assertEqual(pb.hp, 5)

    def test_set_level(self):
        pb = MockPokemonBase()
        pb.set_level(5)
        self.assertEqual(pb.level, 5)

    def test_get_level(self):
        pb = MockPokemonBase()
        self.assertEqual(pb.get_level(), 1)

    def test_get_hp(self):
        pb = MockPokemonBase()
        self.assertEqual(pb.get_hp(), None)

    def test_print(self):
        pb = MockPokemonBase()
        self.assertEqual(str(pb), "None's HP = None and level = 1")
        
if __name__ == '__main__':
    unittest.main()