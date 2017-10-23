'''
Created on Nov 27, 2014

@author: zoya
'''
from math import sqrt
from time import gmtime, strftime

def PDPL(input_file, output_file):
    with open(input_file) as resource_file:
        arr = sorted([int(x) for x in resource_file.readline().split(" ")])
    arr_check = [i for i in arr]
    result = [0, arr.pop()]
    pdpl_recursion(arr, result, result[-1])
    test_result(arr_check, result)
    print (",".join(str(x) for x in sorted(result)))
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(str(x) for x in result))

def pdpl_recursion(arr, result, max_el):
    if len(arr) == 0:
        return True
    else:
        print (result)
        next_el = max(arr)
        pos_diffs = [abs(next_el - k) for k in result]
        neg_diffs = [abs(k - (max_el - next_el)) for k in result]
        if len([k for k in pos_diffs if k not in arr]) == 0:
            result.append(next_el)
            for k in pos_diffs:
                arr.remove(k)
            if not pdpl_recursion(arr, result, max_el):
                result.remove(next_el)
                for k in pos_diffs:
                    arr.append(k)
            else:
                return True
        if len([k for k in neg_diffs if k not in arr]) == 0:
            result.append(max_el - next_el)
            for k in neg_diffs:
                arr.remove(k)
            if not pdpl_recursion(arr, result, max_el):
                result.remove(max_el - next_el)
                for k in neg_diffs:
                    arr.append(k)
            else:
                return True
            
      
def create_test_arr(points):
    result = []
    for i in points:
        for j in points:
            if i < j:
                result.append(j - i)
    print (" ".join(str(x) for x in result))
    return result

create_test_arr([0, 4, 9, 11, 16, 23, 42, 55, 56, 76])  
  
def test_result(arr, result):
    result_arr = sorted(create_test_arr(result))
    arr = sorted(arr)
    if len(arr) != len(result_arr):
        print ("ERROR: result length")
        print (arr)
        print(result_arr)
        return False
    else:
        for i in range(len(arr)):
            if arr[i] != result_arr[i]:
                print ("ERROR: ")
                print (arr)
                print(result_arr)
                return False
    print ("Result checked successfully!!")
    return True
     
    
PDPL("src/data/rosalind_pdpl.txt", "src/data/rosalind_pdpl_result.txt")

