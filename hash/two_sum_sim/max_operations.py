# 题目：K 和数对的最大数目 (LeetCode 1679)
# 难度：中等
# 标签：数组、哈希表、双指针、排序
#
# 题目需求：
#   给你一个整数数组 nums 和一个整数 k。
#   每一步操作中，你需要从数组中选出和为 k 的两个整数，并将它们移出数组。
#   返回你可以对数组执行的最大操作数。
#
# 约束条件：
#   1. 1 <= nums.length <= 10^5
#   2. 1 <= nums[i] <= 10^9
#   3. 1 <= k <= 10^9
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
from collections import Counter
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（两层循环 + 标记移除）
    # 思路：枚举所有可能的数对 (i, j)，找到和为 k 的配对后将两个位置标记为已使用。
    # 时间复杂度：O(n^2) —— 最坏情况下两层循环。
    # 空间复杂度：O(n) —— used 标记数组。
    # ----------------------------------------------------------
    def maxOperations_brute_force(self, nums: List[int], k: int) -> int:
        n = len(nums)
        used = [False] * n
        count = 0
        for i in range(n):
            if used[i]:
                continue
            for j in range(i + 1, n):
                if not used[j] and nums[i] + nums[j] == k:
                    used[i] = used[j] = True
                    count += 1
                    break
        return count

    # ----------------------------------------------------------
    # 解法二：排序 + 双指针法
    # 思路：
    #   1. 先排序数组 O(n log n)
    #   2. 左指针 left 从 0 开始，右指针 right 从末尾开始
    #   3. 若 nums[left] + nums[right] == k，配对成功，两指针同时内移，count += 1
    #      若和 < k，左指针右移（需要更大的数）
    #      若和 > k，右指针左移（需要更小的数）
    # 时间复杂度：O(n log n) —— 排序主导。
    # 空间复杂度：O(1) 或 O(n) —— 取决于排序是否使用额外空间。
    # ----------------------------------------------------------
    def maxOperations_two_pointers(self, nums: List[int], k: int) -> int:
        nums.sort()
        left, right = 0, len(nums) - 1
        count = 0
        while left < right:
            s = nums[left] + nums[right]
            if s == k:
                count += 1
                left += 1
                right -= 1
            elif s < k:
                left += 1
            else:
                right -= 1
        return count

    # ----------------------------------------------------------
    # 解法三：哈希表法（一次遍历）—— 最优解法
    # 思路：
    #   1. 用字典 freq 记录「当前还未被配对的值」的剩余次数
    #   2. 遍历每个数 num：
    #      - 若 k - num 在 freq 中且剩余次数 > 0，说明之前见过可配对的数，
    #        配对成功：count += 1，freq[k - num] -= 1
    #      - 否则将 num 加入 freq，等待后续匹配
    # 时间复杂度：O(n) —— 每个元素只被访问一次。
    # 空间复杂度：O(n) —— 哈希表最多存 n 个元素。
    # ----------------------------------------------------------
    def maxOperations_hash_map(self, nums: List[int], k: int) -> int:
        freq: dict = {}
        count = 0
        for num in nums:
            comp = k - num
            if freq.get(comp, 0) > 0:
                count += 1
                freq[comp] -= 1
            else:
                freq[num] = freq.get(num, 0) + 1
        return count


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",    sol.maxOperations_brute_force),
        ("双指针法",  sol.maxOperations_two_pointers),
        ("哈希表法",  sol.maxOperations_hash_map),
    ]

    test_cases = [
        ([1, 2, 3, 4],          5,  2),
        ([3, 1, 3, 4, 3],       6,  1),
        ([1, 1, 1, 1],          2,  2),
        ([1, 2, 3, 4, 5, 6],    7,  3),
        ([2, 2, 2, 3, 1, 1],    4,  2),
        ([1],                   2,  0),
        ([3, 5, 1, 5],          2,  0),
        ([4, 4, 1, 3, 1, 3, 2], 5,  3),
        ([5, 5, 5, 5],          10, 2),
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 9, 4),
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
        ("暴力法 O(n^2)",      sol.maxOperations_brute_force),
        ("双指针法 O(n log n)", sol.maxOperations_two_pointers),
        ("哈希表法 O(n)",       sol.maxOperations_hash_map),
    ]

    sizes = [100, 1_000, 5_000, 10_000, 50_000, 100_000]
    repeat = 5

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(1, 1_000_000_000) for _ in range(size)]
        k_val = random.randint(1, 2_000_000_000)

        for name, fn in methods:
            if "暴力" in name and size > 1_000:
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
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                   |
|------------|-----------|-----------|----------------------------------------|
| 暴力法     | O(n^2)    | O(n)      | 两层循环，n 较大时不可用                 |
| 双指针法   | O(n log n)| O(1)/O(n) | 排序后左右夹逼，实现简单、无需额外结构     |
| 哈希表法   | O(n)      | O(n)      | 一次遍历边查边配，时间最优，推荐解法       |

哈希表法的关键技巧：
  - freq 字典维护的是「还未配对的剩余值」→ 不是所有元素的频率
  - 遇到 num 时：若 k-num 剩余次数 > 0，说明之前已经放进 freq 等待配对，直接计数 +1 并减少 freq[k-num]
  - 否则把 num 加入 freq，等待后续元素来配对它
  - 这样天然保证了「每对只用一次」和「元素不被重复使用」
  - 这种「先查再加」的模式是经典的两数之和处理思路
""")


if __name__ == "__main__":
    print("=== K 和数对的最大数目：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
