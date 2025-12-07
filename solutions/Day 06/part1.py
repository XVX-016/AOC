def solve_worksheet():
    with open('C:/Computing/AOC/solutions/Day 06/input.txt', 'r') as file:
        lines = [line.rstrip('\n') for line in file.readlines()]
    op_line_idx = -1
    for i, line in enumerate(lines):
        if '*' in line or '+' in line:
            op_line_idx = i
            break
    
    number_lines = lines[:op_line_idx]
    operation_line = lines[op_line_idx]
    parsed_numbers = []
    for line in number_lines:
        numbers = []
        current_num = ''
        for char in line:
            if char.isdigit():
                current_num += char
            elif current_num:
                numbers.append(int(current_num))
                current_num = ''
        if current_num:
            numbers.append(int(current_num))
        parsed_numbers.append(numbers)
    operations = []
    current_op = ''
    for char in operation_line:
        if char in ['*', '+']:
            current_op += char
        elif current_op:
            operations.append(current_op)
            current_op = ''
    if current_op:
        operations.append(current_op)
    num_problems = len(parsed_numbers[0])
    results = []
    for i in range(num_problems):
        operation = operations[i] if i < len(operations) else ''
        if not operation:
            continue
        problem_numbers = [row[i] for row in parsed_numbers if i < len(row)]
        
        if not problem_numbers:
            continue
        if operation == '*':
            result = 1
            for num in problem_numbers:
                result *= num
        else:  # '+'
            result = sum(problem_numbers)
        
        results.append(result)
    
    return sum(results)

print(f"Grand total: {solve_worksheet()}")