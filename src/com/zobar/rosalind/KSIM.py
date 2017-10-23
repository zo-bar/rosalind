'''
Created on Feb 7, 2016

@author: zoya
'''
import copy
from time import gmtime, strftime

MATCH_SCORE = 1
MISMATCH_SCORE = -1
test_mode = True

class Substr:
    def __init__(self, start, check_string):
        self.start = start
        self.check_string = check_string
        self.mismatch_count = 0        
        self.str_len = 0
        self.match_string = ''
        self.main_string = ''
        
def process_candidate_equals(candidate, letter):
    candidate.str_len += 1
    candidate.match_string += letter
    candidate.main_string += letter
    if len(candidate.check_string) > 1:
        candidate.check_string = candidate.check_string[1:]
    else:
        candidate.check_string = ''
    return candidate

def process_candidate_1(candidate, letter):
    # 1 case: insert '-' to main string
    for j, l in enumerate(candidate.check_string):
        if l == letter:
            candidate.mismatch_count += j
            candidate.str_len += 1
            candidate.match_string += candidate.check_string[:j + 1]
            candidate.main_string += '-' * j + letter
            if len(candidate.check_string) > j + 1:
                candidate.check_string = candidate.check_string[j + 1:]
            else:
                candidate.check_string = ''
            return candidate
    candidate.mismatch_count += len(candidate.check_string)
    candidate.main_string += "-" * len(candidate.check_string)
    candidate.match_string += candidate.check_string
    candidate.check_string = ''
    return candidate

def process_candidate_2(candidate, letter):
    # 2 case: insert '-' to match string
    candidate.mismatch_count += 1
    # candidate.str_len += 1
    candidate.match_string += '-'
    candidate.main_string += letter
    return candidate
    
def process_candidate_3(candidate, letter):
    # 3 case:accept mismatch
    candidate.mismatch_count += 1
    candidate.str_len += 1
    candidate.match_string += candidate.check_string[:1]
    candidate.main_string += letter
    if len(candidate.check_string) > 1:
        candidate.check_string = candidate.check_string[1:]
    else:
        candidate.check_string = ''
    return candidate

    
def KSIM(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start KSIM", gmtime())) 
    
    with open(input_file) as resource:
        k = int(resource.readline().rstrip())
        s = resource.readline().rstrip()
        t = resource.readline().rstrip()
    if test_mode: print ("k: %d, s:%s, t:%s" % (k, s, t))
    result = []
    candidates = []
    
    for i, letter in enumerate(t):
        if test_mode: print("Process next letter: %s" % letter)
        elif i % 10 == 0: print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + " Letter %s (%d), candidates count: %d" % (letter, i, len(candidates)))
        
        next_step_candidates = []
        candidates.append(Substr(i + 1, s))
        
        for candidate in candidates:
            if letter == candidate.check_string[0]:
                next_step_candidates.append(process_candidate_equals(candidate, letter))
            else:
                # 1 case: insert '-' to main string
                next_step_candidates.append(process_candidate_1(copy.copy(candidate), letter))
                # 2 case: insert '-' to match string
                next_step_candidates.append(process_candidate_2(copy.copy(candidate), letter))
                # 3 case: accept mismatch 
                next_step_candidates.append(process_candidate_3(copy.copy(candidate), letter))
                
#         if test_mode: 
#             for c in candidates:
#                 print ("Next step candidate start: %d, len: %d, mismatch: %d, match string: %s, main_string:%s" % (c.start, c.str_len, c.mismatch_count, c.match_string, c.main_string)) 
       
        candidates = []           
        for candidate in next_step_candidates:
            if len(candidate.check_string) >= 1:
                if candidate.mismatch_count <= k:
                    candidates.append(candidate) 
            elif candidate.mismatch_count <= k:
                result.append(candidate)
                if test_mode:
                    print ("Added to result -  start: %d, len: %d, mismatch: %d, match string: %s, main_string:%s" % (candidate.start, candidate.str_len, candidate.mismatch_count, candidate.match_string, candidate.main_string)) 
            
        if test_mode: 
            for c in candidates:
                print ("Candidate start: %d, len: %d, mismatch: %d, match string: %s, main_string: %s, check string: %s" % (c.start, c.str_len, c.mismatch_count, c.match_string, c.main_string, c.check_string)) 
    
    for candidate in candidates:
        if len(candidate.check_string) + candidate.mismatch_count <= k:
            candidate.main_string += '-' * len(candidate.check_string)
            candidate.match_string += candidate.check_string
            candidate.mismatch_count += len(candidate.check_string)
            candidate.check_string = ''
            result.append(candidate)
            if test_mode:
                print ("Added to result -  start: %d, len: %d, mismatch: %d, match string: %s, main_string:%s" % (candidate.start, len(candidate.main_string) - candidate.main_string.count('-'), candidate.mismatch_count, candidate.match_string, candidate.main_string)) 
            
    for r in result:
        print ("Result start: %d, len: %d, mismatch: %d, match string: %s, main_string:%s" % (r.start, len(r.main_string) - r.main_string.count('-'), r.mismatch_count, r.match_string, r.main_string)) 
    
    print (strftime("%Y-%m-%d %H:%M:%S Finished KSIM", gmtime()))  

    with open(output_file, "w") as result_file:
        result_file.write('\n'.join(str(r.start) + ' ' + str(len(r.main_string) - r.main_string.count('-')) for r in result))
 
test_mode = False      
KSIM("data/rosalind_ksim_test.txt", "data/rosalind_ksim0_result.txt")
