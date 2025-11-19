import random


class VtMRolls:
    def __init__(self, dice_pool: int, hunger: int = None):
        self.dice_pool = dice_pool
        self.hunger = hunger

        self.bestial_fail = False
        self.messy_critical = False

        self.successes = 0
        self.crit_successes = 0

    def generate(self):
        for i in range(self.dice_pool):
            val = random.randint(1, 10)

            is_hunger = self.hunger is not None and i < self.hunger

            if val == 1:
                self.successes -= 1
                if is_hunger:
                    self.bestial_fail = True

            elif val == 10:
                self.crit_successes += 1
                if is_hunger:
                    self.messy_critical = True

            elif val > 5:
                self.successes += 1
