
"""
Count paths from 'svr' -> 'out' that visit BOTH 'dac' and 'fft'.
Uses bottom-up DP on DAG with a 2-bit mask (dac_seen, fft_seen).
Also optionally enumerates up to ENUM_LIMIT example paths that satisfy the constraint.
"""

from collections import defaultdict, deque
import sys

INPUT_FILE = "input.txt"
START = "svr"
END = "out"
NODE_A = "dac"
NODE_B = "fft"

# safety: don't print a huge number of example paths
ENUM_LIMIT = 2000  

def parse_input(filename=INPUT_FILE):
    g = defaultdict(list)
    nodes = set()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            src, rest = line.split(":", 1)
            src = src.strip()
            dests = rest.strip().split()
            for d in dests:
                if d:
                    g[src].append(d)
                    nodes.add(d)
            nodes.add(src)
    # ensure nodes with no outgoing edges still present in dict
    for n in list(nodes):
        g.setdefault(n, [])
    return g

def topo_sort_kahn(graph):
    indeg = {n:0 for n in graph}
    for u in graph:
        for v in graph[u]:
            indeg[v] = indeg.get(v,0) + 1
    q = deque([n for n,d in indeg.items() if d==0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v]==0:
                q.append(v)
    if len(order) != len(graph):
        return None  # cycle detected
    return order

def build_index(graph):
    names = list(graph.keys())
    name_to_idx = {n:i for i,n in enumerate(names)}
    idx_to_name = names
    n = len(names)
    adj = [[] for _ in range(n)]
    for u in graph:
        ui = name_to_idx[u]
        for v in graph[u]:
            adj[ui].append(name_to_idx[v])
    return name_to_idx, idx_to_name, adj

def dp_count_paths(adj, idx_to_name, name_to_idx, start_name=START, end_name=END, a=NODE_A, b=NODE_B):
    n = len(adj)
    A_idx = name_to_idx.get(a, None)
    B_idx = name_to_idx.get(b, None)
    start_idx = name_to_idx.get(start_name, None)
    end_idx = name_to_idx.get(end_name, None)
    if start_idx is None or end_idx is None:
        raise ValueError("start or end not present in graph")
    indeg = [0]*n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    q = deque([i for i,d in enumerate(indeg) if d==0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v]==0:
                q.append(v)
    if len(topo) != n:
        raise RuntimeError("graph has cycle (not a DAG); algorithm expects DAG")
    dp = [[0]*4 for _ in range(n)]
    for node in range(n):
        mask_node = 0
        if node == A_idx:
            mask_node |= 1
        if node == B_idx:
            mask_node |= 2
        if node == end_idx:
            dp[node][mask_node] = 1
    for u in reversed(topo):
        if u == end_idx:
            continue
        mask_u = 0
        if u == A_idx:
            mask_u |= 1
        if u == B_idx:
            mask_u |= 2
        for v in adj[u]:
            for child_mask in range(4):
                cnt = dp[v][child_mask]
                if cnt == 0:
                    continue
                new_mask = mask_u | child_mask
                dp[u][new_mask] += cnt

    total_paths = sum(dp[start_idx]) 
    mask_both = 1 | 2
    paths_with_both = dp[start_idx][mask_both]
    return {
        "total_paths": total_paths,
        "paths_with_both": paths_with_both,
        "dp": dp,
        "indices": {"start": start_idx, "end": end_idx, "A": A_idx, "B": B_idx},
    }

def enumerate_paths_with_constraint(adj, idx_to_name, start_idx, end_idx, need_set, limit=1000):
    found = []
    stack = [(start_idx, [start_idx])]
    while stack and len(found) < limit:
        node, path = stack.pop()
        if node == end_idx:
            names = {idx_to_name[i] for i in path}
            if need_set.issubset(names):
                found.append([idx_to_name[i] for i in path])
            continue
        for v in reversed(adj[node]):
            stack.append((v, path + [v]))
    return found

def main():
    graph = parse_input(INPUT_FILE)
    topo = topo_sort_kahn(graph)
    if topo is None:
        print("Warning: input graph contains a cycle; the algorithm expects a DAG. Exiting.")
        sys.exit(1)

    name_to_idx, idx_to_name, adj = build_index(graph)
    res = dp_count_paths(adj, idx_to_name, name_to_idx, START, END, NODE_A, NODE_B)
    print("Total paths ({} -> {}): {}".format(START, END, res["total_paths"]))
    print("Paths that visit BOTH '{}' and '{}': {}".format(NODE_A, NODE_B, res["paths_with_both"]))

    if ENUM_LIMIT > 0:
        need_set = {NODE_A, NODE_B}
        start_idx = name_to_idx.get(START)
        end_idx = name_to_idx.get(END)
        if start_idx is not None and end_idx is not None:
            print("\nEnumerating up to {} example paths that visit both:".format(ENUM_LIMIT))
            examples = enumerate_paths_with_constraint(adj, idx_to_name, start_idx, end_idx, need_set, limit=ENUM_LIMIT)
            for p in examples:
                print(",".join(p))
            if len(examples) == 0:
                print("(none found within enumeration limit)")
        else:
            print("(Cannot enumerate: start or end missing)")

if __name__ == "__main__":
    main()
