import math
import time

class TreeNode:
	def __init__(self):
		self.children = {}

	def add_child(self, branch, child):
		self.children[branch] = child

	def is_leaf(self, branch):
		return not(type(self.children[branch]) == TreeNode)

	def has_children(self):
		return (self.children)


def print_TreeNode(root, count):
	#print attribute
	print('\t' * count,f'<{root.att}>')

	#print branches
	for branch in list(root.children):
		if root.is_leaf(branch):
			print('\t' * (count+1),f'{branch}: {root.children[branch][0]} ({root.children[branch][1]})')
		elif not(root.children[branch].has_children()):
			print('\t' * (count+1),f'{branch}: {root.children[branch].att[0]} ({root.children[branch].att[1]})')
		else:
			print('\t' * (count+1),f'{branch}:')
			print_TreeNode(root.children[branch],count+2)

def get_dictionary():
	#Identify csv data
	dataset = input('Please insert the name of the file with the data: ')
	csv = open(dataset,'r')

	#Import csv data to dictionary
	dic = {}
	for line in csv:
		line = line.partition("\n")[0].split(',')
		#Search and convert any number in the line
		line[1:] = convert_if_number(line[1:])
		#insert in dictionary
		dic[line[0]] = line[1:]
	return dic


def if_number(att):
    # Retorna verdadeiro caso o conteudo do atributo possa ser numero real
    for char in att:
        if not('0'<=char<='9' or char=='.'):
            return False
    return True


def convert_if_number(line):
	# Retorna a lista com os possiveis numeros convertidos
	for i, att in enumerate(line):
		if(if_number(att)):
			line[i] = float(att)
	return line


def filter_dictionary(dic, att, val):
	#Extracts from the dictionary all the lines with the value
	pos = get_pos_in_dic(dic, att)
	if(pos is None):
		return {}

	if(type(list(val)[0]) is float):
		return filter_dictionary_number(dic, pos, val)

	new_dic = {}
	new_dic[list(dic)[0]] = dic[list(dic)[0]][0:pos] + dic[list(dic)[0]][pos+1:]
	for line in dic.items():
		if(line[1][pos] == val):
			new_dic[line[0]] = line[1][0:pos] + line[1][pos+1:]
	return new_dic


def filter_dictionary_number(dic, pos, val):
	# Returns a new dictionary with all the correspondent lines removed
	new_dic = {}
	new_dic[list(dic)[0]] = dic[list(dic)[0]][0:pos] + dic[list(dic)[0]][pos+1:]
	for line in list(dic.items())[1:]:
		if(line[1][pos] >= list(val)[0] and line[1][pos] < list(val)[1]):
			new_dic[line[0]] = line[1][0:pos] + line[1][pos+1:]
	return new_dic

def order_vector(dic, pos):
    '''retorna uma lista ordenada e convertida do atributo numero X associado a sua classe'''
    v1 = []
    for line in dic.items():
        if line[0] == list(dic)[0]:	continue
        v1.append([line[1][pos],line[1][-1]])
    return sorted(v1)

def most_common_value(dic):
	vec = order_vector(dic, -1)
	counter = {}
	for value in vec:
		if not(value[-1] in list(counter)):
			counter[value[-1]] = 0
		counter[value[-1]] += 1

	return max(counter, key=counter.get), counter[max(counter, key=counter.get)]


def values_counter(dic):
	vec = order_vector(dic, -1)
	counter = {}
	for value in vec:
		if not(value[-1] in list(counter)):
			counter[value[-1]] = 0
		counter[value[-1]] += 1
	return counter

def is_all_same_value(dic):
	vec = order_vector(dic, -1)
	previous_value = vec[0][0]
	for value in vec:
		if (value[-1] != previous_value):
			return False
	return True

def empty_dic(dic):
	return (len(list(dic)) == 1)

def entropy(values):
	# Calculates the entropy
	examples = sum(values)
	total = 0
	for item in values:
		item = item/examples
		total -= item * math.log2(item)
	return total


def parent_entropy(branch):
	vec = []
	for result in branch.items():
		vec.append(result[1])
	return entropy(vec)

def parent_branching(dic):
	node = {}
	vec = order_vector(dic, -1)
	att = list(dic[list(dic)[0]])[-1]

	node[att] = {}
	node[att][vec[0][0]] = 0

	for item in vec:
		# change of result
		if not(item[1] in list(node[att])): 
			node[att][item[0]] = 0

		node[att][item[0]] += 1

	return node

def branching(dic):
	node = {}
	for pos, att in enumerate(dic[list(dic)[0]]):
		vec = order_vector(dic, pos)

		# IF values are REAL call another function
		if (type(vec[0][0]) is float):
			node[att] = branching_number(vec)
			continue

		#initial values
		node[att] = {}
		node[att][vec[0][0]] = {}
		node[att][vec[0][0]][vec[0][1]] = 0

		for item in vec:
			# change of branch
			if not(item[0] in list(node[att])):
				node[att][item[0]] = {}
				node[att][item[0]][item[1]] = 0

			# change of result
			if not(item[1] in list(node[att][item[0]])): 
				node[att][item[0]][item[1]] = 0

			node[att][item[0]][item[1]] += 1

	node.pop(list(node)[-1])
	return node


def branching_number(vec):
	#initial values
	branch = {}
	final_branch = {}
	init_value = vec[0][0]
	branch[init_value] = {}
	branch[init_value][vec[0][1]] = 0
	length = len(vec)/5
	count = 0

	for item in vec:
		# change of branch
		if(count >= length):
			count = 0
			final_branch[(init_value, item[0])] = branch[init_value]
			init_value = item[0]
			branch[init_value] = {}
			branch[init_value][item[1]] = 0

		# change of result
		if not(item[1] in list(branch[init_value])):
			branch[init_value][item[1]] = 0

		branch[init_value][item[1]] += 1
		count += 1

	final_branch[(init_value, vec[-1][0]+1)] = branch[init_value]
	return final_branch

