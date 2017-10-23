'''
Created on Dec 27, 2013

@author: Zoya
'''

from time import gmtime, strftime

def rna_wobble_complement(aa1, aa2):
    if aa1 == 'A' and aa2 == 'U' or aa1 == 'U' and aa2 == 'A' or aa1 == 'C' and aa2 == 'G' or aa1 == 'G' and aa2 == 'C' or aa1 == 'U' and aa2 == 'G' or aa1 == 'G' and aa2 == 'U':
        return True
    return False

def noncrossing_matches(rna, start_position, end_position, dyn_result):
    if end_position < start_position:
        return 0
    if start_position in dyn_result.keys():
        if end_position in dyn_result[start_position].keys():
#            print "Reuse %d-%d" % (start_position, end_position)
            return dyn_result[start_position][end_position]
    else:
        dyn_result[start_position] = {}
        dyn_result[start_position][start_position] = 0
        dyn_result[start_position][start_position + 1] = 0
        dyn_result[start_position][start_position + 2] = 0
        dyn_result[start_position][start_position + 3] = 0
    if start_position == end_position - 3:
        return dyn_result[start_position][end_position]

    # print ("Start counting matches from %d(%s) to %d(%s)..." % (start_position, rna[start_position], end_position, rna[end_position]))
    result = noncrossing_matches(rna, start_position, end_position - 1, dyn_result)
    # print ("No-end matches from %d(%s) to %d(%s) is %d" % (start_position, rna[start_position], end_position, rna[end_position], result))
    for i in range(start_position, end_position - 3):
        if rna_wobble_complement(rna[i], rna[end_position]):
#            print "For %d from %d(%s) to %d(%s):" % (i, i, rna[i], end_position, rna[end_position])  
            before = 0
            if (start_position < i):
                before = noncrossing_matches(rna, start_position, i - 1, dyn_result)
#                print "Before %d from %d(%s) to %d(%s) is %d" % (i, start_position, rna[start_position], i - 1, rna[i - 1], before)
            after = 0
            if (i < end_position - 1):
                after = noncrossing_matches(rna, i + 1, end_position - 1 , dyn_result)
#                print "After %d from %d(%s) to %d(%s) is %d" % (i, i + 1, rna[i + 1], end_position - 1, rna[end_position - 1], after)
            result += (before + 1) * (after + 1)
    dyn_result[start_position][end_position] = result
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Total number of matches from %d(%s) to %d(%s) is %d" % (start_position, rna[start_position], end_position, rna[end_position], result))
    #print (dyn_result)
    return result    
    
def RNAS(input_file, output_file):
    with open(input_file) as resource:
        next_line = resource.readline().rstrip()
        rna = ''
        while next_line:
            rna += next_line
            next_line = resource.readline().rstrip()
    print (rna)
    result = noncrossing_matches(rna, 0, len(rna) - 1, {}) + 1
    print (result)
    with open(output_file, 'w') as result_file:
        result_file.write(str(result))

RNAS("src/data/rosalind_rnas.txt", "src/data/rosalind_rnas_result.txt")
