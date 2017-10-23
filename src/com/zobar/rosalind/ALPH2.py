'''
Created on Feb 1, 2016

@author: zoya
'''

from time import gmtime, strftime

LETTERS = ['A', 'C', 'G', 'T', '-']
letters_len = 5
test_mode = False

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
        if not test_mode and (bin(next_symbol).count('1') > 1):
            print ("HERE")
        for i in range(len(LETTERS)):
            if next_symbol % 2 == 1:
                taxon_str += LETTERS[i]
                break
            next_symbol = next_symbol / 2
    return taxon_str

def print_result(result):
    for key in result:
        print ("%s (%d) : %s" % (key, len(taxa_code_to_str(result[key])), taxa_code_to_str(result[key])))
    for key in result:
        print ("%s (%d): %s" % (key, len(result[key]), ','.join([bin(x)[2:].zfill(letters_len) for x in result[key]])))
             
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
            if (test_mode):
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
    
def read_input(input_file, taxa):
    with open(input_file) as resource:
        tree = resource.readline().rstrip()
        line = resource.readline().rstrip()
        while line and line[0:1] != '>':
            tree += line
            line = resource.readline().rstrip()
        
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
    # for key in taxa:
    #    print ("%s (%d): %s" % (key, len(taxa[key]), ','.join(bin(x)[2:].zfill(4) for x in taxa[key])))
    
    print (strftime("%Y-%m-%d %H:%M:%S Completed reading file", gmtime()))     
    return tree

def process_vertex(taxon1, taxon2, taxon, taxa, result, dependency):
    if (test_mode):
        print ("Cross %s and %s" % (taxon1, taxon2))
    taxon_code1 = taxa[taxon1]
    taxon_code2 = taxa[taxon2]
    
    distance = 0
    
    taxon_code = []
    dependency[taxon] = dict()
    for i in range(len(taxon_code1)):
        cross = taxon_code2[i] & taxon_code1[i]
        cross_ones_count = (bin(cross).count('1'))
        if cross_ones_count == 0:
            mix = taxon_code2[i] | taxon_code1[i]
            if (test_mode):
                print ("Add mixed taxon %s-%d : %s" % (taxon, i, bin(mix)[2:]))
            taxon_code.append(mix)
            dependency[taxon][i] = [taxon1, taxon2]
            distance += 1
        elif cross_ones_count > 1:
            if (test_mode):
                print ("Add mixed taxon %s-%d : %s" % (taxon, i, bin(cross)))
            taxon_code.append(cross)
            dependency[taxon][i] = [taxon1, taxon2]
        else:
            # cross_ones_count == 1
            taxon_code.append(cross)
            if (taxon_code1[i] != cross):
                # t1 was mixed - restore history
                unroll_dependencies(result, dependency, taxon1, i, cross) 
            if (taxon_code2[i] != cross):
                # t2 was mixed - restore history
                unroll_dependencies(result, dependency, taxon2, i, cross)
            
    result[taxon] = taxon_code
    taxa[taxon] = taxon_code 
                
    return distance  
    
def ALPH(input_file, output_file, mode):
    test_mode = mode
    print (strftime("%Y-%m-%d %H:%M:%S Start ALPH", gmtime()))
    taxa = dict()
    tree = read_input(input_file, taxa)    

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
                
                distance += process_vertex(taxon1, taxon2, taxon, taxa, result, dependency)
                
                if (test_mode):
                    print_result(result)
                
                tree_stack.append(taxon)
                taxon = ''
            if taxon:
                tree_stack.append(taxon)
                taxon = ''
            last_symbol = next_symbol
        else:
            taxon += next_symbol
           
    if (test_mode):
        print ("Process root")
    root = tree_stack.pop()
    for i in range(len(taxa[root])):
        root_code = taxa[root]
        if bin(root_code[i]).count('1') > 1:
            val = 2 ** get_first_one(root_code[i])
            unroll_dependencies(result, dependency, root, i, 2 ** val)
            root_code[i] = val
            
    print (strftime("%Y-%m-%d %H:%M:%S Done. ", gmtime()) + "Distance: %d" % distance)
    print_result(result)
    
    with open(output_file, 'w') as result_file:
        result_file.write(str(distance))
        for key in result.keys():
            result_file.write("\n>" + key + '\n' + taxa_code_to_str(result[key])) 
            
    test_result(taxa, tree)       

ALPH("data/rosalind_alph-3.txt", "data/rosalind_alph_result.txt", False)
