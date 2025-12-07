def solve_part2():
    with open('C:/Computing/AOC/solutions/Day 06/input.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    
    # Find the operation line
    op_line_idx = -1
    for i, line in enumerate(lines):
        if '*' in line or '+' in line:
            op_line_idx = i
            break
    
    num_lines = lines[:op_line_idx]
    op_line = lines[op_line_idx]
    
    # Pad all lines to same length
    max_len = max(len(line) for line in num_lines + [op_line])
    padded_nums = [line.ljust(max_len) for line in num_lines]
    padded_op = op_line.ljust(max_len)
    
    total = 0
    col = 0
    num_rows = len(padded_nums)
    
    while col < max_len:
        # Skip to next operation
        while col < max_len and padded_op[col] not in '*+':
            col += 1
        
        if col >= max_len:
            break
        
        op = padded_op[col]
        
        # Find start and end of this problem's columns
        start_col = col
        end_col = col + 1
        
        # Expand left while previous column has digits in any row
        while start_col > 0:
            has_digits = False
            for r in range(num_rows):
                if padded_nums[r][start_col - 1].isdigit():
                    has_digits = True
                    break
            if not has_digits:
                break
            start_col -= 1
        
        # Expand right while next column has digits in any row
        while end_col < max_len:
            has_digits = False
            for r in range(num_rows):
                if padded_nums[r][end_col].isdigit():
                    has_digits = True
                    break
            if not has_digits:
                break
            end_col += 1
        
        # Process this problem from right to left
        problem_result = None
        
        # Process columns right to left
        for c in range(end_col - 1, start_col - 1, -1):
            # Read number vertically from this column
            num_str = ''
            for r in range(num_rows):
                ch = padded_nums[r][c]
                if ch.isdigit():
                    num_str += ch
            
            if num_str:  # Only process if we found digits
                num = int(num_str)
                if problem_result is None:
                    problem_result = num
                else:
                    if op == '*':
                        problem_result *= num
                    else:
                        problem_result += num
        
        if problem_result is not None:
            total += problem_result
        
        # Skip to next unprocessed column
        col = end_col
    
    return total

print(f"Grand total: {solve_part2()}")