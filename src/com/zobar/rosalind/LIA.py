'''
Created on Jun 27, 2013

@author: Zoya
'''

# Count number of pedegrees of AaBb genotype if all mates are AaBb including 0th generation
def count_probability_in_generation(k, N):
    # k - generation level
    # N - minimum number of AaBb's
    # num - number of people in generation k
    num = 2 ** k
    probabilities = [[-1 for j in range(N + 1)] for i in range(num + 1)]   
    return count_probability(num, N, probabilities)

def count_probability(num, N, probabilities):
    if probabilities[num][N] != -1:
        return probabilities[num][N]
    if num < 0 or N < 0 : print ("ERROR")
    if num == 0 or N == 0: return 1.0
    p = 0.0
    for i in range(num - N + 1):
        notAaBb = 0.75 ** i
        # print "First %d are not AaBbs: %d" % (i, notAaBb)
        # probability that next one is AaBb:
        AaBb = 0.25
        restAaBb = count_probability(num - i - 1, N - 1, probabilities)
        # print "Among last %d there are at least %d AaBbs: %d" % (num - i - 1, N - 1, restAaBb)
        p = p + notAaBb * AaBb * restAaBb 
        # print "Total probability: %f" % p
    probabilities[num][N] = p
    return p
    
print (count_probability_in_generation(5, 9))

