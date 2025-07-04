from decimal import Decimal

from typing import TypedDict


class BarData(TypedDict):
    x: str
    y: int | float | Decimal


class BarSeries(TypedDict):
    data: list[BarData]


x: BarSeries = {"data": [{"x": "abc", "y": 1}]}
