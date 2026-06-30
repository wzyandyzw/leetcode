# 题目：与对应负数同时存在的最大正整数 (LeetCode 2441)
# 难度：简单
# 标签：数组、哈希表、排序、双指针
#
# 题目需求：
#   给定一个不包含任何零的整数数组 nums，找出自身与对应的负数都在数组中
#   存在的最大正整数 k。若不存在返回 -1。
#
# 约束条件：
#   1. 1 <= nums.length <= 1000
#   2. -1000 <= nums[i] <= 1000
#   3. nums[i] != 0
#
# 核心思路：
#   - 需要找最大的正数 k，使得 k 和 -k 都在数组中
#   - 利用哈希集合可以 O(1) 查找，遍历正数即可
#   - 或者利用值域很小（-1000~1000），用布尔数组标记出现情况
#
# 本文件提供四种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（双重循环）
    # 思路：
    #   遍历数组中每个正数 k，再遍历数组检查 -k 是否存在。
    #   记录满足条件的最大值。
    # 时间复杂度：O(n^2)
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def findMaxK_brute_force(self, nums: List[int]) -> int:
        ans = -1
        n = len(nums)
        for i in range(n):
            if nums[i] <= 0:
                continue
            k = nums[i]
            for j in range(n):
                if nums[j] == -k:
                    if k > ans:
                        ans = k
                    break
        return ans

    # ----------------------------------------------------------
    # 解法二：哈希集合法（推荐解法）
    # 思路：
    #   1. 将所有元素放入集合 s 实现 O(1) 查找
    #   2. 遍历数组，对每个正数 k，检查 -k 是否在 s 中
    #   3. 记录满足条件的最大值
    # 时间复杂度：O(n) —— 一次构建集合 + 一次遍历。
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def findMaxK_hash_set(self, nums: List[int]) -> int:
        s = set(nums)
        ans = -1
        for x in nums:
            if x > 0 and -x in s and x > ans:
                ans = x
        return ans

    # ----------------------------------------------------------
    # 解法三：排序 + 双指针法
    # 思路：
    #   1. 将数组排序
    #   2. 左指针 l 从 0 开始（指向负数），右指针 r 从 n-1 开始（指向正数）
    #   3. 若 nums[l] + nums[r] == 0，找到一对，记录 nums[r] 并移动指针继续找更大的；
    #      若 nums[l] + nums[r] < 0（负数绝对值大），左指针右移；
    #      若 nums[l] + nums[r] > 0（正数更大），右指针左移。
    #   由于 r 从最大开始，第一次遇到的匹配就是最大 k，但为了找到最大可能，
    #   仍要继续扫描（因为可能有重复值或指针错过）。实际上当 r 第一次匹配时
    #   nums[r] 已经是最大可能正数，可以直接返回。
    # 时间复杂度：O(n log n) —— 排序 O(n log n)，双指针 O(n)。
    # 空间复杂度：O(1)（若允许原地排序）
    # ----------------------------------------------------------
    def findMaxK_two_pointers(self, nums: List[int]) -> int:
        nums.sort()
        l, r = 0, len(nums) - 1
        while l < r:
            total = nums[l] + nums[r]
            if total == 0:
                return nums[r]
            elif total < 0:
                l += 1
            else:
                r -= 1
        return -1

    # ----------------------------------------------------------
    # 解法四：布尔数组标记法（利用值域有限）
    # 思路：
    #   由于 nums[i] 在 [-1000, 1000] 且不含 0，可用长度为 1001 的布尔数组
    #   seen 记录某个正数/负数是否出现：seen[k] 同时表示 k 和 -k 是否存在。
    #   具体做法：用两个布尔数组 pos 和 neg，或者用一个数组的两位标记。
    #   这里用一个整数数组 cnt，正数值+1，负数值-1对应位置+1，
    #   最后从大到小找第一个 cnt[k] == 2 的 k。
    # 时间复杂度：O(n)
    # 空间复杂度：O(1)（固定大小 1001 的数组）
    # ----------------------------------------------------------
    def findMaxK_bool_array(self, nums: List[int]) -> int:
        pos = [False] * 1001
        neg = [False] * 1001
        for x in nums:
            if x > 0:
                pos[x] = True
            else:
                neg[-x] = True
        for k in range(1000, 0, -1):
            if pos[k] and neg[k]:
                return k
        return -1


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.findMaxK_brute_force),
        ("哈希集合法", sol.findMaxK_hash_set),
        ("双指针法",   sol.findMaxK_two_pointers),
        ("布尔数组法", sol.findMaxK_bool_array),
    ]

    test_cases = [
        ([-1, 2, -3, 3],         3),
        ([-1, 10, 6, 7, -7, 1],  7),
        ([-10, 8, 6, 7, -2, -3], -1),
        ([-1, 1],                1),
        ([-1, -2, -3],           -1),
        ([1, 2, 3],              -1),
        ([-1000, 1000],          1000),
        ([1000, -999, 999, -1000], 1000),
        ([-2, -3, 2, 3],         3),
        ([5, -5, 4, -4, 3, -3],  5),
    ]

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
        ("暴力法 O(n^2)",     sol.findMaxK_brute_force),
        ("哈希集合法 O(n)",   sol.findMaxK_hash_set),
        ("双指针法 O(n log n)", sol.findMaxK_two_pointers),
        ("布尔数组法 O(n)",   sol.findMaxK_bool_array),
    ]

    sizes = [200, 1000, 5000, 10000, 50000, 100000]
    repeat = 100

    print(f"{'数据规模':>10} | {'解法':<22} | {'平均耗时 (μs)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(-1000, 1000) for _ in range(size)]
        nums = [x for x in nums if x != 0]
        while len(nums) < size:
            x = random.randint(-1000, 1000)
            if x != 0:
                nums.append(x)

        for name, fn in methods:
            if "暴力" in name and size > 5000:
                print(f"{size:>10} | {name:<22} | {'> 100000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                data = list(nums)
                start = time.perf_counter()
                fn(data)
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
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                    |
|------------|-----------|-----------|-----------------------------------------|
| 暴力法     | O(n^2)    | O(1)      | 对每个正数线性查找其相反数               |
| 哈希集合法 | O(n)      | O(n)      | 集合 O(1) 查找，最简洁通用              |
| 双指针法   | O(n log n)| O(1)      | 排序后左右指针夹逼，不占额外空间          |
| 布尔数组法 | O(n)      | O(1)      | 利用值域有限，数组标记，常数空间最优      |

双指针法为什么正确？
  - 排序后左指针指向最小（最负），右指针指向最大（最正）
  - 若 nums[l] + nums[r] = 0，说明找到相反数对，返回 nums[r]
    （因为 r 从最大值开始，第一次匹配就是最大 k）
  - 若和 < 0，说明负数绝对值更大，需要让负数变小（左指针右移）
  - 若和 > 0，说明正数更大，需要让正数变小（右指针左移）
  - 单调性保证不会错过正确答案

布尔数组法的优势：
  - 本题值域极小（-1000~1000），数组大小固定为 1001
  - 从 k=1000 倒序查找，第一个 pos[k]&&neg[k] 的 k 就是最大值
  - 不依赖哈希函数，常数因子最小，速度最快
""")


if __name__ == "__main__":
    print("=== 与对应负数同时存在的最大正整数：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
