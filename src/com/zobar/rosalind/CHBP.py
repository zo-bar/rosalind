'''
Created on Jun 13, 2015

@author: zoya
'''
from time import gmtime, strftime

def CHBP(input_file, output_file):
    with open(input_file) as resource:
        print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start processing file")
        line = resource.readline().rstrip()
        taxa = line.split(" ")
        
        brackets = [0 for i in range(len(taxa))]
        taxa_order = [i for  i in range(len(taxa))]

        line = resource.readline().rstrip()

        brackets_count = 0
        while line:
            zero = '0'
            if (sum([int(x) for x in line]) > len(line) / 2):
                zero = '1'
            before = []
            after = []
            group = []
            
            brackets_sum = 0
            for i, el in enumerate(taxa_order):
                if line[el] == zero:    
                    if len(group) == 0:
                        before.append(el)
                    else:
                        after.append(el)
                else:
                    group.append(el)
                    if len(group) > 1:
                        if (brackets_sum < 0 and brackets[i] > 0):
                            brackets_sum = 0
                        brackets_sum += brackets[i]
                        
                        # print ("Move brackets from position %d(%d) to position %d(%d)" % (i, brackets[i], len(before) + len(group) - 1, brackets[len(before) + len(group) - 1]))
                        brackets.insert(len(before) + len(group) - 1, brackets[i])
                        del brackets[i + 1]
            if (brackets_sum < brackets[len(before) + len(group) - 1]):
                brackets_sum = brackets[len(before) + len(group) - 1]
            if (brackets_sum < 0):
                print ("Move %d brackets from position %d(%d) to position %d" % (brackets_sum, len(before) + len(group) - 1, len(brackets), taxa_order.index(group[-1])))
                brackets[len(before) + len(group) - 1] -= brackets_sum
                brackets[taxa_order.index(group[-1])] += brackets_sum
            taxa_order = before + group + after  
            brackets[len(before)] += 1
            brackets[len(before) + len(group) - 1] -= 1
            # print (line)
            # print (group)
            print (",".join(('(' * brackets[i] + taxa[taxa_order[i]] if brackets[i] > 0 else taxa[taxa_order[i]] + ')' * (brackets[i] * (-1)))  for i in range(len(taxa_order))))
            
            brackets_count += 1
            if (sum([k for k in brackets if k > 0]) != brackets_count):
                print ("ERROR! Added more brackets then required!")
            
            line = resource.readline().rstrip()
            
    print (brackets)
    print (sum(brackets))
    result = ('(' + ",".join(('(' * brackets[i] + taxa[taxa_order[i]] if brackets[i] > 0 else taxa[taxa_order[i]] + ')' * (brackets[i] * (-1)))  for i in range(len(taxa_order))) + ');')
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + result)
    with open(output_file, 'w') as result_file:
        result_file.write(str(result))      

CHBP("data/rosalind_chbp.txt", "data/rosalind_chbp_result.txt")
 
# from CTBL import CTBL 
#         while line:
#             zero = '0'
#             # if line[0] == '1':  # reverse line
#             #    zero = '1'
#             before = []
#             after = []
#             group = []
#             
#             br_before = []
#             br_group = []
#             br_after = []
#             br_sum = 0
#             for i, el in enumerate(taxa_order):
#                 if line[el] == zero:    
#                     if len(group) == 0:
#                         before.append(el)
#                         br_before.append(brackets[i])
#                     else:
#                         after.append(el)
#                         br_after.append(brackets[i])
#                 else:
#                     group.append(el)
#                     if brackets[i] < 0 and br_sum + brackets[i] <= 0:# and len(br_after) > 0:
#                         br_after[-1] += br_sum + brackets[i] - 1
#                         br_group.append(brackets[i] + br_sum)
#                         # TODO: check loop ends
#                         print ("HERE")
#                     else:
#                         br_sum += brackets[i]
#                         br_group.append(brackets[i])
#             taxa_order = before + group + after
#             br_group[0] += 1
#             br_group[-1] -= 1
#             print(br_group)
#             brackets = br_before + br_group + br_after
#             
#             print (line)

          
# def CHBP(input_file, output_file):
#     taxa = get_taxa(input_file)
#     res_order = [i for i in range(len(taxa))]
#     # for k in range(100):
#     res_order = order_taxa(taxa, input_file, res_order)
#     
#     add_brackets(taxa, input_file, res_order) 
#                 
#     result = '(' + ",".join(taxa[res_order[i]] for i in range(len(res_order))) + ');'
#     print (result)
#     with open(output_file, 'w') as result_file:
#         result_file.write(str(result))      
#
# def test_chbp():
#     chbp_input_test_file = "data/rosalind_chbp_test.txt"
#     chbp_output_test_file = "data/rosalind_chbp_test_result.txt"
#     CHBP(chbp_input_test_file, chbp_output_test_file)
#     
#    ctbl_output_test_file = "data/rosalind_chbp_test_ctbl_test.txt"
#    CTBL(chbp_output_test_file, ctbl_output_test_file)
    
