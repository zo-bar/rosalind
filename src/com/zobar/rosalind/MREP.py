'''
Created on May 3, 2015

@author: zoya
'''
from com.zobar.rosalind.SuffixTree import SuffixTree
from time import gmtime, strftime

def check_max_repeats(trie, node, result):
    full_substr = node.full_substr()
    child_count = len(node.child_nodes)
    for child in node.child_nodes:
        check_max_repeats(trie, child, result)
        if (child.full_substr() in result):
            child_count += result[child.full_substr()] - 1
    if (child_count > 0):
        result[full_substr] = child_count

def MREP(input_file, output_file):
    with open(input_file) as resource:
        dna = resource.readline().rstrip()
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Start processing string %s ..." % dna)
    occurence_count = dict()
    suff_tree = SuffixTree()
    suff_tree.add_string(dna, 0)
    # print (suff_tree)
    check_max_repeats(suff_tree, suff_tree.root_node, occurence_count)
    occurence_keys = sorted(occurence_count.keys(), key=len, reverse=True)
    # print (occurence_count)
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Occurence map created\nFind maximal repeats...")
    for key in occurence_keys:
        if key in occurence_count.keys():
            for i in range(1, len(key) - 19):
                if key[i:] in occurence_count and occurence_count[key[i:]] == occurence_count[key]:
                    occurence_count.pop(key[i:]) 
    result = []
    for key in occurence_count.keys():
        if (len(key) > 19 and occurence_count[key] > 1):
            result.append(key)
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Done")
    with open(output_file, 'w') as result_file:
        result_file.write("\n".join([x for x in result])) 
    print (result)

MREP("src/data/rosalind_mrep.txt", "src/data/rosalind_mrep_result.txt")

# misunderstand the task - found most common substrings
# def check_repeats(trie, node, result):
#     if node.substr[0] == '$':
#         parent = node.parent_node
#         while parent != trie.root_node:
#             result[parent] = result[parent] + 1
#             parent = parent.parent_node
#     else:
#         result[node] = 0
#         
#     for child_node in node.child_nodes:
#         check_repeats(trie, child_node, result)
# 
# def MREP(input_file, output_file):
#     with open(input_file) as resource:
#         dna = resource.readline().rstrip()
#     result = dict()
#     suff_tree = SuffixTree()
#     suff_tree.add_string(dna, 0)
#     check_repeats(suff_tree, suff_tree.root_node, result)
#     max_repeat = 0
#     max_repeat_strings = []
#     for res in result:
#         res_substr = res.full_substr()
#         # print ("%s appears %d times" % (res.substr, result[res]))
#         if result[res] > max_repeat and len(res_substr) > 20:
#             max_repeat = result[res]
#             max_repeat_strings = []
#         if result[res] == max_repeat and len(res_substr) > 20:
#             max_repeat_strings.append(res_substr)
#     
#     print (max_repeat)
#     print (max_repeat_strings)
#             
#     # with open(output_file, 'w') as result_file:
#     #    result_file.write("\n".join([x for x in result])) 
            # max repeat == has more then 1 children each of them have less then 2 children
#     is_max_repeat = True
#     for child in node.child_nodes:
#         is_max_repeat = is_max_repeat & check_max_repeats(trie, child, result)
#     if is_max_repeat:
#         result.append(node.full_substr())
#         return False
#     if len(node.child_nodes) < 2:
#         return False
#     return
