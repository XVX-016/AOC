import math
from collections import defaultdict
import time

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

def distance_sq(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2

def solve_part2():
    try:
        with open('solutions\Day 08\input.txt', 'r') as f:
            points = [tuple(map(int, line.strip().split(','))) for line in f]
    except FileNotFoundError:
        with open('solutions/Day 08/input.txt', 'r') as f:
            points = [tuple(map(int, line.strip().split(','))) for line in f]
    
    n = len(points)
    print(f"Number of points: {n}")
    
    start_time = time.time()
    
    edges = []
    print("Generating edges...")
    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = distance_sq(points[i], points[j])
            edges.append((dist_sq, i, j))
    
    print(f"Generated {len(edges)} edges in {time.time() - start_time:.2f} seconds")
    
    start_time = time.time()
    print("Sorting edges...")
    edges.sort(key=lambda x: x[0])
    print(f"Sorted edges in {time.time() - start_time:.2f} seconds")
    
    uf = UnionFind(n)
    last_edge = None
    
    print(f"\nStarting with {uf.components} components")
    print("Processing edges until single component...")
    
    start_time = time.time()
    edges_processed = 0
    unions_made = 0
    
    for edge_idx, (dist_sq, i, j) in enumerate(edges):
        edges_processed += 1
        
        if uf.union(i, j):
            unions_made += 1
            
            if uf.components == 1:
                last_edge = (i, j)
                print(f"\n✓ REACHED SINGLE COMPONENT at edge #{edge_idx + 1}")
                print(f"  Total edges processed: {edge_idx + 1}")
                print(f"  Total unions made: {unions_made}")
                print(f"  Time elapsed: {time.time() - start_time:.2f} seconds")
                break
            
            if unions_made % 100 == 0 and uf.components <= 100:
                print(f"  Unions: {unions_made}, Components: {uf.components}")
        
        if edge_idx % 100000 == 0 and edge_idx > 0:
            print(f"  Processed {edge_idx + 1} edges, {uf.components} components remain")
    
    if last_edge:
        i, j = last_edge
        result = points[i][0] * points[j][0]
        print(f"\nLAST CONNECTING PAIR:")
        print(f"  Point {i}: {points[i]}")
        print(f"  Point {j}: {points[j]}")
        print(f"  X coordinates: {points[i][0]} and {points[j][0]}")
        print(f"  Product of X coordinates: {points[i][0]} × {points[j][0]} = {result}")
        
        print(f"\nSTATISTICS:")
        print(f"  Total edges in list: {len(edges)}")
        print(f"  Edges processed: {edges_processed}")
        print(f"  Successful unions: {unions_made}")
        print(f"  Total time: {time.time() - start_time:.2f} seconds")
        
        return result
    else:
        print(f"\nERROR: Never reached a single component!")
        print(f"  Final component count: {uf.components}")
        return 0

if __name__ == "__main__":
    print("Advent of Code 2024 - Day 8 Part 2")
    print("=" * 60)
    result = solve_part2()
    print(f"\n{'='*60}")
    print(f"FINAL ANSWER: {result}")
    print(f"{'='*60}")