# def make_candidates_map(arr, result_len):
#     max_el = arr[-1]
#     candidates = {0:sorted([t for t in set([x for x in arr if arr[-1] - x in arr])])}
#     candidates[0].append(max_el)
#     print("Array length: %d, candidates length: %d, max element: %d" % (len(arr), len(candidates[0]), max_el) + ": " + ",".join(str(x) for x in candidates[0]))
#     
#     for i in range(1, result_len - 1):
#         candidates[i] = set([])  # sorted(set([k + j for k in candidates[i - 1] for j in arr if k + j < max_el and k + j in candidates[0]]))  # set([])
#         for k in candidates[i - 1]:
#             cur_cand_index = 0
#             for j in arr:
#                 if k + j > max_el:
#                     break
#                 # if (k + j) in candidates[i - 1]:
#                 #   candidates[i].add(k + j) 
#                 while cur_cand_index < len(candidates[i - 1]) and candidates[i - 1][cur_cand_index] < k + j:
#                     cur_cand_index += 1
#                 if cur_cand_index >= len(candidates[i - 1]):
#                     break
#                 if candidates[i - 1][cur_cand_index] == k + j:
#                     candidates[i].add(k + j)
#         candidates[i] = sorted([t for t in candidates[i]])
#         print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Added %d candidates for step %d: " % (len(candidates[i]), i) + ",".join(str(x) for x in candidates[i]))
#     # print (candidates[result_len - 1])
#     candidates[result_len - 1] = [max_el]
#     return candidates
# 
# def pdpl_with_candidates(arr):
#     print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Start processing array " + ",".join(str(c) for c in arr))
#     # n2 - n = 2L
#     # n = (-1 +- sqrt(1 + 4*2L)) / 2
#     result_len = int((-1 + sqrt(1 + 8 * len(arr))) / 2)
#     print("Expecting result to be %d in length" % result_len)
#     
#     candidates = make_candidates_map(arr, result_len)
#     
#     arr_usage_track = [0 for x in range(len(arr))]
#     step = 0
#     counter = 0
#     result = [0]
#     checked_candidates = 0
#     while step < result_len:
#         # print ("")
#         if counter % 1000 == 0 :
#             print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Loops count: %d." % counter + " Step %d. Current result: " % step + ",".join(str(x) for x in result))
#             print (result)
#         counter += 1
#         # print ("Choosing next element on step %d..." % step)
#         rollback = True
#         # print (candidates[step])
#         # print (checked_candidates)
#         for candidate in candidates[step][checked_candidates:]:
#             if len(result) > 0 and candidate <= result[-1]:
#                 continue
#             rollback = False
#             used_indexes = []
#             for r in result:
#                 if candidate - r in arr:
#                     k = 0
#                     while k < len(arr):
#                         if arr[k] == candidate - r and arr_usage_track[k] == 0:
#                             used_indexes.append(k)
#                             break
#                         if arr[k] > candidate - r:
#                             rollback = True
#                             break
#                         k += 1
#                     if rollback:
#                         break
#             if not rollback:
#                 break
#         if not rollback:
#             print ("Selected candidate % d on step %d" % (candidate, step))
#             for ui in used_indexes:
#                 arr_usage_track[ui] = step
#             print (arr)
#             print (arr_usage_track)
#             result.append(candidate)
#             step += 1
#         else:
#             print ("Rolling back on step %d" % step)
#             # use next candidate in previous iteration
#             step -= 1
#             print (result)
#             checked_candidates = candidates[step].index(result.pop()) + 1
# 
#     print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Finished!!")
#     print (result)
#     return result
# 
#     
#     
#     
#     
#     
# 
# def find_subsets(arr):
#     # find all subsets of result_len where sum of elements == max element of arr
#     
#     print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Start processing array " + ",".join(str(c) for c in arr))
#     # n2 - n = 2L
#     # n = (-1 +- sqrt(1 + 4*2L)) / 2
#     result_len = int((-1 + sqrt(1 + 8 * len(arr))) / 2)
#     print("Expecting result to be %d in length" % result_len)
#     
#     result = []
#     max_el = arr[-1]
#     print ("Max element:" + str(max_el))
#     subset = arr[0:result_len - 1]
#     print ("Subset sum: " + str(sum(subset)))
#     arr_max_index = result_len
#     while sum(subset) + arr[arr_max_index] < max_el:
#         arr_max_index += 1
#     print ("Max index of array is %d" % arr_max_index)
#     get_subset_recursive([], result_len, arr[0:arr_max_index - 1], result, max(arr), 0, sum(arr[0:arr_max_index - 1]))
#     print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Finish processing array " + ",".join(str(c) for c in arr))
#     
#     return result
# 
# def get_subset_recursive(curset, length, set_to_process, result, result_sum, cur_sum, set_to_process_sum):
#     # print (len(curset))
#     # print (len(set_to_process))
#     if cur_sum + set_to_process_sum < result_sum:
#         return
#     
#     if len(curset) == length:
#         if sum(curset) == result_sum:
#             print ("Add a subset: " + ",".join(str(x) for x in curset))
#             result.append(curset)
#         return
#     if len(curset) + len(set_to_process) < length or sum(curset) >= result_sum:
#         # print ("Stop recursion")
#         return
#     
#     get_subset_recursive(curset, length, set_to_process[0:-1], result, result_sum, cur_sum, set_to_process_sum - set_to_process[-1])
#     curset.append(set_to_process[-1])
#     get_subset_recursive(curset, length, set_to_process[0:-1], result, result_sum, cur_sum + set_to_process[-1], set_to_process_sum - set_to_process[-1])
#     curset.pop()
#     
# def straight_forward_pdpl(arr):
#     print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "Start processing array " + ",".join(str(c) for c in arr))
#     # n2 - n = 2L
#     # n = (-1 +- sqrt(1 + 4*2L)) / 2
#     result_len = int((-1 + sqrt(1 + 8 * len(arr))) / 2)
#     print("Expecting result to be %d in length" % result_len)
#     
#     arr_usage_track = [0 for x in range(len(arr))]
#     # arr_usage_track = [x if x != 0 else 1 for x in arr_usage_track ]
#     # print (",".join(str(c) for c in arr_usage_track))
# 
#     candidates = set([x for x in arr if arr[-1] - x in arr])
#     print("Array length: %d, candidates length: %d" % (len(arr), len(candidates)))
#     
#     result = [0]
#     next_candidate_index = 0
#     step = 1
#     counter = 0
#     while step <= result_len:
#         # print ("")
#         if counter % 100000 == 0 :
#             print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Loops count: %d." % counter + " Step %d. Current result: " % step + ",".join(str(x) for x in result))
#         counter += 1
#         # print ("Next candidate index: %d" % next_candidate_index)
#         
#         # print ("Choosing next element on step %d..." % step)
#         
#         while next_candidate_index < len(arr) and arr_usage_track[next_candidate_index] != 0 and arr[next_candidate_index] in candidates:
#             next_candidate_index += 1
#         if next_candidate_index == len(arr):
#             rollback = True
#         else:
#             # next will be prev plus next of unused in arr
#             next_el = result[-1] + arr[next_candidate_index]
#             # print ("check %d as next element" % next_el)
#             
#             if arr[-1] - next_el in arr:
#                 ui = arr.index(arr[-1] - next_el)
#                 while arr_usage_track[ui] != 0 and arr[ui] == arr[-1] - next_el:
#                     ui += 1
#                 if arr[ui] != arr[-1] - next_el:
#                     rollback = True
#                 else:
#                     # check distances and mark steps
#                     update_indexes = [ui]
#                     rollback = False
#                     for r in result:
#                         if next_el - r in arr:
#                             ui = arr.index(next_el - r)
#                             while arr_usage_track[ui] != 0 and arr[ui] == next_el - r:
#                                 ui += 1
#                             if arr[ui] != next_el - r:
#                                 rollback = True
#                                 break
#                             # print("Update usage track: element %d is used on step %d as distance to %d" % (ui, step, r))
#                             update_indexes.append(ui)
#                         else:
#                             # print ("%d failed to be the next element: no value for distance to %d" % (next_el, r))
#                             rollback = True
#                             break
#             else:
#                 rollback = True
#                 
#         if not rollback:
#             for j in update_indexes:
#                 arr_usage_track[j] = step
#             result.append(next_el)
#             step += 1
#             next_candidate_index = 0
#             # print ("Element %d is chosen as next element on step %d and is added to result" % (next_el, step))
#             # print ("Result is: " + ",".join(str(c) for c in result))
#             # print ("Initial array " + ",".join(str(c) for c in arr))
#             # print ("Usage track is " + ",".join(str(c) for c in arr_usage_track))
#         else:
#             next_candidate_index += 1
#             if next_candidate_index >= len(arr):
#                 # print ("No more candidate elements for step %d. Rolling one step back" % step)
#                 step -= 1
#                 for j in range(len(arr)):
#                     if arr_usage_track[j] == step:
#                         arr_usage_track[j] = 0
#                 # print ("Usage track is " + ",".join(str(c) for c in arr_usage_track))
#                 
#                 # result.pop()
#                 next_candidate_index = arr.index(result.pop()) + 1
#         
#     print ("Result is: " + ",".join(str(c) for c in result))
#     print ("Initial array " + ",".join(str(c) for c in arr))
#     print ("Usage track is " + ",".join(str(c) for c in arr_usage_track))
#     return result
# 
# def check_result(arr, result):
#     arr_usage = [0 for i in range(len(arr))]
#     max_el = arr[-1]
#     for r in result:
#         # mark element as used
#         # mark max_el-element as used
#         distances = [max_el - r]        
#         # mark all distances as used
#         k = 0
#         while result[k] < r:
#             distances.append(r - result[k])
#         for d in distances:
#             if not d in arr:
#                 return False
#             ind = arr.index(d)
#             while arr_usage(ind) == 0:
#                 ind += 1
#             if arr(ind) != d:
#                 return False
#             arr_usage[ind] = 1 
#     
#     return True
# 

# PDPL("src/data/rosalind_pdpl_test.txt", "src/data/rosalind_pdpl_result.txt")
