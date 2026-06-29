# 题目：差的绝对值为 K 的数对数目 (LeetCode 2006)
# 难度：简单
# 标签：数组、哈希表、计数
#
# 题目需求：
#   给你一个整数数组 nums 和一个整数 k，请你返回数对 (i, j) 的数目，
#   满足 i < j 且 |nums[i] - nums[j]| == k。
#
# 约束条件：
#   1. 1 <= nums.length <= 200
#   2. 1 <= nums[i] <= 100
#   3. 1 <= k <= 99
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
from collections import Counter
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（两层循环）
    # 思路：枚举所有 i < j 的数对，直接判断 |nums[i] - nums[j]| 是否等于 k。
    # 时间复杂度：O(n^2) —— n*(n-1)/2 个数对。
    # 空间复杂度：O(1) —— 常数额外空间。
    # ----------------------------------------------------------
    def countKDifference_brute_force(self, nums: List[int], k: int) -> int:
        n = len(nums)
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(nums[i] - nums[j]) == k:
                    count += 1
        return count

    # ----------------------------------------------------------
    # 解法二：哈希表一次遍历法
    # 思路：
    #   1. 遍历数组，对当前数 num：
    #      - 在已见过的数中查找 num - k 和 num + k 出现了几次，加到结果
    #      - 因为 i < j 的约束，当前数的下标一定大于已见过数的下标，天然满足
    #   2. 将 num 加入哈希表
    # 时间复杂度：O(n) —— 每个元素访问一次，哈希表查找 O(1)。
    # 空间复杂度：O(n) —— 哈希表。
    # ----------------------------------------------------------
    def countKDifference_hash_map(self, nums: List[int], k: int) -> int:
        freq: dict = {}
        count = 0
        for num in nums:
            count += freq.get(num - k, 0)
            count += freq.get(num + k, 0)
            freq[num] = freq.get(num, 0) + 1
        return count

    # ----------------------------------------------------------
    # 解法三：Counter 频率法（最优、最简洁）
    # 思路：
    #   1. 先统计每个数字出现的频率
    #   2. 对每个数字 x，差为 k 的配对数 = freq[x] * freq[x + k]
    #      即 x 出现的次数乘以 x+k 出现的次数（笛卡尔积）
    #   3. 注意只查 x + k（不查 x - k），避免重复计数
    # 时间复杂度：O(n) —— 统计频率 O(n)，遍历不同值 O(m) ≤ O(n)。
    # 空间复杂度：O(n) —— Counter。
    # ----------------------------------------------------------
    def countKDifference_counter(self, nums: List[int], k: int) -> int:
        freq = Counter(nums)
        count = 0
        for x in freq:
            if x + k in freq:
                count += freq[x] * freq[x + k]
        return count


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.countKDifference_brute_force),
        ("哈希表法",   sol.countKDifference_hash_map),
        ("Counter法",  sol.countKDifference_counter),
    ]

    test_cases = [
        ([1, 2, 2, 1],     1,  4),
        ([1, 3],           3,  0),
        ([3, 2, 1, 5, 4],  2,  3),
        ([1],              1,  0),
        ([1, 2, 3, 4, 5],  1,  4),
        ([10, 20, 30, 40], 10, 3),
        ([1, 4, 4, 1],     3,  4),
        ([1, 100],         99, 1),
        ([3, 3, 6, 6],     3,  4),
    ]

    for name, fn in methods:
        all_pass = True
        for nums, k_val, expected in test_cases:
            result = fn(list(nums), k_val)
            if result != expected:
                print(f"  ✗ {name}: nums={nums}, k={k_val}, got={result}, expected={expected}")
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
        ("暴力法 O(n^2)",   sol.countKDifference_brute_force),
        ("哈希表法 O(n)",   sol.countKDifference_hash_map),
        ("Counter法 O(n)",  sol.countKDifference_counter),
    ]

    sizes = [200, 1_000, 5_000, 10_000, 50_000, 100_000]
    repeat = 10

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(1, 100) for _ in range(size)]
        k_val = random.randint(1, 99)

        for name, fn in methods:
            if "暴力" in name and size > 5_000:
                print(f"{size:>10} | {name:<20} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums), k_val)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            print(f"{size:>10} | {name:<20} | {avg_ms:>15.3f} | {'':<20}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                    |
|------------|-----------|-----------|-----------------------------------------|
| 暴力法     | O(n^2)    | O(1)      | 两层循环，n 较大时不可用                  |
| 哈希表法   | O(n)      | O(n)      | 一次遍历，边查边加，天然满足 i<j          |
| Counter法  | O(n)      | O(n)      | 统计频率后乘法计算，最简洁直观            |

Counter 法的核心公式：
  - 对每个值 x，差为 k 的配对数 = freq[x] * freq[x + k]
  - 这是乘法原理：从 x 中选 1 个，从 x+k 中选 1 个
  - 只查 x + k（不查 x - k），保证每对只计一次

哈希表法为什么同时查 num-k 和 num+k？
  - 因为遍历到 num 时，前面已见过的数可能比 num 大（差为 -k）或小（差为 k）
  - 而「前面的数」都已在 freq 里，两种情况都要查
  - 遍历顺序天然保证 i<j，不会重复计数
""")


if __name__ == "__main__":
    print("=== 差的绝对值为 K 的数对数目：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
