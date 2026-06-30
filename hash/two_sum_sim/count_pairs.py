# 题目：统计和小于目标的下标对数目 (LeetCode 2824)
# 难度：简单
# 标签：数组、双指针、二分查找、排序
#
# 题目需求：
#   给定下标从 0 开始、长度为 n 的整数数组 nums 和整数 target，
#   返回满足 0 <= i < j < n 且 nums[i] + nums[j] < target 的下标对数目。
#
# 约束条件：
#   1. 1 <= n <= 50
#   2. -50 <= nums[i], target <= 50
#
# 核心观察：
#   题目只要求无序对 (i,j)（i<j）的数量，与元素顺序无关。
#   排序不改变"满足 a+b<target 的无序对数量"，因此可以先排序再用双指针/二分加速。
#
# 本文件提供四种解法，并在末尾做对比试验。


from typing import List
from bisect import bisect_left
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（双重循环）
    # 思路：枚举所有 i<j 的下标对，判断 nums[i]+nums[j] < target。
    # 时间复杂度：O(n^2) —— n<=50 时 n^2=2500，完全够用。
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def countPairs_brute_force(self, nums: List[int], target: int) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] < target:
                    ans += 1
        return ans

    # ----------------------------------------------------------
    # 解法二：排序 + 双指针法（推荐最优解法）
    # 思路：
    #   1. 将数组排序
    #   2. 左指针 l=0，右指针 r=n-1，ans=0
    #   3. 若 a[l]+a[r] < target：由于数组递增，a[l] 与 a[l+1]..a[r]
    #      这 r-l 个元素的和都 < target（因为 a[r] 是最大的右端元素），
    #      一次累加 r-l 对，然后 l++ 尝试下一个左端点。
    #   4. 若 a[l]+a[r] >= target：a[r] 太大，r--。
    # 时间复杂度：O(n log n) —— 排序 O(n log n)，双指针 O(n)。
    # 空间复杂度：O(1)（忽略排序栈空间）
    # ----------------------------------------------------------
    def countPairs_two_pointers(self, nums: List[int], target: int) -> int:
        nums.sort()
        l, r = 0, len(nums) - 1
        ans = 0
        while l < r:
            if nums[l] + nums[r] < target:
                ans += r - l
                l += 1
            else:
                r -= 1
        return ans

    # ----------------------------------------------------------
    # 解法三：排序 + 二分查找法
    # 思路：
    #   1. 将数组排序
    #   2. 对每个 i，在 a[i+1..n-1] 中找到第一个使得 a[i]+a[j] >= target
    #      的位置 k（即 a[j] >= target-a[i] 的下界），则 i 能与 i+1..k-1 配对，
    #      共 k-i-1 对，累加到答案。
    # 时间复杂度：O(n log n) —— 排序 O(n log n)，每次二分 O(log n)，共 O(n log n)。
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def countPairs_binary_search(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        ans = 0
        for i in range(n):
            k = bisect_left(nums, target - nums[i], i + 1, n)
            ans += k - i - 1
        return ans

    # ----------------------------------------------------------
    # 解法四：频率计数法（利用值域极小的特点）
    # 思路：
    #   由于 nums[i] 范围是 [-50, 50]，可以把数平移到 [0, 100]，
    #   用计数数组 freq[v] 表示值 v 出现的次数。
    #   然后枚举所有可能的 (v1, v2) 满足 v1<v2 且 v1+v2<target，
    #   贡献 freq[v1]*freq[v2]；再枚举 v1=v2 且 2*v1<target 的情况，
    #   贡献 C(freq[v1],2) = freq[v1]*(freq[v1]-1)/2。
    # 时间复杂度：O(1) —— 值域固定 101 个值，双重循环 101*101 是常数。
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def countPairs_frequency(self, nums: List[int], target: int) -> int:
        offset = 50
        freq = [0] * 101
        for x in nums:
            freq[x + offset] += 1
        ans = 0
        for v1 in range(-50, 51):
            c1 = freq[v1 + offset]
            if c1 == 0:
                continue
            if 2 * v1 < target:
                ans += c1 * (c1 - 1) // 2
            for v2 in range(v1 + 1, 51):
                c2 = freq[v2 + offset]
                if c2 and v1 + v2 < target:
                    ans += c1 * c2
        return ans


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.countPairs_brute_force),
        ("双指针法",   sol.countPairs_two_pointers),
        ("二分查找法", sol.countPairs_binary_search),
        ("频率计数法", sol.countPairs_frequency),
    ]

    test_cases = [
        ([-1, 1, 2, 3, 1],             2,   3),
        ([-6, 2, 5, -2, -7, -1, 3],    -2,  10),
        ([1, 2, 3],                    7,   3),    # (1+2)=3<7, (1+3)=4<7, (2+3)=5<7 → 3
        ([1, 2, 3],                    4,   2),    # (1+2)=3<4, (1+3)=4≥4, (2+3)=5≥4 → 1 wait: (1,2)=3<4 only → 1
        # Fix: [1,2,3] target=4: sums=3,4,5 → only 3<4 → 1 pair
    ]
    test_cases[-1] = ([1, 2, 3], 4, 1)

    test_cases.append(([-50, -49],                 -99, 0))    # -50+(-49)=-99, need <-99 → 0
    test_cases.append(([-50, -49],                 -98, 1))    # -99<-98 ✓
    test_cases.append(([50, 50],                   101, 1))    # 100<101 ✓
    test_cases.append(([50, 50],                   100, 0))    # 100<100 ✗
    test_cases.append(([0, 0, 0, 0],               1,   6))    # C(4,2)=6 all pairs sum to 0<1
    test_cases.append(([-1, -2, -3],               -3,  2))    # sorted: -3,-2,-1; pairs: (-3)+(-2)=-5<-3 ✓, (-3)+(-1)=-4<-3 ✓, (-2)+(-1)=-3≥-3 ✗ → 2

    for name, fn in methods:
        all_pass = True
        for nums, t, expected in test_cases:
            result = fn(list(nums), t)
            if result != expected:
                print(f"  ✗ {name}: nums={nums}, target={t}, got={result}, expected={expected}")
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
        ("暴力法 O(n^2)",      sol.countPairs_brute_force),
        ("双指针法 O(n log n)", sol.countPairs_two_pointers),
        ("二分查找法 O(n log n)", sol.countPairs_binary_search),
        ("频率计数法 O(1)",    sol.countPairs_frequency),
    ]

    sizes = [50, 200, 1000, 5000, 10000, 50000]
    repeat = 100

    print(f"{'数据规模':>10} | {'解法':<24} | {'平均耗时 (μs)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(-50, 50) for _ in range(size)]
        t = random.randint(-100, 100)

        for name, fn in methods:
            if "暴力" in name and size > 2000:
                print(f"{size:>10} | {name:<24} | {'> 100000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums), t)
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
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                       |
|------------|-----------|-----------|--------------------------------------------|
| 暴力法     | O(n^2)    | O(1)      | 双重循环枚举所有对，n<=50 完全够用           |
| 双指针法   | O(n log n)| O(1)      | 排序后左右夹逼，线性扫描，效率最高           |
| 二分查找法 | O(n log n)| O(1)      | 排序后对每个 i 二分查找右边界                |
| 频率计数法 | O(1)      | O(1)      | 利用值域极小（-50~50），常数时间完成         |

双指针法正确性证明：
  排序后，固定 l 并从 r=n-1 开始向左收缩：
  - 若 a[l]+a[r] < target：因为数组递增，对所有 j∈(l, r]，
    必有 a[l]+a[j] <= a[l]+a[r] < target，共 r-l 个满足条件的 j；
    这 r-l 对全部计入答案后，l 已处理完，l++。
  - 若 a[l]+a[r] >= target：说明 a[r] 与任何左端点（>=a[l]）的和
    都 >= a[l]+a[r] >= target，因此 a[r] 无法与任何剩余左端点配对，r--。
  每个指针只向一个方向移动，总移动次数 O(n)。

二分查找法思路：
  对每个 i，需要找到最大的 j>i 使得 a[i]+a[j] < target，
  即 a[j] < target-a[i]。bisect_left 返回第一个 >= target-a[i] 的位置 k，
  则 (i, i+1), (i, i+2), ..., (i, k-1) 都是合法对，共 k-i-1 个。

频率计数法为何是 O(1)？
  题目约束 nums[i] ∈ [-50, 50]，仅 101 个可能取值。
  枚举 v1∈[-50,50]，再枚举 v2 统计，总枚举 101*101≈10^4 次，常数时间。
  当值域扩展时此法不适用，但在本题约束下是最快的。
""")


if __name__ == "__main__":
    print("=== 统计和小于目标的下标对数目：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
