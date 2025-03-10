"""
Authors:        Jacob Huber / Hannah Proctor
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Generates problem instances (from Logic Games app) and calls algorithm implementations to compare results.
"""

import foward_checking as fc
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
        print("Foward checking...\n")
        start = time.perf_counter()
        park.solution = fc.start_search(park, 1)
        end = time.perf_counter()
        # list of tree locations
        print(f"{park.solution}")
        # number of nodes explored
        print(f"{park.num_nodes_explored} nodes explored")
        # run time
        print(f"{end-start:0.6f}s")
        print("\nFoward checking with constraint learning...")
        # list of tree locations
        # ...
        # number of nodes explored
        # ...
        # run time
        # ...
        print(f"\n{park}\n")
    print()
           

if __name__ == "__main__":
    main()
