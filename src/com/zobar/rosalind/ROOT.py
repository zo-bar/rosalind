'''
Created on Nov 14, 2013

@author: Zoya
'''
def ROOT(n):
    p = 2 * n - 3
    result = 1
    while p > 0:
        result *= p
        p -= 2
    print result
    return result

print ROOT(914) % 1000000
