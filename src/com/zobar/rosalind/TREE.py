'''
Created on Jul 18, 2013

@author: Zoya
'''

def tree(input_file, output_file):
    with open(input_file) as resource:
        nodes = [[] for x in xrange(int(resource.readline()))]
        k = resource.readline()
        while k:
            edge = k.split(" ")
            node1 = int(edge[0].rstrip()) - 1
            node2 = int(edge[1].rstrip()) - 1
            nodes[node1].append(node2)
            nodes[node2].append(node1)
            k = resource.readline()    
#   count the number of isolated sites 
    result = 0
    for i in xrange(len(nodes)):
        next_node = nodes[i]
        if not next_node is None:
            result = result + 1
            # if the node has any edges
            if len(next_node) > 0:
                for node in get_contact_nodes(i, nodes, [i]):
                    nodes[node] = None
#   number of edges needed is the number of isolated sites -1
    result = result - 1
    with open(output_file, "w") as result_file:
        result_file.write(str(result))

def get_contact_nodes(node, nodes, contact_nodes):
    for contact_node in nodes[node]:
#        if it's a new node, add it to contact list and then add all of it contacts
        if contact_nodes.count(contact_node) == 0:
            contact_nodes.append(contact_node)
#            print contact_nodes
            get_contact_nodes(contact_node, nodes, contact_nodes)
    return contact_nodes

tree("data/rosalind_tree.txt", "data/rosalind_tree_result.txt")
