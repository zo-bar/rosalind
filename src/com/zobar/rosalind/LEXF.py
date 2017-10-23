'''
Created on Jul 11, 2013

@author: Zoya
'''
import os
from time import gmtime, strftime

def merge_files(merge_file1, merge_file2, output_file):
    print ("Merge files: %s and %s to %s" % (merge_file1, merge_file2, output_file))
    with open(merge_file1) as file1:
        lines1 = file1.readlines()
#    with open(merge_file2) as file2:
#        lines2 = file2.readlines()
#    with open(output_file, "w") as result_file:
#        result = []
#        for line in lines1:
#            result.append(line.rstrip() + (line.rstrip()).join(lines2))
#        result_file.write("\n".join(result))
    with open(merge_file2) as file2:
        with open(output_file, "w") as result_file:
            line2 = file2.readline()
            while line2:
                result_file.write(line2.rstrip() + (line2.rstrip()).join(lines1))
                line2 = file2.readline()
                if line2:
                    result_file.write("\n")
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
            file1 = output_file + str(len1)
            file2 = output_file + str(len2)
            form_strings(alphabet, len1, output_file)
            if (len1 != len2):
                form_strings(alphabet, len2, output_file)
            merge_files(file1, file2, temp_file)  
    
def lexf(input_file, output_file):
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
    
lexf("data/rosalind_lexf.txt", "data/rosalind_lexf_result.txt")
        
#    # build all files mod2 less then len
#    temp_file = output_file + "1"
#    with open(temp_file, "w") as temp1:
#        temp1.write("\n".join(alphabet))
#    i = 2
#    while(i < int(strings_len)):
#        merge_files(temp_file, temp_file, output_file + str(i))
#        temp_file = output_file + str(i)
#        i = i * 2
#    
#    j = int(strings_len)
#    i = i / 2
#    # os.remove(output_file)
#    while i > 1 and j > 0:
#        if (j % i) != 0:
#            # j = max 2 degree less then j
#            j = j % i
#            i = 2
#            while i < j:
#                i = i * 2
#            i = i / 2
#            temp_file2 = output_file + str(i)
#            merge_files(temp_file2, temp_file, output_file)
#            j = j % i
#            os.remove(temp_file)
#            os.rename(output_file, temp_file)
#    os.rename(temp_file, output_file)
    
# def create_temp_file(i, output_file):
#    if (i % 2 != 0):
#        create_temp_file(i % 2, output_file)
#        merge_files(output_file + str(i / 2), output_file + str(i % 2), output_file + str(i))
#        
    
    
#    perm_list = [x for x in xrange(1, len(alphabet) + 1)]
#    for i in xrange(1, int(strings_len)):
#        result = []
#        # for letter in alphabet:
#        #    result.extend([(letter + x) for x in perm_list])
#        print str(10 ** i)
#        for j in xrange(1, len(alphabet) + 1):
#            result.extend((j * (10 ** i) + x) for x in perm_list)
#        perm_list = result
#        print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + (" - %d finished" % i)
#    print "".join(str(perm_list))
#    with open(output_file, "w") as result_file:
#        result_file.write("\n".join(perm_list))
#    print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + (" - finished")
#    for i in xrange(int(strings_len)):
#        temp_output_file = output_file + str(i)
#        with open(temp_output_file, "w") as temp_file:
#            if (i == 0):
#                temp_file.write("\n".join(alphabet))
#            else:
#                temp_prev_file = output_file + str(i - 1)
#                with open(temp_prev_file, "r") as prev_file:
#                    lines = prev_file.readlines()
#                lines[:] = [x for x in lines if x != "\n"]
# #                temp_file.write((("\n").join(lines)).join(alphabet))
#                for letter in alphabet:    
#                    temp_file.write(("\n" + letter).join(lines))
# #                        k = prev_file.readline()
# #                        while k:
# #                            if (k != "\n"):
# #                                temp_file.write(letter + k)
# #                            k = prev_file.readline()
#                os.remove(temp_prev_file)
#            temp_file.write("\n")
#        print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + (" - %d finished" % i)
#    os.remove(output_file)
#    os.rename(temp_output_file, output_file)

#    with open(output_file, "w") as result_file:
#        with open(temp_output_file) as temp_file:
#            lines = temp_file.readlines()
#        lines2 = [x for x in lines if x != "\n"]
#        result_file.write(("\n" + letter).join(lines2))
# #            k = temp_file.readline()
# #            while k:
# #                if k != "\n":
# #                    result_file.write(k)
# #                k = temp_file.readline()
#    os.remove(temp_output_file)
#    print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + (" - finished")

# def form_strings(alphabet, string_len, prefix, output_file, dynamic):
#    if (len(prefix) == string_len - 1):
#        with open(output_file, "a") as result_file:
#            for letter in alphabet:
# #                print prefix + letter
#                result_file.write("\n" + prefix + letter)
#    else:
#        for letter in alphabet:
#            form_strings(alphabet, string_len, prefix + letter, output_file)
#
#
# def lexf(input_file, output_file):
#    with open(input_file) as input_alphabet:
#        alphabet = input_alphabet.readline().split(" ")
#        alphabet[-1] = alphabet[-1].strip()
#        n = input_alphabet.readline()
#    
#    tmp_file = output_file + "tmp"
#    with open(tmp_file, "w") as tmp:
#        tmp.write("")
#        
#    dynamic = [[-1 for j in xrange(len(alphabet) + 1)] for i in xrange(n + 1)]           
#    form_strings(alphabet, int(n), "", tmp_file, dynamic)
#    
#    with open(output_file, "w") as result_file:
#        with open(tmp_file, "r") as tmp:
#            k = tmp.read(1)  # skip first \n
#            k = tmp.read(1)
#            while k:
#                result_file.write(k)
#                k = tmp.read(1)
#    os.remove(tmp_file)
