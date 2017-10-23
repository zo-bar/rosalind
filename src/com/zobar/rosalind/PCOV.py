'''
Created on Aug 21, 2013

@author: Zoya
'''
def get_cyclic_superstring(lines):
    d = dict()
    for line in lines:
        d[line[:-1]] = line[-1:]
    print d
    result = lines[0][:-1]
    next_line = result
    for i in xrange(len(lines) + 1):
        result += d[next_line]
        next_line = result[-len(next_line):]
        print result
    return result[:-len(next_line) - 1]

def PCOV(input_file, output_file):
    lines = [line.strip() for line in open(input_file)]
    result = get_cyclic_superstring(lines)
#    print result
    with open(output_file, "w") as result_file:
        result_file.write(result)

PCOV("src/data/rosalind_pcov.txt", "src/data/rosalind_pcov_result.txt")

# from SuffixTree import find_common_substrings
# def merge_lines(line1, line2):
#    substr = max(find_common_substrings([line1, line2]), key=len)
#    print substr
#    for i in xrange(len(line1)):
#        if line1[:len(substr)] != substr:
#            line1 = line1[-1] + line1[:-1]
#        else:break
#    for i in xrange(len(line2)):
#        if line2[:len(substr)] != substr:
#            line2 = line2[-1] + line2[:-1]
#        else:break
#    return line1[len(substr):] + substr + line2[len(substr):]

# def merge_lines(line1, line2):
#    print "Compare %s and %s" % (line1, line2)
#    result = []
#    starts = []
#    for i, k in enumerate(line1):
#        for start_point in starts[:]:
#            if i - start_point > len(line2):
#                result.append(line1)
#                starts.remove(start_point)
#            elif k != line2[i - start_point]:
#                line2end = line2[i - start_point:]
#                if len(line2end) > start_point:
#                    print "Check line1[:start_point] == line2end[line2end - start_point:]: %s - %s" % (line1[:start_point], line2end[len(line2end) - start_point:])
#                    if line1[:start_point] == line2end[len(line2end) - start_point:]:
#                        print "Append to result %s" % line2end[:len(line2end) - start_point] + line1
#                        result.append(line2end[:len(line2end) - start_point] + line1)
#                else:
#                    print "Check line1[start_point - len(line2end):start_point] == line2end: %s - %s" % (line1[start_point - len(line2end):start_point], line2end)
#                    if line1[start_point - len(line2end):start_point] == line2end:
#                        print "Append to result line1 %s" % line1
#                        result.append(line1)
#                starts.remove(start_point)
#        if k == line2[0]:
#            starts.append(i)
#    if len(starts) > 0:
#        for start_point in starts:
#            line2end = line2[len(line1) - start_point:]
#            line1start = line1
#            for i in xrange(len(line2end) + 1):
#                if i == len(line2end) + 1:
#                    result.append(line1)
#                elif line1start[i] != line2end[i]:
#                    result.append(line1[i:] + line2end)
#                    break
#    print "Result of merging %s and %s is %s" % (line1, line2, min(result))
#    if len(result) > 0:
#        return min(result)

# def get_cyclic_superstring(lines):
#    #    merged = []
#    cache = []  # [[line] for line in lines]
# #    d = dict()
# #    for line in lines:
# #        d[line] = []
#    print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "Lines count %d" % len(lines)
#    for i in xrange(len(lines)):
#        for j in xrange(i + 1, len(lines)):
#            newline = min([merge_lines(lines[i], lines[j]), merge_lines(lines[j], lines[i])], key=len)
#            cache.append([newline, lines[i], lines[j]])
#        # print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "First step %d done" % i
#    cache.sort(key=lambda x:len(x[0]))
# #    print cache
#    print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "First step done"
#    
#    while len(cache) > 1:
#        merged_line = cache[0][0]
#        oldline1 = cache[0][1]
#        oldline2 = cache[0][2]
#        for merged_lines in cache[:]:
#            if merged_lines.count(oldline1) > 0 or merged_lines.count(oldline2) > 0:
#                cache.remove(merged_lines)
#        lines.remove(oldline1)
#        lines.remove(oldline2)
#        for line in lines:
#            newline = merge_lines(merged_line, line)
#            cache.append([newline, merged_line, line])
#        lines.append(merged_line)
#        cache.sort(key=lambda x:len(x[0]))
# #        print cache
#        print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "Still to merge %d" % len(cache)
#    result = cache[0][0]
#    for i in xrange(len(result) / 2, len(result)):
#        if result.startswith(result[i:]):
#            result = result[:i]
#            break        
#    return result

