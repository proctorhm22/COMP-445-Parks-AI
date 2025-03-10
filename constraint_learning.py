"""
Author:         Jacob Huber
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Implementation of constraint_learning algorithm to solve Parks problem instances. Code is based on the forward 
checking algorithm and uses a modified implementation of constraint learning.

Additional constraints are "learned" by relating variables in a subtree.

The base is determined o consistent children and a "base" o
"""

import copy
from park import Park

def start_learning_search(park: Park, verbosity=0):
    # set of variables currently assigned
    park.num_nodes_explored = 0
    done = set()
    return learning_forward_checking(park.n, park.num_trees, park.variables, park.domains, done, 
                            learning_pick_next_var(park.n, park.variables, park.domains, done), park, 
                                verbosity, park.learning, learning_pick_next_var(park.n, park.variables, park.domains, done), park.prev_var)

def learning_forward_checking(n: int, num_trees: int, variables: set, domains: list, done: set, next_var: int, park: Park, 
                        verbosity: int, learning: set, base_var: int, prev_var: int):
    # if each domain in domains has size 1 (num_trees): return solution
    all_assigned = True
    for domain in domains:
        # if len(domain) != num_trees:
        if len(domain) != 1:
            all_assigned = False
    if all_assigned:
        # increment num_nodes_explored (algorithm still "explores" the current node)
        park.num_nodes_explored = park.num_nodes_explored + 1
        # # (formatting main output)
        if verbosity > 0:
            print(f"next_var = {next_var}")
            print(f"\ttry {copy.copy(domains[next_var]).pop()}; {park.num_nodes_explored} nodes explored\n")
            # print()
        # return solution
        return [domain.pop() for domain in domains[0:n]]
    # else: assign value to next_var# check if current variables violate a learned constraint
    if len(learning) != 0 and prev_var != None:
        for x in range(len(domains)):
            if(len(domains[x]) == 1):
                if verbosity > 1:
                    print("we are checking if this is in the thing: " + str(((x, copy.copy(domains[x]).pop()), (prev_var, copy.copy(domains[prev_var]).pop()))))
                if ((x, copy.copy(domains[x]).pop()), (prev_var, copy.copy(domains[prev_var]).pop())) in learning:
                    if verbosity > 0:
                        print("I LEARNED SOMETHING")
                    return None
    values_to_try = domains[next_var]
    for value in values_to_try:
        # try it: new_domains[next_var] = {value}
        # increment number of nodes explored 
        park.num_nodes_explored = park.num_nodes_explored + 1
        if verbosity > 0:
            print(f"next_var = {next_var}")
            print(f"\ttry {value}; {park.num_nodes_explored} nodes explored")
        # new_domains = copy of domains
        new_domains = copy.copy(domains)
        # run constraint_propogation() on new_domains to detect inconsistencies before recursion
        new_domains = learning_constraint_propagation(n, num_trees, variables, new_domains, value)
        if verbosity == 2:
            print(f"domains = {domains}")
            print(f"new_domains = {new_domains}")
        # detect inconsistencies...
        noEmptyDomains = True
        for domain in new_domains:
            if len(domain) == 0:
            # if len(domain) < num_trees:
                noEmptyDomains = False
                break
        # if new_domains has no empty domains...
        if noEmptyDomains:
            # new_done = copy of done set
            new_done = copy.copy(done)
            new_done.add(next_var)
            # add variables with size 1 (num_tree) domains to new_done
            for k in variables:
                if len(new_domains[k]) == 1 and new_domains[k] == {value}:
                    new_done.add(k)
            # make recursive call
            result = learning_forward_checking(n, num_trees, variables, new_domains, new_done, 
                                     learning_pick_next_var(n, variables, new_domains, new_done), park,
                                       verbosity, learning, base_var, next_var) 	
            # define start of subtree
            base_var = next_var
            if result is not None:
                return result
    # tried all consistent values and none worked
    if verbosity > 0:
        print(f"backtrack [{next_var}]")
    if verbosity > 1:
        print("this is a learned constraint: " + str(((base_var,copy.copy(domains[base_var]).pop()),(prev_var,copy.copy(domains[prev_var]).pop()))))
        print("this is also a learned constraing: " + str(((prev_var,copy.copy(domains[prev_var]).pop()),(base_var,copy.copy(domains[base_var]).pop()))))
    learning.add(((base_var,copy.copy(domains[base_var]).pop()),(prev_var,copy.copy(domains[prev_var]).pop())))
    learning.add(((prev_var,copy.copy(domains[prev_var]).pop()),(base_var,copy.copy(domains[base_var]).pop())))
    #learning.add(((base_var,(copy.copy(domains[base_var]).pop()[1],copy.copy(domains[base_var]).pop()[0])),(prev_var,(copy.copy(domains[prev_var]).pop()[1],copy.copy(domains[prev_var]).pop()[0]))))
    #learning.add((prev_var,(copy.copy(domains[prev_var]).pop()[1],copy.copy(domains[prev_var]).pop()[0]))),((base_var,(copy.copy(domains[base_var]).pop()[1],copy.copy(domains[base_var]).pop()[0])))
    return None


"""
Strategically picks next variable to try (minimum remaining value).
"""
def learning_pick_next_var(n, variables, domains, done):
    # find first variable that hasn't been assigned
    i = 0
    while variables[i] in done and i < 3*n - 1:
        i = i + 1
    # initialize next_var to this variable / get baseline MRV (min_len)
    next_var = i
    min_len = len(domains[i])
    # loop through remaining variables
    for j in range(i, 3*n):
        # if one of them is also unassigned / has a "better" MRV
        if variables[j] not in done and len(domains[j]) < min_len:
            # update next_var 
            next_var = j
            min_len = len(domains[j])
    # returns variable with "lowest" MRV
    return next_var

"""
Runs constraint propogation on the given set of domains. 
Constraints:    Exactly num_trees trees in each row, column, and color. 
                Trees cannot be placed adjacently (all surrounding cells blocked off).
"""
def learning_constraint_propagation(n, num_trees, variables, domains, value):
    # value = (i, j)
    i = value[0]
    j = value[1]
    for k in variables:
        if (i, j) in domains[k]:
            # place tree
            domains[k] = {(i, j)}
        else:
            # clear rest of row / column
            domains[k] = {coord for coord in domains[k] if coord[0] != i and coord[1] != j}
            # clear surrounding cells
            domains[k] = domains[k] - {(i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)}
    return domains
    