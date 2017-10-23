'''
Created on Nov 12, 2013

@author: Zoya
'''
from math import factorial
def CUNR(n):
    result = factorial(2 * n - 4) / (factorial(n - 2) * 2 ** (n - 2))
    print (result)
    return result
    
print (CUNR(953) % 1000000)
