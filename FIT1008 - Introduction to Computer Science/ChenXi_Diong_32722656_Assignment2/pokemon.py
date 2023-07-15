from pokemon_base import PokemonBase, GlitchMon
import random
class Charmander(PokemonBase):
    CHARMANDER_NAME = "Charmander"
    CHARMANDER_POKE_TYPE = "Fire"
    CHARMANDER_BASE_HP = 7
    CHARMANDER_BASE_ATTACK = 6
    CHARMANDER_BASE_DEFENCE = 4
    CHARMANDER_BASE_SPEED = 7
    def __init__(self) -> None:
        PokemonBase.__init__(self)
        self.poke_type = self.CHARMANDER_POKE_TYPE 
        self.hp = self.CHARMANDER_BASE_HP
           
    def name(self) -> str:
        """
        Time complexity: O(n), where n is the length of the string.
        """
        return self.CHARMANDER_NAME
    
    def get_poke_type(self) -> str:
        """
        Time complexity: O(n), where n is the length of the string.
        """
        return self.CHARMANDER_POKE_TYPE

    def attack(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.CHARMANDER_BASE_ATTACK + self.level
    
    def defence(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.CHARMANDER_BASE_DEFENCE
    
    def speed(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.CHARMANDER_BASE_SPEED + self.level
    
    def attacked_dmg(self, dmg: int) -> None:
        """
        Time complexity: O(1), it only returns an integer and only performs mathematical operations.
        """
        assert dmg >= 0, "Damage cannot be negative!"
        if dmg > self.defence():
            self.hp -= dmg
        else:
            self.hp -= int(dmg//2)



class Bulbasaur(PokemonBase):
    BULBASAUR_NAME = "Bulbasaur"
    BULBASAUR_POKE_TYPE = "Grass"
    BULBASAUR_BASE_HP = 9
    BULBASAUR_BASE_ATTACK = 5
    BULBASAUR_BASE_DEFENCE = 5
    BULBASAUR_BASE_SPEED = 7
    def __init__(self) -> None:
        PokemonBase.__init__(self)
        self.poke_type = self.BULBASAUR_POKE_TYPE
        self.hp = self.BULBASAUR_BASE_HP
        
    def name(self) -> str:
        """
        Time complexity: O(n), where n is the length of the string.
        """
        return self.BULBASAUR_NAME

    def get_poke_type(self) -> str:
        """
        Time complexity: O(n), where n is the length of the string.
        """
        return self.BULBASAUR_POKE_TYPE
    
    def attack(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.BULBASAUR_BASE_ATTACK

    def defence(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.BULBASAUR_BASE_DEFENCE
    
    def speed(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.BULBASAUR_BASE_SPEED + self.level//2
    
    def attacked_dmg(self, dmg: int) -> None:
        """
        Time complexity: O(1), it only returns an integer and only performs mathematical operations.
        """
        assert dmg >= 0, "Damage cannot be negative!"
        if dmg > (self.defence()+5):
            self.hp -= dmg
        else:
            self.hp -= int(dmg//2)



class Squirtle(PokemonBase):
    SQUIRTLE_NAME = "Squirtle"
    SQUIRTLE_POKE_TYPE = "Water"
    SQUIRTLE_BASE_HP = 8
    SQUIRTLE_BASE_ATTACK = 4
    SQUIRTLE_BASE_DEFENCE = 6
    SQUIRTLE_BASE_SPEED = 7
    def __init__(self) -> None:
        PokemonBase.__init__(self)
        self.poke_type = self.SQUIRTLE_POKE_TYPE
        self.hp = self.SQUIRTLE_BASE_HP
        
    def name(self) -> str:
        """
        Time complexity: O(n), where n is the length of the string.
        """
        return self.SQUIRTLE_NAME
    
    def get_poke_type(self) -> str:
        """
        Time complexity: O(n), where n is the length of the string.
        """
        return self.SQUIRTLE_POKE_TYPE
    
    def attack(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.SQUIRTLE_BASE_ATTACK + self.level//2
    
    def defence(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.SQUIRTLE_BASE_DEFENCE + self.level
    
    def speed(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.SQUIRTLE_BASE_SPEED
    
    def attacked_dmg(self, dmg: int) -> None:
        """
        Time complexity: O(1), it only returns an integer and only performs mathematical operations.
        """
        assert dmg >= 0, "Damage cannot be negative!"
        if dmg > (self.defence()*2):
            self.hp -= dmg
        else:
            self.hp -= int(dmg//2)
    
    
class MissingNo(GlitchMon):
    MISSINGNO_NAME = "MissingNo"
    MISSINGNO_POKE_TYPE = None
    c = Charmander()
    b = Bulbasaur()
    s = Squirtle()
    MISSINGNO_BASE_HP = int((c.get_hp() + b.get_hp() + s.get_hp())//3)
    MISSINGNO_BASE_ATTACK = int((c.attack() + b.attack() + s.attack())//3)
    MISSINGNO_BASE_DEFENCE = int((c.defence() + b.defence() + s.defence())//3)
    MISSINGNO_BASE_SPEED = int((c.speed() + b.speed() + s.speed())//3)
    def __init__(self) -> None:
        PokemonBase.__init__(self)
        self.poke_type = self.MISSINGNO_POKE_TYPE
        self.hp = self.MISSINGNO_BASE_HP
        
    def name(self) -> str:
        """
        Time complexity: O(n), where n is the length of the string.
        """
        return self.MISSINGNO_NAME
    
    def get_poke_type(self):
        """
        Time complexity: O(1), MissingNo has no poke type, so it returns None.
        """
        return self.MISSINGNO_POKE_TYPE

    
    def attack(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.MISSINGNO_BASE_ATTACK + (self.level-1)
    
    def defence(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.MISSINGNO_BASE_DEFENCE + (self.level-1)
    
    def speed(self) -> int:
        """
        Time complexity: O(1), it only returns an integer.
        """
        return self.MISSINGNO_BASE_SPEED + (self.level-1)

    def get_hp(self):
        """
        Time complexity: O(1), it only returns an integer and only performs mathematical operations.
        """
        return self.hp + (self.level-1)
    
    def attacked_dmg(self, dmg: int) -> None:
        """
        Time complexity: O(log N). The function randint(0, N) is in O(log N). The other lines of code only performs mathematical operations and assignments.
        
        """
        assert dmg >= 0, "Damage cannot be negative!"
        chance = random.randint(0,3)
        if chance == 0:
            self.superpower()
        else:
            key = random.randint(0,2)
            if key == 0:
                if dmg > self.defence():
                    self.hp -= dmg
                else:
                    self.hp -= int(dmg//2)
            elif key == 1:
                if dmg > (self.defence()+5):
                    self.hp -= dmg
                else:
                    self.hp -= int(dmg//2)
            elif key == 2:
                if dmg > (self.defence()+5):
                    self.hp -= dmg
                else:
                    self.hp -= int(dmg//2)
    
