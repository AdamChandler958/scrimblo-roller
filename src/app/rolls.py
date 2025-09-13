import random
import re

class DiceRoll:
    def __init__(self, request: str):
        self.request = request
        self.num_dice = 0
        self.diet_type = 0
        self.keep_op = None
        self.keep_val = 0
        self.modifier_op = None
        self.modifier_val = 0
        self.comment = "Dice Roll Results."
        self.all_rolls = []
        self.kept_rolls = []
        self.total = 0
        self.error = None

    def parse_request(self):
        pattern = re.compile(r"^(\d*)d(\d+)(?:([kK][hH]|[kK][lL])(\d+))?(?:([+-])(\d+))?\s*(.*)?$")
        match = pattern.match(self.request)

        if not match:
            self.error = "Invalid format."
            return False


        num_dice_str, die_type_str, self.keep_op, keep_val_str, self.modifier_op, modifier_val_str, comment = match.groups()

        self.num_dice = int(num_dice_str) if num_dice_str else 1
        self.die_type = int(die_type_str)
        self.keep_val = int(keep_val_str) if keep_val_str else 0
        self.modifier_val = int(modifier_val_str) if modifier_val_str else 0
        self.comment = comment
        self.request = self.request.removesuffix(self.comment).strip(' ')

        return True

    def perform_roll(self):
        if not self.parse_request():
            return
        
        self.all_rolls = [random.randint(1, self.die_type) for _ in range(self.num_dice)]

        if self.keep_op:
            if "h" in self.keep_op.lower():
                self.kept_rolls = sorted(self.all_rolls, reverse=True)[:self.keep_val]
            elif "l" in self.keep_op.lower():
                self.kept_rolls = sorted(self.all_rolls)[:self.keep_val]
        else:
            self.kept_rolls = self.all_rolls

        self.total = sum(self.kept_rolls)

        if self.modifier_op == "+":
            self.total += self.modifier_val
        elif self.modifier_op == "-":
            self.total -= self.modifier_val

    def _get_formatted_rolls(self) -> str:
        formatted_parts = []
        kept_rolls_copy = list(self.kept_rolls).copy()
        
        for roll in self.all_rolls:
            if roll in kept_rolls_copy:
                formatted_parts.append(str(roll))
                kept_rolls_copy.remove(roll) 
            else:
                formatted_parts.append(f"~~{roll}~~")
                
        return f"[{', '.join(formatted_parts)}]"
    
    def get_result(self) -> dict:
        if self.error:
            return {"error": self.error}
            
        return {
            "all_rolls": self.all_rolls,
            "kept_rolls": self.kept_rolls,
            "total": self.total,
            "expression": self.request,
            "formatted_rolls": self._get_formatted_rolls(),
            "comment": self.comment
        }
