# tiny_prefix_sum_array

Precomputes cumulative sums so fixed-range sum queries over an immutable
sequence run in O(1) time.

```python
from tiny_prefix_sum_array import PrefixSumArray

p = PrefixSumArray([1, 2, 3, 4, 5])

p.query(1, 4)      # 9   (sum of values[1:4])
p.query(0, 5)      # 15
p.query(3, 3)      # 0
p.prefix_at(2)     # 3   (sum of the first two elements)
p.total()          # 15
len(p)             # 5
```

## Why this exists

If you need to answer many sum queries over the same sequence, summing the
slice every time is O(n) per query. This library pays O(n) once at
construction and O(1) per query, at the cost of an extra list of length
`n + 1`. The prefix array is stored instead of the original values, so the
class is effectively immutable: construct a new one if your data changes.

## API

- `PrefixSumArray(values)` — build from any iterable of `int`/`float`.
- `query(left, right)` — sum of `values[left:right]` (half-open).
- `prefix_at(index)` — sum of the first `index` elements.
- `total()` — sum of the whole sequence.
- `size` / `len(p)` — number of original elements.

## The awkward edge

`query` and `prefix_at` raise `IndexError` for out-of-bounds indices, and
`query` also raises when `left > right`. Empty ranges like `query(3, 3)` are
valid and return `0`. Non-numeric values raise `TypeError` at construction.
The library stores only prefix sums, so you cannot recover the original
sequence from a `PrefixSumArray`.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

