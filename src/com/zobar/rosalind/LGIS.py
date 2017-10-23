'''
Created on Jul 29, 2013

@author: Zoya
'''
def get_inc(val_list):
    n = len(val_list)
    longest_len = 0
    m = [0 for x in range(n + 1)]
    p = [0 for x in range(n + 1)]
    for i in range(0, n):
        for j in range(longest_len, -1, -1):
            if val_list[m[j]] < val_list[i]:
                break
        p[i] = m[j]
        if j == longest_len or val_list[i] < val_list[m[j + 1]]:
            m[j + 1] = i
            longest_len = max(longest_len, j + 1)
    inc = [0 for x in range(longest_len)]
    val = m[longest_len]
    for i in range(longest_len - 1, -1, -1):
        inc[i] = str(val_list[val])
        val = p[val]
    return inc

def get_dec(val_list):
    n = len(val_list)
    longest_len = 0
    m = [0 for x in range(n)]
    p = [0 for x in range(n)]
    for i in range(0, n):
        for j in range(longest_len, -1, -1):
            if val_list[m[j]] > val_list[i]:
                break
        p[i] = m[j]
        if j == longest_len or val_list[i] > val_list[m[j + 1]]:
            m[j + 1] = i
            longest_len = max(longest_len, j + 1)
    dec = [0 for x in range(longest_len)]
    val = m[longest_len]
    for i in range(longest_len - 1, -1, -1):
        dec[i] = str(val_list[val])
        val = p[val]
    return dec

def LGIS(input_file, output_file):
    with open(input_file) as resource_file:
        n = int(resource_file.readline().rstrip())
        val_list = [int(str.rstrip()) for str in resource_file.read().rstrip().split(" ")]
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(get_inc(val_list)))
        result_file.write("\n")
        result_file.write(" ".join(get_dec(val_list)))

LGIS("data/rosalind_lgis.txt", "data/rosalind_lgis_result.txt")




#    with open(input_file) as resource_file:
#        n = resource_file.readline().rstrip()
#        val_list = resource_file.read().rstrip().split(" ")
#    string1 = "".join(str(x) for x in val_list)
#    val_list.sort()
#    string2 = "".join(str(x) for x in val_list)
#    result_inc = " ".join(longest_common_seq(string1, string2))
#    val_list.reverse()
#    string2 = "".join(str(x) for x in val_list)
#    result_dec = " ".join(longest_common_seq(string1, string2))
#    with open(output_file, "w") as result_file:
#        result_file.write(result_inc + "\n")
#        result_file.write(result_dec)

