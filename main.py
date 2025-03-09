"""
Authors:        Jacob Huber / Hannah Proctor
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Generates problem instances from Logic Games app and calls algorithm implementations to compare results.

5.	Metrics for evaluation will include:
    a.  Run time
    b.	Number of nodes explored (trees placed)

"""

import foward_checking as fc
import time

class Park():
    def __init__(self, level, n, num_trees, color_str):
        self.level = level
        self.n = n
        self.num_trees = num_trees
        self.variables = [i for i in range(0, 3*n)]
        self.colors = read_colors(color_str, n)
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


def main():
    parks = []
    parks.append(Park(level="LEVEL 1", n=5, num_trees=1, color_str="""
    B B V G M
    B B V V M
    Y B V M M
    Y Y Y M M
    Y Y Y Y Y
    """))
    parks.append(Park(level="LEVEL 10", n=6, num_trees=1, color_str="""
    B B V V V V
    B V V G M V
    B V V G M M
    Y Y G G P M
    Y G G P P M
    Y Y Y P P P
    """))
    parks.append(Park(level="LEVEL 14", n=7, num_trees=1, color_str="""
    B B B B V V V
    B B G B M M V
    B Y G P P M V
    B Y G G P M M
    B Y Y G P T T
    B B T T T T T
    T T T T T T T
    """))
    parks.append(Park(level="LEVEL 16", n=8, num_trees=2, color_str="""
    B V V V V L L L
    B V V L L L L L
    B V V L M L L L
    B B M M M Y Y Y
    B M M M P Y D Y
    B T M P P Y D Y
    T T T P P P D D
    T T D D D D D D
    """))
    parks.append(Park(level="LEVEL 17", n=9, num_trees=2, color_str="""
    B B V V V V V L L
    B M M M V V V L L
    B M Y Y Y L L L L
    B M M M Y P D L L
    T T T M G P D D D
    T M M M G P P P D
    T T T G G P P P D
    T G T G G P P P D
    G G G G G G D D D
    """))
    # level 30 took me an hour to solve... 
    parks.append(Park(level="LEVEL 30", n=10, num_trees=2, color_str="""
    B B B B B V V G G G
    B M Y Y P P V V V G
    B M Y Y P P V V V G
    D M Y Y P P V V V L
    D M D O P P L L L L
    D M D O P P L T T T
    D M D O P P L T T T
    D M D O O O L T T T
    D M D D O O L O O T
    D D D D D O O O T T
    """))
    for park in parks:
        print(f"\n{park.level}\n")
        start = time.perf_counter()
        park.solution, num_nodes_explored = fc.start_search(park)
        end = time.perf_counter()
        print(park.solution)
        print(num_nodes_explored)
        print(f"{end-start:0.6f}s")
        print(f"\n{park}\n")
    print()
           

if __name__ == "__main__":
    main()
