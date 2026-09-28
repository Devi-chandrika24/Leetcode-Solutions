class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        \"\"\"
        Do not return anything, modify nums in-place instead.
        Time Complexity: O(n)
        Space Complexity: O(1)
        \"\"\"
        n = len(nums)
        # 1. Find the first decreasing element from the end
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
            
        if i >= 0:
            # 2. Find the element just larger than nums[i] from the end
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            # Swap them
            nums[i], nums[j] = nums[j], nums[i]
            
        # 3. Reverse the elements after index i
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
