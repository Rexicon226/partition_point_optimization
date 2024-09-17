const std = @import("std");

noinline fn partitionPoint(
    comptime T: type,
    items: []const T,
    context: anytype,
    comptime predicate: fn (@TypeOf(context), T) bool,
) usize {
    var low: usize = 0;
    var high: usize = items.len;

    while (low < high) {
        const mid = low + (high - low) / 2;
        if (predicate(context, items[mid])) {
            low = mid + 1;
        } else {
            high = mid;
        }
    }
    return low;
}

noinline fn partitionPointNew(
    comptime T: type,
    items: []const T,
    context: anytype,
    comptime predicate: fn (@TypeOf(context), T) bool,
) usize {
    var it: usize = 0;
    var len: usize = items.len;

    while (len > 1) {
        const half: usize = len / 2;
        len -= half;
        if (predicate(context, items[it + half - 1])) {
            @branchHint(.unpredictable);
            it += half;
        }
    }

    if (it < items.len) {
        it += @intFromBool(predicate(context, items[it]));
    }

    return it;
}

const allocator = std.heap.c_allocator;

const iterations_per_byte = 1024;
const warmup_iterations = 64;

const Tp = u32;

fn lower(other: Tp, item: Tp) bool {
    return item <= other;
}

pub fn main() !void {
    // Pin the process to a single core (1)
    if (@import("builtin").os.tag == .linux) {
        const cpu0001: std.os.linux.cpu_set_t = [1]usize{0b0001} ++ ([_]usize{0} ** (16 - 1));
        try std.os.linux.sched_setaffinity(0, &cpu0001);
    }

    const items: u32 = 10e3;
    var file = try std.fs.cwd().createFile("data.txt", .{});
    defer file.close();
    const stdout = file.writer();

    const total_buffer = try allocator.alloc(Tp, items);
    defer allocator.free(total_buffer);

    for (0..items) |N| {
        try stdout.print("{},", .{N});

        const buffer = total_buffer[0..N];

        inline for (.{ 1, N / 2, N - 1 }) |point| {
            const other: u32 = @intCast(point);

            for (0..N) |i| buffer[i] = @intCast(i);
            clflush(Tp, buffer);

            var new_i: u32 = 0;
            var new_ns: usize = 0;
            while (new_i < iterations_per_byte + warmup_iterations) : (new_i += 1) {
                const start = rdtsc();
                std.mem.doNotOptimizeAway(partitionPointNew(
                    Tp,
                    buffer,
                    other,
                    lower,
                ));
                const end = rdtsc();
                if (new_i > warmup_iterations) new_ns += end - start;
            }

            for (0..N) |i| buffer[i] = @intCast(i);
            clflush(Tp, buffer);

            var old_i: u32 = 0;
            var old_ns: usize = 0;
            while (old_i < iterations_per_byte + warmup_iterations) : (old_i += 1) {
                const start = rdtsc();
                std.mem.doNotOptimizeAway(partitionPoint(
                    Tp,
                    buffer,
                    other,
                    lower,
                ));
                const end = rdtsc();
                if (old_i > warmup_iterations) old_ns += end - start;
            }

            const new_cycles_per_byte = new_ns / iterations_per_byte;
            const old_cycles_per_byte = old_ns / iterations_per_byte;

            try stdout.print("{d},{d},", .{
                new_cycles_per_byte,
                old_cycles_per_byte,
            });
        }

        try stdout.writeAll("\n");

        if (N % 1000 == 0) std.debug.print("N: {d}/{d}\n", .{ N, items });
    }
}

inline fn rdtsc() usize {
    var a: u32 = undefined;
    var b: u32 = undefined;
    asm volatile ("rdtscp"
        : [a] "={edx}" (a),
          [b] "={eax}" (b),
        :
        : "ecx"
    );
    return (@as(u64, a) << 32) | b;
}

inline fn clflush(comptime T: type, slice: []const T) void {
    for (0..slice.len / @sizeOf(T)) |chunk| {
        const offset = slice.ptr + (chunk * @sizeOf(T));
        asm volatile ("clflush %[ptr]"
            :
            : [ptr] "m" (offset),
            : "memory"
        );
    }
}
