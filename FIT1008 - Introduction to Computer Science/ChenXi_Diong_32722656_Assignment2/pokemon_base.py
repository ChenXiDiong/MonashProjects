from abc import ABC, abstractmethod
from typing import TypeVar
import random
T = TypeVar('T')

class PokemonBase(ABC):
    BASE_LEVEL = 1
    def __init__(self) -> None:
        self.poke_type = None
        self.hp = None
        self.level = self.BASE_LEVEL
        
    @abstractmethod
    def name(self):
        """
        This allows the user to get the name of the Pokemon.
        """
        pass

    @abstractmethod
    def get_poke_type(self):
        """
        This allows the user to get the poke_type of the Pokemon.
        """
        pass
        
    def get_hp(self) -> int:
        """
        This allows the user to get the hp of the Pokemon.

        Time complexity : O(1), as it only returns a single value.
        """
        return self.hp
    
    def get_level(self) -> int:
        """
        This allows the user to get the level of the Pokemon.

        Time complexity : O(1), as it only returns a single value.
        """
        return self.level
    
    @abstractmethod
    def attack(self):
        """
        This allows the user to get the attack damage of the Pokemon.
        """
        pass
    
    @abstractmethod
    def defence(self):
        """
        This allows the user to get the defence of the Pokemon.
        """
        pass
    
    @abstractmethod
    def speed(self):
        """
        This allows the user to get the speed of the Pokemon.
        """
        pass
    
    @abstractmethod
    def attacked_dmg(self):
        """
        This allows the user to calculate the damage the Pokemon takes when being attacked by another Pokemon.
        """
        pass

    def set_hp(self, hp):
        """
        This allows the user to set the HP attribute of the Pokemon.

        Time complexity : O(1), as it only has value assignment.
        """
        assert hp >= 0, "HP cannot be negative!"
        self.hp = hp
    
    def set_level(self, level):
        """
        This allows the user to set the level attribute of the Pokemon.

        Time complexity : O(1), as it only has value assignment.
        """
        assert level > 0, "Level cannot be 0 or negative!"
        self.level = level

    def __str__(self) -> str:
        """
        Time complexity: O(n + N) where n is the length of the string and N is the maximum size of the abstract data type.
        """
        return "{}'s HP = {} and level = {}".format(self.name(),self.hp,self.level)  
    
        
class GlitchMon(ABC):
    BASE_LEVEL = 1
    def __init__(self) -> None:
        self.poke_type = None
        self.hp = None
        self.level = self.BASE_LEVEL
        
    @abstractmethod
    def name(self):
        """
        This allows the user to get the name of the Pokemon.
        """
        pass

    @abstractmethod
    def get_poke_type(self):
        """
        This allows the user to get the poke_type of the Pokemon.
        """
        pass
    
    @abstractmethod
    def get_hp(self):
        """
        This allows the user to get the hp of the Pokemon.
        """
        pass
    
    def get_level(self):
        """
        This allows the user to get the level of the Pokemon.

        Time complexity : O(1), as it only returns a single value.
        """
        return self.level
    
    @abstractmethod
    def attack(self):
        """
        This allows the user to get the attack damage of the Pokemon.
        """
        pass
    
    @abstractmethod
    def defence(self):
        """
        This allows the user to get the defence of the Pokemon.
        """
        pass
    
    @abstractmethod
    def speed(self):
        """
        This allows the user to get the speed of the Pokemon.
        """
        pass
    
    @abstractmethod
    def attacked_dmg(self):
        """
        This allows the user to calculate the damage the Pokemon takes when being attacked by another Pokemon.
        """
        pass

    def set_hp(self, hp):
        """
        This allows the user to set the HP attribute of the Pokemon.

        Time complexity : O(1), as it only has value assignment.
        """
        assert hp >= 0, "HP cannot be negative!"
        self.hp = hp
    
    def set_level(self, level):
        """
        This allows the user to set the level attribute of the Pokemon.

        Time complexity : O(1), as it only has value assignment.
        """
        assert level > 0, "Level cannot be 0 or negative!"
        self.level = level

    def inc_hp(self, hp=1):
        """
        This allows the user to increase the HP attribute of the Pokemon.

        Time complexity : O(1), as it only has value assignment and mathematical operation.
        """
        assert hp >= 0, "HP incremented cannot be negative!"
        self.hp += hp

    def superpower(self):
        """
        This has a 25% chance to be performed every time the Pokemon has to defend from an attack.

        Time complexity: O(log N). The function randint(0, N) has a time complexity O(log N). The other lines of code only include comparison of integers and inc_hp() is 
        in O(1).
        """
        chance = random.randint(0,2)
        if chance == 0:
            self.inc_hp()
        elif chance == 1:
            self.set_level(self.level + 1)
        elif chance == 2:
            self.set_level(self.level + 1)
            self.inc_hp()


    def __str__(self) -> str:
        """
        Time complexity: O(n + N) where n is the length of the string and N is the maximum size of the abstract data type.
        """
        return "{}'s HP = {} and level = {}".format(self.name(),self.hp,self.level) 




    
    
    


