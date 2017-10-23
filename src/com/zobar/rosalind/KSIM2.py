'''
Created on Feb 15, 2016

@author: zoya
'''

from time import gmtime, strftime
MATCH_SCORE = 0
MISMATCH_SCORE = -1
test_mode = True
        
def KSIM(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start KSIM", gmtime())) 
    
    with open(input_file) as resource:
        k = int(resource.readline().rstrip())
        s = resource.readline().rstrip()
        t = resource.readline().rstrip()
    if test_mode: print ("k: %d, s:%s, t:%s" % (k, s, t))
    
    len_s = len(s)
    len_t = len(t)
    print (strftime("%Y-%m-%d %H:%M:%S Motif len:", gmtime()) + str(len_s + 1))
    print (strftime("%Y-%m-%d %H:%M:%S String len:", gmtime()) + str(len_t + 1))
    
#     prev_line = [(0, [i]) for i in range(len_t + 1)]
#     next_line = [(-k, [0])]
    prev_line = [0 for i in range(len_t + 1)]
    next_line = [-k * 10]
    
    prev_path = [[i] for i in range(len_t + 1)]
    next_path = [[]]
    for i in range(1, len_s + 1):
        if not test_mode and i % 100 == 0: print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(i))
    
        for j in range(1, len_t + 1):
            up = prev_line[j] + (MISMATCH_SCORE if j < len_t + 1 else 0)
            left = next_line[j - 1] + MISMATCH_SCORE
            diag = prev_line[j - 1] + (MISMATCH_SCORE if s[i - 1] != t[j - 1] else MATCH_SCORE)
            
            max_val = max(up, left, diag)
            next_line.append(max_val)
            max_path = []
#             if max_val == up:
#                 max_path.extend(prev_path[j])
#             if max_val == left:
#                 max_path.extend(next_path[j - 1])
#             if max_val == diag:
#                 max_path.extend(prev_path[j - 1])
            next_path.append(max_path)
        prev_line = next_line
        prev_path = next_path
        if test_mode: print (next_line)
        # next_line = [(-k, [0])]
        next_line = [-k * 10]
        
    print (prev_path)
    print (prev_line)
    result = []
    with open(output_file, "w") as result_file:
        result_file.write('\n'.join(str(r[0]) + ' ' + str(r[1]) for r in result))
 
test_mode = False      
KSIM("data/rosalind_ksim.txt", "data/rosalind_ksim_test_result.txt")


            
#             up = (prev_line[j][0] + (MISMATCH_SCORE if j < len_t + 1 else 0), prev_line[j][1])
#             left = (next_line[j - 1][0] + MISMATCH_SCORE, next_line[j - 1][1])
#             diag = (prev_line[j - 1][0] + (MISMATCH_SCORE if s[i - 1] != t[j - 1] else MATCH_SCORE), prev_line[j - 1][1])
#                        
#             if up < left:
#                 if left < diag:
#                     next_line.append(diag)
#                 elif left == diag:
#                     diag[1].extend(left[1])
#                     next_line.append((diag[0], diag[1]))
#                 else:
#                     next_line.append(left)
#             elif up == left:
#                 if left < diag:
#                     next_line.append(diag)
#                 elif left == diag:
#                     diag[1].extend(left[1])
#                     diag[1].extend(up[1])
#                     next_line.append((diag[0], diag[1]))
#                 else:
#                     diag[1].extend(up[1])
#                     next_line.append(left)
#             else:
#                 if up < diag:
#                     next_line.append(diag)
#                 elif up == diag:
#                     diag[1].extend(up[1])
#                     next_line.append((diag[0], diag[1]))
#                 else:
#                     next_line.append(up)
#    
# result = []
#     for i, pair in enumerate(prev_line):
#         if pair[0] >= -k:
#             result.append((i, set(pair[1])))
#     for r in result:
#         print (r)
#                      

