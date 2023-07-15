import unittest
from tester_base import captured_output
from battle import Battle
from pokemon import Charmander, Squirtle

class TestBattle(unittest.TestCase):
    def test_teamname(self):
        b =  Battle("Me", "You")
        self.assertEqual(b.team1.name, "Me")
        self.assertEqual(b.team2.name, "You")

    def test_set_mode_battle(self):
        b = Battle("A", "B")
        with captured_output("2 1 1\n1 2 1") as (inp, out, err):
            result = b.set_mode_battle()
        self.assertEqual(result, "A")
        self.assertEqual(str(b.team1), "Bulbasaur's HP = 7 and level = 2, Squirtle's HP = 8 and level = 1")
        
    def test_rotating_mode_battle(self):
        b = Battle("A", "B")
        with captured_output("2 0 1\n0 2 1") as (inp, out, err):
            result = b.rotating_mode_battle()
        self.assertEqual(result, "A")
        self.assertEqual(str(b.team1), "Squirtle's HP = 3 and level = 2")

    def test_inflict_dmg(self):
        poke1 = Charmander()
        poke2 = Squirtle()
        b = Battle("A", "B")
        b.inflict_dmg(poke1, poke2)
        self.assertEqual(poke1.hp, 7)
        self.assertEqual(poke2.hp, 7)


if __name__ == "__main__":
    unittest.main()