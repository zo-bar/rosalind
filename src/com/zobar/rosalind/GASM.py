'''
Created on Nov 10, 2013

@author: Zoya
'''
from REVC import reverse_char
FALSE_RETURN = 'FALSE'

def get_deBruijn_graph(lines, k):
    result = dict()
    for line in lines:
        rev_line = ''
        for letter in reversed(line):
            rev_line += reverse_char(letter)
        for i in range(len(line) - k):
            result[line[i:i + k]] = line[i + k]
            result[rev_line[i:i + k]] = rev_line[i + k ]
    print ("de Bruijn graph for k = %d (len = %d)" % (k, len(result)))
#    print result
    return result

def get_cyclic_superstring(deBruijn_graph):
    result = deBruijn_graph.keys()[0]
    next_line = result
    for i in range(len(deBruijn_graph) / 2):
        if not deBruijn_graph.get(next_line):
            return FALSE_RETURN
        result += deBruijn_graph.pop(next_line)
        next_line = result[-len(next_line):]
#        print result
    result = deBruijn_graph.keys()[0]
    next_line = result
    for i in range(len(deBruijn_graph)):
        if not deBruijn_graph.get(next_line):
            return FALSE_RETURN
        result += deBruijn_graph.pop(next_line)
        next_line = result[-len(next_line):]
#        print result
    if len(deBruijn_graph) > 0:
        return FALSE_RETURN
    return result[:-len(next_line)]

def GASM(input_file, output_file):
    lines = [line.strip() for line in open(input_file)]
    for k in range(min([len(line) for line in lines]) - 1, -1, -1):
        deBruijn_graph = get_deBruijn_graph(lines, k)
        result = get_cyclic_superstring(deBruijn_graph)
        if result != FALSE_RETURN:
            break
    print (result)
    with open(output_file, "w") as result_file:
        result_file.write(result)

GASM("src/data/rosalind_gasm.txt", "src/data/rosalind_gasm_result.txt")
