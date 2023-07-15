import unittest
from poke_team import PokeTeam
from tester_base import captured_output

class TestPokeTeam(unittest.TestCase):
    def test_choose_team(self):
        pt = PokeTeam("Ash")
        self.assertEqual(pt.name, "Ash")
        with captured_output("2 2 3\n2 0 1") as (inp, out, err):
            pt.choose_team(0, None)
        self.assertEqual(str(pt), "Charmander's HP = 7 and level = 1, Charmander's HP = 7 and level = 1, Squirtle's HP = 8 and level = 1")

if __name__ == "__main__":
    unittest.main()