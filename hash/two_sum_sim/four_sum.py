# 题目：四数之和 (LeetCode 18)
# 难度：中等
# 标签：数组、双指针、排序
#
# 题目需求：
#   给定一个由 n 个整数组成的数组 nums，和一个目标值 target，
#   请你找出并返回满足下述全部条件且不重复的四元组 [nums[a], nums[b], nums[c], nums[d]]：
#     0 <= a, b, c, d < n
#     a、b、c 和 d 互不相同
#     nums[a] + nums[b] + nums[c] + nums[d] == target
#   你可以按任意顺序返回答案。
#
# 约束条件：
#   1. 1 <= nums.length <= 200
#   2. -10^9 <= nums[i] <= 10^9
#   3. -10^9 <= target <= 10^9
#   4. 答案中不可以包含重复的四元组。
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（四层循环 + 集合去重）
    # 思路：枚举所有可能的四元组 (i, j, k, l)，检查四数之和是否等于 target。
    #       为避免重复，把四元组排序后存入集合。
    # 时间复杂度：O(n^4) —— 四层循环，且每个四元组排序 O(1)。
    # 空间复杂度：O(n) —— 主要是结果存储。
    # ----------------------------------------------------------
    def fourSum_brute_force(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        result = set()
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    for l in range(k + 1, n):
                        if nums[i] + nums[j] + nums[k] + nums[l] == target:
                            quad = tuple(sorted([nums[i], nums[j], nums[k], nums[l]]))
                            result.add(quad)
        return [list(t) for t in result]

    # ----------------------------------------------------------
    # 解法二：哈希表法（两层循环固定前两数 + 哈希表两数求和）
    # 思路：
    #   1. 先排序，便于去重
    #   2. 固定第一个数 nums[i]，跳过重复
    #   3. 固定第二个数 nums[j]，跳过重复
    #   4. 对剩下的两个数，相当于两数之和问题：找 c + d = target - nums[i] - nums[j]
    #   5. 用哈希表存已见过的数，完成一次遍历即可
    # 时间复杂度：O(n^3) —— 外层两层 O(n^2)，内层 O(n)。
    # 空间复杂度：O(n) —— 哈希表和结果存储。
    # ----------------------------------------------------------
    def fourSum_hash_table(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        result = []

        for i in range(n):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            for j in range(i + 1, n):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue

                seen = set()
                two_target = target - nums[i] - nums[j]
                k = j + 1
                while k < n:
                    complement = two_target - nums[k]
                    if complement in seen:
                        result.append([nums[i], nums[j], complement, nums[k]])
                        while k + 1 < n and nums[k] == nums[k + 1]:
                            k += 1
                    else:
                        seen.add(nums[k])
                    k += 1

        return result

    # ----------------------------------------------------------
    # 解法三：排序 + 双指针法 —— 最优解法
    # 思路：
    #   1. 先排序数组 O(n log n)
    #   2. 固定第一个数 nums[i]，跳过重复；若 nums[i] > target 且 nums[i] > 0 可剪枝
    #   3. 固定第二个数 nums[j]，跳过重复
    #   4. 用左指针 left = j + 1、右指针 right = n - 1 做夹逼
    #   5. 若四数之和 == target，记录结果并跳过重复；
    #      若和 < target，左指针右移（需要更大的数）；
    #      若和 > target，右指针左移（需要更小的数）
    #   6. 去重：固定 i 时跳过与前一位相同的数；
    #      固定 j 时跳过与前一位相同的数；
    #      找到解后，左指针向右跳过重复值，右指针向左跳过重复值
    # 时间复杂度：O(n^3) —— 排序 O(n log n)，两层固定 O(n^2)，双指针遍历 O(n)。
    # 空间复杂度：O(1) 或 O(n) —— 取决于排序是否使用额外空间。
    # ----------------------------------------------------------
    def fourSum_two_pointers(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        result = []

        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            if nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break
            if nums[i] + nums[n - 1] + nums[n - 2] + nums[n - 3] < target:
                continue

            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue
                if nums[i] + nums[j] + nums[j + 1] + nums[j + 2] > target:
                    break
                if nums[i] + nums[j] + nums[n - 1] + nums[n - 2] < target:
                    continue

                left, right = j + 1, n - 1
                two_target = target - nums[i] - nums[j]

                while left < right:
                    two_sum = nums[left] + nums[right]
                    if two_sum == two_target:
                        result.append([nums[i], nums[j], nums[left], nums[right]])
                        while left < right and nums[left] == nums[left + 1]:
                            left += 1
                        while left < right and nums[right] == nums[right - 1]:
                            right -= 1
                        left += 1
                        right -= 1
                    elif two_sum < two_target:
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
        ("暴力法",     sol.fourSum_brute_force),
        ("哈希表法",   sol.fourSum_hash_table),
        ("双指针法",   sol.fourSum_two_pointers),
    ]

    test_cases = [
        ([1, 0, -1, 0, -2, 2],           0,  [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
        ([2, 2, 2, 2, 2],                8,  [[2, 2, 2, 2]]),
        ([0, 0, 0, 0],                   0,  [[0, 0, 0, 0]]),
        ([1, -2, -5, -4, -3, 3, 3, 5], -11,  [[-5, -4, -3, 1]]),
        ([-3, -2, -1, 0, 0, 1, 2, 3],    0,  [[-3, -2, 2, 3], [-3, -1, 1, 3], [-3, 0, 0, 3], [-3, 0, 1, 2], [-2, -1, 0, 3], [-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
        ([0, 0, 0, 0, 0],                0,  [[0, 0, 0, 0]]),
        ([1, 2, 3, 4],                   10, [[1, 2, 3, 4]]),
        ([-1, 0, 1, 2, -1, -4],         -1, [[-4, 0, 1, 2], [-1, -1, 0, 1]]),
    ]

    for name, fn in methods:
        all_pass = True
        for nums, target_val, expected in test_cases:
            result = fn(list(nums), target_val)
            if _normalize(result) != _normalize(expected):
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
        ("暴力法 O(n^4)",       sol.fourSum_brute_force),
        ("哈希表法 O(n^3)",     sol.fourSum_hash_table),
        ("双指针法 O(n^3)",     sol.fourSum_two_pointers),
    ]

    sizes = [50, 100, 150, 200]
    repeat = 3

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(-100_000, 100_000) for _ in range(size)]
        target_val = nums[0] + nums[1] + nums[size // 2] + nums[size - 1]

        results_for_size = {}
        for name, fn in methods:
            if "暴力" in name and size > 100:
                print(f"{size:>10} | {name:<20} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums), target_val)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            results_for_size[name] = avg_ms
            print(f"{size:>10} | {name:<20} | {avg_ms:>15.3f} | {'':<20}")

        if len(results_for_size) >= 2:
            tp_name = "双指针法 O(n^3)"
            ht_name = "哈希表法 O(n^3)"
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
| 暴力法     | O(n^4)    | O(n)      | 四重循环，n 较大时不可用                 |
| 哈希表法   | O(n^3)    | O(n)      | 外层固定两数，内层用哈希表两数求和        |
| 双指针法   | O(n^3)    | O(1)/O(n) | 排序后外层固定两数，内层双指针夹逼        |

为什么双指针法更优？
  - 排序后利用有序性，配合剪枝（最小四数和 > target 可 break；最大四数和 < target 可 continue）
  - 去重简单：相同的数字相邻，跳过即可
  - 注意：必须先排序；i 遍历时若 nums[i] + nums[i+1] + nums[i+2] + nums[i+3] > target 可提前 break

去重的关键技巧：
  1. 固定 i：若 nums[i] == nums[i-1]，跳过
  2. 固定 j：若 nums[j] == nums[j-1]，跳过
  3. 找到解后：左指针向右跳过重复，右指针向左跳过重复
  4. 通过排序让相同元素相邻，天然提供去重能力
""")


if __name__ == "__main__":
    print("=== 四数之和：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
