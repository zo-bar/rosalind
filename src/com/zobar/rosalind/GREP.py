'''
Created on Feb 13, 2015

@author: zoya
'''

def get_deBruijn_graph(lines):
    result = dict()
    for line in lines:
        if result.get(line[:-1]):
            result[line[:-1]].append(line[1:])
        else:
            result[line[:-1]] = [line[1:]]
    print (result)
    return result

def get_circular_string_rec(result, cur_string, max_len, k, deBruijn_graph):
    if len(cur_string) == max_len + k:
        if cur_string[:k] == cur_string[max_len:]:
            result.append(cur_string[:max_len])
        return
    for ending in deBruijn_graph[cur_string[-k + 1:]][:]:
        deBruijn_graph[cur_string[-k + 1:]].remove(ending)
        get_circular_string_rec(result, cur_string + ending[-1], max_len, k, deBruijn_graph)
        deBruijn_graph[cur_string[-k + 1:]].append(ending)

def GREP(input_file, output_file):
    lines = [line.strip() for line in open(input_file)]
    deBruijn_graph = get_deBruijn_graph(lines)
    result = []
    get_circular_string_rec(result, lines[0], len(lines), len(lines[0]), deBruijn_graph)
    print ("All variations count: %d" % len(result))
    result = set(result)
    print ('\n'.join(result))
    print ("Unique variations count: %d" % len(result))
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(result))

GREP("src/data/rosalind_grep.txt", "src/data/rosalind_grep_result.txt")
