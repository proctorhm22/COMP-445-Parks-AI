"""
Author:         Jacob Huber / Hannah Proctor
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Implementation of Park class to represent problem instances.

Variables: {
            0, ..., n-1,        // rows [0, n)
            n, ..., 2*n-1,      // columns [n, 2*n)
            2*n, ..., 3*n-1     // colors [2*n, 3*n)
        } 

Domains: {
            {(0,0), (0,1), ..., (0,n-1)}, ..., {(n-1,0), (n-1,1), ..., (n-1,n-1)},  // rows
            {(0,0), (1,0), ..., (n-1,0)}, ..., {(0,n-1), (1,n-1), ..., (n-1,n-1)},  // columns
            {(i,j) | (i,j) is blue}, ..., {(i,j) | (i,j) is gray}                   // colors
        }

**Constraints are hard-coded into algorithm implementations, and are not included in class instances. That said,

Constraints:    Exactly num_trees trees in each row, column, and color. 
                Trees cannot be placed adjacently (all surrounding cells blocked off).

"""

class Park():
    def __init__(self, level, n, num_trees, color_str):
        # set level (from the Logic Games app), e.g. "LEVEL 1"
        self.level = level
        # set size of board 
        self.n = n
        # set number of trees (varies 1-2)
        self.num_trees = num_trees
        # get color_dict from color_str
        self.colors = read_colors(color_str, n)
        # see variable assignment above
        self.variables = [i for i in range(0, 3*n)]
        # see domain assignment above
        self.domains = [{(i, j) for j in range(0, n)} for i in range(0, n)] # rows
        self.domains.extend([{(i, j) for i in range(0, n)} for j in range(0, n)]) # columns
        self.domains.extend(list(self.colors.values())) # colors
        # solution defaults to None
        self.solution = None
        # num_nodes_explored defaults to zero
        self.num_nodes_explored = 0
        # create a set of learned constraints
        self.learning = set()
        # determine the first var of a subset to add to learned constraints
        self.base_var = None
        # determine the second var of a subset to add to learnd constraints
        self.prev_var = None
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