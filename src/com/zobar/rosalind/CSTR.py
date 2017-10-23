'''
Created on Nov 14, 2013

@author: Zoya
'''
def CSTR(input_file, output_file):
    with open(input_file) as resource:
        dnas = [x.rstrip() for x in resource.readlines()]
    result = []
    dna_len = len(dnas[0])
    for i in range(dna_len):
        temp = [dnas[j][i] for j in range(len(dnas))]
        char1 = temp[0]
        char1_count = 0
        char2_count = 0
        trace = ''
        for char in temp:
            if char == char1:
                char1_count += 1
                trace += '1'
            else:
                char2_count += 1
                trace += '0'
        if char1_count > 1 and char2_count > 1:
            result.append(trace)
    print (result)
    with open(output_file, 'w') as result_file:
        result_file.write("\n".join([x for x in result]))        

CSTR("src/data/rosalind_cstr.txt", "src/data/rosalind_cstr_result.txt")
