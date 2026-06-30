# 题目：最长的字母序连续子字符串的长度 (LeetCode 2414)
# 难度：中等
# 标签：字符串
#
# 题目需求：
#   给定仅由小写字母组成的字符串 s，返回最长的"字母序连续子字符串"的长度。
#   字母序连续指字符串中相邻字符在字母表中恰好相差 1（如 "abc", "xyz"）。
#
# 约束条件：
#   1. 1 <= s.length <= 10^5
#   2. s 由小写英文字母组成
#
# 核心思路：
#   从左到右一次扫描，维护"当前连续长度"cur：
#     - 若 s[i] 恰为 s[i-1] 的后继字母（ord 差 1），cur++；
#     - 否则 cur 重置为 1（新的连续段从 s[i] 开始）。
#   过程中持续更新 best = max(best, cur)。
#   每个字符最多处理一次，O(n) 时间、O(1) 空间。
#
# 本文件提供四种解法，并在末尾做对比试验。


import time
import random
import string
from itertools import groupby


class Solution:
    # ----------------------------------------------------------
    # 解法一：一次遍历（推荐最优解法）
    # 思路：
    #   初始化 best=cur=1（单个字符本身就是长度 1 的连续串）。
    #   从下标 1 开始：若当前字符 ord(c) - ord(prev) == 1 则 cur++，
    #   否则 cur 重置为 1；每步更新 best。
    # 时间复杂度：O(n)
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def longestContinuousSubstring_linear(self, s: str) -> int:
        best = cur = 1
        for i in range(1, len(s)):
            if ord(s[i]) - ord(s[i - 1]) == 1:
                cur += 1
                if cur > best:
                    best = cur
            else:
                cur = 1
        return best

    # ----------------------------------------------------------
    # 解法二：一次遍历（更简洁写法，用 max）
    # 思路：同解法一，但用 best = max(best, cur) 更新，代码更整齐。
    # 时间复杂度：O(n)
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def longestContinuousSubstring_concise(self, s: str) -> int:
        best = cur = 1
        for i in range(1, len(s)):
            if ord(s[i]) - ord(s[i - 1]) == 1:
                cur += 1
            else:
                cur = 1
            best = max(best, cur)
        return best

    # ----------------------------------------------------------
    # 解法三：差分数组法
    # 思路：
    #   构造差分数组 diff，其中 diff[i] = 1 当 ord(s[i])-ord(s[i-1])==1，
    #   否则为 0。问题转化为"求最长连续 1 的长度 + 1"。
    #   与解法一等价，但额外使用了数组（主要用于教学展示思路转化）。
    # 时间复杂度：O(n)
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def longestContinuousSubstring_diff(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0
        best = cur = 1
        for i in range(1, n):
            if ord(s[i]) - ord(s[i - 1]) == 1:
                cur += 1
            else:
                best = max(best, cur)
                cur = 1
        return max(best, cur)

    # ----------------------------------------------------------
    # 解法四：itertools.groupby 函数式写法
    # 思路：
    #   用 groupby 按"相邻字符 ord 差是否为 1"分组，但 groupby 只按相邻
    #   相等元素分组，因此需要先构造一个"分组键"序列：对每对相邻字符给出
    #   一个递增的组号，差不为 1 时组号加 1；然后找最长组的长度。
    #   写法更 Pythonic，适合展示函数式风格。
    # 时间复杂度：O(n)
    # 空间复杂度：O(n)（分组过程产生若干中间结构）
    # ----------------------------------------------------------
    def longestContinuousSubstring_groupby(self, s: str) -> int:
        if not s:
            return 0
        groups = [0]
        gid = 0
        for i in range(1, len(s)):
            if ord(s[i]) - ord(s[i - 1]) != 1:
                gid += 1
            groups.append(gid)
        best = 0
        for _, g in groupby(groups):
            length = sum(1 for _ in g)
            if length > best:
                best = length
        return best


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("一次遍历法",   sol.longestContinuousSubstring_linear),
        ("简洁写法",     sol.longestContinuousSubstring_concise),
        ("差分数组法",   sol.longestContinuousSubstring_diff),
        ("groupby法",    sol.longestContinuousSubstring_groupby),
    ]

    test_cases = [
        ("abacaba",   2),
        ("abcde",     5),
        ("a",         1),
        ("ab",        2),
        ("zyx",       1),       # 逆序，每个字符单独为段
        ("abcabc",    3),       # "abc"+"abc"
        ("abxyzcd",   3),       # "ab"(2), "xyz"(3), "cd"(2) → 3
        ("abcdefghijklmnopqrstuvwxyz", 26),
        ("abcbcd",    3),       # "abc"(3), "bcd"(3) → 3
        ("aabbccddeeff", 2),    # 每个重复段长度2，但aa差0不算连续 → 最大为2（ab,bc,cd,de,ef之间）
        # Wait let me recount: "aabbccddeeff": a-a:0, a-b:1, b-b:0, b-c:1, c-c:0, c-d:1, d-d:0, d-e:1, e-e:0, e-f:1, f-f:0
        # Consecutive runs: "a"=1, "ab"=2, "b"=1, "bc"=2, "c"=1, "cd"=2, "d"=1, "de"=2, "e"=1, "ef"=2, "f"=1 → best=2
    ]

    for name, fn in methods:
        all_pass = True
        for s, expected in test_cases:
            result = fn(s)
            if result != expected:
                print(f"  ✗ {name}: s='{s}', got={result}, expected={expected}")
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
        ("一次遍历法 O(n)",   sol.longestContinuousSubstring_linear),
        ("简洁写法 O(n)",     sol.longestContinuousSubstring_concise),
        ("差分数组法 O(n)",   sol.longestContinuousSubstring_diff),
        ("groupby法 O(n)",    sol.longestContinuousSubstring_groupby),
    ]

    sizes = [1000, 10000, 100000]
    repeat = 200

    print(f"{'字符串长度':>10} | {'解法':<22} | {'平均耗时 (μs)':>15}")
    print("-" * 70)

    for size in sizes:
        rng = random.Random(42 + size)
        s = ''.join(rng.choice(string.ascii_lowercase) for _ in range(size))

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(s)
                elapsed = (time.perf_counter() - start) * 1_000_000
                times.append(elapsed)
            avg_us = sum(times) / len(times)
            print(f"{size:>10} | {name:<22} | {avg_us:>15.3f}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("四种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                          |
|------------|-----------|-----------|-------------------------------|
| 一次遍历法 | O(n)      | O(1)      | 最优：一次扫描、常数变量        |
| 简洁写法   | O(n)      | O(1)      | 同解法一，代码更整齐            |
| 差分数组法 | O(n)      | O(n)      | 思路等价，仅作教学展示          |
| groupby法  | O(n)      | O(n)      | 函数式风格，Pythonic            |

为什么一次遍历是正确的？
  - "字母序连续子字符串"要求的是相邻字符差恰好为 1，这是一个纯粹的局部条件：
    只要知道"到位置 i 为止连续了多少个字符"，就能判断 i+1 是否延长了该段。
  - 当 s[i+1] 不是 s[i] 的后继字母时，以 i+1 结尾的连续段长度为 1；
    否则长度为 cur+1。这是典型的动态规划状态转移：
      dp[i] = dp[i-1] + 1  若 ord(s[i])-ord(s[i-1])==1
      dp[i] = 1            否则
  - 由于 dp[i] 只依赖 dp[i-1]，只需一个变量 cur 滚动，不需要完整 dp 数组。
  - 答案为 max(dp)。
""")


if __name__ == "__main__":
    print("=== 最长的字母序连续子字符串的长度：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
