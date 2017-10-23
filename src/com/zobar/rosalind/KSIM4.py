'''
Created on Mar 8, 2016

@author: zoya
'''

from time import gmtime, strftime, time
MATCH_SCORE = 0
MISMATCH_SCORE = -1
test_mode = True
check_mode = False

update_time = 0
def update_dict(dict1, dict2, i, j, step, dist):
    global update_time 
    tt = time()
    if i in dict1.keys():
        for k in dict1[i].keys():
            if dict1[i][k] + step <= dist:
                if not j in dict2.keys():
                    dict2[j] = dict()
                if not k in dict2[j].keys() or dict2[j][k] > dict1[i][k] + step:
                    dict2[j][k] = dict1[i][k] + step
    update_time += time() - tt

# has errors. + way too slow!
def process_strings_3dicts(string1, string2, dist):
    len1 = len(string1)
    len2 = len(string2)
    print (len1)
    print (len2)
    
    result = set()
    
    prev_column = dict()
    prev_column_right_used = dict()
    prev_column_up_used = dict()
    prev_column_up_right_used = dict()
        
#     for l in range(1, dist):
#         prev_column[l] = dict()
#         prev_column[l][0] = prev_column[l - 1][0] + 1
    
    for j in range(len2):
        if not test_mode and j % 100 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "%d" % j)
        if test_mode:print ("j: %d" % j)
        
        next_column = dict()
        next_column_right_used = dict()
        next_column_up_used = dict()
        next_column_up_right_used = dict()
        
        if string1[0] == string2[j]:
            if 0 not in prev_column_up_used.keys():
                prev_column_up_right_used[0] = dict()
            prev_column_up_right_used[0][j] = 0
        else:
            if 0 not in prev_column.keys():
                prev_column[0] = dict()
            prev_column[0][j] = 1
        
        for i in range(len1 - 1):
            if i in prev_column.keys() or i in prev_column_up_used.keys() or i in prev_column_up_right_used.keys():
                # if test_mode:print ("i: %d" % i)
                # right
                if j < len2 - 1 and string1[i] == string2[j + 1]:
                    update_dict(prev_column, next_column_up_right_used, i, i, 0, dist)
                    update_dict(prev_column_up_used, next_column_up_right_used, i, i, 0, dist)
                    update_dict(prev_column_right_used, next_column_right_used, i, i, 1, dist)
                    update_dict(prev_column_up_right_used, next_column_right_used, i, i, 1, dist)
                else:
                    update_dict(prev_column, next_column, i, i, 1, dist)
                    update_dict(prev_column_up_used, next_column, i, i, 1, dist)
                    update_dict(prev_column_right_used, next_column_right_used, i, i, 1, dist)
                    update_dict(prev_column_up_right_used, next_column_right_used, i, i, 1, dist)
                # diag
                if i < len1 - 1 and j < len2 - 1 and string1[i + 1] != string2[j + 1]:
                    update_dict(prev_column, next_column, i, i + 1, 1, dist)
                    update_dict(prev_column_up_used, next_column, i, i + 1, 1, dist)
                    update_dict(prev_column_right_used, next_column, i, i + 1, 1, dist)
                    update_dict(prev_column_up_right_used, next_column, i, i + 1, 1, dist)
                else:
                    update_dict(prev_column, next_column_up_right_used, i, i + 1, 0, dist)
                    update_dict(prev_column_up_used, next_column_up_right_used, i, i + 1, 0, dist)
                    update_dict(prev_column_right_used, next_column_up_right_used, i, i + 1, 0, dist)
                    update_dict(prev_column_up_right_used, next_column_up_right_used, i, i + 1, 0, dist)
                # down
                if i < len1 - 1 and string1[i + 1] == string2[j]:
                    update_dict(prev_column_up_used, prev_column_up_used, i, i + 1, 1, dist)
                    update_dict(prev_column, prev_column_up_right_used, i, i + 1, 0, dist)
                    update_dict(prev_column_right_used, prev_column_up_right_used, i, i + 1, 0, dist)
                    update_dict(prev_column_up_right_used, prev_column_up_right_used, i, i + 1, 1, dist)
                else:
                    update_dict(prev_column, prev_column, i, i + 1, 1, dist)
                    update_dict(prev_column_up_used, prev_column_up_used, i, i + 1, 1, dist)
                    update_dict(prev_column_right_used, prev_column, i, i + 1, 1, dist)
                    update_dict(prev_column_up_right_used, prev_column_up_used, i, i + 1, 1, dist)
                       
        if test_mode:
            print ('     ' + string2[j])
            for print_k in range(len1):
                val = ''
                if print_k in prev_column.keys():
                    val += "N" + str(prev_column[print_k])
                if print_k in prev_column_right_used.keys():
                    val += "R" + str(prev_column_right_used[print_k])
                if print_k in prev_column_up_right_used.keys():
                    val += "UR" + str(prev_column_up_right_used[print_k])
                print (string1[print_k] + "  " + val)
            
