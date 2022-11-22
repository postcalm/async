import itertools
from typing import Iterable, List, TypeVar


T = TypeVar("T")


def chunk_list(iterable: Iterable[T], size: int) -> Iterable[List[T]]:
    """
    Split list or generator by chunks with fixed maximum size.
    """

    iterable = iter(iterable)

    item = list(itertools.islice(iterable, size))
    while item:
        yield item
        item = list(itertools.islice(iterable, size))