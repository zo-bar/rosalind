'''
Created on Dec 16, 2013

@author: Zoya
'''
from CAT import rna_complement
from time import gmtime, strftime

def noncrossing_matches(rna, start_position, end_position, dyn_result):
    if end_position < start_position:
        return 0
    if dyn_result.keys().count(start_position) > 0:
        if dyn_result[start_position].keys().count(end_position) > 0:
#            print "Reuse %d-%d" % (start_position, end_position)
            return dyn_result[start_position][end_position]
    else:
        dyn_result[start_position] = {}
        dyn_result[start_position][start_position] = 1
    if start_position == end_position:
        return dyn_result[start_position][end_position]

#    print "Start counting matches from %d(%s) to %d(%s)..." % (start_position, rna[start_position], end_position, rna[end_position])
    result = noncrossing_matches(rna, start_position, end_position - 1, dyn_result)
#    print "No-start matches from %d(%s) to %d(%s) is %d" % (start_position, rna[start_position], end_position, rna[end_position], result)
    for i in range(start_position, end_position):
        if rna_complement(rna[end_position], rna[i]):
#            print "For %d from %d(%s) to %d(%s):" % (i, i, rna[i], end_position, rna[end_position])  
            before = 1
            if (start_position < i):
                before = noncrossing_matches(rna, start_position, i - 1, dyn_result)
#                print "Before %d from %d(%s) to %d(%s) is %d" % (i, start_position, rna[start_position], i - 1, rna[i - 1], before)
            after = 1
            if (i < end_position - 1):
                after = noncrossing_matches(rna, i + 1, end_position - 1, dyn_result)
#                print "After %d from %d(%s) to %d(%s) is %d" % (i, i + 1, rna[i + 1], end_position - 1, rna[end_position - 1], after)
            result += before * after
    dyn_result[start_position][end_position] = result
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Total number of matches from %d(%s) to %d(%s) is %d" % (start_position, rna[start_position], end_position, rna[end_position], result))
    # print dyn_result
    return result    
    
def MOTZ(input_file, output_file):
    with open(input_file) as resource:
        resource.readline()
        next_line = resource.readline().rstrip()
        rna = ''
        while next_line:
            rna += next_line
            next_line = resource.readline().rstrip()
    print(rna)
    result = noncrossing_matches(rna, 0, len(rna) - 1, {}) 
    print(result)
    print(result % 1000000)
    with open(output_file, 'w') as result_file:
        result_file.write(str(result % 1000000))

MOTZ("src/data/rosalind_motz.txt", "src/data/rosalind_motz_result.txt")
