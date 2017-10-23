'''
Created on Feb 2, 2016

@author: zoya
'''
# greedy algorythm
from time import gmtime, strftime
test_mode = True

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
                    taxa[taxon] = taxon_str
                taxon = line[1:]
                taxon_str = ''
            else:
                taxon_str += line
            line = resource.readline().rstrip()
    if taxon:
        taxa[taxon] = taxon_str
#             if line[0:1] == '>':
#                 taxon = line[1:]
#                 taxa[taxon] = resource.readline().rstrip()
#             line = resource.readline().rstrip()
    
    print (strftime("%Y-%m-%d %H:%M:%S Completed reading file", gmtime()))     
    return tree

def process_vertex(index1, index2, prev_result):
    result = []
    # index1 = taxa_list.index(taxon1)
    # index2 = taxa_list.index(taxon2)
    for prev in prev_result:
        min_prev = min(prev.values())
        res_dict = dict()
        result.append(res_dict)
        for res in prev:
            if prev[res] < min_prev + 1:
                t1 = res[index1]
                t2 = res[index2]
                if t1 == t2:
                    res_dict[res + t1] = prev[res]
                else:
                    res_dict[res + t1] = prev[res] + 1
                    res_dict[res + t2] = prev[res] + 1
    if test_mode: print (result)
    return result

def greedy_alph(tree, taxa, result_taxa):
    tree_stack = []
    taxon = ''
    last_symbol = ''
    taxa_list = list(taxa.keys())
    if test_mode: print (taxa_list)
    taxon_len = len(next(iter(taxa.values())))
    
    result = [{''.join(t[i] for t in taxa.values()):0} for i in range(taxon_len)]    
    if test_mode: print (result)
    
    counter = 0
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')' or next_symbol == ';':
            if (next_symbol == ')' or next_symbol == ',' or next_symbol == ';') and last_symbol == ')':
                # cross last two taxa
                taxon1 = tree_stack.pop()
                taxon2 = tree_stack.pop()
                counter += 1
                if not test_mode and counter % 10 == 0:
                    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "%d : %d" % (counter, len(next(iter(result)))))
                if (test_mode): print ("Cross %d and %d" % (taxon1, taxon2))
                result = process_vertex(taxon1, taxon2, result)
                
                taxa_list.append(taxon)
                tree_stack.append(taxa_list.index(taxon))
                taxon = ''
            if taxon:
                tree_stack.append(taxa_list.index(taxon))
                taxon = ''
            last_symbol = next_symbol
        else:
            taxon += next_symbol
    
    if test_mode: print (result)
    
    distance = 0
    result_taxa.update({t:'' for t in taxa_list})  # ['' for i in range(len(taxa_list))]
    
    for position_values in result:
        min_value = 1000000
        best_position = ''
        for position_value in sorted(position_values.keys()):
            if position_values[position_value] < min_value:
                min_value = position_values[position_value]
                best_position = position_value
        for i, taxon in enumerate(taxa_list):
            result_taxa[taxon] += best_position[i]
        distance += min_value        
    
    if test_mode: print(result_taxa)
    if test_mode: print (distance)
    
    if test_result(result_taxa, tree) != distance:
        print ("WRONG RESULT!")
    return distance
 
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
    return distance     

def ALPH(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start ALPH", gmtime()))
    taxa = dict()
    tree = read_input(input_file, taxa)    
    
    result_taxa = dict()
    distance = greedy_alph(tree, taxa, result_taxa)
    for key in sorted(result_taxa.keys()):
        if key not in taxa.keys():
            print ("%s: %s" % (key, result_taxa[key]))
    print (distance)
    
    with open(output_file, 'w') as result_file:
        result_file.write(str(distance))
        for key in result_taxa.keys():
            if key not in taxa.keys():
                result_file.write("\n>" + key + '\n' + (result_taxa[key])) 
    print (strftime("%Y-%m-%d %H:%M:%S Finish ALPH", gmtime()))     

test_mode = False
ALPH("data/rosalind_alph.txt", "data/rosalind_alph_result.txt")
