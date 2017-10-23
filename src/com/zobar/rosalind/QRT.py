'''
Created on May 17, 2014

@author: zoya
'''
def QRT(input_file, output_file):
    with open(input_file) as resource:
        names = resource.readline().rstrip().split()
        values = [line.rstrip() for line in resource.readlines()]
#     print (names)
#     print (values)
    result = []
    for psplit in values:
        if psplit.count('1') > 1 and psplit.count('0') > 1:
            ones = []
            zeros = []
            for i, letter in enumerate(psplit):
                if letter == '1':
                    ones.append(i)
                elif letter == '0':
                    zeros.append(i)
            one_pairs = []
            zero_pairs = []
            for j, one1 in enumerate(ones):
                for one2 in ones[j + 1:]:
                    one_pairs.append("{%s, %s}" % (names[one1], names[one2]))
            for m, zero1 in enumerate(zeros):
                for zero2 in zeros[m + 1:]:
                    zero_pairs.append("{%s, %s}" % (names[zero1], names[zero2]))
            for one_pair in one_pairs:
                for zero_pair in zero_pairs:
                    if result.count(zero_pair + " " + one_pair) == 0 and  result.count(one_pair + " " + zero_pair) == 0:
                        result.append(one_pair + " " + zero_pair)
    print("\n".join(x for x in set(result)))
    with open(output_file, 'w') as result_file:
        result_file.write("\n".join(x for x in result))        

QRT("data/rosalind_qrt.txt", "data/rosalind_qrt_result.txt")
