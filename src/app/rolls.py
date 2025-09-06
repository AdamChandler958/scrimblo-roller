import random
import re

def dice_roll(dice_size: str) -> int:

    val = random.randint(1, int(dice_size))
    return val

# /roll 3d20+2

# [8, 16, 20]+2 = 46

def parse_dice_string(request: str) -> tuple[str, int]:
    pattern = re.compile(r"(\d*)d(\d+)(?:([+-])(\d+))?")
    match = pattern.match(request)

    if not match:
        return "Please use either NdN or NdN+M format"

    num_dice_str, die_type_str, modifier_op, modifier_val_str = match.groups()

    roll_list = []
    for _ in range(int(num_dice_str)):
        roll_list.append(dice_roll(die_type_str))

    if modifier_op is not None:
        if modifier_op == "+":
            mod_mult = 1

        else:
            mod_mult = -1

        sum_value = sum(roll_list) + (mod_mult*int(modifier_val_str))
    else:
        sum_value = sum(roll_list)

    roll_strings= [str(roll) for roll in roll_list]
    rolls_display = f"[{', '.join(roll_strings)}]"

    return rolls_display, sum_value

