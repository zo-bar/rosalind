'''
Created on Mar 7, 2013

@author: Zoya
'''

pairs = ['AA-AA', 'AA-Aa', 'AA-aa', 'Aa-Aa', 'Aa-aa', 'aa-aa']

def get_dominant_probability(pair):
    parents = pair.split("-")
    recessive_prob = 1
    
    if parents[0].count("A") == 2 or parents[1].count("A") == 2:
        recessive_prob = 0    
    if parents[0].count("A") == 1:
        recessive_prob = recessive_prob * 0.5
    if parents[1].count("A") == 1:
        recessive_prob = recessive_prob * 0.5
    return 1 - recessive_prob

def get_dominant_offsprings(string):
    pair_number = [int(n) for n in string.split()]
    result = 0
    for i in range(len(pair_number)):
        result += pair_number[i] * get_dominant_probability(pairs[i]) * 2
    return result

print (get_dominant_offsprings("18442 18352 16403 16889 17002 16257"))

