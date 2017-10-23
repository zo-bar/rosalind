class Node:
    def __init__(self, node, substr, pass_strings):
        self.child_nodes = []
        self.parent_node = node
        self.substr = substr
        self.pass_strings = pass_strings
        self.level = self.parent_node.level + 1 if self.parent_node != None else 0
    
    def __str__(self):
        if (len(self.child_nodes) == 0):
            return self.substr
        space = "\n" + "  " * (self.level)
        return ("," + space[:len(space) ] + "|_").join(str(self.substr + space + "  |_" + str(child_node)) for child_node in self.child_nodes)         
    
    def full_substr(self):
        result = self.substr
        node = self.parent_node
        while node != None and node.substr != "!":
            result = str(node.substr) + result
            node = node.parent_node        
        return result
            
class SuffixTree:
    def __init__(self):
        self.root_node = Node(None, "!", set([]))
        
    def add_string(self, string, string_id):
        self.root_node.pass_strings.add(string_id)
        for i in range(len(string) - 1, -1, -1):
            self.add_suffix(self.root_node, string[i:], string_id)
        
    def add_suffix(self, node, string, string_id):
        for child_node in node.child_nodes:
            if (child_node.substr[:1] == string[:1]):
                if (child_node.substr == string):
                    for child_child_node in child_node.child_nodes:
                        if child_child_node.substr == "$" + str(string_id):
                            break
                    else:
                        child_node.child_nodes.append(Node(child_node, "$" + str(string_id), set([string_id])))
                        child_node.pass_strings.add(string_id)
                elif (string.startswith(child_node.substr)):
                    self.add_suffix(child_node, string[len(child_node.substr):], string_id)
                    child_node.pass_strings.add(string_id)
                elif (child_node.substr.startswith(string)):
                    self.split_node(child_node, string, string_id)
                    child_node.parent_node.child_nodes.append(Node(child_node.parent_node, "$" + str(string_id), set([string_id])))
                else:
                    # strings differ in the middle
                    for i in range(min(len(string) + 1, len(child_node.substr)) + 1):
                        if string[:i] != child_node.substr[:i]:
                            break
                    self.split_node(child_node, child_node.substr[:i - 1], string_id)
                    self.add_suffix(child_node.parent_node, string[i - 1:], string_id)
                break
        else:
            next_node = Node(node, string, set([string_id]))
            next_node.child_nodes.append(Node(next_node, "$" + str(string_id), set([string_id])))
            node.child_nodes.append(next_node)

    def split_node(self, node, common_string, string_id):
        parent_node = Node(node.parent_node, common_string, set([str_id for str_id in node.pass_strings]))
        parent_node.pass_strings.add(string_id)
        node.parent_node.child_nodes.remove(node)
        node.parent_node.child_nodes.append(parent_node)
        node.parent_node = parent_node
        node.substr = node.substr[len(common_string):]
        self.move_levels(node, 1)
        parent_node.child_nodes.append(node)
        
    def move_levels(self, node, levels):
        node.level = node.level + levels
        for child_node in node.child_nodes:
            self.move_levels(child_node, levels)

    def __str__(self):
        return str(self.root_node)

def check_passing_strings(node, strings_list, result):
    if (not node.pass_strings is None) and (strings_list.issubset(set(node.pass_strings))):     
        result.append(node.full_substr())
        for child_node in node.child_nodes:
            check_passing_strings(child_node, strings_list, result)
        return result
    
def find_common_substrings(strings_list):
    tree = SuffixTree()
    string_ids = set([])
    for i, string in enumerate(strings_list):
        tree.add_string(string, i)
        string_ids.add(i)
    # print tree
    result = check_passing_strings(tree.root_node, string_ids, [])
    # print str(result)
    return result
    
def find_longest_common_substring(strings_list):
    return max(find_common_substrings(strings_list), key=len)    
        
# print str(find_common_substrings(["DA", "D"]))
# print str(find_longest_common_substring([ "ATAATTAATT"]))
