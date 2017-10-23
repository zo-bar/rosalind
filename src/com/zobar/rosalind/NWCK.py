'''
Created on Aug 15, 2013

@author: Zoya
'''

def find_distance(tree, node1, node2):
    start = tree.index(node1) + len(node1)
    finish = tree.index(node2)
    if start > finish: return find_distance(tree, node2, node1)
    print ("Start processing %s" % tree)
    history = []
    for letter in tree[start:finish]:
        if letter == '(':
            history.append(letter)
        elif letter == ',': 
            if (len(history) == 0 or history[-1] != ','):  # and history.count(')') == 0:
                history.append(letter)
#            elif len(history) >0 and history[-1] == ')':
#                history.pop()
#                history.append(letter)
        elif letter == ')':
            if history.count('(') > 0:
                last_hist = history.pop()
                while last_hist != '(':
                    last_hist = history.pop()
            elif len(history) > 0 and history[-1] == ',':
                history.pop()
                history.append(letter)
            else:
                history.append(letter)
    result = 0
    for i in range(len(history) - 1):
        if history[i] == '(' and history[i + 1] == ',' and (len(history) == i + 2 or history[i + 2] == '('):
            result -= 2
    print (history)
    
    for letter in history:
        if letter == '(' or letter == ')':
            result += 1
        elif letter == ",":
            result += 2    
    print (result)
    return result

def NWCK(input_file, output_file):
    lines = [line.strip() for line in open(input_file)]
    i = 0
    result = []
    while i < len(lines):
        result.append(find_distance(lines[i], lines[i + 1].split(" ")[0], lines[i + 1].split(" ")[1]))
        i += 3
    with open(output_file, 'w') as result_file:
        result_file.write(" ".join(str(x) for x in result))

NWCK("data/rosalind_nwck.txt", "data/rosalind_nwck_result.txt")
