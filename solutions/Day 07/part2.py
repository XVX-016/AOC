def count_timelines_dp():
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
    dp = [[0] * cols for _ in range(rows + 1)]
    dp[0][start_col] = 1
    
    for r in range(rows):
        for c in range(cols):
            if dp[r][c] == 0:
                continue
            
            if grid[r][c] == '^':
                if c - 1 >= 0:
                    dp[r + 1][c - 1] += dp[r][c]
                if c + 1 < cols:
                    dp[r + 1][c + 1] += dp[r][c]
            else:
                dp[r + 1][c] += dp[r][c]
    
    total_timelines = sum(dp[rows])
    return total_timelines

if __name__ == "__main__":
    result = count_timelines_dp()
    print(f"Number of timelines: {result}")