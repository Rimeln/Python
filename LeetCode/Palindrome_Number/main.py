class Solution:
    def isPalindrome(self, x: int) -> bool:
        x_str=str(x)
        x_rev=x_str[::-1]
        if x_rev!=x_str:
            return False
        return True