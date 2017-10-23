'''
Created on Aug 10, 2015

@author: zoya
'''
LETTERS = ['A', 'C', 'G', 'T', '-']
EXT_LETTERS = ['B', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
As = ['B', 'D', 'E', 'F', 'N', 'O', 'P', 'Q', 'R', 'S']
Cs = ['B', 'H', 'I', 'J', 'N', 'O', 'P', 'U', 'V', 'W']
Gs = ['D', 'H', 'K', 'L', 'N', 'Q', 'R', 'U', 'V', 'X']
Ts = ['E', 'I', 'K', 'M', 'O', 'Q', 'S', 'U', 'W', 'X']
# A+C=B; A+G=D; A+T=E; A+-=F
# C+G=H; C+T=I; C+-=J
# G+T=K; G+-=L
# T+-=M
# A+C+G=N; A+C+T=O; A+C+-=P; A+G+T=Q; A+G+-=R; A+T+-=S
# C+G+T=U; C+G+-=V; C+T+-=W; G+T+-=X 
import string

def create_comb(arr):
    print (arr)
    comb = []
    comb.extend(arr)
    new_comb = comb
    for i in range(len(arr) - 3):
        new_comb = set(["".join(sorted(l1 + l2)) for l1 in arr for l2 in new_comb if not l1 in l2])
        comb.extend(new_comb)
    return comb

def create_match_dict(comb):
    match_dict = dict((x, string.ascii_uppercase[i]) for i, x in enumerate(list(comb)))
    # match_dict.update(dict((string.ascii_uppercase[i], x) for i, x in enumerate(list(comb))))
    print ([x + ':' + match_dict[x] for x in comb])
    return match_dict
    
def create_match_matrix(comb, match_dict, dim):
    result = [['' for j in range(len(comb))] for i in range(len(comb))]
    for i, l1 in enumerate(comb):
        for j, l2 in enumerate(comb):
            m = [match_dict[k1] for k1 in l1 if k1 in l2]
            if m:
                result[i][j] = m[0]
            else:
                r1 = (''.join(sorted(set(l1 + l2))))
                if len(r1) < dim:
                    result[i][j] = match_dict[r1]
                else:
                    result[i][j] = '?'
        
    #print ('\n'.join(str(x) for x in result))
    return result
    
    
# print(create_match_matrix(LETTERS))

def unroll(position, taxon, letter):
    pass

def get_consensus_str(str1, str2, matrix, match_dict, comb):
    consensus_str = ''
    for i in range(len(str1)):
        l1 = str1[i]
        l2 = str2[i]
        print (l1)
        print (match_dict[l1])
        print (comb.index(match_dict[l1]))
        print (comb.index(match_dict[l2]))
        consensus_str += matrix[comb.index(match_dict[l1])][comb.index(l2)]
        # TODO:if consensus_str[i] in LETTERS:
        #    unroll(i, taxon, consensus_str[i])    
            
            
    return consensus_str
    
def ALPH(input_file, output_file):
    with open(input_file) as resource:
        tree = resource.readline().rstrip()
        line = resource.readline().rstrip()
        while line and line[0:1] != '>':
            tree += line
            line = resource.readline().rstrip()
        
        taxa = dict()
        
        taxon = ''
        taxon_str = ''
        while line:
            if line[0:1] == '>':
                if taxon:
                    taxa[taxon] = taxon_str
                taxon = line[1:]
                taxon_str = ''
            else:
                taxon_str += line
            line = resource.readline().rstrip()
    if taxon:
        taxa[taxon] = taxon_str
        
    tree_stack = []
    taxon = ''
    prev_symb = ''
    
    comb = create_comb(LETTERS)
    match_dict = create_match_dict(comb)
    matrix = create_match_matrix(comb, match_dict, len(LETTERS) - 1)
    print (match_dict)
    match_dict = {match_dict[x]:x for x in match_dict}  # inverts match_dict
    print (match_dict)
    
    result = dict()
    distance = 0
    for letter in tree:
        if letter == '(' or letter == ',' or letter == ')' or letter == ';':
            if (letter == ')' or letter == ',' or letter == ';') and prev_symb == ')':
                # cross last two taxa
                t1 = tree_stack.pop()
                t2 = tree_stack.pop()
                
                print ("Crossing %s with %s for %s" % (t1, t2, taxon))
                # temp_arr = [taxa[t1], taxa[t1], taxa[t1], taxa[t2], taxa[t2], taxa[t2]]
                taxon_str = get_consensus_str(taxa[t1], taxa[t2], matrix, match_dict, comb)  # , priorities)
                
                d1 = sum([0 if taxa[t1][i] == taxon_str[i] else 1 for i in range(len(taxon_str))])
                d2 = sum([0 if taxa[t2][i] == taxon_str[i] else 1 for i in range(len(taxon_str))])
                distance += d1 + d2
                print ("%s (%d) + %s (%d) = %s (%d)" % (taxa[t1][:10], d1, taxa[t2][:10], d2, taxon_str[:10], distance))
                
                result[taxon] = taxon_str
                taxa[taxon] = taxon_str
                tree_stack.append(taxon)
                taxon = ''
            if taxon:
                tree_stack.append(taxon)
                taxon = ''
            prev_symb = letter
        else:
            taxon += letter
    print (distance)
    # print (result)
    with open(output_file, 'w') as result_file:
        result_file.write(str(distance))
        for r in result:
            result_file.write("\n>" + r + '\n' + result[r])        

ALPH("data/rosalind_alph.txt", "data/rosalind_alph_result.txt")


# # make list of all possible taxa (result)
#     taxon_len = len(taxon_str)
#     taxon_list = []
#     char_list = ['A', 'C', 'G', 'T', '-']
#     taxon_list.extend(char_list)
#     
#     cross_matrix = [[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]]
#     for i in range(taxon_len - 1):
#         temp = []
#         cross_matrix_block = cross_matrix
#         # print (cross_matrix_block)
#         matrix_add_block = [[cross_matrix_block[j][k] + 1 for k in range(len(cross_matrix[0]))]for j in range(len(cross_matrix))]
#         # print (matrix_add_block)
#         cross_matrix = []
#         for ch in char_list:
#             for l, taxon in enumerate(taxon_list):
#                 temp.append(ch + taxon)
#                 next_line = []
#                 for ch1 in char_list:
#                     if ch1 == ch:
#                         next_line.extend([cross_matrix_block[l][k] for k in range(len(cross_matrix_block[0]))])
#                     else:
#                         next_line.extend([matrix_add_block[l][k] for k in range(len(matrix_add_block[0]))])
#                 cross_matrix.append(next_line)
#                 # print(next_line)
#         taxon_list = temp
#     print (taxon_list)
#     # print ('\n'.join((str(x) for x in cross_matrix)))
#     
#     for taxon in taxa:
#         taxa[taxon] = [999 if taxa[taxon] != taxon_list[i] else 0 for i in range(len(taxon_list))]
#     # print (taxa)    
#     
#     tree_stack = []
#     taxon = ''
#     prev_symb = ''
#     for letter in tree:
#         if letter == '(' or letter == ',' or letter == ')' or letter == ';':
#             if (letter == ')' or letter == ',' or letter == ';') and prev_symb == ')':
#                 # cross last two taxa
#                 t1 = tree_stack.pop()
#                 t2 = tree_stack.pop()
#                 print ("Crossing %s with %s" % (t1, t2))
#                 print (taxa[t1])
#                 print (taxa[t2])
#                 taxa[taxon] = []
#                 for i, t in enumerate(taxon_list):
#                     v1 = min([taxa[t1][j] + cross_matrix[i][j] for j in range(len(taxon_list))])
#                     v2 = min([taxa[t2][j] + cross_matrix[i][j] for j in range(len(taxon_list))])
#                     taxa[taxon].append(v1 + v2)
#                 print(taxa[taxon])
#                 tree_stack.append(taxon)
#                 taxon = ''
#             if taxon:
#                 tree_stack.append(taxon)
#                 taxon = ''
#             prev_symb = letter
#         else:
#             taxon += letter
#     
#     print (taxa)
#     print (max(taxa[-1]))




# attempt number2
# from collections import Counter
# def get_distance(s1, s2):
#     result = 0
#     for i, letter in enumerate(s1):
#         if letter != s2[i]:
#             result += 1
#     return result
# 
# def get_consensus_str(str_list):
#     consensus_str = ''
#     # dist_counter = 0
#     for i in range(len(str_list[0])):
#         counter = Counter([stri[i] for stri in str_list])
#         next_val = counter.most_common()[0]
#         if next_val[0] == '-':
#             next_val = counter.most_common()[1]
#         consensus_str += next_val[0]
#         # dist_counter += (sum(counter.values()) - next_val[1])
#     # print (consensus_str)
#     # print (dist_counter)
#     return consensus_str
#     
# def ALPH(input_file, output_file):
#     with open(input_file) as resource:
#         tree = resource.readline().rstrip()
#         line = resource.readline().rstrip()
#         while line and line[0:1] != '>':
#             tree += line
#             line = resource.readline().rstrip()
#         
#         taxa = dict()
#         
#         taxon = ''
#         taxon_str = ''
#         while line:
#             if line[0:1] == '>':
#                 if taxon:
#                     taxa[taxon] = taxon_str
#                 taxon = line[1:]
#                 taxon_str = ''
#             else:
#                 taxon_str += line
#             line = resource.readline().rstrip()
#     if taxon:
#         taxa[taxon] = taxon_str
#     consensus_str = 'CACAT'  # get_consensus_str(list(taxa.values()))
#     print (consensus_str)
#     tree_stack = []
#     taxon = ''
#     prev_symb = ''
#     
#     result = dict()
#     distance = 0
#     for letter in tree:
#         if letter == '(' or letter == ',' or letter == ')' or letter == ';':
#             if (letter == ')' or letter == ',' or letter == ';') and prev_symb == ')':
#                 # cross last two taxa
#                 t1 = tree_stack.pop()
#                 t2 = tree_stack.pop()
#                 print ("Crossing %s with %s for %s" % (t1, t2, taxon))
#                 taxon_str = get_consensus_str([taxa[t1], taxa[t2], consensus_str])
#                 
#                 d1 = sum([0 if taxa[t1][i] == taxon_str[i] else 1 for i in range(len(taxon_str))])
#                 d2 = sum([0 if taxa[t2][i] == taxon_str[i] else 1 for i in range(len(taxon_str))])
#                 print ("%s (%d) + %s (%d) = %s" % (taxa[t1], d1, taxa[t2], d2, taxon_str))
#                 
#                 distance += d1 + d2
#                 result[taxon] = taxon_str
#                 taxa[taxon] = taxon_str
#                 tree_stack.append(taxon)
#                 taxon = ''
#             if taxon:
#                 tree_stack.append(taxon)
#                 taxon = ''
#             prev_symb = letter
#         else:
#             taxon += letter
#     print (distance)
#     print (result)
#     with open(output_file, 'w') as result_file:
#         result_file.write(str(distance))
#         for r in result:
#             result_file.write("\n>" + r + '\n' + result[r])        

# attempt #3
# make eval strings
#     priorities = [[0, 0, 0, 0, 0] for i in range (len(taxon_str))]
#     for taxon_str in taxa.values():
#         for i in range(len(taxon_str)):
#             priorities[i][LETTERS.index(taxon_str[i])] += 1    
#     print (priorities)
#     
# def get_consensus_str(str1, str2, priorities):
#     for i in range(len(str1)):
#         priorities[i][LETTERS.index(str1[i])] -= 1
#         priorities[i][LETTERS.index(str2[i])] -= 1
#     consensus_str = ''
#     for i in range(len(str1)):
#         if str1[i] == str2[i]:
#             consensus_str += str1[i]
#         else:
#             if str1[i] == '-':
#                 consensus_str += str2[i]
#             elif str2[i] == '-':
#                 consensus_str += str1[i]
#             elif priorities[i][LETTERS.index(str1[i])] >= priorities[i][LETTERS.index(str2[i])]:
#                 consensus_str += str1[i]
#             else:
#                 consensus_str += str2[i]
#             if priorities[i][LETTERS.index(str1[i])] == priorities[i][LETTERS.index(str2[i])]:
#                 print ("Eq priorities for %s and %s, %s chosen" % (str1[i], str2[i], consensus_str[i]))
#     for i in range(len(consensus_str)):
#         priorities[i][LETTERS.index(consensus_str[i])] += 1
#     
#     return consensus_str
#     

