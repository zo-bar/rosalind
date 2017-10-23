'''
Created on Feb 28, 2013

@author: Zoya
'''


def fibb(n, k):
    print ("n=%d k=%d" % (n, k))
    a, b = 1, 1
    i = 2
    while i < n:
        b = a + k * b
        a, b = b, a
        i += 1
        print ("a=%d" % a)
        print ("b=%d" % b)
    print ("RESULT: %d " % a)


fibb(28, 2)
