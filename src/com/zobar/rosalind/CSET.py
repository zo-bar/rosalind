'''
Created on Aug 5, 2015

@author: zoya
'''
from time import gmtime, strftime

def process_line(line, taxa_order, brackets):
    cur_result = (",".join(('(' * brackets[i] + str(taxa_order[i]) if brackets[i] > 0 else str(taxa_order[i]) + ')' * (brackets[i] * (-1)))  for i in range(len(taxa_order))))
    # print ("Start process line %s (current result: %s)" % (line, cur_result))
    zero = '0'
    if (sum([int(x) for x in line]) > len(line) / 2):
        zero = '1'
    before = []
    after = []
    group = []
    
    brackets_sum = 0
    in_between_brackets_sum = 0
    for i, el in enumerate(taxa_order):
        if line[el] == zero:    
            if len(group) == 0:
                before.append(el)
            else:
                after.append(el)
                in_between_brackets_sum += brackets[i]
                # print (in_between_brackets_sum)
        else:
            # print ("Processing element %d, brackets sum:%d" % (el, in_between_brackets_sum))
            if (in_between_brackets_sum != 0):
                return False
            
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
        # print ("Move %d bracket(s) from position %d(%d) to position %d" % (-brackets_sum, len(before) + len(group) - 1, len(brackets), taxa_order.index(group[-1])))
        brackets[len(before) + len(group) - 1] -= brackets_sum
        brackets[taxa_order.index(group[-1])] += brackets_sum
    taxa_order.clear()
    taxa_order.extend(before + group + after)  
    brackets[len(before)] += 1
    brackets[len(before) + len(group) - 1] -= 1
    return True
    
def CSET(input_file, output_file):
    with open(input_file) as resource:
        print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start processing file")
        
        line = resource.readline().rstrip()

        brackets = [0 for i in range(len(line))]
        taxa_order = [i for  i in range(len(line))]
        
        result = []
        broken_line = ''
        while line:
            if not process_line(line, taxa_order, brackets):
                if broken_line != '':
                    print ("Found second broken line: %s" % line)
                    brackets = [0 for i in range(len(line))]
                    taxa_order = [i for  i in range(len(line))]
                    
                    process_line(line, taxa_order, brackets)
                    broken_line = line
                    for res_line in result:
                        if not process_line(res_line, taxa_order, brackets):
                            # found breaking line
                            print ("Broken line found: %s !" % res_line)
                            broken_line = res_line
                            break
                else:
                    print ("Found first broken line: %s" % line)
                    broken_line = line
            result.append(line)
            line = resource.readline().rstrip()
    result.remove(broken_line)
    print (strftime("%Y-%m-%d %H:%M:%S Finished!", gmtime()))
    with open(output_file, 'w') as result_file:
        result_file.write("\n".join(str(x) for x in sorted(result)))      

CSET("data/rosalind_cset.txt", "data/rosalind_cset_result.txt")
