import random


class VtMRolls:
    def __init__(self, dice_pool: int, hunger: int = None):
        self.dice_pool = dice_pool
        self.hunger = hunger

        self.bestial_fail = False
        self.messy_critical = False

        self.successes = 0
        self.crit_successes = 0

        self.crit_fails = 0

        self.key_val: dict[int, str] = {}

    def generate(self):
        for i in range(self.dice_pool):
            val = random.randint(1, 10)

            is_hunger = self.hunger is not None and i < self.hunger

            # Change to count hunger dice into a different section
            if val == 1:
                self.crit_fails += 1
                self.key_val[i] = ":red_square:"
                if is_hunger:
                    self.bestial_fail = True

            elif val == 10:
                self.crit_successes += 1
                self.key_val[i] = ":white_check_mark:"
                if is_hunger:
                    self.messy_critical = True

            elif val > 5:
                self.successes += 1
                self.key_val[i] = ":green_square:"

            else:
                self.key_val[i] = ":black_large_square:"

    def _calc_total(self):
        return (
            self.successes
            + (self.crit_successes % 2)
            + 4 * (self.crit_successes // 2)
            + -self.crit_fails
        )

    def format_result(self):
        total = self._calc_total()
        if self.messy_critical:
            result = "Messy Critical!"
        elif total <= 0:
            result = "Failure."
        elif self.bestial_fail:
            result = f"{total} success(es). However, if this fails the result is a Beastial Failure."
        else:
            result = f"{total} success(es)."

        return {"overall_result": result, "squares": "".join(self.key_val.values())}
