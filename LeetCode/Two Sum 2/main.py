class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        f = 0
        l = len(numbers) - 1
        while f < l:
            summ = numbers[f] + numbers[l]

            if summ == target:
                return [f+1,l+1]
            elif summ > target:
                l -= 1
            else:
                f += 1
