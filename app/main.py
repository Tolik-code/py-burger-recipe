from __future__ import annotations

from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner: str, name: str) -> None:
        self.public_name, self.protected_name = name, "_" + name

    def __get__(self, instance: BurgerRecipe, owner: str) -> str | int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: BurgerRecipe, value: str | int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value, self.max_value = min_value, max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"Quantity should not be less than "
                f"{self.min_value} and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(
        self, buns: int, cheese: int, tomatoes: int,
        cutlets: int, eggs: int, sauce: str
    ) -> None:
        (
            self.buns, self.cheese, self.tomatoes,
            self.cutlets, self.eggs, self.sauce
        ) = (
            buns, cheese, tomatoes,
            cutlets, eggs, sauce,
        )
