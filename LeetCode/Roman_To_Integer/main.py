class Solution:
    def romanToInt(self, s: str) -> int:
        roman = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        result = 0
        for i in range(len(s)-1):
            a=s[i]
            b=s[i+1]
            if roman[a] < roman[b]:
                result = result - roman[a]
            else:
                result = result + roman[a]
        result=result+roman[s[-1]]
        return result
            