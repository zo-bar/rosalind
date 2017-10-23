'''
Created on Aug 16, 2013

@author: Zoya
'''
def probability(gc, dna):
    result = 1
    for letter in dna:
        pr = 1.0
        if letter == 'T' or letter == 'A':
            pr = (1 - gc) / 2
        else:
            pr = gc / 2
        result *= pr
    print ("Probability that the string equals %s is %f" % (dna, result))
    return result

def substr_probability(str_len, gc, dna):
    prob = probability(gc, dna)
    result = prob * (str_len - len(dna) + 1)
    return round(result, 3)

def EVAL(input_file, output_file):
    lines = [line.strip() for line in open(input_file)]
    str_len = int(lines[0].rstrip())
    dna = lines[1].rstrip()
    gcs = (float(x) for x in lines[2].rstrip().split(" "))
    result = []
    for gc in gcs:
        result.append(substr_probability(str_len, gc, dna))
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(str(x) for x in result))

EVAL("src/data/rosalind_eval.txt", "src/data/rosalind_eval_result.txt")

# (n-3+1) * pr(not equal)
#    dna_len = len(dna)
#    prob = probability(gc, dna)
#    result = 0
#    for i in xrange(1, str_len - 2 * dna_len + 1):
#        result += prob * ((1 - prob) ** i)
#        # print "%s - %f" % (i, result)
#    result += prob * (dna_len - 1)
# #    result *= prob  # * (1 - prob) * (str_len - 2 * dna_len + 1) * (str_len - 2 * dna_len + 2) / 2
#    print result
#    
#    
#    test = prob
#    for i in xrange(7):
#        test += prob * ((1 - prob) ** i)
#        # print "%s - %f" % (i, test)
#    print test
#    return result
