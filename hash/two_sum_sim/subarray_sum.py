# 题目：和为 K 的子数组 (LeetCode 560)
# 难度：中等
# 标签：数组、哈希表、前缀和
#
# 题目需求：
#   给你一个整数数组 nums 和一个整数 k，请你统计并返回该数组中和为 k 的子数组的个数。
#   子数组是数组中元素的连续非空序列。
#
# 约束条件：
#   1. 1 <= nums.length <= 2 * 10^4
#   2. -1000 <= nums[i] <= 1000
#   3. -10^7 <= k <= 10^7
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（两层循环枚举所有子数组）
    # 思路：枚举所有可能的子数组起点 i，然后从 i 开始累加，检查和是否等于 k。
    # 时间复杂度：O(n^2) —— n*(n+1)/2 个子数组。
    # 空间复杂度：O(1) —— 只使用常数额外空间。
    # ----------------------------------------------------------
    def subarraySum_brute_force(self, nums: List[int], k: int) -> int:
        n = len(nums)
        count = 0
        for i in range(n):
            current_sum = 0
            for j in range(i, n):
                current_sum += nums[j]
                if current_sum == k:
                    count += 1
        return count

    # ----------------------------------------------------------
    # 解法二：前缀和数组 + 枚举
    # 思路：
    #   1. 先计算前缀和数组 prefix，prefix[i] = nums[0] + ... + nums[i-1]
    #   2. 子数组 nums[j..i] 的和 = prefix[i+1] - prefix[j]
    #   3. 枚举所有 (j, i) 对，检查 prefix[i+1] - prefix[j] 是否等于 k
    # 时间复杂度：O(n^2) —— 两层循环。
    # 空间复杂度：O(n) —— 前缀和数组。
    # ----------------------------------------------------------
    def subarraySum_prefix(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        count = 0
        for i in range(1, n + 1):
            for j in range(i):
                if prefix[i] - prefix[j] == k:
                    count += 1
        return count

    # ----------------------------------------------------------
    # 解法三：前缀和 + 哈希表 —— 最优解法
    # 思路：
    #   1. 核心洞察：子数组 nums[j..i-1] 的和 = prefix[i] - prefix[j]
    #      所以要找有多少个 j 满足 prefix[j] = prefix[i] - k
    #   2. 用字典记录「前缀和 -> 出现次数」，初始时 prefix[0] = 0 出现 1 次
    #   3. 遍历数组，对每个 i：
    #      - 累计 prefix[i]
    #      - 查字典里 prefix[i] - k 出现过几次，加到结果
    #      - 把当前 prefix[i] 的出现次数加入字典
    # 时间复杂度：O(n) —— 每个元素只被访问一次，哈希表查找 O(1)。
    # 空间复杂度：O(n) —— 哈希表最多存 n 个元素。
    # ----------------------------------------------------------
    def subarraySum_hash_table(self, nums: List[int], k: int) -> int:
        prefix_freq = {0: 1}
        prefix_sum = 0
        count = 0
        for num in nums:
            prefix_sum += num
            count += prefix_freq.get(prefix_sum - k, 0)
            prefix_freq[prefix_sum] = prefix_freq.get(prefix_sum, 0) + 1
        return count


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.subarraySum_brute_force),
        ("前缀和枚举", sol.subarraySum_prefix),
        ("哈希表法",   sol.subarraySum_hash_table),
    ]

    test_cases = [
        ([1, 1, 1],         2,  2),
        ([1, 2, 3],         3,  2),
        ([1, -1, 0],        0,  3),
        ([3, 4, 7, 2, -3, 1, 4, 2], 7,  4),
        ([1],               1,  1),
        ([1],               0,  0),
        ([-1, -1, 1],       0,  1),
        ([1, 2, 1, 2, 1],   3,  4),
        ([0, 0, 0, 0],      0, 10),
        ([2, -2, 2, -2, 2], 2,  6),
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
        ("暴力法 O(n^2)",       sol.subarraySum_brute_force),
        ("前缀和枚举 O(n^2)",   sol.subarraySum_prefix),
        ("哈希表法 O(n)",       sol.subarraySum_hash_table),
    ]

    sizes = [100, 1_000, 5_000, 10_000, 20_000]
    repeat = 5

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(-1000, 1000) for _ in range(size)]
        k_val = random.randint(-1000, 1000)

        results_for_size = {}
        for name, fn in methods:
            if "暴力" in name and size > 5_000:
                print(f"{size:>10} | {name:<20} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue
            if "前缀" in name and size > 5_000:
                print(f"{size:>10} | {name:<20} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums), k_val)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            results_for_size[name] = avg_ms
            print(f"{size:>10} | {name:<20} | {avg_ms:>15.3f} | {'':<20}")

        if len(results_for_size) == 3:
            bf_time = results_for_size["暴力法 O(n^2)"]
            ht_time = results_for_size["哈希表法 O(n)"]
            if bf_time > 0 and ht_time > 0:
                print(f"           | {'  -> 哈希表比暴力法快':<20} | {bf_time / ht_time:>15.2f}x | {f'(n={size})':<20}")


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
| 前缀和枚举   | O(n^2)    | O(n)      | 先算前缀和数组，再枚举所有 (j,i) 对     |
| 哈希表法     | O(n)      | O(n)      | 前缀和 + 哈希表计数，最优解法            |

关键洞察：子数组 nums[j..i-1] 的和 = prefix[i] - prefix[j]
  - 对每个位置 i，我们需要知道：有多少个 j 满足 prefix[j] = prefix[i] - k
  - 用哈希表维护「前缀和 -> 出现次数」，即可 O(1) 查询
  - 注意必须先查字典再更新，避免当前 prefix[i] 被自己计入
  - 初始时 prefix[0] = 0 算一次（处理子数组从起点开始的情况）
""")


if __name__ == "__main__":
    print("=== 和为 K 的子数组：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
