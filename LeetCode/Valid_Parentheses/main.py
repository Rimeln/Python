class Solution:
    def isValid(self, s: str) -> bool:
        brackets = {')':'(', '}':'{', ']':'['}

        values_brackets = set(brackets.values())
        stack = []

        for c in s:
            if c in values_brackets:
                stack.append(c)
            elif c in brackets:
                if not stack or stack.pop() != brackets[c]:
                    return False
        return not stack
        