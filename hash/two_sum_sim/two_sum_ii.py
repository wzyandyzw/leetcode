# 题目：两数之和 II - 输入有序数组 (LeetCode 167)
# 难度：中等
# 标签：数组、双指针、二分查找
#
# 题目需求：
#   给你一个下标从 1 开始的整数数组 numbers，该数组已按非递减顺序排列，
#   请你从数组中找出满足相加之和等于目标数 target 的两个数。
#   如果设这两个数分别是 numbers[index1] 和 numbers[index2]，
#   则 1 <= index1 < index2 <= numbers.length。
#   以长度为 2 的整数数组 [index1, index2] 的形式返回这两个整数的下标。
#
# 约束条件：
#   1. 2 <= numbers.length <= 3 * 10^4
#   2. -1000 <= numbers[i] <= 1000
#   3. numbers 按非递减顺序排列
#   4. -1000 <= target <= 1000
#   5. 仅存在一个有效答案
#   6. 你所设计的解决方案必须只使用常量级的额外空间（O(1)）
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（两层循环）
    # 思路：枚举所有可能的数对 (i, j)，检查 numbers[i] + numbers[j] 是否等于 target。
    # 时间复杂度：O(n^2) —— 最坏情况下要检查 n*(n-1)/2 对数。
    # 空间复杂度：O(1) —— 只使用常数额外空间。
    # ----------------------------------------------------------
    def twoSum_brute_force(self, numbers: List[int], target: int) -> List[int]:
        n = len(numbers)
        for i in range(n):
            for j in range(i + 1, n):
                if numbers[i] + numbers[j] == target:
                    return [i + 1, j + 1]
        return []

    # ----------------------------------------------------------
    # 解法二：二分查找（利用数组有序的特性）
    # 思路：
    #   1. 固定第一个数 numbers[i]
    #   2. 在 i+1 到 n-1 的范围内二分查找 target - numbers[i]
    #   3. 如果找到则返回二者的下标（注意下标从 1 开始）
    # 时间复杂度：O(n log n) —— 外层 O(n)，每次二分查找 O(log n)。
    # 空间复杂度：O(1) —— 只使用常数额外空间。
    # ----------------------------------------------------------
    def twoSum_binary_search(self, numbers: List[int], target: int) -> List[int]:
        n = len(numbers)
        for i in range(n):
            complement = target - numbers[i]
            left, right = i + 1, n - 1
            while left <= right:
                mid = (left + right) // 2
                if numbers[mid] == complement:
                    return [i + 1, mid + 1]
                elif numbers[mid] < complement:
                    left = mid + 1
                else:
                    right = mid - 1
        return []

    # ----------------------------------------------------------
    # 解法三：双指针法 —— 最优解法
    # 思路：
    #   1. 左指针 left 从 0 开始，右指针 right 从 n-1 开始
    #   2. 计算 sum = numbers[left] + numbers[right]
    #   3. 若 sum == target，返回 [left+1, right+1]；
    #      若 sum < target，左指针右移（需要更大的数）；
    #      若 sum > target，右指针左移（需要更小的数）
    # 时间复杂度：O(n) —— 每个元素最多被访问一次。
    # 空间复杂度：O(1) —— 只使用常数额外空间，符合题目要求。
    # ----------------------------------------------------------
    def twoSum_two_pointers(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers) - 1
        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                return [left + 1, right + 1]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return []


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",       sol.twoSum_brute_force),
        ("二分查找法",   sol.twoSum_binary_search),
        ("双指针法",     sol.twoSum_two_pointers),
    ]

    test_cases = [
        ([2, 7, 11, 15],     9,  [1, 2]),
        ([2, 3, 4],          6,  [1, 3]),
        ([-1, 0],           -1,  [1, 2]),
        ([0, 0, 3, 4],       0,  [1, 2]),
        ([5, 25, 75],      100, [2, 3]),
        ([1, 2, 3, 4, 4, 9, 56, 90], 8, [4, 5]),
        ([1, 2, 3, 7, 11],   9,  [2, 4]),
        ([-10, -5, 1, 3, 7], -3, [1, 5]),
    ]

    for name, fn in methods:
        all_pass = True
        for nums, target_val, expected in test_cases:
            result = fn(list(nums), target_val)
            if result != expected:
                print(f"  ✗ {name}: nums={nums}, target={target_val}, got={result}, expected={expected}")
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
        ("暴力法 O(n^2)",       sol.twoSum_brute_force),
        ("二分查找 O(n log n)", sol.twoSum_binary_search),
        ("双指针法 O(n)",       sol.twoSum_two_pointers),
    ]

    sizes = [100, 1_000, 5_000, 10_000, 30_000]
    repeat = 5

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        base = sorted(random.randint(-1000, 1000) for _ in range(size))
        # 确保有序且存在解
        i = size // 5
        j = 4 * size // 5
        target_val = base[i] + base[j]

        results_for_size = {}
        for name, fn in methods:
            if "暴力" in name and size > 5_000:
                print(f"{size:>10} | {name:<20} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(base), target_val)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            results_for_size[name] = avg_ms
            print(f"{size:>10} | {name:<20} | {avg_ms:>15.3f} | {'':<20}")

        if len(results_for_size) == 3:
            bf_time = results_for_size["暴力法 O(n^2)"]
            tp_time = results_for_size["双指针法 O(n)"]
            if bf_time > 0 and tp_time > 0:
                print(f"           | {'  -> 双指针法比暴力法快':<20} | {bf_time / tp_time:>15.2f}x | {f'(n={size})':<20}")


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法         | 时间复杂度 | 空间复杂度 | 说明                                  |
|--------------|-----------|-----------|---------------------------------------|
| 暴力法       | O(n^2)    | O(1)      | 两层循环，n 较大时不可用               |
| 二分查找法   | O(n log n)| O(1)      | 固定一个数，二分查找另一个数            |
| 双指针法     | O(n)      | O(1)      | 左右夹逼，时间最优，符合题目 O(1) 空间要求 |

为什么双指针最优？
  - 利用数组有序性，每次排除一半的可能性
  - 每个元素最多被访问一次，O(n) 是这类问题的理论下界
  - 完美符合题目 O(1) 空间要求
""")


if __name__ == "__main__":
    print("=== 两数之和 II：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
