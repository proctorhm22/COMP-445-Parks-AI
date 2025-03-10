"""
Author:         Hannah Proctor
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Implementation of forward-checking algorithm to solve Parks problem instances (1-2 trees).** Pseudocode inspiration 
taken from class slides.
"""

# TODO: get 2-tree implementation working

import copy
from park import Park

def start_search(park: Park, verbosity=0):
    # set of variables currently assigned
    done = set()
    park.num_nodes_explored = 0
    return forward_checking(park.n, park.num_trees, park.variables, park.domains, done, 
                            pick_next_var(park.n, park.variables, park.domains, done), park, 
                                verbosity)

def forward_checking(n: int, num_trees: int, variables: set, domains: list, done: set, next_var: int, park: Park, 
                        verbosity: int):
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
    # else: assign value to next_var 
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
        new_domains = constraint_propogation(num_trees, variables, new_domains, value)
        if verbosity == 2:
            print(f"\tdomains = {domains}")
            print(f"\tnew_domains = {new_domains}")
        # detect inconsistencies...
        no_empty_domains = True
        for domain in new_domains:
            if len(domain) == 0:
            # if len(domain) < num_trees:
                no_empty_domains = False
                break
        # if new_domains has no empty domains...
        if no_empty_domains:
            # new_done = copy of done set
            new_done = copy.copy(done)
            new_done.add(next_var)
            # add variables with size 1 (num_tree) domains to new_done
            for k in variables:
                if len(new_domains[k]) == 1 and new_domains[k] == {value}:
                    new_done.add(k)
            # make recursive call
            result = forward_checking(n, num_trees, variables, new_domains, new_done, 
                                     pick_next_var(n, variables, new_domains, new_done), park,
                                       verbosity) 	
            if result is not None:
                return result
    # tried all consistent values and none worked
    if verbosity > 0:
        print(f"backtrack [{next_var}]")
    return None


"""
Strategically picks next variable to try (minimum remaining value).
"""
def pick_next_var(n, variables, domains, done):
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
Runs constraint propogation on domains. Essentally, "placing a tree" at (i, j). 
Constraints:    Exactly num_trees trees in each row, column, and color. 
                Trees cannot be placed adjacently (all surrounding cells blocked off).
"""
def constraint_propogation(num_trees, variables, domains, value):
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
    