'''
Created on Nov 8, 2013

@author: Zoya
'''
def SEXL(input_file, output_file):
    with open(input_file) as resource_file:
        input_array = resource_file.readline().rstrip().split(" ")
    result = []
    for prob in input_array:
        result.append(2 * float(prob) * (1 - float(prob)))
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(str(x) for x in result))

SEXL("src/data/rosalind_sexl.txt", "src/data/rosalind_sexl_result.txt")
