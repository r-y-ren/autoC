"""Bounded ordered staging; no parameter access or cross-process collectives on the worker."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PreparedUpdateBatch:
    arrays: dict[str, Any]


class CompletionQueue:
    def __init__(self, wait: Callable[[Any], Any], capacity: int = 2) -> None:
        if capacity < 1:
            raise ValueError("GPU queue capacity must be positive")
        self.wait, self.capacity = wait, capacity
        self.pending: deque[Any] = deque()

    def submit(self, token: Any) -> None:
        self.pending.append(token)
        if len(self.pending) >= self.capacity:
            self.wait(self.pending.popleft())

    def drain(self) -> None:
        while self.pending:
            self.wait(self.pending.popleft())


@contextmanager
def prefetched_batches[Input, Output](
    items: Iterable[Input], prepare: Callable[[Input], Output]
) -> Iterator[Iterator[Output]]:
    iterator = iter(items)
    executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="ppo-stage")

    def consume() -> Iterator[Output]:
        try:
            first = next(iterator)
        except StopIteration:
            return
        future = executor.submit(prepare, first)
        while True:
            current = future.result()
            try:
                following = next(iterator)
            except StopIteration:
                yield current
                return
            future = executor.submit(prepare, following)
            yield current

    try:
        yield consume()
    finally:
        # A failed update must not leave a thread staging into a subsequently reused rollout.
        executor.shutdown(wait=True, cancel_futures=True)
