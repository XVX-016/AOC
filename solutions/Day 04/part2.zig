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
    
    var temp_iter = std.mem.tokenizeAny(u8, input, "\r\n");
    var line_count: usize = 0;
    
    while (temp_iter.next()) |line| {
        if (line.len > 0) {
            line_count += 1;
        }
    }
    
    const height = line_count;
    if (height == 0) {
        std.debug.print("0\n", .{});
        return;
    }
    
    var lines_iter = std.mem.tokenizeAny(u8, input, "\r\n");
    var lines = try allocator.alloc([]const u8, height);
    defer allocator.free(lines);
    
    var i: usize = 0;
    while (lines_iter.next()) |line| {
        if (line.len > 0) {
            lines[i] = line;
            i += 1;
        }
    }
    
    var grid = try allocator.alloc([]u8, height);
    defer {
        for (grid) |row| {
            allocator.free(row);
        }
        allocator.free(grid);
    }
    
    for (0..height) |y| {
        const row_len = lines[y].len;
        grid[y] = try allocator.alloc(u8, row_len);
        @memcpy(grid[y], lines[y]);
    }
    
    const dirs = [_][2]isize{
        .{ -1, -1 }, .{ -1, 0 }, .{ -1, 1 },
        .{  0, -1 },              .{  0, 1 },
        .{  1, -1 }, .{  1, 0 }, .{  1, 1 },
    };
    
    var total_removed: usize = 0;
    var changed: bool = true;

    while (changed) {
        changed = false;

        for (0..height) |y| {
            const row = grid[y];
            const row_len = row.len;
            
            for (0..row_len) |x| {
                if (row[x] == '@') {
                    var adjacent_rolls: usize = 0;

                    for (dirs) |dir| {
                        const ny = @as(isize, @intCast(y)) + dir[0];
                        const nx = @as(isize, @intCast(x)) + dir[1];

                        if (ny >= 0 and ny < height) {
                            const neighbor_row = grid[@intCast(ny)];
                            const neighbor_len = neighbor_row.len;
                            
                            if (nx >= 0 and nx < neighbor_len) {
                                if (neighbor_row[@intCast(nx)] == '@') {
                                    adjacent_rolls += 1;
                                }
                            }
                        }
                    }
                    if (adjacent_rolls < 4) {
                        // Mark with a different character temporarily
                        grid[y][x] = 'x'; // Mark for removal
                        changed = true;
                    }
                }
            }
        }
        for (0..height) |y| {
            const row = grid[y];
            const row_len = row.len;
            
            for (0..row_len) |x| {
                if (row[x] == 'x') {
                    grid[y][x] = '.';
                    total_removed += 1;
                }
            }
        }
    }
    
    std.debug.print("{d}\n", .{total_removed});
}