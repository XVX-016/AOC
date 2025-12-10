import re
from collections import deque
import os

def parse_line(line):
    diag = re.search(r"\[(.*?)\]", line).group(1)
    n = len(diag)
    target = 0
    for i, c in enumerate(diag):
        if c == "#":
            target |= 1 << i
    buttons = []
    for b in re.findall(r"\((.*?)\)", line):
        mask = 0
        for x in b.split(","):
            x = x.strip()
            if x:
                mask |= 1 << int(x)
        buttons.append(mask)
    return diag, n, target, buttons

def mask_string(mask, n):
    return "[" + "".join("#" if mask & (1 << i) else "." for i in range(n)) + "]"

def bfs_path(n, target, buttons):
    start = 0
    if start == target:
        return []
    q = deque([start])
    parent = {start: None}
    press = {}
    while q:
        s = q.popleft()
        for i, m in enumerate(buttons):
            nxt = s ^ m
            if nxt not in parent:
                parent[nxt] = s
                press[nxt] = i
                if nxt == target:
                    path = []
                    cur = nxt
                    while parent[cur] is not None:
                        path.append(press[cur])
                        cur = parent[cur]
                    return list(reversed(path))
                q.append(nxt)
    return None

def solve_and_visualize():
    path = os.path.join("solutions", "Day 10", "input.txt")
    with open(path) as f:
        lines = [x.strip() for x in f if x.strip()]

    total = 0
    mid = 1

    for line in lines:
        diag, n, target, buttons = parse_line(line)
        print("MACHINE", mid)
        print("diagram:", "[" + diag + "]")
        print("target :", mask_string(target, n))
        print("buttons:")
        for i, m in enumerate(buttons):
            print(i, mask_string(m, n))
        path = bfs_path(n, target, buttons)
        presses = len(path)
        total += presses
        print("presses:", presses)
        print("sequence:", path)
        state = 0
        print("step 0:", mask_string(state, n))
        for step, bi in enumerate(path, 1):
            state ^= buttons[bi]
            print("step", step, "press", bi, "→", mask_string(state, n))
        print()
        mid += 1

    print("TOTAL =", total)

solve_and_visualize()
