"""Implicit binary partitions without materializing candidate lists."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BitPrefixPartition:
    n: int
    prefix: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.n < 1 or len(self.prefix) > self.n or any(bit not in (0, 1) for bit in self.prefix):
            raise ValueError("invalid bit-prefix partition")

    @property
    def size(self) -> int:
        return 1 << (self.n - len(self.prefix))

    @property
    def is_leaf(self) -> bool:
        return len(self.prefix) == self.n

    @property
    def prefix_value(self) -> int:
        value = 0
        for bit in self.prefix:
            value = (value << 1) | bit
        return value

    def contains(self, candidate: int) -> bool:
        return 0 <= candidate < 1 << self.n and candidate >> (self.n - len(self.prefix)) == self.prefix_value

    def split(self) -> tuple["BitPrefixPartition", "BitPrefixPartition"]:
        if self.is_leaf:
            raise ValueError("leaf partition cannot be split")
        return (
            BitPrefixPartition(self.n, (*self.prefix, 0)),
            BitPrefixPartition(self.n, (*self.prefix, 1)),
        )

    def only_candidate(self) -> int:
        if not self.is_leaf:
            raise ValueError("partition contains more than one candidate")
        return self.prefix_value
