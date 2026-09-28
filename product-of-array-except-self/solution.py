class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        \"\"\"
        Time Complexity: O(n)
        Space Complexity: O(1) (excluding output array)
        \"\"\"
        n = len(nums)
        res = [1] * n
        
        # Calculate left products
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]
            
        # Calculate right products and multiply
        postfix = 1
        for i in range(n - 1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
            
        return res
