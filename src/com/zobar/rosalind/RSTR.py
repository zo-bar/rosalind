'''
Created on Aug 12, 2013

@author: Zoya
'''

def RSTR(N, x, dna):
    result = 1
    for letter in dna:
        pr = 1
        if letter == 'T' or letter == 'A':
            pr = (1 - x) / 2
        else:
            pr = x / 2
        result *= pr
    print "Probability that the string equals %s is %f" % (dna, result)
    result = 1 - (1 - result) ** N
    print "Probability that at least one of %d equals %s is %f" % (N, dna, result)
    return round(result, 3)

print RSTR(90317, 0.533190, "TCTTCTTCGA")
