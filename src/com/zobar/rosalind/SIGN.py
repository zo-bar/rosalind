'''
Created on Jul 14, 2013

@author: Zoya
'''
def permutations(primes):
    result = []
    for i in primes:
        newlist = [prime for prime in primes if prime != i]
        if len(newlist) == 0:
            result.append([i])
            result.append([-i])
            return result
        subpermutations = permutations(newlist)
        for subpermutation in subpermutations:
            result.append([i] + subpermutation)
            result.append([-i] + subpermutation)
    return result

def sign_permutations(length):
    perm = permutations([i for i in xrange(1, length + 1)])
    with open("data/rosalind_sign_result.txt", "w") as result_file:
        result_file.write(str(len(perm)))
        for permutation in perm:
            result_file.write("\n" + ' '.join(str(num) for num in permutation))

sign_permutations(5)
