# 题目：优质数对的数目 (LeetCode 2354)
# 难度：困难
# 标签：位运算、数组、哈希表、二分查找
#
# 题目需求：
#   给你一个下标从 0 开始的正整数数组 nums 和一个正整数 k。
#   如果数对 (num1, num2) 满足：
#     1. num1 和 num2 都在数组 nums 中存在；
#     2. popcount(num1 OR num2) + popcount(num1 AND num2) >= k，
#   则称其为优质数对。返回不同优质数对的数目。
#   注意：(a,b) 与 (b,a) 当 a != b 时视为不同数对；num1 可以等于 num2。
#
# 约束条件：
#   1. 1 <= nums.length <= 10^5
#   2. 1 <= nums[i] <= 10^9
#   3. 1 <= k <= 60
#
# 核心观察（位运算恒等式）：
#   popcount(a OR b) + popcount(a AND b) = popcount(a) + popcount(b)
#   逐位验证：
#     - a=0,b=0 → OR=0, AND=0 → 0 = 0+0
#     - a=0,b=1 → OR=1, AND=0 → 1 = 0+1
#     - a=1,b=0 → OR=1, AND=0 → 1 = 1+0
#     - a=1,b=1 → OR=1, AND=1 → 2 = 1+1
#   因此原条件等价于：popcount(num1) + popcount(num2) >= k
#
# 本文件提供三种解法，并在末尾做对比试验。


