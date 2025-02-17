"""
Author:         Hannah Proctor
Class:          COMP 445
Assignment:     Research Project
Date:           February 12, 2025

Implementation of foward-checking algorithm to solve the Parks problem.
"""

import copy

"""
Input:  variables = {x1, x2, ..., xn}
        domains = {d1, d2, ..., dn}
        n = board.size
        done = {...}
        0 <= next_var <= 3n-1
Output: solution = {{()}, ..., {()}}
        None if no solution is found
constraints handled in constraint_propogation()
"""
def start_search(variables, domains, n):
    # choose initial next_var based on shortest domain...
    done = set()
    return foward_checking(variables, domains, n, done, pick_next_var(variables, domains, n, done))


"""
0 <= next_var <= 3n-1
choose next_var based on shortest domain...
"""
def foward_checking(variables, domains, n, done, next_var):
    # if each domain in domains has size 1 (num_trees): return domains
    # allAssigned = True
    # for domain in domains:
    #     if len(domain) > 1:
    #         allAssigned = False
    #         break
    # if allAssigned:
    #     return [set.pop() for set in domains[0:n]]
    if len(done) == 3*n:
        return [set.pop() for set in domains[0:n]]
    # print(f"next_var = {next_var}")
    # else run through values in domains[next_var]
    values_to_try = domains[next_var]
    # print(f"values_to_try = {values_to_try}")
    for value in values_to_try:
        # print(f"value = {value}")
        new_domains = copy.copy(domains)
        # new_domains[next_var] = {value}
        # print(f"domains = {domains}")
        new_domains = constraint_propogation(variables, new_domains, n, value)
        # print(f"new_domains = {new_domains}")
        # if new_domains has no empty domains: ...
        hasEmptyDomain = False
        for domain in new_domains:
            if len(domain) == 0:
                hasEmptyDomain = True
                break
                # return None
        if hasEmptyDomain:
            pass
        if not hasEmptyDomain:
            # print("NO EMPTY DOMAINS")
            # print(f"done = {done}")
            new_done = copy.copy(done)
            new_done.add(next_var)
            # print(f"new_done = {done}")
            result = foward_checking(variables, new_domains, n, new_done, pick_next_var(variables, new_domains, n, new_done)) 	
            if result is not None:
                return result
    # tried all consistent values and none worked
    return None


"""
strategically pick the next variable to try (minimum remaining values)
len(variables) = len(domains) = 3*n
"""
def pick_next_var(variables, domains, n, done):
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
def constraint_propogation(variables, domains, n, value):
    # domains = new_domains
    i = value[0]
    j = value[1]
    # 0.000233s...
    # clear rest of row
    domains[i] = {value}
    for k in range(0, n):
        domains[k] = {coord for coord in domains[k] if coord[1] != j or coord == value}
    # clear rest of column
    domains[n+j] = {value}
    for k in range(n, 2*n):
        domains[k] = {coord for coord in domains[k] if coord[0] != i or coord == value}
    # clear rest of surrounding trees
    if i >= 1:
        domains[i - 1] = {k for k in domains[i - 1] if k != (i-1, j-1) and k != (i-1, j+1)}
    if i < n-1:
        domains[i + 1] = {k for k in domains[i + 1] if k != (i+1, j-1) and k != (i+1, j+1)}
    # clear rest of color
    for k in range(2*n, 3*n):
        if (i, j) in domains[k]:
            domains[k] = {(i, j)}
            break
        else:
            domains[k] = {coord for coord in domains[k] if coord not in {(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)}}
    # 0.000664s
    # for k in range(0, 3*n):
    #     if (i, j) in domains[k]:
    #         domains[k] = {(i, j)}
    #         # break
    #     else:
    #         domains[k] = {coord for coord in domains[k] if coord not in {(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)}}
    return domains
    