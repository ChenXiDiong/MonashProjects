from typing import Generator

def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed

def binary_to_decimal(binary: int) -> int:
    """
    Helper function to convert the binary number to decimal.

    Complexity: O(n) where n is the length of the string of the binary number.
    """
    numlst=[]
    a=1
    for num in str(binary):
        base10=int(num)*2**(len(str(binary))-a)
        numlst.append(base10)
        a=a+1
        ans=sum(numlst)    
    return ans

class RandomGen:
    
    def __init__(self,seed:int=0) -> None:
        self.seed = seed
        self.Rg = lcg(pow(2,32), 134775813, 1, seed)

    def randint(self, k: int) -> int:
        """
        Generates a random integer according to the specifications given.

        Complexity: O(n) where n is the length of the binary string after int to str conversion. The 
        dominant line is .format(num), where num is being converted into a string of length 32. Since for 
        any input of k the while loop (while n<=4), and for loops (for a in self.Rg, for num in lst, 
        for i in str(total)) are all performing constant iterations, and the other functions such as empty
        list creation, assignment, return, and mathematical operations are all in O(1), they do not contribute
        much to the overall complexity. The functions binary_to_string and int() are both in O(n), where
        n is the length of the splitted binary string (now of length 16) after int to str conversion, thus it 
        is not as dominant as the .format() function.
        """
        n=0
        lst=[]
        total=0
        new_num=""
        while n <=4:
            for a in self.Rg:    
                lst.append(a)
                break
            n+=1
        for num in lst:
            binary_32='{:032b}'.format(num)
            total+=int(binary_32[0:16])
        for i in str(total):
            if int(i)>=3:
                new_num+="1"
            else:
                new_num+="0"
        return binary_to_decimal(int(new_num))%k+1

if __name__ == "__main__":
    Random_gen = lcg(pow(2,32), 134775813, 1, 0)
