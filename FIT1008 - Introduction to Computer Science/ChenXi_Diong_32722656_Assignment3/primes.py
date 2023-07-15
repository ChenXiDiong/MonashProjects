def largest_prime(k: int) -> int:
    """
    Generates the largest prime number strictly less than k. 

    Complexity: O(k*sqrt(k)) where k is the input integer. 
    In the worst case, the j-loop will loop up to int(sqrt(k)) times, whilst the i-loop will loop up to
    k-2 times (excluding k itself and 1). Thus the overall complexity would be 
    O(k-2)*O(sqrt(k)) = O(k*sqrt(k)).
    """
    for i in range(k-1,1,-1):
        is_prime = True
        for j in range(2,int(i**0.5)):
            if i%j == 0:
                is_prime = False
        if is_prime:
            return i

        
    




  




    

