from typing import Generic, TypeVar, Iterator


T = TypeVar("T")


class Queue(Generic[T]):
    _queue: list[T]

    def __init__(self) -> None:
        self._queue = []

    def push(self, item: T) -> None:
        self._queue.append(item)

    def pop(self) -> T:
        return self._queue.pop(0)

    def peek(self) -> T:
        if self.is_empty():
            return None
        return self._queue[-1]

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)

    def __iter__(self) -> Iterator[T]:
        return iter(self._queue)
