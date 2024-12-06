from typing import Any
from automation.get_input import get_input

input: str = get_input(2024, 5)


class Rule:
    def __init__(self, num: str, not_exceed: list[str]):
        self.num = num
        self.not_exceed = not_exceed

def get_rule(rules: list[Rule], num: str) -> Rule | None:
    for rule in rules:
        if rule.num == num:
            return rule
    return None


def main() -> Any:
    page_ordering_rules, updates = input.split("\n\n")
    rules: list[Rule] = []
    invalid_updates: list[list[str]] = []

    for por in page_ordering_rules.split("\n"):
        num, not_exceed = por.split("|")

        fr = get_rule(rules, num)
        if fr == None:
            rules.append(Rule(num, [not_exceed]))
        else:
            fr.not_exceed.append(not_exceed)

    for update in updates.split("\n"):
        nums: list[str] = update.split(",")
        is_valid = True

        for i, num in enumerate(nums):
            rule = get_rule(rules, num)
            if rule == None:
                continue

            if any(item in nums[:i] for item in rule.not_exceed):
                is_valid = False
                break

        if not is_valid:
            invalid_updates.append(nums)

    return sum(int(vu[len(vu)//2]) for vu in invalid_updates)
