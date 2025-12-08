def count_timelines_optimized():
    with open('solutions\Day 07\input.txt', 'r') as f:
        grid = [line.rstrip() for line in f]
    
    rows = len(grid)
    cols = len(grid[0])
    
    start_col = grid[0].find('S')
    if start_col == -1:
        raise ValueError("No S found")
    grid[0] = grid[0].replace('S', '.')
    prev = [0] * cols
    prev[start_col] = 1
    
    for r in range(rows):
        curr = [0] * cols
        for c in range(cols):
            if prev[c] == 0:
                continue
            
            if grid[r][c] == '^':
                if c > 0:
                    curr[c-1] += prev[c]
                if c < cols - 1:
                    curr[c+1] += prev[c]
            else:
                curr[c] += prev[c]
        
        prev = curr
    
    return sum(prev)

if __name__ == "__main__":
    result = count_timelines_optimized()
    print(f"Number of timelines: {result}")