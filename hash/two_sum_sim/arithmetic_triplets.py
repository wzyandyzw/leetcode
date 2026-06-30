# 题目：等差三元组的数目 (LeetCode 2367)
# 难度：简单
# 标签：数组、哈希表、双指针、枚举
#
# 题目需求：
#   给你一个下标从 0 开始、严格递增的整数数组 nums 和一个正整数 diff。
#   如果三元组 (i, j, k) 满足：
#     - i < j < k
#     - nums[j] - nums[i] == diff
#     - nums[k] - nums[j] == diff
#   则称其为等差三元组。返回不同等差三元组的数目。
#
# 约束条件：
#   1. 3 <= nums.length <= 200
#   2. 0 <= nums[i] <= 200
#   3. 1 <= diff <= 50
#   4. nums 严格递增
#
# 核心思路：
#   由于数组严格递增，等差三元组 (x, x+diff, x+2*diff) 中的三个值都必须在数组中出现。
#   因此只需枚举每个值 x = nums[i]，检查 x+diff 和 x+2*diff 是否同时存在即可。
#   每找到一组 (x, x+diff, x+2*diff)，就对应唯一的一个等差三元组 (i, j, k)。
#
# 本文件提供四种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：三重循环暴力法
    # 思路：枚举所有满足 i<j<k 的三元组，直接判断差值条件。
    # 时间复杂度：O(n^3) —— n<=200 时 n^3=8*10^6，可以通过。
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def arithmeticTriplets_brute_force(self, nums: List[int], diff: int) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                if nums[j] - nums[i] != diff:
                    continue
                for k in range(j + 1, n):
                    if nums[k] - nums[j] == diff:
                        ans += 1
        return ans

    # ----------------------------------------------------------
    # 解法二：哈希集合法
    # 思路：
    #   1. 将数组元素放入集合 s 中，实现 O(1) 查找
    #   2. 遍历每个元素 x = nums[i]，检查 x+diff 和 x+2*diff 是否都在 s 中
    #   3. 若都存在，则 (x, x+diff, x+2*diff) 构成一个等差三元组
    # 时间复杂度：O(n) —— 一次遍历，集合查找 O(1)。
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def arithmeticTriplets_hash_set(self, nums: List[int], diff: int) -> int:
        s = set(nums)
        ans = 0
        for x in nums:
            if (x + diff) in s and (x + 2 * diff) in s:
                ans += 1
        return ans

    # ----------------------------------------------------------
    # 解法三：布尔数组标记法（利用值域较小的特点）
    # 思路：
    #   题目中 nums[i] <= 200，可以用布尔数组代替哈希集合；
    #   为了通用性，这里根据数组最大值 + 2*diff 动态分配数组大小，
    #   其余逻辑与哈希集合法完全相同，数组访问比哈希查找更快。
    # 时间复杂度：O(n)
    # 空间复杂度：O(max(nums) + 2*diff)，在题目约束下为 O(1)
    # ----------------------------------------------------------
    def arithmeticTriplets_bool_array(self, nums: List[int], diff: int) -> int:
        max_val = nums[-1] + 2 * diff
        seen = [False] * (max_val + 1)
        for x in nums:
            seen[x] = True
        ans = 0
        for x in nums:
            if seen[x + diff] and seen[x + 2 * diff]:
                ans += 1
        return ans

    # ----------------------------------------------------------
    # 解法四：三指针法（利用严格递增的单调性）
    # 思路：
    #   利用数组严格递增的性质，用三个指针 i < j < k 同步推进。
    #   对每个 i，移动 j 直到 nums[j] >= nums[i]+diff；
    #   若 nums[j] == nums[i]+diff，则移动 k 直到 nums[k] >= nums[j]+diff；
    #   若 nums[k] == nums[j]+diff，则找到一个三元组。
    #   由于每个指针最多移动 n 次，整体是线性时间。
    # 时间复杂度：O(n) —— 三个指针总共最多移动 3n 次。
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def arithmeticTriplets_three_pointers(self, nums: List[int], diff: int) -> int:
        n = len(nums)
        ans = 0
        j, k = 0, 0
        for i in range(n):
            while j < n and nums[j] < nums[i] + diff:
                j += 1
            if j >= n or nums[j] != nums[i] + diff:
                continue
            while k < n and nums[k] < nums[j] + diff:
                k += 1
            if k < n and nums[k] == nums[j] + diff:
                ans += 1
        return ans


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.arithmeticTriplets_brute_force),
        ("哈希集合法", sol.arithmeticTriplets_hash_set),
        ("布尔数组法", sol.arithmeticTriplets_bool_array),
        ("三指针法",   sol.arithmeticTriplets_three_pointers),
    ]

    test_cases = [
        ([0, 1, 4, 6, 7, 10], 3,  2),
        ([4, 5, 6, 7, 8, 9],   2,  2),
        ([0, 1, 2],            1,  1),
        ([0, 1, 3],            1,  0),
        ([0, 2, 4, 6, 8],      2,  3),    # (0,2,4),(2,4,6),(4,6,8) 共3个
        ([1, 2, 3],            1,  1),
        ([10, 20, 30, 40, 50], 10, 3),    # (0,1,2),(1,2,3),(2,3,4)
        ([0, 100, 200],        100,1),
        ([0, 50, 100, 150, 200], 50, 3),
    ]

    for name, fn in methods:
        all_pass = True
        for nums, d, expected in test_cases:
            result = fn(list(nums), d)
            if result != expected:
                print(f"  ✗ {name}: nums={nums}, diff={d}, got={result}, expected={expected}")
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
        ("暴力法 O(n^3)",     sol.arithmeticTriplets_brute_force),
        ("哈希集合法 O(n)",   sol.arithmeticTriplets_hash_set),
        ("布尔数组法 O(n)",   sol.arithmeticTriplets_bool_array),
        ("三指针法 O(n)",     sol.arithmeticTriplets_three_pointers),
    ]

    sizes = [200, 1000, 5000, 10000, 50000, 100000]
    repeat = 200

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (μs)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums_set = set()
        while len(nums_set) < size:
            nums_set.add(random.randint(0, 10**6))
        nums = sorted(nums_set)
        d = random.randint(1, 50)

        for name, fn in methods:
            if "暴力" in name and size > 500:
                print(f"{size:>10} | {name:<20} | {'> 100000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums), d)
                elapsed = (time.perf_counter() - start) * 1_000_000
                times.append(elapsed)
            avg_us = sum(times) / len(times)
            print(f"{size:>10} | {name:<20} | {avg_us:>15.3f} | {'':<20}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("四种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                       |
|------------|-----------|-----------|--------------------------------------------|
| 暴力法     | O(n^3)    | O(1)      | 三重循环枚举所有三元组，n 较大时不可用         |
| 哈希集合法 | O(n)      | O(n)      | 集合存储元素，对每个 x 检查 x+d 和 x+2d       |
| 布尔数组法 | O(n)      | O(1)      | 利用值域小的特点用数组代替哈希表，速度更快     |
| 三指针法   | O(n)      | O(1)      | 利用严格递增单调性，三个指针线性扫描           |

为什么只需要检查 x+d 和 x+2d？
  - 等差数列公差为 diff，则三元组必为 (x, x+diff, x+2diff)
  - 数组严格递增 → 每个值最多出现一次，每个 x 最多对应一个三元组
  - 因此对每个 x 判断 x+diff 和 x+2diff 是否同时存在即可

三指针法的单调性依据：
  - 当 i 增大时，nums[i]+diff 也增大（数组严格递增），所以 j 不需要回退
  - 同理 k 也不需要回退
  - 每个指针最多从头到尾走一遍，总移动次数 <= 3n，即 O(n)
""")


if __name__ == "__main__":
    print("=== 等差三元组的数目：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
