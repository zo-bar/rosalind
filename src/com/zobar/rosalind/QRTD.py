'''
Created on Jun 27, 2015

@author: zoya
'''
from time import gmtime, strftime

def print_matrix(matrix):
    for i in range(len(matrix)):
        print (" ".join([str(bin(matrix[i][j]))[2:].zfill(len(matrix)) for j in range(len(matrix))]))
    
    
def cross_pairs(taxa1, taxa2, taxa, result, rest_taxa):
    # print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start crossing pairs for %s and %s" % (",".join(taxa1), ",".join(taxa2)))
    pairs_in = [(t1, t2) for t1 in taxa1 for t2 in taxa2]
    
    to = 0  # 2 ** len(taxa) - 1
    for t1 in taxa1:
        to += 2 ** t1
    for t2 in taxa2:
        to += 2 ** t2
    
    to1 = 2 ** len(taxa) - 1 - to
    for p in pairs_in:
#         if p[0] == 0 and p[1] == 4:
#             print (str(bin(result[p[0]][p[1]]))[2:].zfill(len(taxa)))
#             print (str(bin(to)[2:].zfill(len(taxa))))
#             print ("HERE")
        result[p[0]][p[1]] = result[p[0]][p[1]] | to1
        result[p[1]][p[0]] = result[p[1]][p[0]] | to1
    
    for t in range(len(taxa)):
        if t in taxa1 or t in taxa2:
            continue
        for r in rest_taxa:
            if r in taxa1 or r in taxa2:
                continue
            result[t][r] |= to
            result[r][t] |= to
#             pass
    #print_matrix(result)
    #print ("%s%s" % (taxa[taxa1[0]], taxa[taxa2[0]]))
    # print (result)
    return result

def get_fingerprints_list(taxa, tree):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing %s" % tree)
    print (len(taxa))
    last_symbol = ''
    taxon = ''
    taxa_stack = []
    
    counter = 0
    
    rest_taxa = [i for i in range(len(taxa))]
    result = [[0 for i in range(len(taxa))] for j in range (len(taxa))]  # [[0] * len(taxa)] * len(taxa)  # result = ['Unknown'] * total_len  # ['Unknown' for i in range(total_len)]
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
            if last_symbol == '(' or last_symbol == ',':
                if taxon:
                    taxa_stack.append([taxa.index(taxon)])  
                    counter += 1
                    if counter % 100 == 0:
                        print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(counter)) 
                    # print ("Add to taxa_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
            elif last_symbol == ')':
                t1 = taxa_stack.pop()
                t2 = taxa_stack.pop()
                
                if len(t1) == 1:
                    rest_taxa.remove(t1[0])
                if len(t2) == 1:
                    rest_taxa.remove(t2[0])
                cross_pairs(t1, t2, taxa, result, rest_taxa)
                taxa_stack.append(t1 + t2)
            last_symbol = next_symbol
            taxon = ''
        else:
            if next_symbol != ' ':
                taxon += next_symbol
    
    t1 = taxa_stack.pop()
    t2 = taxa_stack.pop()
    t3 = taxa_stack.pop()
    cross_pairs(t1, t2, taxa, result, rest_taxa)
    cross_pairs(t1, t3, taxa, result, rest_taxa)
    cross_pairs(t3, t2, taxa, result, rest_taxa)
    
#     t1_group = 0
#     for t in t1:
#         t1_group |= t
#     t2_group = 0
#     for t in t2:
#         t2_group |= t
#     t3_group = 0
#     for t in t3:
#         t3_group |= t
#     for i in range(len(taxa)):
#         # print (bin(2 ** len(taxa) - 1 - 2 ** i))
#         for j in range(i, len(taxa)):
#             result[i][j] &= 2 ** len(taxa) - 1 - 2 ** i
#             result[j][i] &= 2 ** len(taxa) - 1 - 2 ** i
    return [result, t1, t2, t3]

