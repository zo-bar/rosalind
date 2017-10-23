'''
Created on Mar 1, 2015

@author: zoya
'''
from time import gmtime, strftime

def extend_newick_tries(tries, taxon):
    # print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Start processing taxon: %s" % taxon)
    # print (tries)
    result = []
    ptaxon = ''
    for trie in tries:
        # print ("Next trie: %s" % trie)
        trie_start = ''
        result_stack = []
        for (i, letter) in enumerate(trie):
            if letter in [',', '(', ')']:
                if ptaxon and len(ptaxon) > 0:
                    extension = '(' + ptaxon + ',' + taxon + ')'
                    result.append(trie_start + extension + trie[i:])
                    trie_start += ptaxon
                    ptaxon = ''
                if letter == '(':
                    result_stack.append(trie_start + ptaxon + '(' + taxon + ',')
                    # print ()
                    # print ("Trie start: " + trie_start)
                    # print ("ptaxon: " + ptaxon)
                    # print (result_stack)
                elif letter == ')':
                    result.append(result_stack.pop() + ')' + trie[i:])
                trie_start += letter               
            else:
                ptaxon += letter
            for i in range(len(result_stack)):
                result_stack[i] += letter
            # print (" + letter %s = ->" % letter)
            # print (result_stack)
    return result

def EUBT(input_file, output_file):
    taxa = []
    for line in open(input_file):
        taxa.extend(line.strip().split(" "))
    print (len(taxa))
    result = [ '(' + taxa[1] + ',' + taxa[2] + ')']
    for taxon in taxa[3:]:
        result = extend_newick_tries(result, taxon)
    for i in range(len(result)):
        result[i] = '(' + taxa[0] + ',' + result[i] + ')'
    
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + str(len(result)))
    print (';\n'.join(str(x) for x in result))
    with open(output_file, 'w') as result_file:
        result_file.write(';\n'.join(result) + ';')

EUBT("data/rosalind_eubt.txt", "data/rosalind_eubt_result.txt")


#     result = ['((00,01),02)']
#     for taxon_index in range(3, len(taxa)):
#         result = extend_newick_tries(result, str(taxon_index).zfill(2))
#         
#     for taxon_index in range(len(taxa)):
#         for res in result:
#             res.replace(str(taxon_index).zfill(2), taxa[taxon_index])



# def extend_newick_tries(tries, taxon):
#     print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Start processing taxon: %s" % taxon)
#     print (tries)
#     result = []
#     ptaxon = ''
#     for trie in tries:
#         print ("Next trie: %s" % trie)
#         # need_ext = True
#         trie_start = ''
#         first_skipped = False
#         for (i, letter) in enumerate(trie):
#             if letter in [',', '(', ')']:
#                 if ptaxon and len(ptaxon) > 0:
#                     if not first_skipped:
#                         first_skipped = True
#                         trie_start += ptaxon + letter
#                         result.append(trie_start + '(' + taxon + trie[i:] + ')')
#                         ptaxon = ''
#                     else:
#                         extension = '(' + ptaxon + ',' + taxon + ')'
#                         result.append(trie_start + extension + trie[i:])
#                         print ("First: %s" % (trie_start + extension + trie[i:]))
#                         trie_start += ptaxon + letter
#                         print ("Second: %s" % (trie_start + '(' + taxon + trie[i:] + ')'))
#                         result.append(trie_start + '(' + taxon + trie[i:] + ')')
#                         
#                         ptaxon = ''
#                         # need_ext = not need_ext
#                 else:
#                     trie_start += letter
#             else:
#                 ptaxon += letter
#         # if not need_ext:
#         # result.append('(' + trie + ',' + taxon + ')')
#         result.pop()
#         result.pop()
#     print (len(result))
#     print (",\n".join(str(x) for x in result))
#     return result

