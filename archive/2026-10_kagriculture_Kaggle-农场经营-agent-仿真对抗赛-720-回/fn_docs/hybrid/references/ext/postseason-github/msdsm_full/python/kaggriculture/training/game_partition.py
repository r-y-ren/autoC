"""Partition a fixed global game batch without requiring divisibility by Pod count."""

from __future__ import annotations

from dataclasses import dataclass


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


@dataclass(frozen=True)
class GamePartition:
    total_games: int
    games_per_step: int
    processes: int
    rank: int

    def __post_init__(self) -> None:
        if min(self.total_games, self.games_per_step, self.processes) <= 0:
            raise ValueError("game counts and process count must be positive")
        if not 0 <= self.rank < self.processes:
            raise ValueError("rank outside process count")

    @property
    def games(self) -> int:
        quotient, remainder = divmod(self.total_games, self.processes)
        return quotient + (self.rank < remainder)

    @property
    def seed_offset(self) -> int:
        quotient, remainder = divmod(self.total_games, self.processes)
        return self.rank * quotient + min(self.rank, remainder)

    @property
    def emissions(self) -> int:
        return ceil_div(self.total_games, self.games_per_step)

    def group(self, emission: int) -> slice:
        if not 0 <= emission < self.emissions:
            raise ValueError("emission outside update")
        start = emission * self.games_per_step
        end = min(start + self.games_per_step, self.total_games)
        # Rotating the remainder avoids assigning every extra game to the same rank.
        return slice(
            max(0, ceil_div(start - self.rank, self.processes)),
            max(0, ceil_div(end - self.rank, self.processes)),
        )

    def global_group_games(self, emission: int) -> int:
        if not 0 <= emission < self.emissions:
            raise ValueError("emission outside update")
        return min(self.games_per_step, self.total_games - emission * self.games_per_step)
