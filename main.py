"""
Authors:        Jacob Huber / Hannah Proctor
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Generates problem instances (from Logic Games app) and calls algorithm implementations to compare results.
"""

import forward_checking as fc
import constraint_learning as cl
import time
from park import Park

def main():
    # generate list of problem instances
    parks: list[Park] = []
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
    # level 30 took me an hour to solve on my own...
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
    parks.append(Park(level="LEVEL 35", n=11, num_trees=2, color_str="""
    B B B B V V V V G G G
    B B B B V V V G G G G
    M M B Y V P V G G G G
    M M M Y P P P G G G G
    M M M Y Y Y Y D D D L
    M M M Y Y D Y D L L L
    M F M F F D D D L D L
    F F F F F D D D D D L
    F F F F F F F F D O L
    F F F W W D D D D O O
    F F W W W D D D D D O
    """))
    parks.append(Park(level="LEVEL 38", n=11, num_trees=2, color_str="""
    B B V V V G G G G G G
    B B V V V V G G G G G
    B B V V V G G G G G G
    B B V M M G G G G G Y
    P M M M M D D D Y Y Y
    P P M M L L F D Y Y Y
    P P P L L L F F F Y Y
    P P L L L L F F F Y Y
    P P L L L L O O O O Y
    L L L L L L O O O O O
    L L L L L L O T T T T
    """))
    parks.append(Park(level="LEVEL 41", n=12, num_trees=2, color_str="""
    B B V V G G G G G G G G
    B B V V G G G G G G G M
    B B V V V Y G G G M M M
    B B V V V Y G G M M M M
    B B V V V Y Y M M M M M
    B P P D D D D D M L M M
    P P P D D D D L L L L L
    P P P P D D D L L L L F
    P P P P O O L L W W W F
    P P P O O O W W W W F F
    P P P P O O W W W W F F
    P P P O O O O T T T F F
    """))
    # loop through problem instances / call algorithm implementations and compare results
    for park in parks:
        print(f"\n{park.level}\n")
        print("Forward checking...\n")
        start = time.perf_counter()
        park.solution = fc.start_search(park, 0)
        end = time.perf_counter()
        # list of tree locations
        print(f"{park.solution}")
        # number of nodes explored
        print(f"{park.num_nodes_explored} nodes explored")
        # run time
        print(f"{(end-start)*1000:f}ms")
        print("\nForward checking with constraint learning...\n")
        start = time.perf_counter()
        park.solution = cl.start_learning_search(park, 0)
        end = time.perf_counter()
        # list of tree locations
        print(f"{park.solution}")
        # number of nodes explored
        print(f"{park.num_nodes_explored} nodes explored")
        # run time
        print(f"{(end-start)*1000:f}ms")
        # print(f"\n{park}\n")
    print()
           

if __name__ == "__main__":
    main()
