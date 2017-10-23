'''
Created on Jan 23, 2016

@author: zoya
'''
# works great and fast, but when choosing between 01101 and 01001 chooses any one A or G, 
# but has to consider next element, otherwise can make not the best choice

from time import gmtime, strftime

LETTERS = ['A', 'C', 'G', 'T', '-']
letters_len = 5

def get_first_one(num):
    for i in range(letters_len):
        if num % 2 == 1:
            return i
        num = num / 2
    return i

def taxa_str_to_code(taxon_str):
    taxon_code = []        
    for next_symbol in taxon_str:
        taxon_code.append(2 ** LETTERS.index(next_symbol))
    return taxon_code

def taxa_code_to_str(taxon_code):
    taxon_str = ''
    for next_symbol in taxon_code:
        if (bin(next_symbol).count('1') > 1):
            print ("HERE")
        for i in range(len(LETTERS)):
            if next_symbol % 2 == 1:
                taxon_str += LETTERS[i]
                break
            next_symbol = next_symbol / 2
    return taxon_str

def unroll_dependencies(result, dependency, taxon, i, cross):
    # print (dependency)
    if taxon in result.keys():
        curr_val = result[taxon][i]
        if bin(curr_val).count('1') > 1:
            if ((bin(curr_val & cross).count('1')) == 0):
                # assign any letter, anyway it differs from the best choice
                for j in range(letters_len):
                    if (curr_val % 2 == 1):
                        cross = 2 ** j
                        break
                    else:
                        curr_val = curr_val / 2
         
            if i in dependency[taxon].keys():
                for taxon_dep in dependency[taxon][i]:
                    unroll_dependencies(result, dependency, taxon_dep, i, cross)
            result[taxon][i] = cross
            print (taxon + "-%d was mixed. Choose %s " % (i, bin(cross)[2:].zfill(letters_len)))            
        dependency[taxon][i] = []

def test_result(taxa, tree):
    print ("Start test")
    tree_stack = []
    last_symbol = ''
    taxon = ''
    distance = 0
    # l = len(result[taxa.get(0)])
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')' or next_symbol == ';':
            if (next_symbol == ')' or next_symbol == ',' or next_symbol == ';') and last_symbol == ')':
                # cross last two taxa
                taxon1 = tree_stack.pop()
                taxon2 = tree_stack.pop()
                
                for i in range(len(taxa[taxon1])):
                    if taxa[taxon1][i] != taxa[taxon2][i]:
                        distance += 1
                # print ("Cross %s and %s. Distance: %d" % (taxon1, taxon2, distance))
                tree_stack.append(taxon)
                taxon = ''
            if taxon:
                tree_stack.append(taxon)
                taxon = ''
            last_symbol = next_symbol
        else:
            taxon += next_symbol
    print ("Tested distance = %d" % distance)
    
def ALPH(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start ALPH", gmtime()))
    with open(input_file) as resource:
        tree = resource.readline().rstrip()
        line = resource.readline().rstrip()
        while line and line[0:1] != '>':
            tree += line
            line = resource.readline().rstrip()
        
        taxa = dict()
        
        taxon = ''
        taxon_str = ''
        while line and line != 'END TEST':
            if line[0:1] == '>':
                if taxon:
                    taxa[taxon] = taxa_str_to_code(taxon_str)
                taxon = line[1:]
                taxon_str = ''
            else:
                taxon_str += line
            line = resource.readline().rstrip()
    if taxon:
        taxa[taxon] = taxa_str_to_code(taxon_str)
    
    print (strftime("%Y-%m-%d %H:%M:%S Completed reading file", gmtime()))    
    # for key in taxa:
    #    print ("%s (%d): %s" % (key, len(taxa[key]), ','.join(bin(x)[2:].zfill(4) for x in taxa[key])))
    
    tree_stack = []
    taxon = ''
    last_symbol = ''
    
    result = dict()
    dependency = dict()
    distance = 0
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')' or next_symbol == ';':
            if (next_symbol == ')' or next_symbol == ',' or next_symbol == ';') and last_symbol == ')':
                # cross last two taxa
                taxon1 = tree_stack.pop()
                taxon2 = tree_stack.pop()
                print ("Cross %s and %s" % (taxon1, taxon2))
                taxon_code1 = taxa[taxon1]
                taxon_code2 = taxa[taxon2]
                
                taxon_code = []
                dependency[taxon] = dict()
                for i in range(len(taxon_code1)):
                    cross = taxon_code2[i] & taxon_code1[i]
                    # if ((bin(cross).count('1')) == 1):
                    if ((bin(cross).count('1')) >= 1):
                        if (bin(cross).count('1')) >= 1:
                            cross = 2 ** get_first_one(cross)
                        taxon_code.append(cross)
                        if (taxon_code1[i] != cross):
                            # t1 was mixed - restore history
                            unroll_dependencies(result, dependency, taxon1, i, cross) 
                        if (taxon_code2[i] != cross):
                            # t2 was mixed - restore history
                            unroll_dependencies(result, dependency, taxon2, i, cross)
                    else:
                        distance += 1
                        # print ("%d Found mismatch %s and %s. Current distance %d" % (i, bin(taxon_code1[i])[2:], bin(taxon_code2[i])[2:], distance))
                        
                        print ("Add mixed taxon %s-%d : %s" % (taxon, i, bin(taxon_code2[i] | taxon_code1[i])[2:]))
                        taxon_code.append(taxon_code2[i] | taxon_code1[i])
                        dependency[taxon][i] = [taxon1, taxon2]
                        # if bin(taxa[taxon1][i]).count('1') > 1:
                        #    dependency[taxon][i].append(taxon1)
                        # if bin(taxa[taxon2][i]).count('1') > 1:
                        #    dependency[taxon][i].append(taxon2)
                
                result[taxon] = taxon_code
                
                for key in result:
                    print ("%s (%d): %s" % (key, len(result[key]), ','.join([bin(x)[2:].zfill(letters_len) for x in result[key]])))
                # print (distance)
                
                taxa[taxon] = taxon_code 
                tree_stack.append(taxon)
                taxon = ''
            if taxon:
                tree_stack.append(taxon)
                taxon = ''
            last_symbol = next_symbol
        else:
            taxon += next_symbol
            
    root = tree_stack.pop()
    for i in range(len(taxa[root])):
        root_code = taxa[root]
        if bin(root_code[i]).count('1') > 1:
            curr = root_code[i]
            for j in range(letters_len):
                if curr % 2 == 1:
                    unroll_dependencies(result, dependency, root, i, 2 ** j)
                    root_code[i] = 2 ** j
                    break
                curr = curr / 2

    print (strftime("%Y-%m-%d %H:%M:%S Done. ", gmtime()) + "Distance: %d" % distance)
    for key in result:
        print ("%s (%d) : %s" % (key, len(taxa_code_to_str(result[key])), taxa_code_to_str(result[key])))
    for key in result:
        print ("%s (%d): %s" % (key, len(result[key]), ','.join([bin(x)[2:].zfill(letters_len) for x in result[key]])))

    with open(output_file, 'w') as result_file:
        result_file.write(str(distance))
        for key in result.keys():
            result_file.write("\n>" + key + '\n' + taxa_code_to_str(result[key])) 
            
    test_result(taxa, tree)       

ALPH("data/rosalind_alph-3.txt", "data/rosalind_alph_result.txt")


