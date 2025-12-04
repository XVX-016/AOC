const std = @import("std");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    const file = try std.fs.cwd().openFile("C:\\Computing\\AOC\\solutions\\Day 04\\input.txt", .{});
    defer file.close();
    
    const file_size = (try file.stat()).size;
    const buffer = try allocator.alloc(u8, @as(usize, @intCast(file_size)));
    defer allocator.free(buffer);
    
    const bytes_read = try file.read(buffer);
    const input = buffer[0..bytes_read];
    
    var line_iter = std.mem.tokenizeAny(u8, input, "\r\n");
    var line_count: usize = 0;
    var max_width: usize = 0;
    
    while (line_iter.next()) |line| {
        if (line.len > 0) {
            line_count += 1;
            if (line.len > max_width) {
                max_width = line.len;
            }
        }
    }
    
    const h = line_count;
    if (h == 0) {
        std.debug.print("0\n", .{});
        return;
    }
    
    // Second pass: store lines
    line_iter = std.mem.tokenizeAny(u8, input, "\r\n");
    var lines = try allocator.alloc([]const u8, h);
    defer allocator.free(lines);
    
    var i: usize = 0;
    while (line_iter.next()) |line| {
        if (line.len > 0) {
            lines[i] = line;
            i += 1;
        }
    }
    
    var count: usize = 0;
    
    for (0..h) |y| {
        const row = lines[y];
        const w = row.len;
        
        for (0..w) |x| {
            if (row[x] == '@') {
                var adjacent: usize = 0;
                
                // Check all 8 neighbors
                for ([_]isize{-1, 0, 1}) |dy| {
                    for ([_]isize{-1, 0, 1}) |dx| {
                        if (dy == 0 and dx == 0) continue; // Skip self
                        
                        const ny = @as(isize, @intCast(y)) + dy;
                        const nx = @as(isize, @intCast(x)) + dx;
                        
                        if (ny >= 0 and ny < h) {
                            const neighbor_row = lines[@intCast(ny)];
                            const nw = neighbor_row.len;
                            if (nx >= 0 and nx < nw) {
                                if (neighbor_row[@intCast(nx)] == '@') {
                                    adjacent += 1;
                                }
                            }
                        }
                    }
                }
                
                if (adjacent < 4) {
                    count += 1;
                }
            }
        }
    }
    
    std.debug.print("{d}\n", .{count});
}