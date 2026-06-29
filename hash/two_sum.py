# 题目：两数之和 (LeetCode 1)
# 难度：简单
# 标签：哈希表、数组
#
# 题目需求：
#   给定一个整数数组 nums 和一个整数目标值 target，
#   请你在该数组中找出和为目标值 target 的那两个整数，
#   并返回它们的数组下标。
#
# 约束条件：
#   1. 你可以假设每种输入只会对应一个答案。
#   2. 你不能重复使用相同的元素（即同一个下标不能用两次）。
#   3. 你可以按任意顺序返回答案。
#   4. 2 <= nums.length <= 10^4
#   5. -10^9 <= nums[i] <= 10^9
#   6. -10^9 <= target <= 10^9
#   7. 只会存在一个有效答案。
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（两层循环）
    # 思路：枚举所有可能的数对 (i, j)，检查 nums[i] + nums[j] 是否等于 target。
    # 时间复杂度：O(n^2) —— 最坏情况下要检查 n*(n-1)/2 对数。
    # 空间复杂度：O(1) —— 只使用常数额外空间。
    # ----------------------------------------------------------
    def twoSum_brute_force(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

    # ----------------------------------------------------------
    # 解法二：双指针法（排序 + 保留原始下标）
    # 思路：
    #   1. 把 nums 转成 (数值, 原始下标) 的列表
    #   2. 按数值大小排序
    #   3. 左指针从 0 开始，右指针从末尾开始，向中间夹逼
    #   4. 若和 == target，返回二者原始下标；
    #      若和 < target，左指针右移（需要更大的数）；
    #      若和 > target，右指针左移（需要更小的数）
    # 时间复杂度：O(n log n) —— 排序占主要时间。
    # 空间复杂度：O(n) —— 存储 (数值, 下标) 对。
    # 注意：排序后原始顺序被打乱，因此必须保留原始下标才能返回正确答案。
    # ----------------------------------------------------------
    def twoSum_two_pointers(self, nums: List[int], target: int) -> List[int]:
        nums_with_index = [(num, idx) for idx, num in enumerate(nums)]
        nums_with_index.sort(key=lambda x: x[0])

        left, right = 0, len(nums_with_index) - 1
        while left < right:
            current_sum = nums_with_index[left][0] + nums_with_index[right][0]
            if current_sum == target:
                return [nums_with_index[left][1], nums_with_index[right][1]]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return []

    # ----------------------------------------------------------
    # 解法三：哈希表法（一次遍历）—— 最优解法
    # 思路：用字典存 {数值: 下标}，遍历当前元素时看 target - nums[i] 是否已在字典里。
    # 时间复杂度：O(n) —— 每个元素只被访问一次，哈希表查找 O(1)。
    # 空间复杂度：O(n) —— 哈希表最多存 n 个元素。
    # ----------------------------------------------------------
    def twoSum_hash_table(self, nums: List[int], target: int) -> List[int]:
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",   sol.twoSum_brute_force),
        ("双指针法", sol.twoSum_two_pointers),
        ("哈希表法", sol.twoSum_hash_table),
    ]

    test_cases = [
        ([2, 7, 11, 15], 9,         [0, 1]),
        ([3, 2, 4],       6,        [1, 2]),
        ([3, 3],          6,        [0, 1]),
        ([-1, -2, -3, -4, -5], -8,  [2, 4]),
        ([-3, 4, 3, 90],  0,        [0, 2]),
        ([1, 5, 7, 2, 9], 11,       [3, 4]),
    ]

    for name, fn in methods:
        for nums, target, _ in test_cases:
            result = fn(nums, target)
            assert len(result) == 2 and result[0] != result[1] \
                and nums[result[0]] + nums[result[1]] == target, \
                f"{name} 失败: nums={nums}, target={target}, got={result}"
        print(f"  ✓ {name}: 所有 {len(test_cases)} 个测试用例通过")


# ============================================================
# 性能对比试验
# ============================================================
def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验（测量每种解法在不同规模数据上的运行时间）")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("暴力法 O(n^2)",      sol.twoSum_brute_force),
        ("双指针法 O(n log n)", sol.twoSum_two_pointers),
        ("哈希表法 O(n)",      sol.twoSum_hash_table),
    ]

    sizes = [100, 1_000, 5_000, 10_000, 20_000]
    repeat = 5  # 每个测试重复取平均

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)  # 固定种子让结果可复现
        nums = [random.randint(-1_000_000, 1_000_000) for _ in range(size)]
        i, j = size // 3, 2 * size // 3
        target = nums[i] + nums[j]  # 保证解存在

        results_for_size = {}
        for name, fn in methods:
            if "暴力" in name and size > 5_000:
                print(f"{size:>10} | {name:<20} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(nums, target)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            results_for_size[name] = avg_ms
            print(f"{size:>10} | {name:<20} | {avg_ms:>15.3f} | {'':<20}")

        if len(results_for_size) == 3:
            bf_time = results_for_size["暴力法 O(n^2)"]
            hs_time = results_for_size["哈希表法 O(n)"]
            if bf_time > 0 and hs_time > 0:
                print(f"           | {'  -> 哈希表比暴力法快':<20} | {bf_time / hs_time:>15.2f}x | {f'(n={size})':<20}")


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                 |
|------------|-----------|-----------|--------------------------------------|
| 暴力法     | O(n^2)    | O(1)      | 最简单但最慢，n 大时不可用            |
| 双指针法   | O(n log n)| O(n)      | 需要排序，且必须保留原始下标          |
| 哈希表法   | O(n)      | O(n)      | 时间最优，此题的标准推荐解法          |

为什么哈希表最优？
  - 利用哈希表 O(1) 查找的特性，把"找另一个数"从 O(n) 降到 O(1)
  - 只需遍历数组一次，无需排序，适合流数据场景
  - 注意：本题要求返回下标，所以双指针法必须保留原始下标（否则排序后就丢了）
""")


if __name__ == "__main__":
    print("=== 两数之和：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
