"""
Author:         Hannah Proctor
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Implementation of a foward-checking algorithm to solve Parks problem instances (1-2 trees).

Input:  variables = {x1, x2, ..., xn}
        domains = {d1, d2, ..., dn}
        n = board.size
        done = {...}
        0 <= next_var <= 3n-1

Output: solution = {{()}, ..., {()}}
        None if no solution is found

"""

import copy
from main import Park

def start_search(park: Park):
    done = set()
    num_nodes_explored = 0
    return foward_checking(park.n, park.num_trees, park.variables, park.domains, done, 
                           pick_next_var(park.n, park.variables, park.domains, done), num_nodes_explored)


"""
0 <= next_var <= 3n-1
choose next_var based on shortest domain
"""
def foward_checking(n, num_trees, variables, domains, done, next_var, num_nodes_explored):
    # if len(done) == len(variables): return domains
    if len(done) == 3*n:
        return [domain.pop() for domain in domains[0:n]], num_nodes_explored
    # else: run through values in domains[next_var]
    # print(f"next_var = {next_var}")
    values_to_try = domains[next_var]
    # print(f"values_to_try = {values_to_try}")
    for value in values_to_try:
        num_nodes_explored = num_nodes_explored + 1
        # print(f"value = {value}")
        new_domains = copy.copy(domains)
        # new_domains[next_var] = {value}
        # print(f"domains = {domains}")
        new_domains = constraint_propogation(n, num_trees, variables, new_domains, value)
        # print(f"new_domains = {new_domains}")
        # if new_domains has no empty domains: ...
        noEmptyDomains = True
        for domain in new_domains:
            if len(domain) == 0:
            # if len(domain) < num_trees:
                noEmptyDomains = False
                break
        if noEmptyDomains:
            # print(f"done = {done}")
            new_done = copy.copy(done)
            new_done.add(next_var)
            # print(f"new_done = {done}")
            result = foward_checking(n, num_trees, variables, new_domains, new_done, 
                                     pick_next_var(n, variables, new_domains, new_done), num_nodes_explored) 	
            if result is not None:
                return result
    # tried all consistent values and none worked
    return None


"""
strategically pick the next variable to try (minimum remaining values)
len(variables) = len(domains) = 3*n
"""
def pick_next_var(n, variables, domains, done):
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
value = (i, j)
0 <= next_var <= 3n-1
"""
def constraint_propogation(n, num_trees, variables, domains, value):
    i = value[0]
    j = value[1]
    for k in range(0, 3*n):
        if value in domains[k]:
            domains[k] = {value}
        else:
            domains[k] = {coord for coord in domains[k] if coord[0] != i and coord[1] != j}
            domains[k] = domains[k] - {(i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)}
    return domains
    