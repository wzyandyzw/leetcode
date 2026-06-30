# 题目：不同的平均值数目 (LeetCode 2465)
# 难度：简单
# 标签：数组、哈希表、排序、双指针
#
# 题目需求：
#   给定偶数长度的整数数组 nums，重复以下步骤直到数组为空：
#     1. 找到最小值并删除
#     2. 找到最大值并删除
#     3. 计算两数的平均值 (a+b)/2
#   返回上述过程能得到的不同平均值的数目。
#   注意：若最小值/最大值有重复，删任意一个即可，不影响不同平均值的统计。
#
# 约束条件：
#   1. 2 <= nums.length <= 100（偶数）
#   2. 0 <= nums[i] <= 100
#
# 核心观察：
#   - 将数组排序后，每次删除的最小/最大值就是当前未处理部分的首尾元素
#   - 即第 i 步的配对是 (nums[i], nums[n-1-i])，共 n/2 对
#   - 为避免浮点数精度问题，用两数之和 a+b 来判定平均值是否相同
#     （因为 (a+b)/2 不同 ⇔ a+b 不同）
#
# 本文件提供四种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：模拟法（反复找最值并删除）
    # 思路：
    #   完全按照题目描述模拟：每次找 min 和 max，移除后计算平均值加入集合。
    #   使用 list.remove() 每次 O(n)，共 n/2 轮，每轮两次线性查找 + 两次删除。
    # 时间复杂度：O(n^2) —— n 轮操作，每轮 O(n)。
    # 空间复杂度：O(n) —— 复制数组 + 集合。
    # ----------------------------------------------------------
    def distinctAverages_simulation(self, nums: List[int]) -> int:
        arr = list(nums)
        avgs = set()
        while arr:
            mn = min(arr)
            mx = max(arr)
            arr.remove(mn)
            arr.remove(mx)
            avgs.add((mn + mx) / 2.0)
        return len(avgs)

    # ----------------------------------------------------------
    # 解法二：排序 + 双指针 + 哈希集合（推荐解法）
    # 思路：
    #   1. 将数组排序
    #   2. 用双指针 l=0, r=n-1 从两端向中间配对
    #   3. 每次将 nums[l] + nums[r] 加入集合（用和代替平均值避免浮点问题）
    #   4. 集合的大小即为不同平均值的数目
    # 时间复杂度：O(n log n) —— 排序 O(n log n)，双指针 O(n)。
    # 空间复杂度：O(n) —— 集合存储不同的和。
    # ----------------------------------------------------------
    def distinctAverages_two_pointers(self, nums: List[int]) -> int:
        nums.sort()
        l, r = 0, len(nums) - 1
        seen = set()
        while l < r:
            seen.add(nums[l] + nums[r])
            l += 1
            r -= 1
        return len(seen)

    # ----------------------------------------------------------
    # 解法三：排序 + 布尔数组标记（利用值域极小）
    # 思路：
    #   由于 nums[i] 范围是 [0, 100]，两数之和范围为 [0, 200]，
    #   可以用长度为 201 的布尔数组代替集合，空间 O(1)，速度更快。
    # 时间复杂度：O(n log n)
    # 空间复杂度：O(1)（固定大小 201 的数组）
    # ----------------------------------------------------------
    def distinctAverages_bool_array(self, nums: List[int]) -> int:
        nums.sort()
        l, r = 0, len(nums) - 1
        seen = [False] * 201
        count = 0
        while l < r:
            s = nums[l] + nums[r]
            if not seen[s]:
                seen[s] = True
                count += 1
            l += 1
            r -= 1
        return count

    # ----------------------------------------------------------
    # 解法四：排序 + 和集合（用浮点平均值）
    # 思路：
    #   与解法二相同，但直接把 (a+b)/2.0 的浮点值加入集合。
    #   在本题数值范围（0~100 的整数对）下，浮点除法不会产生精度问题，
    #   但使用整数和仍然是更稳妥的做法。
    # 时间复杂度：O(n log n)
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def distinctAverages_float_set(self, nums: List[int]) -> int:
        nums.sort()
        l, r = 0, len(nums) - 1
        avgs = set()
        while l < r:
            avgs.add((nums[l] + nums[r]) / 2.0)
            l += 1
            r -= 1
        return len(avgs)


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("模拟法",      sol.distinctAverages_simulation),
        ("双指针法",    sol.distinctAverages_two_pointers),
        ("布尔数组法",  sol.distinctAverages_bool_array),
        ("浮点集合法",  sol.distinctAverages_float_set),
    ]

    test_cases = [
        ([4, 1, 4, 0, 3, 5],     2),
        ([1, 100],               1),
        ([0, 0],                 1),    # avg=0
        ([1, 2, 3, 4],           2),    # (1+4)/2=2.5, (2+3)/2=2.5 → 1? wait: sorted [1,2,3,4], pairs (1,4) sum=5, (2,3) sum=5 → 1 distinct
    ]

    # Fix: [1,2,3,4] sums = 5,5 → 1 distinct average
    test_cases[-1] = ([1, 2, 3, 4], 1)

    test_cases.append(([0, 0, 0, 0],                 1))   # sums: 0,0
    test_cases.append(([0, 1, 2, 3, 4, 5, 6, 7],     4))   # pairs: (0,7)=7,(1,6)=7,(2,5)=7,(3,4)=7 → wait all sums 7? → 1
    # Wait: [0,1,2,3,4,5,6,7] sorted, pairs (0,7)=7,(1,6)=7,(2,5)=7,(3,4)=7, all same → 1
    test_cases[-1] = ([0, 1, 2, 3, 4, 5, 6, 7], 1)

    test_cases.append(([9, 5, 7, 8, 7, 9, 8, 2, 0, 7], 5))  # LeetCode example style, let me verify
    # Let me just pick a known case: [1,3,4,4] sorted, pairs (1,4)=5, (3,4)=7 → 2 averages
    test_cases.append(([1, 3, 4, 4], 2))

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
        ("模拟法 O(n^2)",      sol.distinctAverages_simulation),
        ("双指针法 O(n log n)", sol.distinctAverages_two_pointers),
        ("布尔数组法 O(n log n)", sol.distinctAverages_bool_array),
        ("浮点集合法 O(n log n)", sol.distinctAverages_float_set),
    ]

    sizes = [20, 100, 500, 1000, 5000, 10000]
    repeat = 100

    print(f"{'数据规模':>10} | {'解法':<24} | {'平均耗时 (μs)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(0, 100) for _ in range(size)]
        if len(nums) % 2 == 1:
            nums.append(random.randint(0, 100))

        for name, fn in methods:
            if "模拟" in name and size > 500:
                print(f"{size:>10} | {name:<24} | {'> 100000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums))
                elapsed = (time.perf_counter() - start) * 1_000_000
                times.append(elapsed)
            avg_us = sum(times) / len(times)
            print(f"{size:>10} | {name:<24} | {avg_us:>15.3f} | {'':<20}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("四种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                      |
|------------|-----------|-----------|-------------------------------------------|
| 模拟法     | O(n^2)    | O(n)      | 反复调用 min/max/remove，n 大时不可用       |
| 双指针法   | O(n log n)| O(n)      | 排序 + 首尾指针 + 集合查重，推荐通用解法    |
| 布尔数组法 | O(n log n)| O(1)      | 利用值域 0~200，固定数组标记，空间最优     |
| 浮点集合法 | O(n log n)| O(n)      | 同双指针但存浮点值，可读性好但略逊于整数    |

为什么排序 + 双指针是正确的？
  - 数组严格按从小到大排序后，全局最小值必然是 nums[0]，
    全局最大值必然是 nums[n-1]；删除二者后，剩余数组的
    最小值是 nums[1]、最大值是 nums[n-2]，以此类推。
  - 因此每一步的配对就是 (nums[l], nums[r])，l 递增、r 递减。

为什么用「和」代替「平均值」？
  - 平均值 (a+b)/2 可能产生 .5 的小数（如示例 1 的 2.5），
    浮点数在一般情况下有精度隐患；
  - 而 (a+b)/2 的不同值 ↔ a+b 的不同值一一对应（除以 2 是双射），
    用整数和既精确又高效。

题目中"重复元素可删任意一个"为何不影响答案？
  - 当有多个相同最小值或最大值时，删哪一个对平均值集合无影响：
    若删的两个数都是 x，配对仍然是 x；若删一个最小 min 和一个最大 max，
    其和是固定的，不同选择只会产生不同的顺序，但不会改变集合中
    最终的不同和数量。
""")


if __name__ == "__main__":
    print("=== 不同的平均值数目：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
