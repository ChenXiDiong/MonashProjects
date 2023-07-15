class Potion:
    
    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """
        Creates an empty (i.e. quantity of 0) Potion.

        Complexity: O(n) where n is max(length of potion_type, length of name). The __init__ method 
        and object creation are both in O(1), thus the dominant line is the string parameters passed
        into the __init__ method. Therefore, the complexity depends on the length of the str input
        parameters, potion_type or name.
        """
        return Potion(potion_type, name, buy_price, 0)

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        A good hash function.

        Complexity: O(n), where n is the length of potion_name.
        It will always loop len(potion_name) times. There's no condition that will 
        make the loop stop earlier. Hence, Best-Case = Worst-case
        """
        rethash = 0
        hash_base = 27
        for i in range(len(potion_name)):
            rethash = (rethash * hash_base + ord(potion_name[i])) % tablesize
        return rethash

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        A bad hash function.
        
        Complexity: O(1)
        It only perform some simple mathematical calculation regardless of the len(potion_name)
        """
        return ord(potion_name[0]) % tablesize

