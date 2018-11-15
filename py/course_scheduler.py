#!/usr/bin/env python
"""
coding=utf-8

Python 3.5.2

Schedule courses taking into account prerequisites
Closely follows this problem setup: https://leetcode.com/problems/course-schedule-ii/description/

"""

# Imports
import json
import sys

def err_print(*args, **kwargs):
	"""
	Method to print to stderr
	
	:return: None
	:rtype: None
	"""
	print(*args, file=sys.stderr, **kwargs)

def schedule(graph):
	"""
	Method to perform topological sorting of the input graph (in adjacency list format) to find a valid schedule
	Complexity: O(V+E) time and O(V+E) space
	
	:return: The correct order of courses to be taken or null list if no valid order found
	:rtype: List[int]
	"""
	numCourses = len(graph) # number of courses
	indegree = [[] for _ in range(numCourses)]  # indegree
	outdegree = [0] * numCourses  # outdegree

	# Calculate the indegree and outdegree of each vertex
	for i in range(numCourses):
		outdegree[i] = len(graph[i])
		if len(graph[i])>0:
			for prereq in graph[i]:
				indegree[prereq].append(i)
	
	order = []
	# First we can take the courses with no prerequisites
	for i in range(numCourses):
		if outdegree[i]==0:
			order.append(i)
	
	ctr = 0
	# Perform Topo Sort to get the order of the rest of the courses
	while ctr!=len(order):
		v = order[ctr]
		ctr += 1
		for u in indegree[v]:
			outdegree[u] -= 1
			if outdegree[u] == 0:
				order.append(u)
	
	return order if ctr == numCourses else []

def generate_graph(data, course_to_id):
	"""
	Method to read the JSON and build the directed graph of courses (= DAG of course IDs)
	The graph is represented in an adjacency list format
	
	:return: A graph in adjacency list format, with vertices as course IDs and directed edges implying prerequisite relation
	:rtype: List[List[int]]
	"""
	graph = [] * len(course_to_id)
	ctr = 0
	for obj in data:
		graph.append([])
		for prereq in obj["prerequisites"]:
			graph[ctr].append(course_to_id[prereq.strip()])
		ctr += 1
	return graph

def map_course_to_id(data):
	"""
	Method to parse the JSON text and map the course names to a numeric ID
	Also checks for validity of prerequisites by checking if any course which has not been
	declared has been mentioned in a prerequisite list (raise an error in such a case)
	
	:return: A lookup table mapping course names to a numeric ID
	:rtype: Dict(str, int)
	"""
	course_to_id = {}
	ctr = 0
	# Map the course names to a numeric ID
	for obj in data:
		course_to_id[obj["name"].strip()] = ctr
		ctr += 1
	for obj in data:
		for prereq in obj["prerequisites"]:
			if prereq.strip() not in course_to_id:
				# Unknown, undeclared course encountered in prerequisites
				err_print("Error: Prerequisites requirement (if any) of course "+prereq.strip()+" is not mentioned")
				sys.exit(0)
	return course_to_id

def validate_json(data):
	"""
	Method to validate the JSON input

	This method reads and prints any error it might find in the JSON object
	If error is found, program exits
	
	:return: None
	:rtype: None
	"""
	if len(data)==0:
		err_print("Error: No data present")
		sys.exit(0)
	ctr = -1
	d = {}
	for obj in data:
		ctr += 1
		
		# Check for presence of 'name' and 'prerequisites' keys
		if "name" not in obj and "prerequisites" not in obj:
			err_print("Error: \'name\' and \'prerequisites\' keys not found in JSON object "+str(ctr))
			sys.exit(0)
		if "name" not in obj:
			err_print("Error: \'name\' key not found in JSON object "+str(ctr))
			sys.exit(0)
		if "prerequisites" not in obj:
			err_print("Error: \'prerequisites\' key not found in JSON object "+str(ctr))
			sys.exit(0)

		# Check for self-prerequisites and conflicting prerequisites inputs
		if obj["name"] not in d:
			if obj["name"] not in obj["prerequisites"]:
				d[obj["name"]] = obj["prerequisites"]
			else:
				err_print("Error: The course "+obj["name"]+" cannot be a prerequisite to itself")
				sys.exit(0)
		elif obj["name"] in d and set(d[obj["name"]])!=set(obj["prerequisites"]):
			err_print("Error: Conflicting prerequisites input for "+obj["name"])
			sys.exit(0)

def main():
	"""
	Main method

	This method reads and cleans the input JSON by calling methods, and finally calls the scheduler algorithm
	Algorithm output is printed to stdout
	Sample input file: data/course_scheduler_input1.json

	:return: None
	:rtype: None
	"""

	# Check validity of number of arguments
	if len(sys.argv)<2:
		err_print("Error: No arguments provided")
		sys.exit(0)

	# Take the first and only argument as the input file
	input_file = sys.argv[1] 

	# Attempt to read the file
	with open(input_file) as f:
		try:
			data = json.load(f)
		except ValueError:
			# Print issue with malformed JSON input
			err_print("Error: Issue with input file")
			sys.exit(0)

	# Validate input JSON file & delete duplicate objects
	validate_json(data)
	data = {d['name'] : d for d in data}.values()
	
	# Parse the text data into a more suitable numeric format
	course_to_id = map_course_to_id(data) # Mapping courses to IDs
	id_to_course = {v: k for k, v in course_to_id.items()} # Mapping the IDs to courses
	
	# Generate the graph of prerequisites and courses
	graph = generate_graph(data, course_to_id)
	
	# Run the scheduler algorithm
	answer = schedule(graph)
	
	if len(answer)>0:
		# Valid order exists
		print("Order: ", end='')
		for course in answer[:-1]:
			print(id_to_course[course], end=' -> ')
		print(id_to_course[answer[-1]])
	else:
		# No valid order exists
		err_print("Error: No valid schedule found")


if __name__ == '__main__':
	main()