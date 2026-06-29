# 题目：找出数组中的所有 K 近邻下标 (LeetCode 2200)
# 难度：简单
# 标签：数组、双指针
#
# 题目需求：
#   给你一个下标从 0 开始的整数数组 nums 和两个整数 key 和 k。
#   K 近邻下标是 nums 中的一个下标 i，并满足至少存在一个下标 j 使得
#   |i - j| <= k 且 nums[j] == key。
#   以列表形式返回按递增顺序排序的所有 K 近邻下标。
#
# 约束条件：
#   1. 1 <= nums.length <= 1000
#   2. 1 <= nums[i] <= 1000
#   3. key 是数组 nums 中的一个整数
#   4. 1 <= k <= nums.length
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力枚举法
    # 思路：
    #   1. 先找出所有 key 所在下标 key_positions
    #   2. 枚举每个 i，遍历 key_positions 检查是否存在 j 使得 |i-j| <= k
    # 时间复杂度：O(n * m) —— m 为 key 出现次数，最坏 O(n^2)。
    # 空间复杂度：O(m) —— 存储 key 位置。
    # ----------------------------------------------------------
    def findKDistantIndices_brute_force(self, nums: List[int], key: int, k: int) -> List[int]:
        key_positions = [j for j, v in enumerate(nums) if v == key]
        result = []
        for i in range(len(nums)):
            for j in key_positions:
                if abs(i - j) <= k:
                    result.append(i)
                    break
        return result

    # ----------------------------------------------------------
    # 解法二：布尔数组标记法（区间标记）
    # 思路：
    #   1. 创建一个长度为 n 的布尔数组 marked，初始全为 False
    #   2. 对每个 key 位置 j，把区间 [max(0, j-k), min(n-1, j+k)] 内的下标全部标记为 True
    #   3. 收集所有被标记为 True 的下标
    # 时间复杂度：O(n * k) 最坏，若所有 key 区间不重叠则 O(n)。
    # 空间复杂度：O(n) —— 标记数组。
    # ----------------------------------------------------------
    def findKDistantIndices_boolean(self, nums: List[int], key: int, k: int) -> List[int]:
        n = len(nums)
        marked = [False] * n
        for j, v in enumerate(nums):
            if v == key:
                start = max(0, j - k)
                end = min(n - 1, j + k)
                for i in range(start, end + 1):
                    marked[i] = True
        return [i for i in range(n) if marked[i]]

    # ----------------------------------------------------------
    # 解法三：差分数组法 —— 最优解法
    # 思路：
    #   1. 对每个 key 位置 j，影响区间为 [L, R] = [max(0, j-k), min(n-1, j+k)]
    #   2. 用差分数组 diff 做区间 +1：diff[L] += 1，diff[R+1] -= 1（注意 R+1 越界）
    #   3. 最后做一次前缀和，前缀和 > 0 的下标即被某个区间覆盖，也就是答案
    #   4. 由于 key 位置本身按顺序递增，可以直接在一次扫描中生成结果列表
    # 时间复杂度：O(n) —— 两次线性扫描。
    # 空间复杂度：O(n) —— 差分数组（可省略，直接生成结果）。
    # ----------------------------------------------------------
    def findKDistantIndices_diff(self, nums: List[int], key: int, k: int) -> List[int]:
        n = len(nums)
        diff = [0] * (n + 1)
        for j, v in enumerate(nums):
            if v == key:
                L = max(0, j - k)
                R = min(n - 1, j + k)
                diff[L] += 1
                diff[R + 1] -= 1

        result = []
        cur = 0
        for i in range(n):
            cur += diff[i]
            if cur > 0:
                result.append(i)
        return result


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",   sol.findKDistantIndices_brute_force),
        ("布尔标记", sol.findKDistantIndices_boolean),
        ("差分数组", sol.findKDistantIndices_diff),
    ]

    test_cases = [
        ([3, 4, 9, 1, 3, 9, 5], 9, 1, [1, 2, 3, 4, 5, 6]),
        ([2, 2, 2, 2, 2],        2, 2, [0, 1, 2, 3, 4]),
        ([1, 2, 3, 4, 5],        3, 1, [1, 2, 3]),
        ([1, 3, 2, 3, 1],        3, 1, [0, 1, 2, 3, 4]),
        ([1],                     1, 1, [0]),
        ([1, 2, 1, 2, 1],        2, 1, [0, 1, 2, 3, 4]),
        ([5, 1, 5, 1, 5],        1, 2, [0, 1, 2, 3, 4]),
        ([1, 2, 3],              2, 2, [0, 1, 2]),
        ([1, 2, 3, 4],           4, 1, [2, 3]),
        ([1, 2, 3, 4],           1, 1, [0, 1]),
    ]

    for name, fn in methods:
        all_pass = True
        for nums, key_val, k_val, expected in test_cases:
            result = fn(list(nums), key_val, k_val)
            if result != expected:
                print(f"  ✗ {name}: nums={nums}, key={key_val}, k={k_val}, got={result}, expected={expected}")
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
        ("暴力法 O(n*m)",     sol.findKDistantIndices_brute_force),
        ("布尔标记 O(n*k)",   sol.findKDistantIndices_boolean),
        ("差分数组 O(n)",     sol.findKDistantIndices_diff),
    ]

    sizes = [100, 1_000, 5_000, 10_000, 50_000, 100_000]
    repeat = 20

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(1, 100) for _ in range(size)]
        key_val = nums[size // 2]
        k_val = size // 10

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums), key_val, k_val)
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
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                      |
|------------|-----------|-----------|-------------------------------------------|
| 暴力法     | O(n*m)    | O(m)      | 对每个 i 检查是否在任何 key 的 k 范围内      |
| 布尔标记   | O(n*k)最坏| O(n)      | 对每个 key 标记区间，可能重复标记同一位置     |
| 差分数组   | O(n)      | O(n)      | 差分区间加，前缀和输出结果，线性最优          |

差分数组法核心思想：
  - 区间 [L, R] 整体 +1 可以用两次端点操作代替：diff[L] += 1, diff[R+1] -= 1
  - 最后一次前缀和，每个位置的值就是它被多少个区间覆盖
  - 值 > 0 表示该下标至少在一个 key 的 k 邻域内 → 即 K 近邻下标
  - 这种「区间加、最后单点查询」的场景，差分数组是经典 O(n) 做法
""")


if __name__ == "__main__":
    print("=== 找出数组中的所有 K 近邻下标：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
