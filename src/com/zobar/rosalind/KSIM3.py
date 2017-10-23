'''
Created on Feb 16, 2016

@author: zoya
'''

from time import gmtime, strftime, time
MATCH_SCORE = 0
MISMATCH_SCORE = -1
test_mode = True
check_mode = False
update_time = 0

def print_matrix(matrix, string1, string2):
    print ("    " + " "*3 + (" "*3).join(string2))
    for i in range(len(matrix)):
        stri = ' '
        if i > 0:
            stri = string1[i - 1]
        print (stri + " " + " ".join(str(x).zfill(3) for x in matrix[i]))
        
def create_distance_matrix(string1, string2):
    tt = time()
    
    len1 = len(string1)
    len2 = len(string2)
    print (len1)
    print (len2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    # matrix[0] = [i * MISMATCH_SCORE for i in range(len(matrix[0]))]
    # for i in range(len(matrix)):
    #    matrix[i][0] = i * MISMATCH_SCORE
    print (strftime("%Y-%m-%d %H:%M:%S Motif len:", gmtime()) + str(len1 + 1))
    for i in range(1, len1 + 1):
        if not test_mode and i % 100 == 0: print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(i))
        
        si = string1[i - 1]
        max_val = 0  # MISMATCH_SCORE
        up = matrix[i - 1][0]
        # sj_arr = list(string2)
        for j in range(1, len2 + 1):
            left = max_val  # + MISMATCH_SCORE
            diag = up  # + (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE)
            up = matrix[i - 1][j]  # + (MISMATCH_SCORE)  # if j < len2 + 1 else 0)
            
            # max_val = max(up + MISMATCH_SCORE, left + MISMATCH_SCORE, diag + (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE))
#             if si != sj_arr.pop():  # string2[j - 1]:
#                 max_val = 1
            if si == string2[j - 1]:
                max_val = diag
            else:
                max_val = diag + MISMATCH_SCORE
            if max_val < up + MISMATCH_SCORE:
                max_val = up + MISMATCH_SCORE
            if max_val < left + MISMATCH_SCORE:
                max_val = left + MISMATCH_SCORE
            matrix[i][j] = max_val
            
    if test_mode: print_matrix(matrix, string1, string2)
    print (time() - tt)
    return matrix

def update_dict(dict1_i, dict2, j, step, dist):
    global update_time 
    tt = time()
    for k in dict1_i.keys():
        if dict1_i[k] + step <= dist:
            if not j in dict2.keys():
                dict2[j] = dict()
            if not k in dict2[j].keys() or dict2[j][k] > dict1_i[k] + step:
                dict2[j][k] = dict1_i[k] + step
    update_time += time() - tt
    
def get_trace_back_dicts(string1, string2, matrix, dist):
    print (strftime("%Y-%m-%d %H:%M:%S Start checking paths", gmtime()))
    result = set()
    len1 = len(string1)
    len2 = len(string2)
    
    prev_back = dict()
    
    for j in range(len2, -1, -1):
        if not test_mode and j % 1000 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "%d" % j)
        if matrix[len1][j] >= -dist:
            if len1 not in prev_back.keys():
                prev_back[len1] = dict()
            prev_back[len1][j] = 0
        if len(prev_back.keys()) == 0:
            continue
        
        sj = string2[j - 1]
        next_back = dict()
        for i in range(len1 + 1, 0 , -1):
            if i in prev_back.keys():
                # diag
                if matrix[i - 1][j - 1] >= -dist:
                    
                    # if diag_distance >= -1:
                    if string1[i - 1] != sj:
                        update_dict(prev_back[i], next_back, i - 1, 1, dist)
                    else:
                        diag_distance = matrix[i][j] - matrix[i - 1][j - 1]
                
                        if diag_distance == MATCH_SCORE:
                            update_dict(prev_back[i], next_back, i - 1, 0, dist)
                # up 
                if matrix[i - 1][j] >= -dist:
                    update_dict(prev_back[i], prev_back, i - 1, 1, dist)
                # left
                if matrix[i][j - 1] >= -dist:
                    update_dict(prev_back[i], next_back, i, 1, dist)
                                
                prev_back.pop(i)
                 
                if len(prev_back.keys()) == 0:
                    break
        
        if 0 in prev_back.keys():
            for res in prev_back[0].keys():
                for k in range(dist - prev_back[0][res] + 1):
                    if j + 1 - k >= 0:
                        result.add((j + 1 - k, res - j + k))
            
            if test_mode: print ('\n'.join(["Start:%d, len:%d" % (x[0], x[1]) for x in result]))
        
        prev_back = next_back
    
    print (update_time)
    return result

