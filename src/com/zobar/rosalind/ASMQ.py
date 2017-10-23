'''
Created on Dec 16, 2013

@author: Zoya
'''
def ASMQ(input_file, output_file):
    lines = [line.rstrip() for line in open(input_file)]
    total_len = sum([len(x) for x in lines])
    lines.sort(key=len)
    curr_len = 0
    n50 = total_len
    n75 = total_len
    for i in range(len(lines) - 1, -1, -1):
        curr_len += len(lines[i])
        if n50 == total_len and curr_len > total_len * 0.5:
            n50 = len(lines[i])
        if curr_len > total_len * 0.75:
            n75 = len(lines[i])
            break
    result = str(n50) + " " + str(n75)
    print (result)
    with open(output_file, "w") as result_file:
        result_file.write(str(result))

ASMQ("src/data/rosalind_asmq.txt", "src/data/rosalind_asmq_result.txt")
