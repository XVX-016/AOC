from collections import defaultdict
import sys
sys.setrecursionlimit(10**7)

def parse_input(filename="input.txt"):
    graph = defaultdict(list)
    with open(filename) as f:
        for line in f:
            if ":" not in line:
                continue
            src, rest = line.split(":")
            dests = rest.strip().split()
            graph[src.strip()] = dests
    return graph


memo = {}

def count_paths(node, graph):
    if node == "out":
        return 1
    if node in memo:
        return memo[node]

    total = 0
    for nxt in graph[node]:
        total += count_paths(nxt, graph)

    memo[node] = total
    return total


def main():
    graph = parse_input("input.txt")
    ans = count_paths("you", graph)
    print(ans)


if __name__ == "__main__":
    main()