def check_result(file1, file2):
    print ("Start checking result")
    r1 = []
    with open(file1) as f1:
        line = f1.readline().rstrip()
        while (line):
            r1.append(line)
            line = f1.readline().rstrip()
    
    r2 = []
    with open(file2) as f2:
        line = f2.readline().rstrip()
        while (line):
            r2.append(line)
            line = f2.readline().rstrip()
            
    if len(r1) != len(r2):
        print ("Len differs: %d vs %d" % (len(r1), len(r2)))
    
    for r11 in r1:
        if not r11 in r2:
            print ("%s found in file %s and not found in %s" % (r11, file1, file2))

    for r22 in r2:
        if not r22 in r1:
            print ("%s found in file %s and not found in %s" % (r22, file2, file1))

# works great but slow - about 5 mins on real data 
def get_trace_back_pairs(string1, string2, matrix, dist):
    print (strftime("%Y-%m-%d %H:%M:%S Start checking paths", gmtime()))
    result = set()
    len1 = len(string1)
    len2 = len(string2)
    
    prev_back = dict()
    
    for j in range(len2, -1, -1):
        if matrix[len1][j] >= -dist:
            if len1 not in prev_back.keys():
                prev_back[len1] = set()
            prev_back[len1].add((matrix[len1][j] + dist, j))
        if len(prev_back.keys()) == 0:
            continue
        
        if test_mode:print ("j: %d" % j)
        if test_mode:print (prev_back)
        next_back = dict()
        for i in range(len1 + 1, 0 , -1):
            if i in prev_back.keys():
                # diag
                diag_distance = matrix[i][j] - matrix[i - 1][j - 1]
                if string1[i - 1] != string2[j - 1]:
                    if diag_distance == MISMATCH_SCORE:
                        next_back[i - 1] = set([x for x in prev_back[i]])
                    elif diag_distance == MATCH_SCORE:
                        # better path used for matrix, but this path works as well
                        for k in prev_back[i]:
                            if k[0] > 0:
                                if not i - 1 in next_back.keys():
                                    next_back[i - 1] = set()
                                next_back[i - 1].add((k[0] - 1, k[1]))
                else:
                    if diag_distance == MATCH_SCORE:
                        next_back[i - 1] = set([x for x in prev_back[i]])
                # up 
                up_distance = matrix[i][j] - matrix[i - 1][j]
                if up_distance == MISMATCH_SCORE:
                    if i - 1 in prev_back.keys():
                        prev_back[i - 1].update(prev_back[i])
                    else:
                        prev_back[i - 1] = set([x for x in prev_back[i]])
                elif up_distance >= MATCH_SCORE:
                    # better path used for matrix, but this path works as well
                    # print (prev_back)
                    for k in prev_back[i]:
                        if k[0] > up_distance - MATCH_SCORE:
                            if not i - 1 in prev_back.keys():
                                prev_back[i - 1] = set()
                            prev_back[i - 1].add((k[0] - (up_distance - MATCH_SCORE) - 1, k[1]))
                # left
                left_distance = matrix[i][j] - matrix[i][j - 1]
                if left_distance == MISMATCH_SCORE:
#                     if i == len1:
#                         next_back[i] = set([(x[0] + 1, x[1]) for x in prev_back[i] if x[]])
#                     else:
                    if i in next_back.keys():
                        next_back[i].update(prev_back[i])
                    else:
                        next_back[i] = set([x for x in prev_back[i]])
                elif left_distance >= MATCH_SCORE:
                    # better path used for matrix, but this path works as well
                    for k in prev_back[i]:
                        if k[0] > left_distance - MATCH_SCORE:
                            if not i in next_back.keys():
                                next_back[i] = set()
                            next_back[i].add((k[0] - (left_distance - MATCH_SCORE) - 1, k[1]))
                            
                prev_back.pop(i)
                 
                if len(prev_back.keys()) == 0:
                    break
        
        if 0 in prev_back.keys():
            for res in prev_back[0]:
                for k in range(res[0] + 1):