from typing import List
from collections import Counter
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（去重后枚举所有有序对）
    # 思路：
    #   1. 对 nums 去重（相同值的数对不计多次）
    #   2. 枚举所有有序对 (x, y)，检查 popcount(x)+popcount(y) >= k
    # 时间复杂度：O(m^2)，m 为去重后元素个数，最坏 m = 10^5 → 10^10 次运算，超时。
    # 空间复杂度：O(m)
    # ----------------------------------------------------------
    def countExcellentPairs_brute_force(self, nums: List[int], k: int) -> int:
        unique = list(set(nums))
        m = len(unique)
        pc = [bin(x).count('1') for x in unique]
        ans = 0
        for i in range(m):
            for j in range(m):
                if pc[i] + pc[j] >= k:
                    ans += 1
        return ans

    # ----------------------------------------------------------
    # 解法二：频率统计 + 后缀和（最优解法）
    # 思路：
    #   1. 去重后，统计每个 popcount 值 c 出现的次数 cnt[c]
    #      由于 nums[i] <= 10^9，popcount 范围为 [1, 30]，cnt 数组长度为 31 即可
    #   2. 预处理后缀和 suffix[c] = sum_{i=c}^{30} cnt[i]，即 popcount >= c 的不同数字个数
    #   3. 对每个可能的 popcount 值 c1，需要 popcount(c2) >= k - c1
    #      贡献数对数 = cnt[c1] * suffix[max(0, k - c1)]
    # 时间复杂度：O(n + 31) = O(n) —— 去重 O(n)，统计 O(n)，计算答案 O(31)。
    # 空间复杂度：O(31) = O(1)
    # ----------------------------------------------------------
    def countExcellentPairs_suffix_sum(self, nums: List[int], k: int) -> int:
        cnt = [0] * 32
        for x in set(nums):
            c = bin(x).count('1')
            cnt[c] += 1

        suffix = [0] * 33
        for c in range(30, -1, -1):
            suffix[c] = suffix[c + 1] + cnt[c]

        ans = 0
        for c1 in range(31):
            if cnt[c1] == 0:
                continue
            need = k - c1
            if need <= 0:
                ans += cnt[c1] * suffix[0]
            elif need <= 30:
                ans += cnt[c1] * suffix[need]
        return ans

    # ----------------------------------------------------------
    # 解法三：频率统计 + 双指针
    # 思路：
    #   1. 去重后，把所有 popcount 值放入一个排序数组 bits
    #   2. 用双指针（或排序后二分）计算满足 b1 + b2 >= k 的有序对数目
    #      具体做法：将 bits 排序后，对每个 bits[i] 用二分/双指针找到最小 j
    #      使得 bits[i] + bits[j] >= k，答案累加 m - j
    #   实际上利用 popcount 最多 31 种取值，可以用频率数组 + 双指针更高效：
    #      让左指针 l 从 0 开始，右指针 r 从 30 开始，累加贡献
    # 时间复杂度：O(n + 31) = O(n)
    # 空间复杂度：O(31) = O(1)
    # ----------------------------------------------------------
    def countExcellentPairs_two_pointers(self, nums: List[int], k: int) -> int:
        cnt = [0] * 32
        for x in set(nums):
            cnt[bin(x).count('1')] += 1

        ans = 0
        r = 30
        window_sum = 0
        for l in range(31):
            while r >= 0 and l + r >= k:
                window_sum += cnt[r]
                r -= 1
            ans += cnt[l] * window_sum
        return ans


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.countExcellentPairs_brute_force),
        ("后缀和法",   sol.countExcellentPairs_suffix_sum),
        ("双指针法",   sol.countExcellentPairs_two_pointers),
    ]

    test_cases = [
        ([1, 2, 3, 1],          3,  5),
        ([5, 1, 1],             10, 0),
        ([1, 2, 4, 8, 16, 32],  2,  36),   # 每个 popcount=1，6个元素，1+1=2>=2，全部 6*6=36 对均满足
        ([42353123, 12312, 123],1,  9),    # 3个不同元素，k=1 全部满足 3*3=9
        ([1, 1, 1, 1],          2,  1),    # 去重后 {1}, popcount(1)=1, 1+1=2>=2 → 1对
        ([3, 3, 3],             4,  1),    # popcount(3)=2, 2+2=4>=4 → 1对
        ([3, 3, 3],             5,  0),    # 2+2=4<5 → 0
        ([1, 2],                3,  0),    # 1+1=2<3
        ([1, 2, 3],             3,  5),    # same as example 1 without duplicate 1
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
        ("暴力法 O(m^2)",     sol.countExcellentPairs_brute_force),
        ("后缀和法 O(n)",     sol.countExcellentPairs_suffix_sum),
        ("双指针法 O(n)",     sol.countExcellentPairs_two_pointers),
    ]

    sizes = [100, 1_000, 5_000, 10_000, 50_000, 100_000]
    repeat = 10

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(1, 10**9) for _ in range(size)]
        k_val = random.randint(1, 60)

        for name, fn in methods:
            if "暴力" in name and size > 5_000:
                print(f"{size:>10} | {name:<20} | {'> 1000':>15} | {'跳过（太慢）':<20}")
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
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                       |
|------------|-----------|-----------|--------------------------------------------|
| 暴力法     | O(m^2)    | O(m)      | 去重后枚举所有有序对，m=10^5 时不可用         |
| 后缀和法   | O(n)      | O(1)      | popcount 频率统计 + 后缀和，最优推荐解法      |
| 双指针法   | O(n)      | O(1)      | popcount 频率统计 + 双指针累加，同样 O(n)     |

核心公式推导：popcount(a OR b) + popcount(a AND b) = popcount(a) + popcount(b)
  按二进制每一位独立分析：
    该位 a b | OR | AND | OR+AND | a+b
    ---------+----+-----+--------+-----
      0  0   | 0  |  0  |   0    |  0
      0  1   | 1  |  0  |   1    |  1
      1  0   | 1  |  0  |   1    |  1
      1  1   | 1  |  1  |   2    |  2
  每一位上 OR+AND 的 1 个数恰好等于 a+b 的 1 个数，逐位相加等式成立。
  因此原条件 popcount(OR) + popcount(AND) >= k 等价于 popcount(a)+popcount(b)>=k。

为什么必须先去重？
  - 题目问的是「不同」优质数对的数目，(a,b) 和 (a,b) 是同一个数对（值相同）。
  - 即使某个值在 nums 中出现多次，它贡献的数对也只算一次。
  - 但 (a,b) 和 (b,a) 当 a!=b 时是不同的有序对，都要计入。

为什么空间是 O(1)？
  - nums[i] <= 10^9，二进制最多 30 位，popcount 取值范围 1~30。
  - 频率数组 cnt 只需要大小 32，是常数空间。
""")


if __name__ == "__main__":
    print("=== 优质数对的数目：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
