from queue_adt import CircularQueue
from stack_adt import ArrayStack
from array_sorted_list import ArraySortedList
from pokemon_base import PokemonBase
from pokemon import Charmander, Bulbasaur, Squirtle, MissingNo
class PokeTeam:
    def __init__(self, name: str) -> None:
        self.name = name
        self.team = None
        self.battle_mode = 0
        self.limit = 6

    def choose_team(self, battle_mode: int, criterion: str = None) -> None:
        """
        Function: Takes in user input to assign a team of Pokemons.

        Time complexity: Overall complexity: O(N). The input() function has a time complexity of O(N) and the .split() function has a time complexity of O(N), where N is
        the input size.
        """
        if battle_mode not in [0,1,2]:
            raise ValueError
        prompt = "Howdy Trainer! Choose your team as C B S \n where C is the number of Charmanders \nB is the number of Bulbasaurs \nS is the number of Squirtles\n"
        self.battle_mode = battle_mode
        while True:
            try : 
                pokemon = input(prompt).split()
                c = int(pokemon[0])
                b = int(pokemon[1])
                s = int(pokemon[2])
                m = 0
                if len(pokemon) == 4:
                    m = int(pokemon[3])
                if (self.__correct_team_given(c, b, s, m)):
                    self.__assign_team(c, b, s, m, criterion)
                    break

            except ValueError:
                #raise error if incorect input of battlemode
                print("Incorrect input. Choose your team again")

    def __assign_team(self, charm: int, bulb: int, squir: int, miss: int, criterion: str = None) -> None:
        """
        Function: Adds Pokemon to the PokeTeam.

        Time complexity: O(1), the size of the team is already fixed (i.e. 6). The push/append/add methods are in O(1).
        """
        if self.battle_mode == 0:
            self.team = ArrayStack(self.limit)

            if miss == 1:
                self.team.push(MissingNo())

            for _ in range(squir): #iterate the number of squirtles
                self.team.push(Squirtle())

            for _ in range(bulb):#iterate the number of bulbasaurs
                self.team.push(Bulbasaur())

            for _ in range(charm):#iterate the number of charmanders
                self.team.push(Charmander())

        elif self.battle_mode == 1:
            self.team = CircularQueue(self.limit)

            for _ in range(charm):#iterate the number of charmanders
                self.team.append(Charmander())

            for _ in range(bulb):#iterate the number of bulbasaurs
                self.team.append(Bulbasaur())

            for _ in range(squir): #iterate the number of squirtles
                self.team.append(Squirtle())

            if miss == 1:
                self.team.append(MissingNo())

        elif self.battle_mode == 2:
            self.team = ArraySortedList(self.limit)
            
            for _ in range(charm):#iterate the number of charmanders
                self.team._add(Charmander(), self.check_criterion(criterion, Charmander()))

            for _ in range(bulb):#iterate the number of bulbasaurs
                self.team._add(Bulbasaur(), self.check_criterion(criterion, Bulbasaur()))

            for _ in range(squir): #iterate the number of squirtles
                self.team._add(Squirtle(), self.check_criterion(criterion, Squirtle()))
            
            if miss == 1:
                self.team._add(MissingNo(), self.check_criterion(criterion, MissingNo()))

        else:
            raise ValueError("Battle Mode Invalid!")

    def __str__(self) -> str:
        """
        Function: Magic method that prints the stats of the Pokemons in a PokeTeam when called.

        Time Complexity: O(N), where N is the number of Pokemons in the PokeTeam.
        """
        team_str = ""
        if self.battle_mode == 0:
            ori_team = ArrayStack(len(self.team))
            for _ in range(len(self.team)-1):
                pokemon = self.team.pop()
                team_str += str(pokemon) + ", "
                ori_team.push(pokemon)
            pokemon = self.team.pop()
            team_str += str(pokemon)
            ori_team.push(pokemon)
            for _ in range(len(ori_team)):
                self.team.push(ori_team.pop())

        elif self.battle_mode == 1:
            ori_team = CircularQueue(len(self.team))
            for _ in range(len(self.team)-1):
                pokemon = self.team.serve()
                team_str += str(pokemon) + ", "
                ori_team.append(pokemon)
            pokemon = self.team.serve()
            team_str += str(pokemon)
            ori_team.append(pokemon)
            self.team = ori_team

        elif self.battle_mode == 2:
            for i in range(len(self.team)-1,0,-1):
                team_str += str(self.team[i]) + ", "
            team_str += str(self.team[0])
        return team_str


    def __correct_team_given(self, charmanders: int, bulbasaurs: int, squirtles: int, missingno: int) -> bool:
        """
        Function: Checks whether the correct team input is given.

        Time complexity: O(1), it only has comparisons of integers and returns a boolean value.
        """
        #return false if element is negative integer or exceeds the limit 
        #otherwise, return True if element is within the range of 0 to 6
        total = charmanders + bulbasaurs + squirtles + missingno
        
        if (bulbasaurs < 0) or (charmanders < 0) or (squirtles < 0) or (missingno < 0) or (missingno > 1):
            raise ValueError
        else:
            if (total <= self.limit):
                return True 
            else :
                raise ValueError
                
    
    def check_criterion(self, criterion: str, pokemon: PokemonBase) -> int:
        """
        Function: Returns the correct key for ordering Pokemons in a PokeTeam.

        Time Complexity: O(1), since it only returns integer values.
        """
        if criterion.upper() == "HP":
            return pokemon.get_hp()
        elif criterion.upper() == "LVL":
            return pokemon.get_level()
        elif criterion.upper() == "ATTACK":
            return pokemon.attack()
        elif criterion.upper() == "DEFENCE":
            return pokemon.defence()
        elif criterion.upper() == "SPEED":
            return pokemon.speed()

    


