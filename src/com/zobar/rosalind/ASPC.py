'''
Created on Jul 29, 2013

@author: Zoya
'''
def ASPC(n, m):
    item = 1
    result = 2 ** n - item
    for i in range(1, m):
        item = item * (n - i + 1) / i
        result -= item
    print (result % 1000000)

ASPC(1916, 767)
