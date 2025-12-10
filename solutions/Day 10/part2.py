"""
1. Install Z3 Python bindings:
   pip install z3-solver

2. Put the puzzle input in a text file (example below) and run:
   python3 solve_z3.py input.txt
"""
import re
import sys
from z3 import Ints, Optimize, Int, sat


def parse_line(line):
    btn_txts = re.findall(r"\((.*?)\)", line)
    buttons = []
    for t in btn_txts:
        t = t.strip()
        if t == "":
            buttons.append([])
        else:
            parts = [p.strip() for p in t.split(",") if p.strip() != ""]
            buttons.append([int(x) for x in parts])
    m = re.search(r"\{(.*?)\}", line)
    if not m:
        raise ValueError("Line does not contain a target vector in braces: {}".format(line))
    targ_txt = m.group(1)
    target = [int(x.strip()) for x in targ_txt.split(",") if x.strip() != ""]

    return buttons, target


def solve_machine(buttons, target):
    n_buttons = len(buttons)
    n_counters = len(target)
    presses = [Int(f"p_{i}") for i in range(n_buttons)]

    opt = Optimize()
    for p in presses:
        opt.add(p >= 0)
    for i in range(n_counters):
        contributing = [presses[j] for j in range(n_buttons) if i in buttons[j]]
        if not contributing:
            if target[i] != 0:
                return None, None 
            else:
                continue
        opt.add(sum(contributing) == target[i])
    total = sum(presses)
    h = opt.minimize(total)

    res = opt.check()
    if res != sat:
        return None, None
    m = opt.model()
    vals = [m[p].as_long() for p in presses]
    min_total = sum(vals)
    return min_total, vals


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solve_z3.py input.txt")
        sys.exit(1)

    path = sys.argv[1]
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            s = raw.strip()
            if s == "":
                continue
            lines.append(s)

    grand_total = 0
    for idx, line in enumerate(lines, start=1):
        try:
            buttons, target = parse_line(line)
        except Exception as e:
            print(f"Failed to parse line {idx}: {e}")
            continue

        min_presses, vals = solve_machine(buttons, target)
        if min_presses is None:
            print(f"Machine {idx}: impossible to reach target (unsat). Line: {line}")
        else:
            grand_total += min_presses
            print(f"Machine {idx}: min presses = {min_presses}")
            print(f"  presses per button: {vals}")
    print(f"Grand total (all machines): {grand_total}")


if __name__ == '__main__':
    main()
