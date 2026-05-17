from __future__ import annotations

__all__ = [
    "PaperDimensions",
    "merge_dicts_recursively",
    "get_page_dimensions",
    "get_paper_dimensions",
]


import itertools as it
from typing import Any, NamedTuple

class PaperDimensions(NamedTuple):
    width: float
    height: float


# Taken from https://github.com/3b1b/manim/blob/master/manimlib/utils/dict_ops.py
def merge_dicts_recursively(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """
    Creates a dict whose keyset is the union of all the
    input dictionaries.  The value for each key is based
    on the first dict in the list with that key.

    dicts later in the list have higher priority

    When values are dictionaries, it is applied recursively
    """
    result: dict[Any, Any] = dict()
    all_items = it.chain(*[d.items() for d in dicts])
    for key, value in all_items:
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts_recursively(result[key], value)  # pyright: ignore[reportUnknownArgumentType]
        else:
            result[key] = value
    return result


def get_paper_dimensions(paper_size: str = "a4") -> PaperDimensions:
    if paper_size == "letter":
        return PaperDimensions(21.6, 27.9)
    else:
        return PaperDimensions(21.0, 29.7)


def get_page_dimensions(paper_dims: PaperDimensions, margin_left_cm: float, margin_right_cm: float, margin_top_cm: float, margin_bottom_cm: float):
    return PaperDimensions(
        paper_dims.width - margin_left_cm - margin_right_cm,
        paper_dims.height - margin_top_cm - margin_bottom_cm
    )


