'''
Created on Jul 22, 2013

@author: Zoya
'''
import math

def count_probability(gc_content, letter):
    if letter == 'C' or letter == 'G':
        return gc_content / 2
    return (1 - gc_content) / 2

def PROB(input_file, output_file):
    with open(input_file) as resource_file:
        dna = resource_file.readline().rstrip()
        next_line = resource_file.readline().rstrip()
        while (next_line[0] != '0'):
            dna = dna + next_line
            next_line = resource_file.readline().rstrip()
        array_a = next_line.split(" ")
    result = []
    for gc_content in array_a:
        prob = 0
        for letter in dna:
            prob = prob + math.log(count_probability(float(gc_content), letter), 10)
        result.append(str(round(prob, 3)))
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(result))

PROB("data/rosalind_prob.txt", "data/rosalind_prob_result.txt")