def count_quartets_in_groups(taxa, taxa_group1, taxa_group2, matrix1, matrix2):
    print ("Cross group %s and %s  ..." % (''.join([taxa[t] for t in taxa_group1]), ''.join([taxa[t] for t in taxa_group2])))
    group1 = 0
    for t in taxa_group1:
        group1 |= 2 ** t
    group2 = 0
    for t in taxa_group2:
        group2 |= 2 ** t
    
    quartets = 0
    if bin(group1 & group2).count('1') > 1:
        shared_taxa = bin(group1 & group2).count('1')
        shared_pairs = int(shared_taxa * (shared_taxa - 1) / 2)
        total_taxa = bin(group1 | group2).count('1')  # + bin(group2).count('1')
        other_taxa = len(taxa) - total_taxa
        other_pairs = int(other_taxa * (other_taxa - 1) / 2)
        quartets = shared_pairs * other_pairs
        #print ("Outer quartets count %d" % (quartets))
        for t1 in taxa_group1:
            for t2 in taxa_group2:
                shared_taxa = bin(matrix1[t1][t2] & matrix2[t1][t2] & group1 & group2).count('1')
                if shared_taxa > 1:
                    pair_count = int((shared_taxa) * (shared_taxa - 1) / 2)
                    quartets += pair_count
    #print ("Shared quartets count: %d" % (quartets))
    return quartets

def count_shared_quartets(taxa, matrix1, t11, t12, t13, matrix2, t21, t22, t23):
    print_matrix(matrix1)
    print_matrix(matrix1)
    print ("Start counting shared quartets count...")
    tsum = 0
    tsum += count_quartets_in_groups(taxa, t11, t21, matrix1, matrix2)
    tsum += count_quartets_in_groups(taxa, t11, t22, matrix1, matrix2)
    tsum += count_quartets_in_groups(taxa, t11, t23, matrix1, matrix2)
    tsum += count_quartets_in_groups(taxa, t12, t21, matrix1, matrix2)
    tsum += count_quartets_in_groups(taxa, t12, t22, matrix1, matrix2)
    tsum += count_quartets_in_groups(taxa, t12, t23, matrix1, matrix2)
    tsum += count_quartets_in_groups(taxa, t13, t21, matrix1, matrix2)
    tsum += count_quartets_in_groups(taxa, t13, t22, matrix1, matrix2)
    tsum += count_quartets_in_groups(taxa, t13, t23, matrix1, matrix2)
#     for i in range(len(taxa)):
#         for j in range(i + 1, len(taxa)):
#             counted_as_pairs = bin(matrix2[i][j] & matrix1[i][j])[(len(taxa) - i):].count('1')
#             shared_taxa = bin(matrix2[i][j] & matrix1[i][j])[:(len(taxa) - i)].count('1')
#             pair_count = 0
#             if shared_taxa > 1:
#                 pair_count = int((shared_taxa) * (shared_taxa - 1) / 2)
#             pair_count += shared_taxa * counted_as_pairs
#             tsum += pair_count
#             
#             # if (pair_count > 0):
#                 # print (bin(fps2[i][j] & fps1[i][j])[2:(len(taxa) - i)])
#             print ("%s%s share %d pairs (%s vs %s) (%d / %d)" % (taxa[i], taxa[j], pair_count, str(bin(matrix1[i][j])[2:]), str(bin(matrix2[i][j])[2:]), shared_taxa, counted_as_pairs))
    print (tsum)
    return tsum
    
