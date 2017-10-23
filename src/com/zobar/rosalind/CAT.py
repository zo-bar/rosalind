'''
Created on Nov 7, 2013

@author: Zoya
'''
def rna_complement(aa1, aa2):
    if aa1 == 'A' and aa2 == 'U' or aa1 == 'U' and aa2 == 'A' or aa1 == 'C' and aa2 == 'G' or aa1 == 'G' and aa2 == 'C':
        return True
    return False

def noncrossing_perfect_matches(rna, start_position, end_position, dyn_result):
    if dyn_result.keys().count(start_position) > 0:
        if dyn_result[start_position].keys().count(end_position) > 0:
#            print "Reuse %d-%d" % (start_position, end_position)
            return dyn_result[start_position][end_position]
    result = 0
    for i in range(start_position + 1, end_position + 1, 2):
        if rna_complement(rna[start_position], rna[i]):
            i_result = 1
            if i - 1 > start_position:
                i_result *= noncrossing_perfect_matches(rna, start_position + 1, i - 1, dyn_result)
            if i_result > 0 and i + 1 < end_position:
                i_result *= noncrossing_perfect_matches(rna, i + 1, end_position, dyn_result)
            result += i_result
    if dyn_result.keys().count(start_position) == 0:
        dyn_result[start_position] = {}
    dyn_result[start_position][end_position] = result
#    print dyn_result
    return result

def CAT(input_file, output_file):
    rna = ''
    with open(input_file) as resource:
        resource.readline()
        next_line = resource.readline().rstrip()
        while next_line:
            rna += next_line
            next_line = resource.readline().rstrip()
    print(rna)
    result = noncrossing_perfect_matches(rna, 0, len(rna) - 1, {})
    print(result)
    print(result % 1000000)
    with open(output_file, 'w') as result_file:
        result_file.write(str(result))

# CAT("src/data/rosalind_cat.txt", "src/data/rosalind_cat_result.txt")
