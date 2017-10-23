'''
Created on May 8, 2014

@author: zoya
'''

def count_probabilities(left_prob, right_prob):
    result = [0, 0, 0]
    a = left_prob[0]
    b = left_prob[1]
    c = left_prob[2]
    x = right_prob[0]
    y = right_prob[1]
    z = right_prob[2]
    result[0] = a * x + 0.5 * (a * y + b * x) + 0.25 * b * y
    result[1] = a * z + c * x + 0.5 * (a + c) * y + 0.5 * b  # * (x + y + z)==1  
    result[2] = c * z + 0.5 * (c * y + b * z) + 0.25 * b * y
    return result

def fill_prob(anc):
    return [1 if anc.count('a') == x else 0 for x in range(3)]
        
def parse_nwck(line):
    next_anc = ''
    history = []
    left_prob_history = []
    for letter in line:
        if letter == 'A' or letter == 'a':
            next_anc += letter
            if len(next_anc) == 2:
                last_history = history[-1]
                if last_history == ',':
                    # count pedigree prob
                    left_prob_history.append(count_probabilities(left_prob_history.pop(), fill_prob(next_anc)))
                    history.pop()
                elif last_history == '(':
                    left_prob_history.append(fill_prob(next_anc))
                else:
                    print("ERROR in history. Unknown symbol " + last_history)
                next_anc = ''
        elif letter == ',':
            history.append(letter)
        elif letter == '(':
            history.append(letter)
        elif letter == ')':
            if history.count('(') > 0:
                last_hist = history.pop()
                while last_hist != '(':
                    last_hist = history.pop()
            else:
                print ("Error in history. No ( for )")
            if len(history) > 0 and history[-1] == ',':
                left_prob_history.append(count_probabilities(left_prob_history.pop(), left_prob_history.pop()))
                next_anc = ''
                history.pop()
            if len(history) > 0 and history[-1] == ',':
                print ("Error in history. Two , in a row")
    
    print (" ".join(str(x) for x in left_prob_history))
    if len(left_prob_history) != 1:
        print("error. too many results")
    return left_prob_history.pop()


def MEND(input_file, output_file):
    with open(input_file) as resource_file:
        line = resource_file.readline()
    result = parse_nwck(line)
    print (" ".join(str((round(x, 3))) for x in result))
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(str((round(x, 3))) for x in result))
        
MEND("src/data/rosalind_mend.txt", "src/data/rosalind_mend_result.txt")
