# 题目：三数之和 (LeetCode 15)
# 难度：中等
# 标签：数组、双指针、排序
#
# 题目需求：
#   给定一个整数数组 nums，判断是否存在三元组 [nums[i], nums[j], nums[k]]
#   满足 i != j、i != k 且 j != k，同时还满足 nums[i] + nums[j] + nums[k] == 0。
#   请你返回所有和为 0 且不重复的三元组。
#
# 约束条件：
#   1. 答案中不可以包含重复的三元组。
#   2. 3 <= nums.length <= 3000
#   3. -10^5 <= nums[i] <= 10^5
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（三层循环 + 集合去重）
    # 思路：枚举所有可能的三元组 (i, j, k)，检查 nums[i] + nums[j] + nums[k] 是否等于 0。
    #       为避免重复，把三元组排序后存入集合。
    # 时间复杂度：O(n^3) —— 三层循环，且每个三元组排序 O(1)。
    # 空间复杂度：O(n) —— 主要是结果存储。
    # ----------------------------------------------------------
    def threeSum_brute_force(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        result = set()
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                        result.add(triplet)
        return [list(t) for t in result]

    # ----------------------------------------------------------
    # 解法二：哈希表法（两层循环 + 哈希表找第三个数）
    # 思路：
    #   1. 先排序，便于去重
    #   2. 固定第一个数 nums[i]
    #   3. 对剩下的两个数，相当于两数之和问题：找 b + c = -nums[i]
    #   4. 用哈希表存已见过的数，完成一次遍历即可
    # 时间复杂度：O(n^2) —— 外层 O(n)，内层 O(n)。
    # 空间复杂度：O(n) —— 哈希表和结果存储。
    # ----------------------------------------------------------
    def threeSum_hash_table(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        result = []

        for i in range(n):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            seen = set()
            j = i + 1
            while j < n:
                complement = -nums[i] - nums[j]
                if complement in seen:
                    result.append([nums[i], complement, nums[j]])
                    while j + 1 < n and nums[j] == nums[j + 1]:
                        j += 1
                else:
                    seen.add(nums[j])
                j += 1

        return result

    # ----------------------------------------------------------
    # 解法三：排序 + 双指针法 —— 最优解法
    # 思路：
    #   1. 先排序数组 O(n log n)
    #   2. 固定第一个数 nums[i]，转化为"两数之和 = -nums[i]" 的问题
    #   3. 用左指针 left = i + 1、右指针 right = n - 1 做夹逼
    #   4. 若三数之和 == 0，记录结果并跳过重复；
    #      若和 < 0，左指针右移（需要更大的数）；
    #      若和 > 0，右指针左移（需要更小的数）
    #   5. 去重：固定 nums[i] 时跳过与前一位相同的数；
    #      找到解后，左指针向右跳过重复值，右指针向左跳过重复值
    # 时间复杂度：O(n^2) —— 排序 O(n log n)，双指针遍历 O(n^2)。
    # 空间复杂度：O(1) 或 O(n) —— 取决于排序是否使用额外空间。
    # ----------------------------------------------------------
    def threeSum_two_pointers(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        result = []

        for i in range(n):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1
            target = -nums[i]

            while left < right:
                two_sum = nums[left] + nums[right]
                if two_sum == target:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif two_sum < target:
                    left += 1
                else:
                    right -= 1

        return result


# ============================================================
# 正确性测试用例
# ============================================================
def _normalize(result: List[List[int]]) -> set:
    return set(tuple(sorted(t)) for t in result)


def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.threeSum_brute_force),
        ("哈希表法",   sol.threeSum_hash_table),
        ("双指针法",   sol.threeSum_two_pointers),
    ]

    test_cases = [
        ([-1, 0, 1, 2, -1, -4],  [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1],               []),
        ([0, 0, 0],               [[0, 0, 0]]),
        ([-2, 0, 1, 1, 2],        [[-2, 0, 2], [-2, 1, 1]]),
        ([0, 0, 0, 0],            [[0, 0, 0]]),
        ([-1, 0, 1, 0],           [[-1, 0, 1]]),
        ([1, 2, -2, -1],          []),
    ]

    for name, fn in methods:
        all_pass = True
        for nums, expected in test_cases:
            result = fn(list(nums))
            if _normalize(result) != _normalize(expected):
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
        ("暴力法 O(n^3)",       sol.threeSum_brute_force),
        ("哈希表法 O(n^2)",     sol.threeSum_hash_table),
        ("双指针法 O(n^2)",     sol.threeSum_two_pointers),
    ]

    sizes = [100, 500, 1_000, 2_000, 3_000]
    repeat = 3

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(-100_000, 100_000) for _ in range(size)]

        results_for_size = {}
        for name, fn in methods:
            if "暴力" in name and size > 500:
                print(f"{size:>10} | {name:<20} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums))
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            results_for_size[name] = avg_ms
            print(f"{size:>10} | {name:<20} | {avg_ms:>15.3f} | {'':<20}")

        if len(results_for_size) >= 2:
            tp_name = "双指针法 O(n^2)"
            ht_name = "哈希表法 O(n^2)"
            if tp_name in results_for_size and ht_name in results_for_size:
                tp = results_for_size[tp_name]
                ht = results_for_size[ht_name]
                if tp > 0 and ht > 0:
                    ratio = ht / tp if tp < ht else tp / ht
                    faster = "双指针法" if tp < ht else "哈希表法"
                    print(f"           | {f'  -> {faster}更快':<20} | {ratio:>15.2f}x | {f'(n={size})':<20}")


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
| 暴力法     | O(n^3)    | O(n)      | 三重循环，n 较大时不可用                 |
| 哈希表法   | O(n^2)    | O(n)      | 外层固定一个数，内层用哈希表两数求和      |
| 双指针法   | O(n^2)    | O(1)/O(n) | 排序后双指针夹逼，时间常数较小，推荐解法  |

为什么双指针法最优？
  - 排序后利用有序性，避免了哈希表的常数开销
  - 去重简单：相同的数字相邻，跳过即可
  - 注意：必须先排序；i 遍历时若 nums[i] > 0 可提前 break

去重的关键技巧：
  1. 固定 i：若 nums[i] == nums[i-1]，跳过
  2. 找到解后：左指针向右跳过重复，右指针向左跳过重复
  3. 通过排序让相同元素相邻，天然提供去重能力
""")


if __name__ == "__main__":
    print("=== 三数之和：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
