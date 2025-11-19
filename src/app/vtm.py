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

        self.successes += self.crit_successes // 2

    def format_result(self):
        if self.messy_critical:
            result = "Messy Critical!"
        elif self.successes <= 0:
            result = "Failure."
        elif self.bestial_fail:
            result = f"{self.successes} success(es). However, if this fails the result is a Beastial Failure."
        else:
            result = f"{self.successes} success(es)."

        successes = [":green_square:" for _ in len(self.successes)]
        fails = [":grey_square:" for _ in len(self.dice_pool - self.successes)]

        formatted_squares = successes + fails
        formatted_squares = random.shuffle(formatted_squares)

        return {"overall_result": result, "squares": "".join(formatted_squares)}
