from decimal import Decimal

from typing import TypedDict


class BarData(TypedDict):
    x: str
    y: int | float | Decimal


class BarSeries(TypedDict):
    data: list[BarData]


class LineSeries(TypedDict):
    data: list[BarData]
