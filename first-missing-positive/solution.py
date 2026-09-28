class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        \"\"\"
        Time Complexity: O(n)
        Space Complexity: O(1)
        \"\"\"
        n = len(nums)
        # Place each number in its right place (e.g., 1 at index 0, 2 at index 1)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                # Swap nums[i] with nums[nums[i] - 1]
                nums[nums[i] - 1], nums[i] = nums[i], nums[nums[i] - 1]
        
        # Find the first missing positive
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
                
        return n + 1
