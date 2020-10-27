"""Contains the definitions of the currencies
"""

from enum import Enum, unique


@unique
class Currency(Enum):
    """Defines unique currencies that are available"""
    Dollars = "Dollars"
    Euros = "Euros"