#                     if k >= 1:
#                         print ("HERE")
                    result.add((j + 1 - k, res[1] - j + k))
            
            if test_mode: print ('\n'.join(["Start:%d, len:%d" % (x[0], x[1]) for x in result]))
        
        prev_back = next_back

    return result

def KSIM(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start KSIM", gmtime())) 
    
    with open(input_file) as resource:
        k = int(resource.readline().rstrip())
        s = resource.readline().rstrip()
        t = resource.readline().rstrip()
    if test_mode: print ("k: %d, s:%s, t:%s" % (k, s, t))
    
    matrix = create_distance_matrix(s, t)
    print (strftime("%Y-%m-%d %H:%M:%S Matrix done", gmtime())) 
    
    tt = time()
    result = set(get_trace_back_dicts(s, t, matrix, k))
    print ("Matrix processing time: %d" % (time() - tt))
    
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Finished")
        
    if test_mode: print ('\n'.join(str(r[0]) + ' ' + str(r[1]) for r in sorted(result)))
    
    if check_mode:  # and False
        print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start check result")
        tt = time()
        result1 = set(get_trace_back_pairs(s, t, matrix, k))
        print ("Checking time: %d" % (time() - tt))
    
        print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start comparing results")
        print (len(result))
        if len (result) != len(result1):
            print("len differs: %d vs %d" % (len(result), len(result1)))
        else:
            print ("Same length")
        if result == result1:
            print ("Same results")
        else:
            if len(result1 - result) > 0:
                print ("Answer has:")
                print (result1 - result)
            if len(result - result1) > 0:
                print ("Curr result has:")
                print (result - result1)
    
    with open(output_file, "w") as result_file:
        result_file.write('\n'.join(str(r[0]) + ' ' + str(r[1]) for r in sorted(result)))
        
    
# test on big data with result  
# test_mode = False      
# KSIM("data/rosalind_ksim_test_big.txt", "data/rosalind_ksim_big_result.txt")
# check_result("data/rosalind_ksim_big_result.txt", "data/rosalind_ksim_test_big_answ.txt")

# test and compare with known result
# test_mode = False
# check_mode = True
# KSIM("data/rosalind_ksim_test.txt", "data/rosalind_ksim3_result.txt")
# check_result("data/rosalind_ksim0_result.txt", "data/rosalind_ksim3_result.txt")

# main
test_mode = False
KSIM("data/rosalind_ksim.txt", "data/rosalind_ksim_result.txt")
    
def get_trace_back_matrix(string1, string2, matrix, k):
    print (strftime("%Y-%m-%d %H:%M:%S Start checking paths", gmtime()))
    
    len1 = len(string1)
    len2 = len(string2)
    back_matrix = [[[] for y in range(len2 + 1)] for x in range(len1 + 1)]
    
    for j in range(len1 - 2, len2 + 1):
        if matrix[len1][j] >= -k:
            back_matrix[len1][j].append(j)
    
    i = len1
    while i > 0:
        if not test_mode and i % 100 == 0: print (strftime("%Y-%m-%d %H:%M:%S i:", gmtime()) + str(i))
    
        j = len2
        while j > 0:
            if not test_mode and j % 100 == 0: print (strftime("%Y-%m-%d %H:%M:%S   j:", gmtime()) + str(j))
    
            if len(back_matrix[i][j]) > 0:
                if matrix[i - 1][j - 1] == matrix[i][j] - (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE):
                    back_matrix[i - 1][j - 1].extend(back_matrix[i][j])
                if matrix[i - 1][j] == matrix[i][j] - (MISMATCH_SCORE if j > 0 and j < len(string2) + 1 else 0):
                    back_matrix[i - 1][j].extend(back_matrix[i][j])
                if matrix[i][j - 1] == matrix[i][j] - MISMATCH_SCORE:
                    back_matrix[i][j - 1].extend(back_matrix[i][j])
            j -= 1
        i -= 1
    if test_mode: print_matrix(back_matrix, string1, string2)
    return back_matrix          
    
def get_trace_back_array(string1, string2, matrix, k):
    print (strftime("%Y-%m-%d %H:%M:%S Start checking paths", gmtime()))
    result = []
    len1 = len(string1)
    len2 = len(string2)
    
    prev_back = dict()
    
    for j in range(len2, -1, -1):
        if matrix[len1][j] >= -k:
            prev_back[len1] = set({0})
        if len(prev_back.keys()) == 0:
            continue
        
        print ("j: %d" % j)
        print (prev_back)
        next_back = dict()
        for i in range(len1 + 1, 0 , -1):
            if i in prev_back.keys():
                # diag
                if matrix[i - 1][j - 1] == matrix[i][j] - (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE):
                    next_back[i - 1] = set([x + 1 for x in prev_back[i]])
                # up 
                if matrix[i - 1][j] == matrix[i][j] - (MISMATCH_SCORE):  # if j > 0 and j < len(string2) + 1 else 0):
                    if i - 1 in prev_back.keys():
                        prev_back[i - 1].update(prev_back[i])  # [x + 1 for x in prev_back[i]])
                    else:
                        prev_back[i - 1] = set(prev_back[i])  # [x + 1 for x in prev_back[i]])
                # left
                if matrix[i][j - 1] == matrix[i][j] - MISMATCH_SCORE:
                    if i in next_back.keys():
                        next_back[i].update([x + 1 for x in prev_back[i]])
                    else:
                        next_back[i] = set([x + 1 for x in prev_back[i]])
                prev_back.pop(i) 
                if len(prev_back.keys()) == 0:
                    break
        
        if 0 in prev_back.keys():
            result.extend([(j + 1, x) for x in prev_back[0]])
            if test_mode: print ('\n'.join(["Start:%d, len:%d" % (j + 1, x) for x in prev_back[0]]))
        
        prev_back = next_back

    return result
    
def get_trace_back_dict(string1, string2, matrix, k):
    print (strftime("%Y-%m-%d %H:%M:%S Start checking paths", gmtime()))
    result = []
    len1 = len(string1)
    len2 = len(string2)
    
    prev_back = dict()
    
    for j in range(len2, -1, -1):
        if matrix[len1][j] >= -k:
            prev_back[len1] = {matrix[len1][j] + k:set({j})}
        if len(prev_back.keys()) == 0:
            continue
        
        print ("j: %d" % j)
        print (prev_back)
        next_back = dict()
        for i in range(len1 + 1, 0 , -1):
            if i in prev_back.keys():
                # diag
                if matrix[i - 1][j - 1] == matrix[i][j] - (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE):
                    next_back[i - 1] = prev_back[i]
                # up 
                if matrix[i - 1][j] == matrix[i][j] - (MISMATCH_SCORE):  # if j > 0 and j < len(string2) + 1 else 0):
                    if i - 1 in prev_back.keys():
                        if 0 in prev_back[i - 1].keys():
                            prev_back[i - 1].update(prev_back[i])
                        else:
                            prev_back[i - 1] = prev_back[i]
                    else:
                        prev_back[i - 1] = prev_back[i]
                # left
                if matrix[i][j - 1] == matrix[i][j] - MISMATCH_SCORE:
                    if i in next_back.keys():
                        if 0 in next_back[i].keys():
                            next_back[i][0].update(prev_back[i][0])
                        else:
                            next_back[i][0] = prev_back[i][0]
                    else:
                        next_back[i] = prev_back[i]
                
                if len([x for x in prev_back[i].keys() if x != 0]) > 0:
                    print ("HERE")
                    # diag
                    if matrix[i - 1][j - 1] == matrix[i][j] - MISMATCH_SCORE and string1[i - 1] != string2[j - 1]:
                        if not i - 1 in next_back.keys():
                            next_back[i - 1] = dict()
                        for k in prev_back[i].keys():
                            if k > 0:
                                next_back[i - 1][k - 1] = prev_back[i][k]
                    # up 
                    if matrix[i - 1][j] == matrix[i][j]:
                        for k in range(len2):
                            if k in prev_back[i].keys():
                                if k - 1 in prev_back[i - 1].keys():
                                    prev_back[i - 1][k - 1].update(prev_back[i][k])
                                else:
                                    prev_back[i - 1][k - 1] = prev_back[i][k]
                    # left
                    if matrix[i][j - 1] == matrix[i][j]:
                        for k in range(len2):
                            if k in prev_back[i].keys():
                                if k - 1 in next_back[i].keys():
                                    next_back[i][k - 1].update(prev_back[i][k])
                                else:
                                    next_back[i][k - 1] = prev_back[i][k]                    
                
                prev_back.pop(i)
                 
                if len(prev_back.keys()) == 0:
                    break
        
        if 0 in prev_back.keys():
            result.extend([(j + 1, x - j) for x in prev_back[0][0]])
            if test_mode: print ('\n'.join(["Start:%d, len:%d" % (j + 1, x - j) for x in prev_back[0][0]]))
        
        prev_back = next_back

    return result

def get_trace_back_cells(string1, string2, matrix, dist):
    print (strftime("%Y-%m-%d %H:%M:%S Start checking paths", gmtime()))
    result = []
    len1 = len(string1)
    len2 = len(string2)
    
    prev_back = dict()
    
    for j in range(len2, -1, -1):
        if matrix[len1][j] >= -dist:
            prev_back[len1] = {matrix[len1][j] + dist : set({j})}
        if len(prev_back.keys()) == 0:
            continue
        
        print ("j: %d" % j)
        print (prev_back)
        next_back = dict()
        for i in range(len1 + 1, 0 , -1):
            if i in prev_back.keys():
                # diag
                diag_distance = matrix[i][j] - matrix[i - 1][j - 1]
                if string1[i - 1] != string2[j - 1]:
                    if diag_distance == MISMATCH_SCORE:
                        next_back[i - 1] = dict.copy(prev_back[i])
                    elif diag_distance == MATCH_SCORE:
                        # better path used for matrix, but this path works as well
                        for k in prev_back[i].keys():
                            if k > 0:
                                if not i - 1 in next_back.keys():
                                    next_back[i - 1] = dict()
                                next_back[i - 1][k - 1] = prev_back[i][k]
                else:
                    if diag_distance == MATCH_SCORE:
                        next_back[i - 1] = dict.copy(prev_back[i])
                # up 
                up_distance = matrix[i][j] - matrix[i - 1][j]
                if up_distance == MISMATCH_SCORE:
                    if i - 1 in prev_back.keys():
                        for k in prev_back[i].keys():
                            if k in prev_back[i - 1].keys():
                                prev_back[i - 1][k].update(prev_back[i][k])
                            else:
                                prev_back[i - 1][k] = set([x for x in prev_back[i][k]])
                    else:
                        prev_back[i - 1] = dict.copy(prev_back[i])
                elif up_distance == MATCH_SCORE:
                    # better path used for matrix, but this path works as well
                    for k in prev_back[i].keys():
                        if k > 0:
                            if not i - 1 in prev_back.keys():
                                prev_back[i - 1] = dict()
                            if k - 1 in prev_back[i - 1].keys():
                                prev_back[i - 1][k - 1].update([x for x in prev_back[i][k]])
                            else:
                                prev_back[i - 1][k - 1] = set([x for x in prev_back[i][k]])
                # left
                left_distance = matrix[i][j] - matrix[i][j - 1]
                if left_distance == MISMATCH_SCORE:
                    if i in next_back.keys():
                        for k in prev_back[i].keys():
                            if k in next_back[i].keys():
                                next_back[i][k].update(prev_back[i][k])
                            else:
                                next_back[i][k] = set([x for x in prev_back[i][k]])
                    else:
                        next_back[i] = dict.copy(prev_back[i])
                elif left_distance == MATCH_SCORE:
                    # better path used for matrix, but this path works as well
                    for k in prev_back[i].keys():
                        if k > 0:
                            if not i in next_back.keys():
                                next_back[i] = dict()
                            if k - 1 in next_back[i].keys():
                                next_back[i][k - 1].update([x for x in prev_back[i][k]])
                            else:
                                next_back[i][k - 1] = set([x for x in prev_back[i][k]])                   
            
                prev_back.pop(i)
                 
                if len(prev_back.keys()) == 0:
                    break
        
        if 0 in prev_back.keys():
            result.extend([(j + 1, x - j) for x in prev_back[0][0]])
            if test_mode: print ('\n'.join(["Start:%d, len:%d" % (j + 1, x - j) for x in prev_back[0][0]]))
        
        prev_back = next_back

    return result

class CellCandidate():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.gaps = dict()
    
    def add_candidates(self, candidates_list, gap):
        if gap in self.gaps.keys():
            self.gaps[gap].extend(candidates_list)
        else:
            self.gaps[gap] = candidates_list

