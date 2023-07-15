"""
Name: Chen Xi Diong
Student ID: 32722656

FIT3155 S1 2023 Assignment 3 - Question 1
"""
from math import ceil, log
from random import randint, seed
import sys

def mod_exp(a, e, N):
    """
    Performs modular exponentiation of the formula a^e mod N with repeated squaring.
    """
    #binary representation of the exponent
    e_bin = bin(e) 
    #Init result
    res = 1
    #Init a^(2^0) mod N = a mod N
    temp = a % N 

    #We loop from LSB to MSB
    for i in range(len(e_bin)-1,-1,-1):
        #If the current bit is 1, we multiply to the result
        if e_bin[i] == '1': 
            res = (res * temp) % N
        #Update by squaring
        temp = (temp * temp) % N
        
    return res

def is_prime(n):
    """
    Performs Miller Rabin's Primality Testing to determine whether the number n is prime.
    """
    #Set a seed for consistency
    seed(123)
    
    #Covering the small n cases where n = 1,2,3, since we select a = [2 ... n-2], n cannot be less than 4.
    if n%2 == 0 or n == 1:
        return False
    elif n == 2 or n == 3: 
        return True
    
    #Calculating the number of times to perform the test for a decent confidence level. Reference: Week 6 Slides
    k = ceil(log(n))

    s = 0
    t = n-1
    while (t%2 == 0):
        s += 1
        t >>= 1

    while k > 0:
        a = randint(2, n-2)
        previous = mod_exp(a, t, n)

        #Case 2: if x_0 = 1, n is probably prime
        if previous == 1:
            k -= 1
            continue

        for _ in range(1, s):
            curr = (previous * previous) % n
            #Case 3: if x_k = 1
            if curr == 1: 
                if previous == 1 or previous == n-1:
                    continue
                #Case 3a: if x_k-1 != 1, n is composite
                #Case 3b: if x_k-1 != n-1, n is composite
                else:
                    return False
                
            previous = curr
                
        if (previous * previous) % n != 1:
            return False
            
        k -= 1
    return True

def gcd(a, b):
    """
    The Euclidean Algorithm to find the Greatest Common Divisor of two numbers a and b.
    """
    while b > 0:
        a, b = b, a % b

    return a
    
def generate_primes(d):
    """
    Generates the smallest two prime integers of the form 2^x - 1 where x >= d.
    """
    primes = []
    num = (1 << d) - 1
    while len(primes) < 2:
        if is_prime(num):
            primes.append(num)
        num = (num << 1) + 1
        d+=1
    return primes

if __name__ == '__main__':
    _, d = sys.argv
    d = int(d)
    
    #Generating the primes p and q
    primes = generate_primes(d)
    p = primes[0]
    q = primes[1]

    f = open("secretprimes.txt", "w")
    f.write("# p\n")
    f.write(str(p))
    f.write("\n# q\n")
    f.write(str(q))
    f.close()

    #Generating n
    n = p*q

    #Generating e
    lam = (p-1)*(q-1)//gcd(p-1, q-1)
    e = randint(3,lam-1)
    while gcd(e,lam) != 1:
        e = randint(3,lam-1)

    f = open("publickeyinfo.txt", "w")
    f.write("# modulus (n)\n")
    f.write(str(n))
    f.write("\n# exponent (e)\n")
    f.write(str(e))
    f.close()





    


    