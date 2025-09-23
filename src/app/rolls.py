import random 
import re

class DiceRoll:
    """
    The DiceRoll object handles the logic of dice rolls as well as formatted and calculating totals.

    Args:
        roll_string (str): The string representing the dice roll request.
    """

    def __init__(self, request: str):
        self.request = request
        self.comment = "Dice Roll Results."
        self.rolls = []
        self.total = 0
        self.error = None
        self.expression = None

    def parse_request(self):
        """
        Parses a dice roll request string to extract all components.

        This function supports rolling any number of dice of any size, with optional
        modifiers, keep-highest/keep-lowest logic, and an attached comment.

        Returns:
            A boolean for the validity of the request

        Example Usage:
            - `2d20+5`: Roll two 20-sided dice and add 5.
            - `3d6kh2`: Roll three 6-sided dice and keep the 2 highest results.
            - `d10-3`: Roll one 10-sided die and subtract 3.
            - `10`: A simple modifier of 10.
            - `2d4-1+2d8 This is a comment`: Multiple dice rolls and a comment.

        The request string is parsed according to the following components:

        | Component       | Description                                                     
        |-----------------|-----------------------------------------------------------------
        | `Number of Dice`| The number of dice to roll (optional, defaults to 1 if omitted).
        | `Dice Size`     | The number of sides on the die.
        | `Modifier`      | A number to add or subtract from the total roll.
        | `Keep Highest`  | Keeps a specified number of the highest rolls.
        | `Keep Lowest`   | Keeps a specified number of the lowest rolls.
        | `Comment`       | A string of text after the roll expression.
        """

        roll_pattern = re.compile(r"([+-]?)\s*(?:(\d*)d(\d+)(?:([kK][hH]|[kK][lL])(\d+))?|(\d+))")

        comment_pattern = re.compile(r"^(.*?)(?:\s+(.*))?$")
        
        match = comment_pattern.match(self.request)
        main_request = match.group(1)
        self.expression = main_request
        self.comment = match.group(2).removesuffix(' ') if match.group(2) else "Dice Roll Results."

        components = roll_pattern.findall(main_request)
        
        if not components:
            self.error = "Invalid format."
            return False
        
        self.rolls = []
        for sign, num_dice_str, die_type_str, keep_op, keep_val_str, modifier_val_str in components:
            component = {
                "sign": sign if sign else "+",
                "expression": "", 
                "num_dice": 0,
                "die_type": 0,
                "keep_op": None,
                "keep_val": "",
                "modifier_val": 0,
                "all_rolls": [],
                "kept_rolls": [],
                "total": 0,
                "formatted_rolls": ""
            }

            if die_type_str:
                component["num_dice"] = int(num_dice_str) if num_dice_str else 1
                component["die_type"] = int(die_type_str)
                component["expression"] = f"{component['num_dice']}d{component['die_type']}"
                if keep_op:
                    component["keep_op"] = keep_op
                    component["keep_val"] = int(keep_val_str)
                    component["expression"] += f"{keep_op}{component['keep_val']}"
            else:
                component["modifier_val"] = int(modifier_val_str)
                component["expression"] = str(component["modifier_val"])

            self.rolls.append(component)

        return True

    def perform_roll(self):
        """
        Based on the components extracted from DiceRoll.parse_request() each of the desired dice are rolled, logic applied
        and total calculated.

        After the dice have been rolled and values calculated a single call is made to format the output string for display
        purposes.
        """

        if not self.parse_request():
            return
        
        grand_total = 0
        
        for roll_data in self.rolls:
            if roll_data["die_type"] > 0:
                all_rolls = [random.randint(1, roll_data["die_type"]) for _ in range(roll_data["num_dice"])]
                roll_data["all_rolls"] = all_rolls
                
                if roll_data["keep_op"]:
                    if "h" in roll_data["keep_op"].lower():
                        kept_rolls = sorted(all_rolls, reverse=True)[:roll_data["keep_val"]]
                    elif "l" in roll_data["keep_op"].lower():
                        kept_rolls = sorted(all_rolls)[:roll_data["keep_val"]]
                    roll_data["kept_rolls"] = kept_rolls
                else:
                    roll_data["kept_rolls"] = all_rolls

                component_total = sum(roll_data["kept_rolls"])
                roll_data["total"] = component_total
            else:

                component_total = roll_data["modifier_val"]
                roll_data["total"] = component_total


            if roll_data["sign"] == "-":
                grand_total -= component_total
            else:
                grand_total += component_total

            roll_data["formatted_rolls"] = self._get_formatted_rolls(roll_data)

        self.total = grand_total

    def _get_formatted_rolls(self, roll_data) -> str:
        if not roll_data["all_rolls"]:
            return ""

        formatted_parts = []
        kept_rolls_copy = list(roll_data["kept_rolls"]).copy()
        
        for roll in roll_data["all_rolls"]:
            if roll in kept_rolls_copy:
                formatted_parts.append(str(roll))
                kept_rolls_copy.remove(roll) 
            else:
                formatted_parts.append(f"~~{roll}~~")
                
        return f"[{', '.join(formatted_parts)}]"
    
    def get_result(self) -> dict:
        """
        Retrieves the dice roll results and returns the current state of the DiceRoll object.

        Returns:
            result (dict): The formatted form of the results of the initial roll request.
        """

        if self.error:
            return {"error": self.error}
            
        formatted_expression = []

        for roll_data in self.rolls:
            if roll_data['die_type'] > 0:
                component_string = f" {roll_data['sign']} {roll_data['num_dice']}d{roll_data['die_type']}{roll_data['keep_op'] if roll_data['keep_op'] else ""}{roll_data['keep_val']}: {roll_data['formatted_rolls']} ({roll_data['total']})"
            else:
                component_string = f" {roll_data['sign']} {roll_data['modifier_val']}"
            formatted_expression.append(component_string)

        result = {
            "grand_total": self.total,
            "expression": self.expression,
            "comment": self.comment,
            "components": self.rolls, 
            "formatted_result_string": " ".join(formatted_expression)
        }
        result["formatted_result_string"] = result["formatted_result_string"][2:]

        return result