#         for prev_key in prev_column_up_used.keys():
#             if prev_key in prev_column.keys():
#                 for val_key in prev_column_up_used[prev_key].keys():
#                     if val_key in prev_column[prev_key].keys():
#                         if prev_column_up_used[prev_key][val_key] < prev_column[prev_key][val_key]:
#                             prev_column[prev_key][val_key] = prev_column_up_used[prev_key][val_key]
#                     else:
#                         prev_column[prev_key][val_key] = prev_column_up_used[prev_key][val_key]
#             else:
#                 prev_column[prev_key] = prev_column_up_used[prev_key]
#         
#         for prev_key in prev_column_up_right_used.keys():
#             if prev_key in prev_column_right_used.keys():
#                 for val_key in prev_column_up_right_used[prev_key].keys():
#                     if val_key in prev_column_right_used[prev_key].keys():
#                         if prev_column_up_right_used[prev_key][val_key] < prev_column_right_used[prev_key][val_key]:
#                             prev_column_right_used[prev_key][val_key] = prev_column_up_right_used[prev_key][val_key]
#                     else:
#                         prev_column_right_used[prev_key][val_key] = prev_column_up_right_used[prev_key][val_key]
#             else:
#                 prev_column_right_used[prev_key] = prev_column_up_right_used[prev_key]
        
        
        if len1 - 1 in prev_column.keys():
            for res in prev_column[len1 - 1].keys():
                for k in range(prev_column[len1 - 1][res], dist + 1):
                    result.add((res + 1, j - res + 1))
        if len1 - 1 in prev_column_right_used.keys():
            for res in prev_column_right_used[len1 - 1].keys():
                for k in range(prev_column_right_used[len1 - 1][res], dist + 1):
                    result.add((res + 1, j - res + 1))
        if len1 - 1 in prev_column_up_right_used.keys():
            for res in prev_column_up_right_used[len1 - 1].keys():
                print (prev_column_up_right_used[len1 - 1][res])
                for k in range(prev_column_up_right_used[len1 - 1][res], dist + 1):
                    result.add((res + 1, j - res + 1))
            
        if test_mode: print ('\n'.join(["Start:%d, len:%d" % (x[0], x[1]) for x in result]))
        
        prev_column = next_column
        prev_column_right_used = next_column_right_used
        prev_column_up_used = next_column_up_used
        prev_column_up_right_used = next_column_up_right_used
        
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
    else:
        print ("Len the same")
    for r11 in r1:
        if not r11 in r2:
            print ("%s found in file %s and not found in %s" % (r11, file1, file2))

    for r22 in r2:
        if not r22 in r1:
            print ("%s found in file %s and not found in %s" % (r22, file2, file1))
    print ("Finished checking result")

def KSIM(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start KSIM", gmtime())) 
    
    with open(input_file) as resource:
        k = int(resource.readline().rstrip())
        s = resource.readline().rstrip()
        t = resource.readline().rstrip()
    if test_mode: print ("k: %d, s:%s, t:%s" % (k, s, t))
    
    result = process_strings_3dicts(s, t, k)
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Finished")
        
    if test_mode: print ('\n'.join(str(r[0]) + ' ' + str(r[1]) for r in sorted(result)))
    
    with open(output_file, "w") as result_file:
        result_file.write('\n'.join(str(r[0]) + ' ' + str(r[1]) for r in sorted(result)))
    if check_mode:
        check_result(output_file, "data/rosalind_ksim3_result.txt") 

# main
# test_mode = False
# KSIM("data/rosalind_ksim.txt", "data/rosalind_ksim_result.txt")

# test and compare with known result
# test_mode = False
# check_mode = True
# KSIM("data/rosalind_ksim_test.txt", "data/rosalind_ksim4_result.txt")

test_mode = False
# check_mode = True
KSIM("data/rosalind_ksim_test_big.txt", "data/rosalind_ksim4_big_result.txt")

def process_strings(string1, string2, dist):
    len1 = len(string1)
    len2 = len(string2)
    print (len1)
    print (len2)
    
    result = set()
    
    prev_column = dict()
    
    for j in range(len2):
        if not test_mode and j % 100 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "%d" % j)
        
        prev_column[0] = dict()
        prev_column[0][j] = 0
        
        if test_mode:print ("j: %d" % j)
        
        next_column = dict()
        
        for i in range(len1):
            if i in prev_column.keys():
                if test_mode:print ("i: %d" % i)
                # diag
                if string1[i] != string2[j]:
                    update_dict(prev_column, next_column, i, i + 1, 1, dist)
                else:
                    update_dict(prev_column, next_column, i, i + 1, 0, dist)
                # down
                if i < len1 - 1 and string1[i] != string2[j] and string1[i + 1] == string2[j]:
                    update_dict(prev_column, prev_column, i, i + 1, 0, dist)
                else:
                    update_dict(prev_column, prev_column, i, i + 1, 1, dist)
                # right
                if j < len2 - 1 and string1[i] != string2[j] and string1[i] == string2[j + 1]:
                    update_dict(prev_column, next_column, i, i, 0, dist)
                else:
                    update_dict(prev_column, next_column, i, i, 1, dist)
                       
#             prev_column.pop(i)
        if test_mode:print (next_column)
        
        if len1 in prev_column.keys():
            for res in prev_column[len1].keys():
                for k in range(prev_column[len1][res], dist):
                    result.add((res, j - res + 1))
            
            if test_mode: print ('\n'.join(["Start:%d, len:%d" % (x[0], x[1]) for x in result]))
        
        prev_column = next_column
    
    print (update_time)
    return result

