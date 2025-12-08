def count_splits():
    with open('solutions\Day 07\input.txt', 'r') as f:
        grid = [list(line.rstrip()) for line in f.readlines()]
    
    rows = len(grid)
    cols = len(grid[0])
    start_col = None
    for c in range(cols):
        if grid[0][c] == 'S':
            start_col = c
            grid[0][c] = '.' 
            break
    
    if start_col is None:
        raise ValueError("No starting position S found in first row")
    beams = {start_col}
    total_splits = 0
    for r in range(rows):
        next_beams = set()
        for c in beams:
            if grid[r][c] == '^':
                total_splits += 1
                if c - 1 >= 0:
                    next_beams.add(c - 1)
                if c + 1 < cols:
                    next_beams.add(c + 1)
            else:
                next_beams.add(c)
        
        beams = next_beams
    
    return total_splits

if __name__ == "__main__":
    result = count_splits()
    print(f"Total splits: {result}")