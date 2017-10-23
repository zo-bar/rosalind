'''
Created on Oct 20, 2013

@author: Zoya
'''
def CTBL(input_file, output_file):
    with open(input_file) as resource:
        newick = resource.read()
    result = {}
    curr_stack = ''
    curr_taxa = ''
    newick = newick.rstrip()
    for letter in newick:
        if letter == '(':
            if len(curr_taxa) > 0:
                result[curr_taxa] = curr_stack
            curr_taxa = ''
            for taxa in result:
                result[taxa] += '0'
            curr_stack += '1'
        elif letter == ')':
            if len(curr_taxa) > 0:
                result[curr_taxa] = curr_stack
            curr_taxa = ''
            for i in range(len(curr_stack) - 1, -1, -1):
                if curr_stack[i] == '1':
                    curr_stack = curr_stack[:i] + '0' + curr_stack[i + 1:]
                    break
        elif letter == ',' or letter == ';':
            if len(curr_taxa) > 0:
                result[curr_taxa] = curr_stack
            curr_taxa = ''
        else:
            curr_taxa += letter.lower()
    if len(curr_taxa) > 0:
        result[curr_taxa] = curr_stack
    taxa_num = len(result) - 1
    print (sorted(result.items()))
    transponented = ["".join(result[key][i] for key in sorted(result.keys())) for i in range(len(curr_stack)) if sum([int(result[key1][i]) for key1 in result.keys()]) < taxa_num and sum([int(result[key1][i]) for key1 in result.keys()]) > 1 ]
    duplicates = []
    for i in range(len(transponented)):
        for j in range(i):
            if transponented[i] == "".join([str(1 - int(k)) for k in transponented[j]]):
                duplicates.append(transponented[i])
                continue
    print (duplicates)
    with open(output_file, 'w') as result_file:
        result_file.write("\n".join([x for x in transponented if duplicates.count(x) == 0]))        

#CTBL("src/data/rosalind_ctbl.txt", "src/data/rosalind_ctbl_result.txt")
