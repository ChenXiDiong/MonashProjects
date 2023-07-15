from poke_team import PokeTeam
from pokemon_base import PokemonBase
class Battle:
    def __init__(self, trainer_one_name: str, trainer_two_name: str):
        self.team1 = PokeTeam(trainer_one_name)
        self.team2 = PokeTeam(trainer_two_name)
        self.battle_mode = None

    def set_mode_battle(self) -> str:
        """
        Function: Performs set mode battle for two PokeTeams.

        Time complexity: O(while) of self.battle() as it is the dominant line of code.
        """
        self.battle_mode = 0
        self.team1.choose_team(self.battle_mode, None)
        self.team2.choose_team(self.battle_mode, None)
        res = self.battle(self.team1, self.team2, self.battle_mode)
        return res
                
    def rotating_mode_battle(self) -> str:
        """
        Function: Performs rotating mode battle for two PokeTeams.

        Time complexity: O(while) of self.battle() as it is the dominant line of code.
        """
        self.battle_mode = 1
        self.team1.choose_team(self.battle_mode, None)
        self.team2.choose_team(self.battle_mode, None)
        res = self.battle(self.team1, self.team2, self.battle_mode)
        return res

    def optimised_mode_battle(self, criterion_team1: str, criterion_team2: str) -> str:
        """
        Function: Performs optimised mode battle for two PokeTeams.

        Time complexity: O(while) of self.battle() as it is the dominant line of code.
        """
        self.battle_mode = 2
        self.team1.choose_team(self.battle_mode, criterion_team1)
        self.team2.choose_team(self.battle_mode, criterion_team2)
        res = self.battle(self.team1, self.team2, self.battle_mode, criterion_team1, criterion_team2)
        return res

    def inflict_dmg(self, poke1: PokemonBase, poke2: PokemonBase):
        """
        Function: Compares the poke_type of the two pokemon, then calculates and applies the dmg from the attacking pokemon to the defending pokemon.

        Time complexity: O(n), where n is the maximum length of the strings in comparison. It only does comparison of strings and performs arithmetic which is in O(1).
        """
        if poke1.poke_type == "Water":
            if poke2.poke_type == "Water":
                dmg1 = poke1.attack()
                poke2.attacked_dmg(dmg1)
            elif poke2.poke_type == "Fire":
                dmg1 = poke1.attack()*2
                poke2.attacked_dmg(dmg1)
            elif poke2.poke_type == "Grass":
                dmg1 = poke1.attack()*0.5
                poke2.attacked_dmg(dmg1)
            else:
                dmg1 = poke1.attack()
                poke2.attacked_dmg(dmg1)

        elif poke1.poke_type == "Fire":
            if poke2.poke_type =="Water":
                dmg1 = poke1.attack()*0.5
                poke2.attacked_dmg(dmg1)
            elif poke2.poke_type == "Fire":
                dmg1 = poke1.attack()
                poke2.attacked_dmg(dmg1)
            elif poke2.poke_type == "Grass":
                dmg1 = poke1.attack()*2
                poke2.attacked_dmg(dmg1)
            else:
                dmg1 = poke1.attack()
                poke2.attacked_dmg(dmg1)

        elif poke1.poke_type == "Grass":
            if poke2.poke_type =="Water":
                dmg1 = poke1.attack()*2
                poke2.attacked_dmg(dmg1)
            elif poke2.poke_type == "Fire":
                dmg1 = poke1.attack()*0.5
                poke2.attacked_dmg(dmg1)
            elif poke2.poke_type == "Grass":
                dmg1 = poke1.attack()
                poke2.attacked_dmg(dmg1)
            else:
                dmg1 = poke1.attack()
                poke2.attacked_dmg(dmg1)

    def battle(self, team1: PokeTeam, team2: PokeTeam, battle_mode: int, criterion_team1: str=None, criterion_team2: str=None) -> str:
        """
        Function: This executes the battle phase of two Pokemon teams.

        Time complexity: All of the comparisons, pop/serve/delete_at_index and pop/append/add are in O(1), the dominant line of code would be "while not won", the complexity
        would be in O(while) since we cannot determine how many times the loop will be iterated.
        """
        won = False
        while not won:
            #If both teams have no pokemon left, it is a draw.
            if self.team1.team.is_empty() and self.team2.team.is_empty():
                return "Draw"
            #If either of the teams have no pokemon left, the other team is the winner.
            elif self.team1.team.is_empty():
                return self.team2.name
            elif self.team2.team.is_empty():
                return self.team1.name

            if self.battle_mode == 0:
                poke1 = self.team1.team.pop()
                poke2 = self.team2.team.pop()

            elif self.battle_mode == 1:
                poke1 = self.team1.team.serve()
                poke2 = self.team2.team.serve()

            elif self.battle_mode == 2:
                poke1 = self.team1.team.delete_at_index(len(self.team1.team)-1)
                poke2 = self.team2.team.delete_at_index(len(self.team2.team)-1)

        
            #Battle phase:
            if poke1.speed() > poke2.speed():
                self.inflict_dmg(poke1, poke2)
                if poke2.hp > 0:
                    self.inflict_dmg(poke2, poke1)
                    if poke1.hp <= 0:
                        poke2.set_level(poke2.level + 1)
                        if self.battle_mode == 0:
                            self.team2.team.push(poke2)
                        elif self.battle_mode == 1:
                            self.team2.team.append(poke2)
                        elif self.battle_mode == 2:
                            self.team2.team._add(poke2, self.team2.check_criterion(criterion_team2, poke2))
                else:
                    poke1.set_level(poke1.level + 1)
                    if self.battle_mode == 0:
                        self.team1.team.push(poke1)
                    elif self.battle_mode == 1:
                        self.team1.team.append(poke1)
                    elif self.battle_mode == 2:
                        self.team1.team._add(poke1, self.team1.check_criterion(criterion_team1, poke1))

            elif poke1.speed() < poke2.speed():
                self.inflict_dmg(poke2, poke1)
                if poke1.hp > 0:
                    self.inflict_dmg(poke1, poke2)
                    if poke2.hp <= 0:
                        poke1.set_level(poke1.level + 1)
                        if self.battle_mode == 0:
                            self.team1.team.push(poke1)
                        elif self.battle_mode == 1:
                            self.team1.team.append(poke1)
                        elif self.battle_mode == 2:
                            self.team1.team._add(poke1, self.team1.check_criterion(criterion_team1, poke1))
                else:
                    poke2.set_level(poke2.level + 1)
                    if self.battle_mode == 0:
                        self.team2.team.push(poke2)
                    elif self.battle_mode == 1:
                        self.team2.team.append(poke2)
                    elif self.battle_mode == 2:
                            self.team2.team._add(poke2, self.team2.check_criterion(criterion_team2, poke2))

            else:
                self.inflict_dmg(poke1, poke2)
                self.inflict_dmg(poke2, poke1)
                if poke1.hp > 0 and poke2.hp <= 0:
                    poke1.set_level(poke1.level + 1)
                    if self.battle_mode == 0:
                        self.team1.team.push(poke1)
                    elif self.battle_mode == 1:
                        self.team1.team.append(poke1)
                    elif self.battle_mode == 2:
                        self.team1.team._add(poke1, self.team1.check_criterion(criterion_team1, poke1))
                elif poke1.hp <= 0 and poke2.hp > 0:
                    poke2.set_level(poke2.level + 1)
                    if self.battle_mode == 0:
                        self.team2.team.push(poke2)
                    elif self.battle_mode == 1:
                        self.team2.team.append(poke2)
                    elif self.battle_mode == 2:
                            self.team2.team._add(poke2, self.team2.check_criterion(criterion_team2, poke2))

            if poke1.hp > 0 and poke2.hp > 0:
                poke1.hp -= 1
                poke2.hp -= 1

                if poke1.hp > 0 and poke2.hp <= 0:
                    poke1.set_level(poke1.level + 1)
                    if self.battle_mode == 0:
                        self.team1.team.push(poke1)
                    elif self.battle_mode == 1:
                        self.team1.team.append(poke1)
                    elif self.battle_mode == 2:
                        self.team1.team._add(poke1, self.team1.check_criterion(criterion_team1, poke1))
                elif poke1.hp <= 0 and poke2.hp > 0:
                    poke2.set_level(poke2.level + 1)
                    if self.battle_mode == 0:
                        self.team2.team.push(poke2)
                    elif self.battle_mode == 1:
                        self.team2.team.append(poke2)
                    elif self.battle_mode == 2:
                        self.team2.team._add(poke2, self.team2.check_criterion(criterion_team2, poke2))
                elif poke1.hp > 0 and poke2.hp > 0:
                    if self.battle_mode == 0:
                        self.team1.team.push(poke1)
                        self.team2.team.push(poke2)
                    elif self.battle_mode == 1:
                        self.team1.team.append(poke1)
                        self.team2.team.append(poke2)
                    elif self.battle_mode == 2:
                        self.team1.team._add(poke1, self.team1.check_criterion(criterion_team1, poke1))
                        self.team2.team._add(poke2, self.team2.check_criterion(criterion_team2, poke2))

    

                    
    






