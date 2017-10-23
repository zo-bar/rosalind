'''
Created on Aug 8, 2013

@author: Zoya
'''
from time import gmtime, strftime

def get_reversal_distance(m1, m2):
    print "%s Started at " % m1 + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    result = [2 - len(m1)]
    get_reversal_distance_step(m1, m2, 0, result)
    print result[0]
    if (result[0] < 0):
        result[0] = 9
    return result[0]

def get_reversal_distance_step(m1, m2, curr_result, best_result):
    if curr_result >= abs(best_result[0]):
        return
    if m1 == m2:
        best_result[0] = min(abs(best_result[0]), curr_result)
        return
    for i in xrange(len(m1)):
        if m1[i] != m2[i]:
            j = m1.index(m2[i])
            reverse_array(m1, i, j)
            get_reversal_distance_step(m1, m2, curr_result + 1, best_result)
            reverse_array(m1, j, i)
        if i > 1 and m1[i - 1] == m2[i - 1]:
            j = m1.index(m2[i - 2])
            if j > i:
                print "ff %d %d" % (i, j)
                reverse_array(m1, i, j)
                get_reversal_distance_step(m1, m2, curr_result + 1, best_result)
                reverse_array(m1, j, i)
    return

def reverse_array(arr, first, last):
    if first > last:
        first, last = last, first
    while first < last:
        temp = arr[first]
        arr[first] = arr[last]
        arr[last] = temp
        first += 1
        last -= 1

def REAR(input_file, output_file):
    result = []
    with open(input_file) as resource_file:
        c = 'empty'
        while c:
            m1 = [int(x.rstrip()) for x in resource_file.readline().split(" ")]
            m2 = [int(x.rstrip()) for x in resource_file.readline().split(" ")]
            result.append(get_reversal_distance(m1, m2))
            c = resource_file.readline()
    print result
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(str(x) for x in result))

# REAR("data/rosalind_rear.txt", "data/rosalind_rear_result.txt")
REAR("data/rosalind_sort.txt", "data/rosalind_sort_rear_result.txt")

#    result = 0
#    for i in xrange(len(m1) - 1):
#        if m1[i] != m2[i]:
#            j = m1.index(m2[i])
#            k = i
#            while k < j:
#                temp = m1[j]
#                m1[j] = m1[k]
#                m1[k] = temp
#                k += 1
#                j -= 1
#            print " Iteration %d: m1 = %s" % (i, m1)
#            result += 1
#    print result
#    return result


# def get_cycles_count(m1, m2):
#    result = 0
#    arr = [x for x in m1]
#    for i in xrange(len(arr)):
#        if arr[i]:
#            j = i
#            arr[j] = None
#            while arr.count(m2[j]) > 0:
#                j = arr.index(m2[j])
#                arr[j] = None
#            result += 1
#    print "Cycles count %d" % result
#    return result

                
#        for j in xrange(i, len(m2)):
#            reverse_array(m1, i, j)
# #            print "Array %s at index %d (i=%d, j=%d, curr result = %d) " % (arr, index, i, j, curr_result)
#            result = get_reversal_distance_step(m1, m2, i + 1, curr_result + 1, best_result)
#            if m1 == m2 and result < best_result[0]:
#                best_result[0] = result
#                print "     " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " New best result is %d" % best_result[0]
 #            reverse_array(m1, j, i)
 
