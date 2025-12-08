import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from collections import defaultdict

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
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
        return True

def distance_sq(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2

def visualize_components(points, uf, title="Components"):
    """Visualize 3D points colored by their connected component"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    components = {}
    for i in range(len(points)):
        root = uf.find(i)
        components.setdefault(root, []).append(i)
    
    colors = plt.cm.tab20(np.linspace(0, 1, min(20, len(components))))
    
    for idx, (root, point_indices) in enumerate(components.items()):
        color = colors[idx % len(colors)]
        comp_points = [points[i] for i in point_indices]
        if comp_points:
            xs, ys, zs = zip(*comp_points)
            ax.scatter(xs, ys, zs, color=color, s=30, alpha=0.7, 
                      label=f'Size: {len(point_indices)}', 
                      depthshade=True)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'{title}\nTotal components: {len(components)}')
    
    if len(components) <= 10:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()
    
    return components

def solve_with_visualization():
    with open('solutions\Day 08\input.txt', 'r') as f:
        points = [tuple(map(int, line.strip().split(','))) for line in f]
    
    n = len(points)
    print(f"Number of points: {n}")
    
    print(f"Generating {n*(n-1)//2} pairs...")
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = distance_sq(points[i], points[j])
            pairs.append((dist_sq, i, j))
    
    print("Sorting pairs...")
    pairs.sort(key=lambda x: x[0])
    
    uf = UnionFind(n)
    
    print("\n=== INITIAL STATE ===")
    initial_components = visualize_components(points, uf, "Initial State - All Points Separate")
    print(f"Initial components: {len(initial_components)}")
    
    print("\n=== PROCESSING 1000 CLOSEST PAIRS ===")
    successful_unions = 0
    
    for idx in range(1000):
        if idx >= len(pairs):
            break
            
        dist_sq, i, j = pairs[idx]
        if uf.union(i, j):
            successful_unions += 1
        
        if (idx + 1) % 200 == 0 or idx == 999:
            current_components = len(set(uf.find(x) for x in range(n)))
            print(f"  Processed {idx + 1} pairs, {successful_unions} successful unions, {current_components} components remaining")
    
    print(f"\nTotal successful unions: {successful_unions}")
    
    print("\n=== FINAL STATE ===")
    final_components = visualize_components(points, uf, f"Final State - After 1000 Closest Pairs")
    
    comp_sizes = defaultdict(int)
    for i in range(n):
        root = uf.find(i)
        comp_sizes[root] = uf.size[root]
    
    sizes = sorted(comp_sizes.values(), reverse=True)
    
    print(f"\n=== RESULTS ===")
    print(f"Total components: {len(sizes)}")
    print(f"All component sizes: {sizes}")
    print(f"Top 10 component sizes: {sizes[:10]}")
    
    if len(sizes) >= 3:
        result = sizes[0] * sizes[1] * sizes[2]
        print(f"\nTop 3 component sizes: {sizes[0]}, {sizes[1]}, {sizes[2]}")
        print(f"Product: {sizes[0]} × {sizes[1]} × {sizes[2]} = {result}")
        return result
    else:
        print(f"\nWarning: Only {len(sizes)} components")
        if len(sizes) == 2:
            result = sizes[0] * sizes[1] * 0
            print(f"Product of top 3 (with 0 for third): {result}")
            return result
        elif len(sizes) == 1:
            result = sizes[0] * 0 * 0
            print(f"Product of top 3 (with 0 for second and third): {result}")
            return result
        else:
            return 0

if __name__ == "__main__":
    print("Advent of Code 2024 - Day 8: Playground")
    print("=" * 50)
    result = solve_with_visualization()
    print(f"\n{'='*50}")
    print(f"FINAL ANSWER: {result}")
    print(f"{'='*50}")