def rebranching(dic, node):
	new_node = node.copy()
	for att in list(node):
		for branch in list(node[att]):
			node[att][branch] = values_counter(filter_dictionary(dic, att, branch))
	return new_node

def information_gain(parent_ent, node):
	# calculate node entropy
	total = 0
	node_ent = []
	for branch in node.items():
		aux = []
		for result in branch[1].items():
			aux.append(result[1])
			total += result[1]
		node_ent.append([sum(aux),entropy(aux)])

	# calculate weighted average
	total_node = 0
	for values in node_ent:
		total_node += (values[0]/total)*values[1]

	# return information gain
	return parent_ent - total_node

def get_pos_in_dic(dic, find_att):
	for i, att in enumerate(dic[list(dic)[0]]):
		if(att == find_att): return i
	return None

def get_next_att(node, parent_ent):
	#get best information gain
	max_att = [list(node)[0],information_gain(parent_ent, node[list(node)[0]])]
	for att in list(node):
		val = information_gain(parent_ent, node[att])
		if (val > max_att[1]):	max_att = [att, val]

	return max_att[0]

def no_more_value(node, parent_ent):
	for att in list(node):
		if (information_gain(parent_ent, node[att]) > 0):
			return False
	return True


def get_decision_tree(dictionary, parent_ent):
	node = branching(dictionary)
	att = get_next_att(node, parent_ent)
	root = TreeNode(att, node[att])
	for branch in list(root.children):
		if(len(node[att][branch]) == 1):
			root.add_leaf(branch,list(node[att][branch])[0])
		else:
			new_dic = filter_dictionary(dictionary, get_pos_in_dic(dictionary, att), branch)
			root.add_child(branch, get_decision_tree(new_dic, parent_entropy(node[att][branch])))
	return root

def ID3(dictionary, attributes, parent_ent):
	root = TreeNode()

	if (is_all_same_value(dictionary)):
		root.att = most_common_value(dictionary)
		return root

	if not(attributes):
		root.att = most_common_value(dictionary)
	else:
		node = rebranching(dictionary, attributes)
		root.att = get_next_att(node, parent_ent)
		new_dictionary = []
		new_attributes = []
		for branch in attributes[root.att]:
			new_dictionary.append(filter_dictionary(dictionary, root.att, branch))
			if(empty_dic(new_dictionary[-1])):
				root.add_child(branch, most_common_value(dictionary))
			else:
				new_attributes.append(attributes.copy())
				new_attributes[-1].pop(root.att)
				root.add_child(branch, ID3(new_dictionary[-1], new_attributes[-1], parent_entropy(node[root.att][branch])))
	return root

def main():
	#read csv file into dictionary
    time_before_dic = time.time()
    dictionary = get_dictionary()
    time_after_dic = time.time()
    time_dic = time_after_dic - time_before_dic
    print("time_dic =", time_dic)

	#Build decision tree
    time_before_parent_branching = time.time()
    node = parent_branching(dictionary)
    time_after_parent_branching = time.time()
    time_parent_branching = time_after_parent_branching - time_before_parent_branching
    print("time_parent_branching =", time_parent_branching)
    
    time_before_ent = time.time()
    parent_ent = parent_entropy(node[list(node)[0]])
    time_after_ent = time.time()
    time_ent = time_after_ent - time_before_ent
    print("time_ent =", time_ent)
    
    time_before_branching = time.time()
    node = branching(dictionary)
    time_after_branching = time.time()
    time_branching = time_after_branching - time_before_branching
    print("time_branching =", time_branching)
    
    time_before_ID3 = time.time()
    root = ID3(dictionary, node, parent_ent)
    time_after_ID3 = time.time()
    time_ID3 = time_after_ID3 - time_before_ID3
    print("time_ID3 =", time_ID3)
    

	#Print decision tree
    time_before_print = time.time()
    print_TreeNode(root,0)
    time_after_print = time.time()
    time_print = time_after_print - time_before_print
    print("time_print =", time_print)

    example(root)


def get_dictionary_example():
	#Identify csv data
	dataset = input('Please insert the name of the file with the data for the example testing: ')
	csv = open(dataset,'r')

	#Import csv data to dictionary
	dic = {}
	for line in csv:
		line = line.partition("\n")[0].split(',')
		#Search and convert any number in the line
		line[1:] = convert_if_number(line[1:])
		#insert in dictionary
		dic[line[0]] = line[1:]
	return dic

def example(root):
        dic = get_dictionary_example()
        root_base = root
        attr = dic[list(dic)[0]]
        for example in list(dic)[1:]:
                ex = dic[example][:-1]
                root = root_base
                for i in range(len(ex)):
                        ex[i] = str(ex[i])
                while True:
                        att_pos = attr.index(root.att)
                        Z = ex_aux(ex[att_pos],root)
                        if type(Z[0]) == TreeNode:
                                if not(root.children[Z[1]].has_children()):
                                        print(root.children[Z[1]].att[0])
                                        break
                                else:
                                        root = root.children[Z[1]]
                        else:
                                print(root.children[Z[1]][0])
                                break

def ex_aux(Z,root):
        if '0'<=Z<='9':
                for i in list(root.children):
                        if float(i[0])<=float(Z)<=float(i[1]):
                                return (root.children[i],i)               
        else:
                return (root.children[Z],Z)
                           
main()
