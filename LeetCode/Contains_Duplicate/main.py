class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        s = sorted(nums)
        for i in range(0,len(nums)-1):
            if s[i] == s[i+1]:
                return True
        return False
        