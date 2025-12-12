import sys
import time

def read_input(filename):
    with open(filename, 'r') as f:
        content = f.read()
    parts = content.strip().split('\n\n')
    
    shapes = []
    for part in parts:
        lines = part.strip().split('\n')
        if not lines:
            continue
        
        if lines[0].strip().endswith(':') and not 'x' in lines[0]:
            shape_lines = lines[1:]
            coords = []
            for r, row in enumerate(shape_lines):
                for c, ch in enumerate(row):
                    if ch == '#':
                        coords.append((r, c))
            
            if coords:
                min_r = min(r for r, _ in coords)
                min_c = min(c for _, c in coords)
                normalized = [(r - min_r, c - min_c) for r, c in coords]
                shapes.append(normalized)
    regions = []
    for line in content.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if 'x' in line and ':' in line:
            dim_part, quant_part = line.split(':')
            try:
                w, h = map(int, dim_part.strip().split('x'))
                quantities = list(map(int, quant_part.strip().split()))
                regions.append((w, h, quantities))
            except:
                continue
    
    return shapes, regions

def get_all_orientations(shape):
    orientations = set()
    
    def normalize(coords):
        min_r = min(r for r, _ in coords)
        min_c = min(c for _, c in coords)
        return tuple(sorted((r - min_r, c - min_c) for r, c in coords))
    
    current = shape
    for _ in range(4):
        orientations.add(normalize(current))
        reflected = [(-r, c) for r, c in current]
        orientations.add(normalize(reflected))
        current = [(c, -r) for r, c in current]
    
    return [list(orient) for orient in orientations]

def solve_region(w, h, quantities, all_orientations):
    total_cells_needed = 0
    for shape_idx, count in enumerate(quantities):
        if count > 0:
            cells_in_shape = len(all_orientations[shape_idx][0])
            total_cells_needed += count * cells_in_shape
    
    if total_cells_needed > w * h:
        return False
    shapes_to_place = []
    for shape_idx, count in enumerate(quantities):
        for _ in range(count):
            shapes_to_place.append(shape_idx)
    
    if not shapes_to_place:
        return True
    shapes_to_place.sort(key=lambda x: len(all_orientations[x][0]), reverse=True)
    grid = 0  
    total_cells = w * h
    
    @lru_cache(maxsize=None)
    def dfs(idx, grid_mask):
        if idx == len(shapes_to_place):
            return True
        
        shape_type = shapes_to_place[idx]
        for cell in range(total_cells):
            if (grid_mask >> cell) & 1:
                continue
            
            r = cell // w
            c = cell % w
            for orientation in all_orientations[shape_type]:
                cells_needed = []
                valid = True
                
                for dr, dc in orientation:
                    nr, nc = r + dr, c + dc
                    if nr < 0 or nr >= h or nc < 0 or nc >= w:
                        valid = False
                        break
                    
                    cell_pos = nr * w + nc
                    if (grid_mask >> cell_pos) & 1:
                        valid = False
                        break
                    
                    cells_needed.append(cell_pos)
                
                if valid:
                    new_mask = grid_mask
                    for cell_pos in cells_needed:
                        new_mask |= (1 << cell_pos)
                    
                    if dfs(idx + 1, new_mask):
                        return True
        
        return False
    
    return dfs(0, 0)

from functools import lru_cache

def main():
    shapes, regions = read_input('input.txt')
    
    print(f"Shapes: {len(shapes)}, Regions: {len(regions)}")
    
    if len(shapes) == 0:
        print("Error: No shapes found!")
        return
    
    all_orientations = [get_all_orientations(shape) for shape in shapes]
    
    for i, (shape, orientations) in enumerate(zip(shapes, all_orientations)):
        print(f"Shape {i}: {len(shape)} cells, {len(orientations)} orientations")
    
    count = 0
    start_time = time.time()
    
    sample_regions = min(5, len(regions))
    for i, (w, h, quantities) in enumerate(regions[:sample_regions]):
        total_shapes = sum(quantities)
        total_cells = w * h
        shape_cells = sum(q * len(all_orientations[idx][0]) for idx, q in enumerate(quantities))
        print(f"\nRegion {i}: {w}x{h} ({total_cells} cells), {total_shapes} shapes, {shape_cells} shape cells")
        print(f"Quantities: {quantities}")
        
        if solve_region(w, h, quantities, all_orientations):
            count += 1
            print(f"  -> Fits")
        else:
            print(f"  -> Doesn't fit")
    print(f"\nProcessing all {len(regions)} regions...")
    for i, (w, h, quantities) in enumerate(regions):
        if solve_region(w, h, quantities, all_orientations):
            count += 1
        
        if (i + 1) % 100 == 0:
            elapsed = time.time() - start_time
            print(f"Processed {i + 1}/{len(regions)}, Fittable: {count}, Time: {elapsed:.1f}s")
    
    print(f"\nFinal result: {count}")
    return count

if __name__ == "__main__":
    main()