#     taxon = ''
#     taxa = []
#     with open(chbp_output_test_file) as my_output:
#         s = my_output.read(1)
#         while s:
#             if s != ',' and s != ')' and s != '(' and s != 'A':
#                 taxon = taxon + s
#             else:
#                 if taxon != '':
#                     taxa.append(taxon)
#                     taxon = ''
#             s = my_output.read(1)
#         
#     print ("My taxa are:")
#     print (taxa)
#     
#     input_tbl = []
#     with open(chbp_input_test_file) as given_file:
#         line = given_file.readline().rstrip()
#         
#         while line and line[0] != '0' and line[0] != '1':
#             line = given_file.readline().rstrip()
#         
#         while line:
#             if line[0] == '1':
#                 next_line = ''
#                 for l in line:
#                     next_line = next_line + ('0' if l == 1 else '1')
#                 input_tbl.append(next_line)
#             else:
#                 input_tbl.append(line) 
#             line = given_file.readline().rstrip()
#     input_tbl = sorted(input_tbl)
#     
#     my_tbl = []   
#     with open(ctbl_output_test_file) as result_file:
#         line = result_file.readline().rstrip()
#         
#         while line:
#             if line[0] == '1':
#                 next_line = ''
#                 for l in line:
#                     next_line = next_line + ('0' if l == 1 else '1')
#                 my_tbl.append(next_line)
#             else:
#                 my_tbl.append(line) 
#             line = result_file.readline().rstrip()
#     
# #     f_my_tbl = []
# #     for line in my_tbl:
# #         new_str = ''
# #         for taxon in taxa:
# #             new_str += line[int(taxon) - 1]
# #         f_my_tbl.append(new_str)
# #     
# #     my_tbl = f_my_tbl
#     my_tbl = sorted(my_tbl)
#      
#     print (input_tbl)
#     print (my_tbl)
#     
#     print ("In initial file, but not in my result (%d): " % (len([x for x in input_tbl if x not in my_tbl])))
#     print ("\n".join([x for x in input_tbl if x not in my_tbl]))
#     
#     print ("In my result file, but not in initial file (%d): " % (len([x for x in my_tbl if x not in input_tbl])))
#     print ("\n".join([x for x in my_tbl if x not in input_tbl]))        
    
    
# test_chbp() 
    
    
# def get_taxa(input_file):
#     with open(input_file) as resource:
#         print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start processing file")
#         line = resource.readline().rstrip()
#         taxa = line.split(" ")
#         
#         print (taxa)
#     return taxa
# 
# def order_taxa(taxa, input_file, res_order):
#     print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start ordering...")
#     
#     with open(input_file) as resource:       
#         line = resource.readline().rstrip()
#         line = resource.readline().rstrip()
#         
#         # counter = 0
#         # t = ''
#         while line:
#             # counter += 1
#             # print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start processing line '%s'" % line)
#             
#             zero = '0'
#             if line[0] == '1':  # reverse line
#                 zero = '1'
#             
#             zeros = []
#             ones = []
#             for el in res_order:
#                 if line[el] == zero:
#                     zeros.append(el)
#                 else:
#                     ones.append(el)
#             res_order = zeros + ones
#             
# #             new_t = ",".join(str(x) for x in res_order if x in [23, 42, 57, 70])
# #             if new_t != t:
# #                 t = new_t
# #                 print ("Test: 0,23,42,57,70: %s%s%s%s%s, %s" % (line[0], line[23], line[42], line[57], line[70], t))
#             print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "New order: " + ", ".join(str(x) for x in res_order))
#             
#             line = resource.readline().rstrip()           
#     print ("Taxa count: %d" % len(taxa))
#     # print ("Row count: %d" % counter)
#     return res_order
# 
# def add_brackets(taxa, input_file, res_order):
#     with open(input_file) as resource:       
#         print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start adding brackets...")
#         
#         line = resource.readline().rstrip()
#         line = resource.readline().rstrip()
#         
#         while line:
#             # print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start processing line '%s'" % line)
#             
#             one = '1'
#             if line[0] == '1':  # reverse line
#                 one = '0'
#             
#             for (i, el) in enumerate(res_order):
#                 if line[el] == one:
#                     taxa[el] = '(' + taxa[el]
#                     break
#             
#             for (j, el_b) in enumerate(res_order[::-1]):
#                 if line[el_b] == one:
#                     taxa[el_b] = taxa[el_b] + ')'
#                     break
#             temp = ''
#             temp_taxa = []
#             while (i < len(res_order) - j):
#                 temp += line[res_order[i]]
#                 temp_taxa.append(taxa[res_order[i]])
#                 i += 1
#             print (temp + " From order %d to %d (taxa: %s)" % (el, el_b, ",".join(temp_taxa)))
#             
#             # print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "With brackets added: " + ", ".join(str(x) for x in res_order))
#             
#             line = resource.readline().rstrip()
#     return
