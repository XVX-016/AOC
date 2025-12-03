const std = @import("std");

fn isInvalidID(n: u64) bool {
    var buffer: [20]u8 = undefined; // 20 is enough for u64 max digits
    const s = std.fmt.bufPrint(&buffer, "{d}", .{n}) catch return false;
    const len = s.len;
    
    
    if (len < 2) return false;
    var divisor: usize = 1;
    while (divisor <= len / 2) : (divisor += 1) {
        // Check if divisor divides len evenly
        if (len % divisor != 0) continue;
        
        const repetitions = len / divisor;
        if (repetitions < 2) continue;
        
        
        var valid = true;
        const part = s[0..divisor];
        
        var i: usize = 1;
        while (i < repetitions) : (i += 1) {
            const start_idx = i * divisor;
            const next_part = s[start_idx .. start_idx + divisor];
            
            if (!std.mem.eql(u8, part, next_part)) {
                valid = false;
                break;
            }
        }
        
        if (valid) return true;
    }
    
    return false;
}

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    const file = try std.fs.cwd().openFile(
        "C:\\Computing\\AOC\\solutions\\Day 02\\input.txt", 
        .{}
    );
    defer file.close();
    
    const file_size = (try file.stat()).size;
    const buffer = try allocator.alloc(u8, @as(usize, @intCast(file_size)));
    defer allocator.free(buffer);
    
    const bytes_read = try file.read(buffer);
    const input_str = std.mem.trim(u8, buffer[0..bytes_read], "\r\n");
    
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
            if (isInvalidID(n)) {
                total_sum += n;
            }
        }
    }
    
    std.debug.print("Sum of invalid IDs: {d}\n", .{total_sum});
}