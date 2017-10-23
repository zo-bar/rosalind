'''
Created on Jun 12, 2015

@author: zoya
'''

def CNTQ(input_file, output_file):
    with open(input_file) as resource:
        n = int(resource.readline())
    # print (n)
    result = 0
    for k in range(n - 2):
        # print (result)
        result += (k + 1) * (n - k - 3) * (n - k - 2) / 2
    result = int(result) % 1000000
    with open(output_file, 'w') as result_file:
        result_file.write(str(result))      
    
#CNTQ("data/rosalind_cntq.txt", "data/rosalind_cntq_result.txt")
