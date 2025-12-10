def read_points(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                points.append((x, y))
    return points

def add_line(p1, p2, grid_set):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid_set.add((x1, y))
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            grid_set.add((x, y1))
    else:
        raise ValueError("Points not aligned")

def get_boundary_set(points):
    boundary = set()
    n = len(points)
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        boundary.add(p1)
        add_line(p1, p2, boundary)
    return boundary

def get_interior_filled(boundary_set, points):
    # Find bounding box
    min_x = min(x for x, _ in boundary_set)
    max_x = max(x for x, _ in boundary_set)
    min_y = min(y for _, y in boundary_set)
    max_y = max(y for _, y in boundary_set)

    # Use even-odd rule scanline for orthogonal polygon
    # For each y, get all x where vertical edges are
    # Actually, simpler: for each y, collect x from boundary points on horizontal edges? 
    # Better: use ray casting for each (x,y) in bbox
    interior = set()
    for y in range(min_y, max_y + 1):
        inside = False
        for x in range(min_x, max_x + 1):
            if (x, y) in boundary_set and (x, y+1) not in boundary_set:
                # Wait — need robust rule: toggle at vertical edges
                pass
    # Let's do a simpler approach: flood fill from a known interior point
    # Find interior point by scanning from left boundary to right at middle y
    mid_y = (min_y + max_y) // 2
    # Collect all boundary x's at this y
    xs_at_y = sorted({x for (x, yy) in boundary_set if yy == mid_y})
    # Between each pair of xs, middle is inside
    inside_points = []
    for i in range(0, len(xs_at_y) - 1, 2):
        x_start = xs_at_y[i]
        x_end = xs_at_y[i + 1]
        for x in range(x_start + 1, x_end):
            inside_points.append((x, mid_y))

    if not inside_points:
        # Try different y
        for test_y in range(min_y, max_y + 1):
            xs_at_y = sorted({x for (x, yy) in boundary_set if yy == test_y})
            if len(xs_at_y) >= 2:
                for i in range(0, len(xs_at_y) - 1, 2):
                    x_start = xs_at_y[i]
                    x_end = xs_at_y[i + 1]
                    for x in range(x_start + 1, x_end):
                        inside_points.append((x, test_y))
                if inside_points:
                    break

    # Flood fill from these inside points
    filled = set(boundary_set)
    stack = inside_points[:]
    visited = set(stack)
    while stack:
        x, y = stack.pop()
        filled.add((x, y))
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in filled and (nx, ny) not in visited:
                if min_x <= nx <= max_x and min_y <= ny <= max_y:
                    visited.add((nx, ny))
                    stack.append((nx, ny))
    return filled

def is_rectangle_valid(x1, y1, x2, y2, green_red_set):
    x_start, x_end = sorted([x1, x2])
    y_start, y_end = sorted([y1, y2])
    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end + 1):
            if (x, y) not in green_red_set:
                return False
    return True

def solve(filename):
    points = read_points(filename)
    boundary_set = get_boundary_set(points)
    green_red_set = get_interior_filled(boundary_set, points)

    max_area = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            if x1 == x2 or y1 == y2:
                continue  # Not opposite corners
            if is_rectangle_valid(x1, y1, x2, y2, green_red_set):
                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
                if area > max_area:
                    max_area = area
    return max_area

if __name__ == "__main__":
    result = solve("solutions\Day 09\input.txt")
    print(result)