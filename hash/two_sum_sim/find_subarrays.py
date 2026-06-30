# 题目：和相等的子数组 (LeetCode 2395)
# 难度：简单
# 标签：数组、哈希表、排序
#
# 题目需求：
#   给你一个下标从 0 开始的整数数组 nums，判断是否存在两个长度为 2 的子数组，
#   它们的和相等，且起始位置下标不同。存在返回 true，否则返回 false。
#
# 约束条件：
#   1. 2 <= nums.length <= 1000
#   2. -10^9 <= nums[i] <= 10^9
#
# 核心转化：
#   长度为 2 的子数组 [nums[i], nums[i+1]] 的和就是 nums[i] + nums[i+1]。
#   共有 n-1 个这样的和（i 取 0,1,...,n-2）。
#   问题等价于：这 n-1 个相邻和中是否存在重复值？
#
# 本文件提供四种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（双重循环）
    # 思路：
    #   枚举所有起始位置对 (i, j)，其中 0 <= i < j <= n-2，
    #   比较 nums[i]+nums[i+1] 与 nums[j]+nums[j+1] 是否相等。
    # 时间复杂度：O(n^2) —— (n-1)(n-2)/2 对比较。
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def findSubarrays_brute_force(self, nums: List[int]) -> bool:
        n = len(nums)
        for i in range(n - 1):
            s_i = nums[i] + nums[i + 1]
            for j in range(i + 1, n - 1):
                if nums[j] + nums[j + 1] == s_i:
                    return True
        return False

    # ----------------------------------------------------------
    # 解法二：哈希集合法（一次遍历，推荐解法）
    # 思路：
    #   遍历每个相邻和 s = nums[i] + nums[i+1]：
    #   - 若 s 已在集合中，说明之前出现过相同的和，返回 true
    #   - 否则将 s 加入集合
    #   遍历结束未找到重复则返回 false
    # 时间复杂度：O(n) —— 一次遍历，集合查找/插入 O(1) 均摊。
    # 空间复杂度：O(n) —— 集合最多存 n-1 个和。
    # ----------------------------------------------------------
    def findSubarrays_hash_set(self, nums: List[int]) -> bool:
        seen = set()
        for i in range(len(nums) - 1):
            s = nums[i] + nums[i + 1]
            if s in seen:
                return True
            seen.add(s)
        return False

    # ----------------------------------------------------------
    # 解法三：排序法
    # 思路：
    #   1. 先计算所有 n-1 个相邻和，放入数组 sums
    #   2. 对 sums 排序
    #   3. 遍历排序后的数组，检查是否存在相邻元素相等
    # 时间复杂度：O(n log n) —— 排序 O(n log n)，线性扫描 O(n)。
    # 空间复杂度：O(n) —— sums 数组。
    # ----------------------------------------------------------
    def findSubarrays_sorting(self, nums: List[int]) -> bool:
        sums = [nums[i] + nums[i + 1] for i in range(len(nums) - 1)]
        sums.sort()
        for i in range(1, len(sums)):
            if sums[i] == sums[i - 1]:
                return True
        return False

    # ----------------------------------------------------------
    # 解法四：字典频率法
    # 思路：
    #   与哈希集合法类似，但用字典记录每个和出现的次数；
    #   一旦某个和出现第二次即返回 true。
    #   逻辑与集合法等价，但字典还可以统计出现频率。
    # 时间复杂度：O(n)
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def findSubarrays_dict(self, nums: List[int]) -> bool:
        freq = {}
        for i in range(len(nums) - 1):
            s = nums[i] + nums[i + 1]
            if s in freq:
                return True
            freq[s] = 1
        return False


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.findSubarrays_brute_force),
        ("哈希集合法", sol.findSubarrays_hash_set),
        ("排序法",     sol.findSubarrays_sorting),
        ("字典法",     sol.findSubarrays_dict),
    ]

    test_cases = [
        ([4, 2, 4],                True),
        ([1, 2, 3, 4, 5],          False),
        ([0, 0, 0],                True),
        ([1, 1],                   False),  # n=2 只有一个子数组，不存在两个
        ([1, 2, 3],                False),  # 和为3,5，无重复
        ([1, 3, 2, 4],             True),   # 和为4,5,6... wait: 1+3=4, 3+2=5, 2+4=6 无重复 → false
    ]

    # Fix the last test case: [1,3,2,4] sums = 4,5,6 (no duplicate), should be False
    test_cases[-1] = ([1, 3, 2, 4], False)

    # Add correct true case
    test_cases.append(([77, 95, 70, 15, 41, 95, 41, 70, 15], True))  # has duplicate sums
    test_cases.append(([-5, 5, -5, 5], True))   # sums: 0, 0, 0 → duplicates
    test_cases.append(([1000000000, -1000000000, 1000000000, -1000000000], True))
    test_cases.append(([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False))

    for name, fn in methods:
        all_pass = True
        for nums, expected in test_cases:
            result = fn(list(nums))
            if result != expected:
                print(f"  ✗ {name}: nums={nums}, got={result}, expected={expected}")
                all_pass = False
        if all_pass:
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
        ("暴力法 O(n^2)",   sol.findSubarrays_brute_force),
        ("哈希集合法 O(n)", sol.findSubarrays_hash_set),
        ("排序法 O(n log n)", sol.findSubarrays_sorting),
        ("字典法 O(n)",     sol.findSubarrays_dict),
    ]

    sizes = [200, 1000, 5000, 10000, 50000, 100000]
    repeat = 100

    print(f"{'数据规模':>10} | {'解法':<22} | {'平均耗时 (μs)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(-10**9, 10**9) for _ in range(size)]

        for name, fn in methods:
            if "暴力" in name and size > 5000:
                print(f"{size:>10} | {name:<22} | {'> 100000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums))
                elapsed = (time.perf_counter() - start) * 1_000_000
                times.append(elapsed)
            avg_us = sum(times) / len(times)
            print(f"{size:>10} | {name:<22} | {avg_us:>15.3f} | {'':<20}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("四种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                     |
|------------|-----------|-----------|------------------------------------------|
| 暴力法     | O(n^2)    | O(1)      | 双重循环比较所有和对，n 较大时不可用        |
| 哈希集合法 | O(n)      | O(n)      | 一次遍历 + 集合查重，最优推荐解法           |
| 排序法     | O(n log n)| O(n)      | 排序后检查相邻元素，思路直观但略慢          |
| 字典法     | O(n)      | O(n)      | 与集合法等价，可额外统计频率               |

为什么问题可以转化为"找重复的相邻和"？
  - 长度为 2 的子数组完全由其起始位置 i 决定，和为 nums[i]+nums[i+1]
  - 两个子数组起始位置不同但和相等 ⇔ 在 n-1 个相邻和中有重复值
  - 这是一个经典的"查重"问题，哈希集合是标准解法

注意边界情况：
  - n = 2 时只有一个长度为 2 的子数组，不可能存在两个不同起始位置的子数组，必返回 false
  - 题目保证 n >= 2，无需处理空数组
""")


if __name__ == "__main__":
    print("=== 和相等的子数组：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
