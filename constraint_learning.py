"""
Author:         Jacob Huber
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Implementation of foward-checking algorithm to solve Parks problem instances with 1-2 trees**. Code is based on
the forward checking algorithm and uses a modified implementation of constraint learning.

Additional constraints are "learned" by relating variables in a subset.
The base is determined o consistent children and a "base" o

**Currently, all 2-tree problems are solved as if they are 1-tree problems. 
"""

# TODO: get 2-tree implementation working

# TODO: adjust comments in learning_forward_checking() to better align with pseudocode

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
    # if len(done) == len(variables): return domains
    #print("learned set: " + str(learning))
    if len(done) == 3*n:
        if verbosity > 0:
            print()
        return [domain.pop() for domain in domains[0:n]], park.num_nodes_explored
    # check if current variables violate a learned constraint
    if len(learning) != 0 and prev_var != None:
        for x in range(len(domains)):
            if(len(domains[x]) == 1):
                if verbosity > 1:
                    print("we are checking if this is in the thing: " + str(((x, copy.copy(domains[x]).pop()), (prev_var, copy.copy(domains[prev_var]).pop()))))
                if ((x, copy.copy(domains[x]).pop()), (prev_var, copy.copy(domains[prev_var]).pop())) in learning:
                    if verbosity > 0:
                        print("I LEARNED SOMETHING")
                    return None
        #print("done checking for now")
    # else: iterate through values in domains[next_var]
    values_to_try = domains[next_var]
    for value in values_to_try:
        # try it
        # new_domains[next_var] = {value}
        park.num_nodes_explored = park.num_nodes_explored + 1
        if verbosity > 0:
            print(f"next_var = {next_var}")
            print(f"\ttry {value}; {park.num_nodes_explored} nodes explored")
        new_domains = copy.copy(domains)
        new_domains = learning_constraint_propagation(n, num_trees, variables, new_domains, value)
        if verbosity == 2:
            print(f"domains = {domains}")
            print(f"new_domains = {new_domains}")
        # if new_domains has no empty domains: ...
        noEmptyDomains = True
        for domain in new_domains:
            if len(domain) == 0:
            # if len(domain) < num_trees:
                noEmptyDomains = False
                break
        if noEmptyDomains:
            new_done = copy.copy(done)
            new_done.add(next_var)
            result = learning_forward_checking(n, num_trees, variables, new_domains, new_done, 
                                     learning_pick_next_var(n, variables, new_domains, new_done), park,
                                       verbosity, learning, base_var, next_var) 	
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
    i = 0
    while variables[i] in done and i < 3*n - 1:
        i = i + 1
    next_var = i
    min_len = len(domains[i])
    for j in range(i, 3*n):
        if variables[j] not in done and len(domains[j]) < min_len:
            next_var = j
            min_len = len(domains[j])
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
    for k in range(0, 3*n):
        if value in domains[k]:
            domains[k] = {value}
        else:
            domains[k] = {coord for coord in domains[k] if coord[0] != i and coord[1] != j}
            domains[k] = domains[k] - {(i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)}
    return domains
    