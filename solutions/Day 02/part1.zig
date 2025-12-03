const std = @import("std");

fn isRepeatedID(n: u64) bool {
    var buffer: [20]u8 = undefined; // 20 is enough for u64 max digits
    const s = std.fmt.bufPrint(&buffer, "{d}", .{n}) catch return false;
    const len = s.len;
    
    if (len % 2 != 0 or len == 0) return false;
    const half = len / 2;
    
    for (0..half) |half_idx| {
        if (s[half_idx] != s[half_idx + half]) return false;
    }
    return true;
}

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    const file = try std.fs.cwd().openFile(
        "C:\\Computing\\AOC\\solutions\\Day 02\\input.txt", 
        .{}
    );
    defer file.close();
    
    const file_size = (try file.stat()).size;
    const buffer = try allocator.alloc(u8, file_size);
    defer allocator.free(buffer);
    
    _ = try file.read(buffer); // readAll is now just read
    const input_str = std.mem.trim(u8, buffer, "\r\n");
    
    var ranges_it = std.mem.splitScalar(u8, input_str, ',');
    var total_sum: u64 = 0;
    
    while (ranges_it.next()) |range_str| {
        var parts = std.mem.splitScalar(u8, range_str, '-');
        const start_str = parts.next() orelse continue;
        const end_str = parts.next() orelse continue;
        
        const start_num = try std.fmt.parseInt(u64, start_str, 10);
        const end_num = try std.fmt.parseInt(u64, end_str, 10);
        
        var n = start_num;
        while (n <= end_num) : (n += 1) {
            if (isRepeatedID(n)) {
                total_sum += n;
            }
        }
    }
    
    std.debug.print("Sum of invalid IDs: {d}\n", .{total_sum});
}