def QRTD(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing")
    lines = [line.strip() for line in open(input_file)]
    taxa = lines[0].split(' ')
    tree1 = lines[1]
    tree2 = lines[2]
    # print (tree1)
    # print (tree2)
    
    fps1 = get_fingerprints_list(taxa, tree1)
    fps2 = get_fingerprints_list(taxa, tree2)
    
    tsum = count_shared_quartets(taxa, fps1[0], fps1[1], fps1[2], fps1[3], fps2[0], fps2[1], fps2[2], fps2[3])

    total = 0
    for k in range(len(taxa) - 2):
        # print (result)
        total += (k + 1) * (len(taxa) - k - 3) * (len(taxa) - k - 2) / 2
    print ("Total quartetes: %d" % total)
    
    result = int(2 * total - 2 * tsum)
    
    print ("Result: %d" % result)

    with open(output_file, 'w') as result_file:
        result_file.write(str(result))

QRTD("data/rosalind_qrtd.txt", "data/rosalind_qrtd_result.txt")


# shared pairs calculation - failed as root point differs
#     for i in range(len(fps1)):
#         print (" ".join([str(bin(fps1[i][j]))[2:].zfill(len(fps1)) for j in range(len(fps1))]))
#     print ("")
#     for i in range(len(fps2)):
#         print (" ".join([str(bin(fps2[i][j]))[2:].zfill(len(fps2)) for j in range(len(fps2))]))    
#     tsum = 0
#     for i in range(len(taxa)):
#         for j in range(i + 1, len(taxa)):
#             counted_as_pairs = bin(fps2[i][j] & fps1[i][j])[(len(taxa) - i):].count('1')
#             shared_taxa = bin(fps2[i][j] & fps1[i][j])[:(len(taxa) - i)].count('1')
#             pair_count = 0
#             if shared_taxa > 1:
#                 pair_count = int((shared_taxa) * (shared_taxa - 1) / 2)
#             pair_count += shared_taxa * counted_as_pairs
#             tsum += pair_count
#             
#             # if (pair_count > 0):
#                 # print (bin(fps2[i][j] & fps1[i][j])[2:(len(taxa) - i)])
#             print ("%s%s share %d pairs (%s vs %s) (%d / %d)" % (taxa[i], taxa[j], pair_count, str(bin(fps1[i][j])[2:]), str(bin(fps2[i][j])[2:]), shared_taxa, counted_as_pairs))
#     print (tsum)


# attemp #3. Still slow
# def cross_pairs(taxa1, taxa2, taxa, rest_pairs):
#     print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start crossing pairs for %s and %s" % (",".join(taxa1), ",".join(taxa2)))
#     new_pairs = []
#     tl = len(taxa)
#     
#     for t1 in taxa1:
#         for t2 in taxa2:
#             k = taxa.index(t1)
#             m = taxa.index(t2)
#             if k > m:
#                 m = k
#                 k = taxa.index(t2)
#             j = 0
#             for i in range(k):
#                 j += tl - i - 1
#             pair_index = j + m - k - 1
#             new_pairs.append(pair_index)
#     
#     exclude_pairs = []    
#     for t in taxa1 + taxa2:
#         k = taxa.index(t)
#         j = 0
#         for i in range(k):
#             exclude_pairs.append(j + k - i - 1)
#             j += tl - i - 1
#         for i in range(tl - k - 1):
#             exclude_pairs.append(j + i)
#     
#     new_pairs = set(new_pairs)
#     result = []
# #     for cp1 in rest_pairs - set(exclude_pairs):
# #         for cp2 in new_pairs:
# #             if cp1 < cp2:
# #                 result.append((cp1, cp2))
# #             else:
# #                 result.append((cp2, cp1))
# #                 
#     rest_pairs = rest_pairs - new_pairs
#     
#     return result
# 
# def get_fingerprints_list(taxa, tree):
#     print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing %s" % tree)
#     last_symbol = ''
#     taxon = ''
#     taxa_stack = []
#     
#     result = []  
#     rest_pairs = set([j for j in range(int(len(taxa) * (len(taxa) - 1) / 2))])
#         
#     for next_symbol in tree:
#         if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
#             if last_symbol == '(' or last_symbol == ',':
#                 if taxon:
#                     taxa_stack.append([taxon])   
#                     # print ("Add to taxa_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
#             elif last_symbol == ')':
#                 t1 = taxa_stack.pop()
#                 t2 = taxa_stack.pop()
# 
#                 r = len(result)
#                 result.extend(cross_pairs(t1, t2, taxa, rest_pairs))
#                 print (len(result) - r)
#                 taxa_stack.append(t1 + t2)
#             last_symbol = next_symbol
#             taxon = ''
#         else:
#             if next_symbol != ' ':
#                 taxon += next_symbol
# 
#     return result
#     
# def QRTD(input_file, output_file):
#     print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing")
#     lines = [line.strip() for line in open(input_file)]
#     taxa = lines[0].split(' ')
#     tree1 = lines[1]
#     tree2 = lines[2]
#     print (tree1)
#     print (tree2)
#     
#     fps1 = set(get_fingerprints_list(taxa, tree1))
#     fps2 = set(get_fingerprints_list(taxa, tree2))
#     print (sum([sum(f) for f in fps1]))
#     
#     total = len(fps1)
#     print ("Total quartetes: %d" % total)
#      
#     print ("Start counting matches...")
#     print (sorted(fps1))
#     print (sorted(fps2))
#     match = len([i for i in fps1 if i in fps2])
#     print ("Match count: %d" % match)
#     
#     result = int(2 * (total - match))
#     print ("Result: %d" % result)
# 
#     with open(output_file, 'w') as result_file:
#         result_file.write(str(result))
 


# attempt2. works too long
# import random
# from time import gmtime, strftime
# 
# def cross_pairs(taxa1, taxa2, taxa_list, processed_taxa):
#     print ("Start crossing pairs for %s and %s" % (",".join(taxa1), ",".join(taxa2)))
#     result = []
#     rest_taxa_list = [x for x in taxa_list if x not in processed_taxa]  # and x not in taxa1 and x not in taxa2]
#     rest_taxa_pairs = []
#     for i, t1 in enumerate(rest_taxa_list):
#         for t2 in rest_taxa_list[i + 1:]:
#             rest_taxa_pairs.append((t1, t2))
#         for t in processed_taxa - taxa1 - taxa2:
#             rest_taxa_pairs.append((t1, t))
#     for t1 in taxa1:
#         for t2 in taxa2:
#             for t3 in rest_taxa_pairs:
#                 result.append("".join(sorted([t1, t2, t3[0], t3[1]])))  
#     print (result)
#     return result
# 
# def get_fingerprints_list(taxa, taxa_dict, tree):
#     print ("Start processing %s" % tree)
#     result = []
#     last_symbol = ''
#     taxon = ''
#     taxa_stack = []
#     processed_taxa = set()
#      
#     for next_symbol in tree:
#         if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
#             if last_symbol == '(' or last_symbol == ',':
#                 if taxon:
#                     taxa_stack.append(set(taxon))   
#                     # print ("Add to taxa_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
#             elif last_symbol == ')':
#                 t1 = taxa_stack.pop()
#                 t2 = taxa_stack.pop()
# 
#                 processed_taxa.update(t1.union(t2))
#                 result.extend(cross_pairs(t1, t2, taxa, processed_taxa))
#                 
#                 taxa_stack.append(t1.union(t2))
#                 print ("Crossing %s and %s: %s" % (t1, t2, len(result)))
#             last_symbol = next_symbol
#             taxon = ''
#         else:
#             if next_symbol != ' ':
#                 taxon += next_symbol
#     # print (result)
#     return result
#     
# def QRTD(input_file, output_file):
#     print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + " Start processing")
#     lines = [line.strip() for line in open(input_file)]
#     taxa = lines[0].split(' ')
#     tree1 = lines[1]
#     tree2 = lines[2]
#     print (tree1)
#     print (tree2)
#      
#     taxa_dict = {taxon:(random.randint(0, 2 << 12), random.randint(0, 2 << 12)) for taxon in taxa}  # random.randint(0, 2 << 12) taxa.index(taxon) + 1
#     print (taxa_dict)
#      
#     fps1 = get_fingerprints_list(taxa, taxa_dict, tree1)
#     fps2 = get_fingerprints_list(taxa, taxa_dict, tree2)
#     total = len(fps1)
#     print ("Total quartetes: %d" % total)
#      
#     print ("Start counting matches...")
#     print (sorted(fps1))
#     print (sorted(fps2))
#     match = len([i for i in fps1 if i in fps2])
#     print ("Match count: %d" % match)
#     
#     result = int(2 * (total - match))
#     print ("Result: %d" % result)
# 
#     with open(output_file, 'w') as result_file:
#         result_file.write(str(result))
#  
# QRTD("data/rosalind_qrtd_test.txt", "data/rosalind_qrtd_result.txt")


# attempt 1. Missunderstood task
# import random
# from time import gmtime, strftime
# 
# CHECK_MULT = 3
# def cross_fingerprints(fing1, fing2):
#     return ((fing1[0] ^ fing2[0]), fing1[1] ^ fing2[1])
# 
# def get_fingerprints_list(taxa, taxa_dict, tree):
#     # print ("Start processing %s" % tree)
#     fingerprints = []
#     levels = []
#     last_symbol = ''
#     taxon = ''
#     taxa_stack = []
#     level = 0
#     
#     for next_symbol in tree:
#         if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
#             
#             if last_symbol == '(' or last_symbol == ',':
#                 if taxon:
#                     taxa_stack.append(((taxa_dict[taxon], taxa_dict[taxon] * CHECK_MULT), 1))
#                     # print ("Add to taxa_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
#             elif last_symbol == ')':
#                 t1 = taxa_stack.pop()
#                 t2 = taxa_stack.pop()
#                 t = cross_fingerprints(t1[0], t2[0])  
#                 taxa_stack.append((t, t1[1] + t2[1]))
#                 fingerprints.append((t, t1[1] + t2[1]))
#                 levels.append(level)
#                 print ("Crossing %s and %s: %s" % (t1, t2, fingerprints[-1]))
#             last_symbol = next_symbol
#             taxon = ''
#             if (next_symbol == '('):level += 1
#             elif (next_symbol == ')'):level -= 1
#             
#         else:
#             if next_symbol != ' ':
#                 taxon += next_symbol
#     # print (result)
#     # return result
#     return [fingerprints, levels]
# 
# def find_match_quartets_count(taxa, tree1, tree2):
#     taxa_dict = {taxon:random.randint(0, 2 << 11) for taxon in taxa}  # random.randint(0, 2 << 12) taxa.index(taxon) + 1
#     print (taxa_dict)
#     
#     n = len(taxa_dict)
#     fps1 = get_fingerprints_list(taxa, taxa_dict, tree1)
#     print (fps1)
#     fps2 = get_fingerprints_list(taxa, taxa_dict, tree2)
#     print (fps2)
#     
#     # print (fps1[1])
#     # print (min([fps1[1][i + 1] - fps1[1][i] for i in range(len(fps1[1]) - 1)]))
#     # print (min([fps2[1][i + 1] - fps2[1][i] for i in range(len(fps2[1]) - 1)]))
#     
#     total_cross = (0, 0)
#     for taxon in taxa:
#         total_cross = cross_fingerprints((taxa_dict[taxon], taxa_dict[taxon] * CHECK_MULT), total_cross)  # (total_cross[0] ^ taxa_dict[taxon], int(total_cross[1] * (taxa_dict[taxon])))  # cross_fingerprints((, taxa_dict[taxon]), total_cross)#cross_fingerprints((taxa_dict[taxon], taxa_dict[taxon]), total_cross)  # (total_cross[0] ^ taxa_dict[taxon], int(total_cross[1] * taxa_dict[taxon]) % 1000000000000)  # cross_fingerprints((, taxa_dict[taxon]), total_cross)
#     print (total_cross)
#     print ("Start counting matches...")
#     match = 0
#     counted_pairs = [0 for i in range(len(taxa) - 2)]
#     counter = 0
#     for i, f2 in enumerate(fps2[0]):
#         f2_addition = (cross_fingerprints(total_cross, f2[0]), n - f2[1])  # ((total_cross[0] ^ f2[0][0], int(total_cross[1] / f2[0][1])), n - f2[1])
# 
#         level = fps2[1][i]
#         tail_pairs = 0
#         tail_used_pairs = 0 
#         while (level < len(counted_pairs) - 1):
#             tail_used_pairs += counted_pairs.pop()
#         while (level > len(counted_pairs) - 1):
#             counted_pairs.append(0)
#         
#         if (fps1[0].count(f2) > 0 or fps1[0].count(f2_addition) > 0):  # and fps1[1][fps1.index(f2)] == fps2[1][i] or fps1[0].count(f2_addition) > 0):    
#             print (f2)
#             print (f2_addition)
#             print (fps1[0].count(f2))
#             rest_used_pairs = int(sum(counted_pairs))
#             tail_len = f2[1]
#             tail_pairs = int(tail_len * (tail_len - 1) / 2)
#             rest_pairs = int((n - tail_len) * (n - tail_len - 1) / 2)
#             new_quartets = (tail_pairs - tail_used_pairs) * (rest_pairs - rest_used_pairs)
#             match += new_quartets  # - used_pairs * (n - tail_len)
# 
#             print ("Common edge %d(#%d), tail length %d, in use tail: %d, in use rest: %d, edge quartets count: %d, match: %d" % (f2[0][0], i, f2[1], tail_used_pairs, rest_used_pairs, new_quartets, match))
#             tail_used_pairs = tail_pairs
#             counter += 1
#         
#         counted_pairs.append(tail_used_pairs + counted_pairs.pop())
#     
#     print (counter)
#     return match
# 
# def QRTD(input_file, output_file):
#     print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + " Start processing")
#     lines = [line.strip() for line in open(input_file)]
#     taxa = lines[0].split(' ')
#     tree1 = lines[1]
#     tree2 = lines[2]
#     print (tree1)
#     print (tree2)
#     
#     match = find_match_quartets_count(taxa, tree1, tree2)
#     print ("Match count: %d" % match)
#     
#     total = 0
#     for k in range(len(taxa) - 2):
#         total += (k + 1) * (len(taxa) - k - 3) * (len(taxa) - k - 2) / 2
#     print ("Total quartetes: %d" % total)
#     result = int(2 * (total - match))
#     
#     print (result)
#     print (int(2 * total))
#     with open(output_file, 'w') as result_file:
#         result_file.write(str(result))
# 
# QRTD("data/rosalind_qrtd1.txt", "data/rosalind_qrtd_result.txt")

#     print (7 ^ 1)
#     print (7 * 3 ^ 1 * 3)
#     print (5 ^ 3)
#     print (5 * 3 ^ 3 * 3)
#     
# which is obvious :)
# def test_mid_crossing():
#     a = 5
#     b = 1
#     c = 7
#     d = 4
#     e = 3
#     f = 6
#     
#     ab = a ^ b
#     abc = a ^ b ^ c
#     def1 = d ^ e ^ f
#     cdef = c ^ d ^ e ^ f
#     abcdef = a ^ b ^ c ^ d ^ e ^ f
#     
#     print ("abc=%s, def=%s, abc^abcdef=%s" % (abc, def1, abc ^ abcdef))
#     print ("ab=%s, cdef=%s, ab^abcdef=%s" % (ab, cdef, ab ^ abcdef))
#     
# test_mid_crossing()


# def get_fingerprints_list(taxa, taxa_dict, tree):
#     # print ("Start processing %s" % tree)
#     total_cross = 0
#     for taxon in taxa:
#         total_cross = cross_fingerprints(taxa_dict[taxon], total_cross)
#     n = len(taxa)
#     
#     result = []
#     last_symbol = ''
#     taxon = ''
#     taxa_stack = []
#     
#     m = int((n - 2) * (n - 3) / 2)
#     print (m)  
#       
#     for next_symbol in tree:
#         if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
#             if last_symbol == '(' or last_symbol == ',':
#                 if taxon:
#                     taxa_stack.append((taxa_dict[taxon], 1, 0))
#                     # print ("Add to taxa_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
#             elif last_symbol == ')':
#                 t1 = taxa_stack.pop()
#                 t2 = taxa_stack.pop()
#                 t = cross_fingerprints(t1[0], t2[0])  
#                 # print ("Crossing %s and %s: %s" % (t1, t2, t))
#                 taxa_stack.append((t, t1[1] + t2[1], int(m * t2[1])))
#                 result.append(taxa_stack[-1])  # (t, t1[1] + t2[1], int(t1[1] * t2[1] * (m * (m - 1) / 2))))  # int(t1[1] * t2[1] * n * (n - 1) / 2)))
#                 print ("Crossing %s and %s: %s" % (t1, t2, taxa_stack[-1]))
#                 m -= int(t1[1] * t2[1])
#                 print (m)
#                 
# #                 result.append((cross_fingerprints(total_cross, t), n - t1[1] - t2[1], int(t1[1] * t2[1] * (m * (m - 1) / 2))))
# #                 print (result[-1])
# #                 print (result[-2])
#             last_symbol = next_symbol
#             taxon = ''
#         else:
#             if next_symbol != ' ':
#                 taxon += next_symbol
#     # print (result)
#     return result

# shared = []
#     i = len(fingerprints1) - 1
#     j = len(fingerprints2) - 1
#     while i > -1 and j > -1:
#         if fingerprints1[i] == fingerprints2[j]:
#             # print ("Shared: %d" % fingerprints1[i])
#             shared.append(fingerprints1[i])
#             i -= 1
#             j -= 1
#         elif  fingerprints1[i] > fingerprints2[j]:
#             i -= 1
#         elif fingerprints1[i] < fingerprints2[j]:
#             j -= 1
#     

# match_count = 0
#         taxa_len = len(taxa)
#         for el in new_match:
#             len1 = el[1]
#             len2 = taxa_len - len1
#             match_count += (len1 * (len1 - 1) / 2) * (len2 * (len2 - 1) / 2)
#         # print (match_count)
#         
#         if (len(new_match) < len(match)):
#             print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "%d Update match %d" % (i, len(new_match)))
#             print (new_match)
#             print (match_count)
#             match = new_match
#         if not len(new_match) in eq_count.keys():
#             eq_count[len(new_match)] = 0
#         eq_count[len(new_match)] += 1
#    

# eq_count = dict()
#     match = [i for i in range(len(taxa))]
#     for i in range(1):
#         new_match = find_distance(taxa, tree1, tree2)
#         
#         
#     print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(sorted(["%d:%d" % (x, eq_count[x]) for x in eq_count])))
#     match_count = 0
#     taxa_len = len(taxa)
#     for el in match:
#         match_count += el[2]
#     
#     total = 0
#     for k in range(taxa_len - 2):
#         # print (result)
#         total += (k + 1) * (taxa_len - k - 3) * (taxa_len - k - 2) / 2
#          print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Match count: %d, total count: %d" % (match_count, total))

# mult = 1
    # for el in taxa_dict:
    #    mult *= taxa_dict[el]
    # print (mult)
    # print (taxa_dict['E'] * taxa_dict['F'] * taxa_dict['G'])
    # abcdh = taxa_dict['A'] * taxa_dict['B'] * taxa_dict['C'] * taxa_dict['D'] * taxa_dict['H'] 
    # print (abcdh)
    # print (int(mult / abcdh))
    
    
   
