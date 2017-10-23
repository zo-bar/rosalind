'''
Created on Sep 29, 2013

@author: Zoya
'''
def get_weight(tree, i):
    weight = 0
    index = tree.index(":", i) + 1
    while tree[index].isdigit():
        weight = weight * 10 + int(tree[index])
        index += 1
    return weight

def find_distance(tree, node1, node2):
    start = tree.index(node1) + len(node1)
    finish = tree.index(node2)
    if start > finish: return find_distance(tree, node2, node1)
    print "Start processing %s" % tree
    history = []
    weights = []
    for i, letter in enumerate(tree[start:finish]):
        if letter == '(':
            history.append(letter)
        elif letter == ',':
            if (len(history) == 0 or history[-1] == ')'):
                history.append(letter)
            elif len(history) > 0 and history[-1] == ',':
                weights.pop()
            elif len(history) > 0 and history[-1] == '(':
                weights.pop()
#                history.append(letter)
                # print "i=%d, pop for ',' %s" % (i, ", ".join(str(w) for w in weights))
        elif letter == ')':
            if history.count('(') > 0:
                last_hist = history.pop()
                weights.pop()
                while last_hist != '(':
                    last_hist = history.pop()
                    weights.pop()
                    # print "i=%d, pop for ')' %s" % (i, ", ".join(str(w) for w in weights))
            elif len(history) > 0 and history[-1] == ',':
                history.pop()
                weights.pop()
                history.append(letter)
            else:
                history.append(letter)
        elif letter == ":":
            weights.append(get_weight(tree, i + start))
            # print "i=%d, add for ':' %s" % (i, ", ".join(str(w) for w in weights))
    
    print history
    print weights
        
    weights.append(get_weight(tree, finish))
    
    i = finish + 1
    braces_to_close = history.count('(')
    new_braces = 0
    while i < len(tree) and braces_to_close > 0:
        if tree[i] == ')':
            if new_braces > 0:
                new_braces -= 1
            else:
                weights.append(get_weight(tree, i))
                braces_to_close -= 1
        elif tree[i] == '(':
            new_braces += 1 
        i += 1
#    return sum(weights)
    print history
    print weights
    result = sum(weights)
    print result
    return result
    
def NKEW(input_file, output_file):
    lines = [line.strip() for line in open(input_file)]
    i = 0
    result = []
    while i < len(lines):
        result.append(find_distance(lines[i], lines[i + 1].split(" ")[0], lines[i + 1].split(" ")[1]))
        i += 3
    with open(output_file, 'w') as result_file:
        result_file.write(" ".join(str(x) for x in result))

NKEW("src/data/rosalind_nkew.txt", "src/data/rosalind_nkew_result.txt")
