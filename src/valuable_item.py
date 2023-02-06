"""Valuable item class"""
from dataclasses import dataclass


@dataclass
class ValuableItem:
    """Valuable item class
    option: str
    cost: float
    profit: float

    @property
    profit_ratio(self) -> float

    """

    option: str
    cost: float
    profit: float

    @property
    def profit_ratio(self) -> float:
        """Returns the profit / value."""
        return self.profit / (self.cost + 1e-9)
