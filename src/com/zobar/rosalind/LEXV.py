'''
Created on Jul 17, 2013

@author: Zoya
'''
import os
from time import gmtime, strftime

def merge_files(len1, len2, output_file):
    merge_file1 = output_file + str(len1)
    merge_file2 = output_file + str(len2)
    print ("Merge files: %s and %s to %s" % (merge_file1, merge_file2, output_file))
    with open(merge_file1) as file1:
        lines1 = file1.readlines()
    with open(merge_file2) as file2:
        with open(output_file + str(len1 + len2), "w") as result_file:
            line2 = file2.readline()
            while line2:
                line2 = line2.rstrip()
                result_file.write(line2 + "\n")
                if len(line2) == len2:
                    result_file.write(line2 + line2.join(lines1))
                    line2 = file2.readline()
                    if line2:
                        result_file.write("\n")
                else:
                    line2 = file2.readline()
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + (" - %s file finished" % output_file))
    
def form_strings(alphabet, strings_len, output_file):
    temp_file = output_file + str(strings_len)
    if not os.path.exists(temp_file):
        if strings_len == 1:
            with open(temp_file, "w") as temp1:
                temp1.write("\n".join(alphabet))
        else:
            len1 = strings_len / 2
            len2 = strings_len - (strings_len / 2)
            form_strings(alphabet, len1, output_file)
            if (len1 != len2):
                form_strings(alphabet, len2, output_file)
            merge_files(len1, len2, output_file)  
    
def lexv(input_file, output_file):
    if(os.path.exists(output_file)):
        os.remove(output_file)
    with open(input_file) as input_alphabet:
        alphabet = input_alphabet.readline().split(" ")
        alphabet[-1] = alphabet[-1].strip()
        n = int(input_alphabet.readline())
    for i in range(n):
        if (os.path.exists(output_file + str(i))):
            os.remove(output_file + str(i))
    form_strings(alphabet, n, output_file)
    os.rename(output_file + str(n), output_file)
    for i in range(n):
        if (os.path.exists(output_file + str(i))):
            os.remove(output_file + str(i))
    
lexv("data/rosalind_lexv.txt", "data/rosalind_lexv_result.txt")
