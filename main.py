import foward_checking as fc
import time

"""
variables = [row1, ..., rown, col1, ..., coln, color1, ..., colorn] 
          = [0, ..., n-1, n, ..., 2n-1, 2n, ..., 3n-1]

domains = [{(0, 0), ..., (0, n-1)}, ..., {(n-1, 0), ..., (n-1, n-1)}, # rows
                {(0, 0), ..., (n-1, 0)}, ..., {(0, n-1), ..., (n-1, n-1)} # cols
                {...}, ..., {...}] # colors
"""
def main():
    problem_instances = get_problem_instances()
    for instance in problem_instances:
        # print()
        # print(instance[0])
        start = time.perf_counter()
        solution = fc.start_search(instance[1], instance[2], instance[0])
        end = time.perf_counter()
        print(f"solution = {solution}")
        print(f"{end-start:0.6f}s")
        print()
        print_board(solution, instance[3])
        print()


"""
used in get_problem_instances()... makes it easier to input game board data
"""
def read_colors(colors: str, n: int) -> dict:
    colors_dict = dict()
    colors = colors.split()
    # print(colors)
    for k in range(0, len(colors)):
        temp = colors_dict.get(colors[k], set())
        i = int(k / n)
        j = int(k % n)
        # print(f"colors[{k}]: ({i}, {j})")
        temp.add((i, j))
        colors_dict[colors[k]] = temp
    # print(colors_dict)
    # return list(colors_dict.values())
    return colors_dict


"""
generates instances for level 1 (n=5), level 10 (n=6), and level 14 (n=7)
"""
def get_problem_instances() -> list:
    probs = []
    # LEVEL 1
    n = 5
    variables = [i for i in range(0, 3*n)]
    # print(variables)
    domains = [{(i, j) for j in range(0, n)} for i in range(0, n)] # rows
    domains.extend([{(j, i) for j in range(0, n)} for i in range(0, n)]) # columns
    s = """
    B B V G M
    B B V V M
    Y B V M M
    Y Y Y M M
    Y Y Y Y Y
    """
    colors = read_colors(s, n)
    domains.extend(list(colors.values()))
    # print(domains)
    probs.append((n, variables, domains, colors))
    # LEVEL 10
    n = 6
    variables = [i for i in range(0, 3*n)]
    # print(variables)
    domains = [{(i, j) for j in range(0, n)} for i in range(0, n)] # rows
    domains.extend([{(j, i) for j in range(0, n)} for i in range(0, n)]) # columns
    s = """
    B B V V V V
    B V V G M V
    B V V G M M
    Y Y G G P M
    Y V G P P M
    Y Y Y P P P
    """
    colors = read_colors(s, n)
    domains.extend(list(colors.values()))
    # print(domains)
    probs.append((n, variables, domains, colors))
    # LEVEL 14
    n = 7
    variables = [i for i in range(0, 3*n)]
    # print(variables)
    domains = [{(i, j) for j in range(0, n)} for i in range(0, n)] # rows
    domains.extend([{(j, i) for j in range(0, n)} for i in range(0, n)]) # columns
    s = """
    B B B B V V V
    B B G B M M V
    B Y G P P M G
    B Y G G P M M
    B Y Y G P T T
    B B T T T T T
    T T T T T T T
    """
    colors = read_colors(s, n)
    domains.extend(list(colors.values()))
    # print(domains)
    probs.append((n, variables, domains, colors))
    return probs


"""
prints a board-looking solution, instead of just coordinates
"""
def print_board(solution: set, colors: dict) -> None:
    s = ""
    for i in range(0, len(colors)):
        for j in range(0, len(colors)):
            k = "?"
            for color in colors.keys():
                if (i, j) in colors[color]:
                    k = color
            if (i, j) in solution:
                s = s + f"{k} TREE\t"
            else:
                s = s + f"{k} ....\t"
        s = s + "\n\n"
    s = s.strip()
    print(s)


if __name__ == "__main__":
    main()

