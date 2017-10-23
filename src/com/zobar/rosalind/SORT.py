'''
Created on Aug 13, 2013

@author: Zoya
'''
from time import gmtime, strftime

def get_reversal_distance(m1, m2):
    print "%s Started at " % m1 + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    result = []
    get_reversal_distance_step(m1, m2, [], result)
    print "%s Finished at " % m1 + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return result[0]

def get_reversal_distance_step(m1, m2, curr_result, best_result):
    if len(best_result) > 0 and len(curr_result) >= len(best_result[0]):
        return
    if m1 == m2:
        print "\n" + str(len(curr_result))
        print "\n".join(" ".join(str(y) for y in x) for x in curr_result)
        if len(best_result) == 0:
            best_result.append([x for x in curr_result]) 
        elif len(curr_result) < len(best_result[0]):
            best_result[0] = [x for x in curr_result]
        return
    for i in xrange(len(m1)):
        if m1[i] != m2[i]:
            j = m1.index(m2[i])
            move_to_next_step(i, j, m1, m2, curr_result, best_result)
        if i > 1 and m1[i - 1] == m2[i - 1]:
            j = m1.index(m2[i - 2])
            if j > i:
                move_to_next_step(i, j, m1, m2, curr_result, best_result)
    return

def move_to_next_step(i, j, m1, m2, curr_result, best_result):
    if (i > j):
        i, j = j, i
    m1[i:j + 1] = reversed(m1[i:j + 1])
    curr_result.append([i + 1, j + 1])
    get_reversal_distance_step(m1, m2, curr_result, best_result)
    m1[i:j + 1] = reversed(m1[i:j + 1])
    curr_result.pop()
  
def SORT(input_file, output_file):
    with open(input_file) as resource_file:
        m1 = [int(x.rstrip()) for x in resource_file.readline().split(" ")]
        m2 = [int(x.rstrip()) for x in resource_file.readline().split(" ")]
    result = get_reversal_distance(m1, m2)
    print result
    with open(output_file, "w") as result_file:
        result_file.write(str(len(result)) + "\n")
        result_file.write("\n".join(" ".join(str(y) for y in x) for x in result))

SORT("data/rosalind_sort.txt", "data/rosalind_sort_result.txt")
