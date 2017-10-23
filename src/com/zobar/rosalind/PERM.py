'''
Created on Mar 1, 2013

@author: Zoya
'''

def permutations(primes):
    result = []
    for i in primes:
        newlist = [prime for prime in primes if prime != i]
        if len(newlist) == 0:
            subresult = [i]
            result.append(subresult)
            return result
        subpermutations = permutations(newlist)
        for subpermutation in subpermutations:
            subresult = [i]
            subresult.extend(subpermutation)
            result.append(subresult)
#    print result
    return result


def printPermutations(n):
    perm = permutations(xrange(1, n + 1))
    with open("data/permutations_result.txt", "w") as result_file:
        result_file.write(str(len(perm)))
        for permutation in perm:
            result_file.write("\n" + ' '.join(str(num) for num in permutation))

# printPermutations(7)
