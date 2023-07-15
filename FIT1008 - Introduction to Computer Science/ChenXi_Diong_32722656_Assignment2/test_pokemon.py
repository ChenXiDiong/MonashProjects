import unittest
from pokemon import Charmander, Bulbasaur, Squirtle, MissingNo
import random

class TestPokemon(unittest.TestCase):
    def test_name(self):
        c = Charmander()
        self.assertEqual(c.name(), "Charmander")
        b = Bulbasaur()
        self.assertEqual(b.name(), "Bulbasaur")
        s = Squirtle()
        self.assertEqual(s.name(), "Squirtle")
        m = MissingNo()
        self.assertEqual(m.name(), "MissingNo")

    def test_get_poketype(self):
        c = Charmander()
        self.assertEqual(c.get_poke_type(), "Fire")
        b = Bulbasaur()
        self.assertEqual(b.get_poke_type(), "Grass")
        s = Squirtle()
        self.assertEqual(s.get_poke_type(), "Water")
        m = MissingNo()
        self.assertEqual(m.get_poke_type(), None)

    def test_attack(self):
        c = Charmander()
        self.assertEqual(c.attack(), 7)
        b = Bulbasaur()
        self.assertEqual(b.attack(), 5)
        s = Squirtle()
        self.assertEqual(s.attack(), 4)
        m = MissingNo()
        self.assertEqual(m.attack(), 5)

    def test_defence(self):
        c = Charmander()
        self.assertEqual(c.defence(), 4)
        b = Bulbasaur()
        self.assertEqual(b.defence(), 5)
        s = Squirtle()
        self.assertEqual(s.defence(), 7)
        m = MissingNo()
        self.assertEqual(m.defence(), 5)

    def test_speed(self):
        c = Charmander()
        self.assertEqual(c.speed(), 8)
        b = Bulbasaur()
        self.assertEqual(b.speed(), 7)
        s = Squirtle()
        self.assertEqual(s.speed(), 7)
        m = MissingNo()
        self.assertEqual(m.speed(), 7)
    
    def test_attacked_dmg(self):
        c = Charmander()
        c.attacked_dmg(5)
        self.assertEqual(c.hp, 2)
        b = Bulbasaur()
        b.attacked_dmg(5)
        self.assertEqual(b.hp, 7)
        s = Squirtle()
        s.attacked_dmg(5)
        self.assertEqual(s.hp, 6)
        #As MissingNo randomly chooses a defence and chance to activate superpower, a seed for random is assigned.
        random.seed(123)
        m = MissingNo()
        m.attacked_dmg(5)
        self.assertEqual(m.hp, 8)
        

    def test_get_level(self):
        c = Charmander()
        lvl = c.get_level()
        self.assertEqual(lvl, 1)
        m = MissingNo()
        lvl = m.get_level()
        self.assertEqual(lvl, 1)

    def test_get_hp(self):
        c = Charmander()
        hp = c.get_hp()
        self.assertEqual(hp, 7)
        m = MissingNo()
        hp = m.get_level()
        self.assertEqual(hp, 1)

    def test_print(self):
        c = Charmander()
        self.assertEqual(str(c), "Charmander's HP = 7 and level = 1")
        m = MissingNo()
        self.assertEqual(str(m), "MissingNo's HP = 8 and level = 1")

    def test_superpower(self):
        m = MissingNo()
        random.seed(123)
        #in this seed, superpower activates increment of hp only.
        m.superpower()
        self.assertEqual(m.hp, 9)
        self.assertEqual(m.level, 1)

if __name__ == '__main__':
    unittest.main()