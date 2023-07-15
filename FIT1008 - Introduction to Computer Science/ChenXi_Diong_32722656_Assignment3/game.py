from __future__ import annotations





# ^ In case you aren't on Python 3.10

from random_gen import RandomGen
from hash_table import LinearProbePotionTable
from potion import Potion
from array_sorted_list import ArraySortedList,ListItem
from array_list import ArrayList
import copy
class Game:
    
    def __init__(self, seed=0) -> None:
        
        self.rand = RandomGen(seed=seed)
    
    def set_total_potion_data(self, potion_data: list) -> None:
        """
        Initial setup for potion data in PotionCorp.

        Complexity: O(n) where n is the length of potion_data. It traverses through the whole list
        for potions to add to the potion table.
        """
        self.potions = LinearProbePotionTable(len(potion_data), True, -1)
        for potion in potion_data:
            self.potions.insert(potion[1],Potion.create_empty(potion[0], potion[1], potion[2]))

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Adds potions to the current available potions-to-sell inventory of PotionCorp.

        Complexity: O(C x log(n)), where C is the length of potion_name_amount_pairs, and n is the
        length of self.inventory. It traverses through the whole list of potion_name_amount_pairs
        which is in O(C), and uses O(log(n)) to find the index to add an item into the array sorted 
        list in each iteration.
        """
        self.inventory = ArraySortedList(len(potion_name_amount_pairs))
        for potion in potion_name_amount_pairs:
            buy_price=self.potions[potion[0]].buy_price
            temp=list(potion)
            temp.append(buy_price)
            self.inventory.add(ListItem(temp,buy_price))
        
    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        Vendor potion selection process.

        Complexity: O(C x log(n)) where C is the number of vendors (num_vendors) and n is the number of 
        potions in the currently available potions for sale (self.inventory). It always iterates through
        the number of vendors, which is in O(C), and then chooses the index to remove the potion in each 
        iteration, which is in O(log(n)).
        """
        lst=[]
        self.vendors = ArrayList(num_vendors)
        for _ in range(num_vendors):
            choice = self.rand.randint(len(self.inventory))
            
            choose = self.inventory.delete_at_index(len(self.inventory)-choice)
            
            lst.append(choose)

        for i in lst:
            self.inventory.add(i)
        return lst
        
    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        """
        Solving the game.

        Complexity: O(N x C + M x N), where N is the length of potion_valuations, M is the length
        of starting_money, and C is the length of self.inventory.
        The first for loop has a total complexity of O(N x C). It goes through N iterations, and in 
        each iteration the dominant line is the find() function, which is in O(C). 
        The second for loop has a total complexity of O(M x N). It goes through M iterations, and in 
        each iteration it iterates through pipo, spio, bpio and aio (which are copies of 
        profit_in_pv_order, sell_price_in_order, bp_in_order and amount_in_order) that have the same 
        length as potion_valuations.
        
        """
        profit_in_pv_order = []
        sell_price_in_order = []
        bp_in_order = []
        amount_in_order = []
        total = 0
        solve = []
        
        for potion in potion_valuations:
            sell_price = potion[1]
            sell_price_in_order.append(sell_price)
            buy_price = self.potions[potion[0]].buy_price
            profit_in_pv_order.append(sell_price / buy_price)
            bp_in_order.append(buy_price)
            temp = self.inventory.find(buy_price)
            amount_in_order.append(temp.value[1])

        for m in starting_money:
            pipo = copy.deepcopy(profit_in_pv_order)
            spio = copy.deepcopy(sell_price_in_order)
            bpio = copy.deepcopy(bp_in_order)
            aio = copy.deepcopy(amount_in_order)
            
            while m !=0:
                curr_ind = pipo.index(max(pipo))
                if m < bpio[curr_ind]:
                    
                    pipo.pop(curr_ind)
                    spio.pop(curr_ind)
                    bpio.pop(curr_ind)
                    aio.pop(curr_ind)
                    
                elif m < bpio[curr_ind] * aio[curr_ind]:
                    
                    max_amount_available = m/bpio[curr_ind]
                    total += spio[curr_ind] * max_amount_available
                    m = m - bpio[curr_ind] * max_amount_available
                    
                else:
                    
                    max_amount = aio[curr_ind] * bpio[curr_ind]
                    m -= max_amount
                    total += aio[curr_ind] * spio[curr_ind]
                    pipo.pop(curr_ind)
                    spio.pop(curr_ind)
                    bpio.pop(curr_ind)
                    aio.pop(curr_ind)
                    
            
            solve.append(total)
            total = 0   
        return solve
        

