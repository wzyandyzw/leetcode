# 题目：子集中元素的最大数量 (LeetCode 3020)
# 难度：中等
# 标签：哈希表、数学、枚举
#
# 题目需求：
#   给定正整数数组 nums，选出一个子集，将子集排成如下模式：
#     [x, x², x⁴, ..., x^{k/2}, x^k, x^{k/2}, ..., x⁴, x², x]
#   其中 k 是 2 的非负次幂（k = 1, 2, 4, 8, ...）。
#   返回满足条件的子集中元素的最大数量。
#
# 约束条件：
#   1. 2 <= nums.length <= 10^5
#   2. 1 <= nums[i] <= 10^9
#
# 核心思路：
#   模式是对称的"平方链"：从 x 开始不断平方上升到峰值 x^k，再对称下降回 x。
#   链中每个非峰值需要至少 2 个拷贝（左右各一个），峰值需要至少 1 个拷贝。
#   对每个起始值 x，沿 v = x, x², x⁴, ... 向上走，
#   每层若 count[v] >= 2 则可作为非峰值继续向上；
#   每层若 count[v] >= 1 则可作为峰值，此时模式长度 = 2*i + 1。
#   由于平方增长极快（x, x², x⁴, ... 几步就超过 10^9），链长远小于 log n，
#   总复杂度 O(n * log log max_val) ≈ O(n)。
#
# 特殊情况 x = 1：
#   1² = 1，整条链都是 1，模式 [1,1,1,...,1] 全部都是 1。
#   设 count[1] = c，最大模式长 = 最大奇数 ≤ c（即 c 或 c-1）。
#
# 本文件提供三种解法，并在末尾做对比试验。


