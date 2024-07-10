from enum import Enum

class Currency(Enum):
  USD = "United States Dollar"
  EUR = "Euro"
  BRL = "Brazilian Real"

  def __str__(self):
    return self._name_