# from time import gmtime, strftime
# def merge_lines(line1, line2):
#    result = []
#    result.append(line1 + line2)
#    len1 = len(line1)
#    len2 = len(line2)
#    i = line1.find(line2[:len2 / 2])
#    while i < len1 - len2 / 2 and i != -1:       
#        for j in xrange(len2 / 2, len2):
#            if i + j >= len1:
#                if line1[i - len2 + j:i] == line2[j:]:
#                    result.append(line1)
#                else:
#                    result.append(line1 + line2[j:])
#                break
#            elif line1[i + j] != line2[j]:
#                if i - len2 + j > 0:
#                    if line1[i - len2 + j:i] == line2[j:]:
#                        result.append(line1)
#                elif line1[:i] == line2[j:]:
#                    result.append(line2[:j] + line1)
#                break
#        i = line1.find(line2[:len2 / 2], i + 1)
#    i = line1.find(line2[len2 / 2:])
#    while i < len1 - len2 / 2 and i != -1:
#        for j in xrange(len2 / 2):
#            if i - j < 0:
#                if line1[i + len2 / 2:i + len2 - j] == line2[:j]:
#                    result.append(line1)
#                else:
#                    result.append(line2[:len2 / 2 - j + 1] + line1)
#                break
#            elif line1[i - j] != line2[len2 / 2 - j]:
#                if i + len2 / 2 + j > len1:
#                    if line1[i + len2 / 2:] == line2[:len1 - i - len2 / 2 - j]:
#                        result.append(line1 + line2[len1 - i - len2 / 2 - j:])
#                elif line1[(i + len2 / 2) :(i + len2 / 2 + j)] == line2[:j]:
#                    result.append(line1)
#                break
#        i = line1.find(line2[len2 / 2:], i + 1)
#    for i in xrange(len2 / 2 + 1):
#        if line1.startswith(line2[len2 / 2 + i:]):
#            result.append(line2[:len2 / 2 + i] + line1)
#            break
#    for i in xrange(1, len2 / 2 + 1):
#        if line1.endswith(line2[:i]):
#            result.append(line1 + line2[i:])
#            break
# #    print "All superstrings for %s and %s are %s" % (line1, line2, ",".join(result))
#    return min(result, key=len)
#   

#    result = lines[0]
#    cache = dict()
#    max_i = len(max(lines, key=len)) + 1
#    for i in xrange(max_i):
#        cache[i] = []
#    cache_lines = dict()
#    for line in lines:
#        cache_lines[line] = 1  # len(line)
#    i = 1
#    cache[i] = lines[:]
#    while len(lines) > 0 and i < max_i + 1:
#        for line in cache[i]:
#            merged_line = merge_lines(result, line)
#            mlen = len(merged_line) - len(result)
#            if mlen == 0:
#                lines.remove(line)
#                cache_lines[line] = None
#                cache[i].remove(line)
#            elif mlen == i:
#                result = merged_line
#                lines.remove(line)
#                cache_lines[line] = None
#                cache[i].remove(line)
#                i = 1
#                break
#            else:
#                if cache[mlen] is None:
#                    cache[mlen] = []
#                if cache_lines[line] is not None and cache[cache_lines[line]].count(line) > 0:
#                    cache[cache_lines[line]].remove(line)
#                cache[mlen].append(line)
#                cache_lines[line] = mlen
#        for i in xrange(len(cache)):
#            if len(cache[i]) > 0:
#                break
#
#    print cache
#    print cache_lines

# def merge_lines(string1, string2):
#    result = string1 + string2
#    distances = []
#    if string1.count(string2) > 0:
#        return string1
#    for i, k in enumerate(string1[-len(string2):]):
#        for distance in distances[:]:
#            if k != string2[i - distance]:
#                distances.remove(distance)
#        if k == string2[0]:
#            distances.append(i)
#    if len(distances) > 0:
#        result = string1[:distances[0] - len(string2)] + string2
#    # print "Merged %s and %s is %s" % (string1, string2, result)
#    return result
#
# def get_cyclic_superstring(lines):
#    result = lines[0]
#    for line in lines:
#        result = merge_lines(result, line)
#    cycle = True
#    while cycle:
#        cycle = False
#        for i in xrange(1, len(result)):
#            if result.startswith(result[i:]):
#                result = result[:i]
#                cycle = True
#                break
#    return result
