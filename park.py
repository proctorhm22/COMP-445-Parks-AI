"""
Author:         Hannah Proctor
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Implementation of Park class to represent problem instances.
"""

class Park():
    def __init__(self, level, n, num_trees, color_str):
        self.level = level
        self.n = n
        self.num_trees = num_trees
        self.colors = read_colors(color_str, n)
        self.variables = [i for i in range(0, 3*n)]
        self.domains = [{(i, j) for j in range(0, n)} for i in range(0, n)] # rows
        self.domains.extend([{(i, j) for i in range(0, n)} for j in range(0, n)]) # columns
        self.domains.extend(list(self.colors.values())) # colors
        self.solution = None
        self.num_nodes_explored = 0
    def __str__(self):
        s = ""
        for i in range(0, self.n):
            for j in range(0, self.n):
                k = "?"
                for color in self.colors.keys():
                    if (i, j) in self.colors[color]:
                        k = color
                if self.solution != None and (i, j) in self.solution:
                    s = s + f"{k} TREE\t"
                else:
                    s = s + f"{k} ....\t"
            s = s + "\n\n"
        s = s.strip()
        return s
    

"""
Given color_str of the form:
    B B V G M
    B B V V M
    Y B V M M
    Y Y Y M M
    Y Y Y Y Y
Return color_dict of the form:
    {"B":{(i, j) | (i, j) is blue}, "V":{(i, j) | (i, j) is green}, ... "G":{(i, j) | (i, j) is gray}}
"""
def read_colors(colors_str: str, n: int) -> dict[str, set]:
    colors_dict = dict()
    # split color_str into color_list: ["B", "B", "V", "G", "M", "B", "B", "V", "V", "M", ..., "Y"]
    colors_list = colors_str.split()
    # iterate over color_list to build dictionary
    for k in range(0, len(colors_list)):
        temp = colors_dict.get(colors_list[k], set())
        i = int(k / n)
        j = int(k % n)
        temp.add((i, j))
        colors_dict[colors_list[k]] = temp
    return colors_dict