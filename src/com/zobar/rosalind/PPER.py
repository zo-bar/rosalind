'''
Created on Jul 26, 2013

@author: Zoya
'''
import math

def PPER(n, k):
    return (math.factorial(n) / math.factorial(n - k)) % 1000000

print PPER(94, 10)
