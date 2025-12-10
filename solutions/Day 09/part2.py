
import sys
from collections import defaultdict
from bisect import bisect_left

def read_points(path):
    pts = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x,y = line.split(',')
            pts.append((int(x), int(y)))
    return pts

def build_edges(pts):
    n = len(pts)
    edges = []
    for i in range(n):
        x1,y1 = pts[i]
        x2,y2 = pts[(i+1)%n]
        edges.append((x1,y1,x2,y2))
    return edges

def compute_allowed_intervals(pts):
    edges = build_edges(pts)
    ys = [y for (_,y) in pts]
    min_y, max_y = min(ys), max(ys)
    horiz_by_y = defaultdict(list)  
    vertical_edges = [] 
    for x1,y1,x2,y2 in edges:
        if x1 == x2:  
            ylo, yhi = min(y1,y2), max(y1,y2)
            vertical_edges.append((x1, ylo, yhi))
        else: 
            xlo, xhi = min(x1,x2), max(x1,x2)
            horiz_by_y[y1].append((xlo, xhi))

    allowed = {}  

    for y in range(min_y, max_y+1):
        xs = []
        for x, ylo, yhi in vertical_edges:
            if ylo <= y < yhi:
                xs.append(x)
        xs.sort()
        intervals = []
        i = 0
        while i+1 < len(xs):
            a = xs[i]
            b = xs[i+1]
            left = a
            right = b
            if left <= right - 1e-12: 
                xi0 = int((left + (1 - 1e-12))//1) 
                if xi0 < left: xi0 += 1
                xi0 = int((left + 0.9999999999) // 1)
                xi1 = int((right - 1e-12) // 1)
                if xi0 <= xi1:
                    intervals.append((xi0, xi1))
            i += 2
        for xlo,xhi in horiz_by_y.get(y, ()):
            intervals.append((xlo, xhi))

        if not intervals:
            allowed[y] = []
            continue
        intervals.sort()
        merged = []
        cur_lo, cur_hi = intervals[0]
        for lo,hi in intervals[1:]:
            if lo <= cur_hi + 1:
                cur_hi = max(cur_hi, hi)
            else:
                merged.append((cur_lo, cur_hi))
                cur_lo, cur_hi = lo, hi
        merged.append((cur_lo, cur_hi))
        allowed[y] = merged

    return allowed

def interval_covers(intervals, x0, x1):
    lo_list = [iv[0] for iv in intervals]
    idx = bisect_left(lo_list, x0)
    if idx < len(intervals) and intervals[idx][0] == x0:
        return intervals[idx][1] >= x1
    i = idx - 1
    if i >= 0:
        if intervals[i][0] <= x0 and intervals[i][1] >= x1:
            return True
    return False

def find_max_rectangle(pts, allowed):
    red_set = set(pts)
    n = len(pts)
    best_area = 0
    best_pair = None
    for i in range(n):
        x1,y1 = pts[i]
        for j in range(i+1, n):
            x2,y2 = pts[j]
            if x1 == x2 or y1 == y2:
                continue
            minx, maxx = min(x1,x2), max(x1,x2)
            miny, maxy = min(y1,y2), max(y1,y2)
            width = maxx - minx + 1
            height = maxy - miny + 1
            area = width * height
            if area <= best_area:
                continue 
            ok = True
            for y in range(miny, maxy+1):
                intervals = allowed.get(y, [])
                if not intervals:
                    ok = False
                    break
                if not interval_covers(intervals, minx, maxx):
                    ok = False
                    break
            if ok:
                best_area = area
                best_pair = ((x1,y1),(x2,y2))
    return best_area, best_pair

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    pts = read_points(path)
    if not pts:
        print("No points read from", path)
        return
    allowed = compute_allowed_intervals(pts)
    area, pair = find_max_rectangle(pts, allowed)
    if area == 0:
        print("No valid rectangle found.")
    else:
        (a,b),(c,d) = pair
        print("Largest area:", area)
        print("Corners:", (a,b), (c,d))

if __name__ == "__main__":
    main()
