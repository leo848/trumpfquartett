from dataclasses import dataclass

import colors


@dataclass
class Card:
    title: str
    height: float  # in cm
    weight: float  # in kg
    age: float  # in years

    def __str__(self):
        return f"""
    {colors.BOLD}{self.title}{colors.END}
    (a) Größe:      {self.height} cm
    (b) Gewicht:    {self.weight} kg
    (c) Alter:      {self.age} Jahre
        """

    def attr_str(self, attr):
        return f'{getattr(self, attr)} { {"height": "cm", "weight": "kg", "age": "Jahre"}[attr] }'
