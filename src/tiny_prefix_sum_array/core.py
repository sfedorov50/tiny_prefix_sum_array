"""Core implementation of tiny_prefix_sum_array.

Why this exists: answering many fixed-range sum queries over an immutable
sequence is O(n) per query if done naively. Precomputing cumulative sums once
makes each query O(1) at the cost of O(n) extra memory. The trade-off is
memory for query speed; the array must be treated as immutable after
construction.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from typing import Iterable, List, Sequence, TypeVar, Union

T = TypeVar("T", int, float)


class PrefixSumArray:
    """Immutable prefix-sum array for O(1) range-sum queries.

    The prefix array has length ``n + 1``. ``prefix[i]`` is the sum of the
    first ``i`` elements of the original sequence. This layout lets a query
    for ``[left, right)`` be answered as ``prefix[right] - prefix[left]``
    without any special case for ``left == 0``.

    The original sequence is not stored; only the prefix sums are kept. If
    you need the original values, keep them yourself.
    """

    __slots__ = ("_prefix", "_n")

    def __init__(self, values: Iterable[Union[int, float]]) -> None:
        """Build the prefix array from an iterable of numbers.

        The iterable is consumed once. ``bool`` is accepted because it is a
        subclass of ``int`` in Python, but mixing booleans with floats is the
        caller's responsibility.
        """
        prefix: List[Union[int, float]] = [0]
        total: Union[int, float] = 0
        count = 0
        for value in values:
            if not isinstance(value, (int, float)) or isinstance(value, complex):
                raise TypeError(
                    f"PrefixSumArray only supports int and float, got {type(value).__name__}"
                )
            total += value
            prefix.append(total)
            count += 1
        self._prefix: List[Union[int, float]] = prefix
        self._n: int = count

    @property
    def size(self) -> int:
        """Number of elements in the original sequence."""
        return self._n

    def __len__(self) -> int:
        return self._n

    def total(self) -> Union[int, float]:
        """Sum of the whole original sequence. O(1)."""
        return self._prefix[-1]

    def query(self, left: int, right: int) -> Union[int, float]:
        """Return the sum of ``values[left:right]`` in O(1).

        ``left`` is inclusive and ``right`` is exclusive, matching Python
        slicing. Raises ``IndexError`` if the half-open range is not within
        ``[0, size]`` or if ``left > right``. Empty ranges are allowed and
        return ``0``.
        """
        if not (0 <= left <= right <= self._n):
            raise IndexError(
                f"range [{left}, {right}) is out of bounds for size {self._n}"
            )
        return self._prefix[right] - self._prefix[left]

    def prefix_at(self, index: int) -> Union[int, float]:
        """Return the sum of the first ``index`` elements.

        ``index`` must be in ``[0, size]``. ``prefix_at(0)`` is ``0`` and
        ``prefix_at(size)`` equals ``total()``.
        """
        if not (0 <= index <= self._n):
            raise IndexError(
                f"prefix index {index} is out of bounds for size {self._n}"
            )
        return self._prefix[index]

    def __repr__(self) -> str:
        return f"PrefixSumArray(size={self._n})"
