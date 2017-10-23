'''
Created on Feb 4, 2016

@author: zoya
'''

from time import gmtime, strftime
test_mode = True

class ReversedSubstiution():
    def __init__(self, i, s, w, si, wi):
        self.position = i
        self.original_taxon = None
        self.original_symbol = si
        self.changed_taxon = w
        self.substituted_symbol = wi
        self.changed_back_taxon = s

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

    print (strftime("%Y-%m-%d %H:%M:%S Completed reading file", gmtime()))     
    return tree

def process_vertex(child1, child2, parent, taxa, candidates, result):
    candidates[parent] = dict()
    for i in range(len(taxa[parent])):
        c = []
        if child1 in candidates and i in candidates[child1]:
            for cand in candidates[child1][i]:
                if cand.substituted_symbol == taxa[parent][i]:
                    # stays candidate
                    cand.changed_taxon = parent
                    c.append(cand)
                elif cand.original_symbol == taxa[parent][i]:
                    # reversed substitution found
                    cand.original_taxon = parent
                    result.append(cand)
        if child2 in candidates and i in candidates[child2]:
            for cand in candidates[child2][i]:
                if cand.substituted_symbol == taxa[parent][i]:
                    # stays candidate
                    cand.changed_taxon = parent
                    c.append(cand)
                elif cand.original_symbol == taxa[parent][i]:
                    # reversed substitution found
                    cand.original_taxon = parent
                    result.append(cand)
        
        if taxa[child1][i] != taxa[parent][i]:
            c.append(ReversedSubstiution(i, child1, parent, taxa[child1][i], taxa[parent][i]))
        if taxa[child2][i] != taxa[parent][i]:
            c.append(ReversedSubstiution(i, child2, parent, taxa[child2][i], taxa[parent][i]))
            
        if len(c) > 0:
            candidates[parent][i] = c
    return

def greedy_alph(tree, taxa):
    tree_stack = []
    taxon = ''
    last_symbol = ''
    candidates = dict()
    result = []
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')' or next_symbol == ';':
            if (next_symbol == ')' or next_symbol == ',' or next_symbol == ';') and last_symbol == ')':
                # cross last two taxa
                taxon1 = tree_stack.pop()
                taxon2 = tree_stack.pop()
                
                if (test_mode): print ("Cross %s and %s" % (taxon1, taxon2))
                
                process_vertex(taxon1, taxon2, taxon, taxa, candidates, result)
                
                tree_stack.append(taxon)
                taxon = ''
            if taxon:
                tree_stack.append(taxon)
                taxon = ''
            last_symbol = next_symbol
        else:
            taxon += next_symbol
    
    for s in result:
        print ("Substitution: %s %s %d %s->%s->%s" % (s.changed_taxon, s.changed_back_taxon, s.position + 1, s.original_symbol, s.substituted_symbol, s.original_symbol))
    return result
 

def RSUB(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start ALPH", gmtime()))
    taxa = dict()
    tree = read_input(input_file, taxa)    
    
    result = greedy_alph(tree, taxa)
    
    with open(output_file, 'w') as result_file:
        for s in result:
            result_file.write("%s %s %d %s->%s->%s\n" % (s.changed_taxon, s.changed_back_taxon, s.position + 1, s.original_symbol, s.substituted_symbol, s.original_symbol))
    print (strftime("%Y-%m-%d %H:%M:%S Finish ALPH", gmtime()))     

test_mode = False
RSUB("data/rosalind_rsub.txt", "data/rosalind_rsub_result.txt")
