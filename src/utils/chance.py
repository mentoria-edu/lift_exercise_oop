from random import random


class Chance:

    @staticmethod
    def happens_by_chance(
            chance_modifier: float
    ) -> bool:
        if not 0.0 <= chance_modifier < 1.0:
            raise ValueError(
                "chance_modifier must be equal or "
                "greater than 0, and less than 1"
            )

        percentage = random()
        happened = percentage <= chance_modifier

        return happened