from typing import List
from collections import Counter
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：哈希计数 + 枚举每个起点向上平方链（推荐最优解法）
    # 思路：
    #   1. 用 Counter 统计每个数字出现次数。
    #   2. 特殊处理 1：所有 1 的模式长度为最大奇数 ≤ count[1]。
    #   3. 对每个不同的 x（x != 1），沿 v = x → x² → x⁴ → ... 向上走，
    #      每层都尝试以当前层为峰值，计算长度 2*i + 1。
    #      若 cnt[v] >= 2 则可继续向上；否则只能停在这层。
    # 时间复杂度：O(n * log log max_val) —— 链长远小于 log n（平方增长太快）。
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def maximumLength_hash_chain(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        best = 1

        if 1 in cnt:
            c = cnt[1]
            length = c if c % 2 == 1 else c - 1
            if length > best:
                best = length

        for x in cnt:
            if x == 1:
                continue
            v = x
            i = 0
            while v in cnt:
                peak_len = 2 * i + 1
                if peak_len > best:
                    best = peak_len
                if cnt[v] < 2:
                    break
                v = v * v
                if v > 10**9:
                    break
                i += 1
        return best

    # ----------------------------------------------------------
    # 解法二：哈希计数 + 排序后枚举起点（避免重复枚举链上的点）
    # 思路：
    #   与解法一类似，但只从"链的真正起点"开始枚举，
    #   即不存在 sqrt(x) 不在 cnt 中（即 x 不是某个数的平方）的数才作为起点。
    #   这样每个链只枚举一次，减少重复计算。
    #   虽然链本身很短，优化有限，但逻辑上更"干净"。
    # 时间复杂度：O(n)
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def maximumLength_chain_roots(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        best = 1

        if 1 in cnt:
            c = cnt[1]
            length = c if c % 2 == 1 else c - 1
            if length > best:
                best = length

        for x in cnt:
            if x == 1:
                continue
            s = int(x ** 0.5)
            if s * s == x and s in cnt:
                continue  # x is a perfect square of another number in set, skip
            v = x
            i = 0
            while v in cnt:
                peak_len = 2 * i + 1
                if peak_len > best:
                    best = peak_len
                if cnt[v] < 2:
                    break
                v = v * v
                if v > 10**9:
                    break
                i += 1
        return best

    # ----------------------------------------------------------
    # 解法三：记忆化搜索（自顶向下 DP）
    # 思路：
    #   定义 dp[v] = 以 v 为峰值的最长模式长度。
    #   递推：若 v 在 cnt 中：
    #     - cnt[v] >= 1: dp[v] = 1 (至少峰值本身)
    #     - 若 sqrt(v) 在 cnt 中且 cnt[sqrt_v] >= 2: dp[v] = dp[sqrt_v] + 2
    #       (左右各加一层 sqrt(v))
    #   用记忆化递归计算 dp[v]。
    #   对每个 v in cnt，答案 = max(dp[v])。
    #   同样需要单独处理 1。
    # 时间复杂度：O(n)（每个值仅计算一次）
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def maximumLength_dp(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        memo = {}

        def dp(v: int) -> int:
            if v not in cnt:
                return 0
            if v in memo:
                return memo[v]
            res = 1  # at least the peak itself
            s = int(v ** 0.5)
            if s * s == v and s != v and cnt[s] >= 2:
                res = dp(s) + 2
            memo[v] = res
            return res

        best = 1
        if 1 in cnt:
            c = cnt[1]
            length = c if c % 2 == 1 else c - 1
            if length > best:
                best = length

        for v in cnt:
            if v == 1:
                continue
            best = max(best, dp(v))
        return best


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("哈希链法",   sol.maximumLength_hash_chain),
        ("链根法",     sol.maximumLength_chain_roots),
        ("记忆化DP法", sol.maximumLength_dp),
    ]

    test_cases = [
        ([5, 4, 1, 2, 2],                              3),    # ex1: [2,4,2]
        ([1, 3, 2, 4],                                   1),   # ex2: single element only
        ([2, 4, 16, 4, 2],                              5),   # full chain: 2,4,16,4,2
        ([3, 9, 3],                                     3),   # [3,9,3]
        ([2, 4, 8, 4, 2],                               3),   # 8 is not 4²=16, so chain is 2,4 (peak 4): [2,4,2]
        ([1, 1, 1, 1, 1],                               5),   # all 1s: odd count 5
        ([1, 1, 1, 1],                                  3),   # all 1s: even count → 3
        ([1],                                            1),   # single 1
        ([2, 2],                                        1),   # two 2s: only [2] (but can we make [2,2,2]? No, because 2²=4 not 2. So length 1.
        ([4, 4, 16, 16, 256],                         5),   # 4,16,256,16,4 — but need two 4s, two 16s, one 256. length 5.
        ([2, 2, 4, 4, 16, 16, 256, 65536],            7),   # 2,4,16,256,16,4,2? Wait peak? Let me trace:
        # 2:2, 4:2, 16:2, 256:1, 65536:1
        # chain from 2: i=0 v=2 cnt=2: peak_len=1. cnt>=2 continue. v=4.
        # i=1 v=4 cnt=2: peak_len=3. cnt>=2 continue. v=16.
        # i=2 v=16 cnt=2: peak_len=5. cnt>=2 continue. v=256.
        # i=3 v=256 cnt=1: peak_len=7. cnt<2 break.
        # best=7. So [2,4,16,256,16,4,2] length 7. Correct!
    ]
    # Fix: I made a typo above: "[1] should be ([1], 1)
    test_cases[7] = ([1], 1)
    test_cases[8] = ([2, 2], 1)

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
    print("性能对比试验")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("哈希链法 O(n)",   sol.maximumLength_hash_chain),
        ("链根法 O(n)",     sol.maximumLength_chain_roots),
        ("记忆化DP O(n)",  sol.maximumLength_dp),
    ]

    sizes = [1000, 10000, 100000]
    repeat = 20

    print(f"{'数组长度':>10} | {'解法':<24} | {'平均耗时 (ms)':>15}")
    print("-" * 70)

    for size in sizes:
        rng = random.Random(42 + size)
        nums = [rng.randint(1, 10**9) for _ in range(size)]

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                data = list(nums)
                start = time.perf_counter()
                fn(data)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            print(f"{size:>10} | {name:<24} | {avg_ms:>15.3f}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                            |
|------------|-----------|-----------|---------------------------------|
| 哈希链法   | O(n)      | O(n)      | 每个起点向上平方扩展，代码最简洁    |
| 链根法     | O(n)      | O(n)      | 只从链的起点开始，避免重复枚举      |
| 记忆化DP   | O(n)      | O(n)      | 自顶向下，每个值算一次           |

为什么链为什么是 O(n)？
  - 平方链 v → v² → v⁴ → ... 增长极快，几步就超过 10^9。
  - 例如 v=2: 2, 4, 16, 256, 65536, 4294967296 (>10^9) —— 仅 5 层。
  - v=1000: 1000, 1000000, 1e12 (>10^9) —— 仅 2 层。
  - 平均链长远小于 10，因此总操作 ≈ 10 * n = O(n)。

模式长度公式：
  - 峰值在第 i 层（0 起）：长度 = 2*i + 1
  - 0..i-1 层需要 cnt[v] >= 2（左右各出现一次）
  - 第 i 层需要 cnt[v] >= 1（峰值，只出现一次）

x = 1 的特殊性：
  - 1² = 1，整条链都是 1，模式 [1,1,1,...,1] 全部是 1。
  - count[1] = c：最大模式长 = 最大奇数 ≤ c
    即 c 若奇数则 c，c 若偶数则 c-1。
  - 因为模式长度必须是奇数（2m+1）。
""")


if __name__ == "__main__":
    print("=== 子集中元素的最大数量：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
