'''
Created on Mar 14, 2013

@author: Zoya
'''
from collections import deque

def fibd(n, k):
    print ("n=%d k=%d" % (n, k))
    queue = deque([0] * (k - 3) + [1, 1, 1])
    print (queue)
    a, b = 1, 1
    print ("f(1)=%d" % a)
    print ("f(2)=%d" % b)
    i = 2
    while i < n:
        temp = [queue[m] for m in range(k - 1)]
        b = sum(temp)
        a, b = b, a
        i += 1
        queue.popleft()
        queue.append(a)
        print (queue)
        print ("f(%d) = %d" % (i, a))
    print ("RESULT: %d " % a)

fibd(96, 20)
