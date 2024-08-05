export fn menor_ou_igual(n: usize, l: usize, l_len: usize, is_le: usize, is_gt: usize, resultcounter_is_le: usize, resultcounter_is_gt: usize) void {
    const l_array: [*c]c_int = @ptrFromInt(l);
    var is_le_array: [*c]c_int = @ptrFromInt(is_le);
    var is_gt_array: [*c]c_int = @ptrFromInt(is_gt);
    var resultcounter_is_le_array: [*c]usize = @ptrFromInt(resultcounter_is_le);
    var resultcounter_is_gt_array: [*c]usize = @ptrFromInt(resultcounter_is_gt);
    const n_array: [*c]c_int = @ptrFromInt(n);
    for (0..l_len) |it0| {
        if (l_array[it0] > n_array[0]) {
            is_gt_array[resultcounter_is_gt_array[0]] = l_array[it0];
            resultcounter_is_gt_array[0] += 1;
        } else {
            is_le_array[resultcounter_is_le_array[0]] = l_array[it0];
            resultcounter_is_le_array[0] += 1;
        }
    }
}
