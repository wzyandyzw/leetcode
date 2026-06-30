# 题目：有效的字母异位词 (LeetCode 242)
# 难度：简单
# 标签：哈希表、字符串、排序
#
# 题目需求：
#   给定两个字符串 s 和 t，判断 t 是否是 s 的字母异位词
#   （即是否由相同字符以任意顺序排列组成）。
#
# 约束条件：
#   1. 1 <= s.length, t.length <= 5 * 10^4
#   2. s 和 t 仅包含小写字母
#
# 进阶问题：
#   如果输入字符串包含 unicode 字符怎么办？
#   → 使用字典（哈希表）而不是固定大小数组，因为 unicode 字符集太大，
#     无法用数组直接计数；Python 的 dict/defaultdict/Counter 天然支持。
#
# 本文件提供五种解法（含 unicode 版本），并在末尾做对比试验。


from typing import Dict
from collections import Counter, defaultdict
import time
import random
import string


class Solution:
    # ----------------------------------------------------------
    # 解法一：排序比较法
    # 思路：
    #   字母异位词排序后必然相同；长度不同直接返回 false。
    # 时间复杂度：O(n log n) —— 排序占主要时间。
    # 空间复杂度：O(n)（取决于排序实现，此处为 Python sorted 的开销）
    # ----------------------------------------------------------
    def isAnagram_sort(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)

    # ----------------------------------------------------------
    # 解法二：双数组计数法
    # 思路：
    #   用两个长度为 26 的数组分别统计 s 和 t 中各字母出现次数，
    #   最后比较两个数组是否完全相等。
    # 时间复杂度：O(n)
    # 空间复杂度：O(1) —— 两个固定大小 26 数组。
    # ----------------------------------------------------------
    def isAnagram_two_arrays(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        cnt_s = [0] * 26
        cnt_t = [0] * 26
        for ch in s:
            cnt_s[ord(ch) - ord('a')] += 1
        for ch in t:
            cnt_t[ord(ch) - ord('a')] += 1
        return cnt_s == cnt_t

    # ----------------------------------------------------------
    # 解法三：单数组计数法（推荐最优解法）
    # 思路：
    #   只用一个长度为 26 的数组：遍历 s 时对对应位置 +1，
    #   遍历 t 时对对应位置 -1；最后检查数组是否全为 0。
    #   节省了一个数组空间，且一次扫描即可（但仍需先判断长度）。
    # 时间复杂度：O(n)
    # 空间复杂度：O(1) —— 单个固定大小数组。
    # ----------------------------------------------------------
    def isAnagram_single_array(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        for ch in t:
            idx = ord(ch) - ord('a')
            cnt[idx] -= 1
            if cnt[idx] < 0:
                return False
        return all(v == 0 for v in cnt)

    # ----------------------------------------------------------
    # 解法四：Counter 字典法（支持 Unicode，进阶答案）
    # 思路：
    #   使用 collections.Counter 统计两个字符串中各字符的频次，
    #   直接比较两个 Counter 是否相等。
    #   Counter 基于哈希表，天然支持任意 unicode 字符。
    # 时间复杂度：O(n)
    # 空间复杂度：O(k)，k 为不同字符数；小写字母时 k=26 即 O(1)。
    # ----------------------------------------------------------
    def isAnagram_counter(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)

    # ----------------------------------------------------------
    # 解法五：defaultdict 手动字典法（支持 Unicode，不依赖 Counter）
    # 思路：
    #   用 defaultdict(int) 手动维护字符计数：+s 字符，-t 字符，
    #   最后检查所有值是否为 0。
    #   相比 Counter 更底层，适用于任何字符集（包括 unicode）。
    # 时间复杂度：O(n)
    # 空间复杂度：O(k)
    # ----------------------------------------------------------
    def isAnagram_dict(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        cnt: Dict[str, int] = defaultdict(int)
        for ch in s:
            cnt[ch] += 1
        for ch in t:
            cnt[ch] -= 1
            if cnt[ch] < 0:
                return False
        for v in cnt.values():
            if v != 0:
                return False
        return True


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("排序法",       sol.isAnagram_sort),
        ("双数组法",     sol.isAnagram_two_arrays),
        ("单数组法",     sol.isAnagram_single_array),
        ("Counter法",    sol.isAnagram_counter),
        ("字典法",       sol.isAnagram_dict),
    ]

    test_cases_ascii = [
        ("anagram", "nagaram", True),
        ("rat",     "car",     False),
        ("",        "",        True),
        ("a",       "a",       True),
        ("a",       "b",       False),
        ("ab",      "ba",      True),
        ("ab",      "ab",      True),
        ("abc",     "abd",     False),
        ("aacc",    "ccac",    False),
        ("listen",  "silent",  True),
    ]

    test_cases_unicode = [
        ("你好世界", "界世好你", True),
        ("你好世界", "好你啊界", False),
    ]

    for name, fn in methods:
        all_pass = True
        for s, t, expected in test_cases_ascii:
            result = fn(s, t)
            if result != expected:
                print(f"  ✗ {name}: s='{s}', t='{t}', got={result}, expected={expected}")
                all_pass = False
        supports_unicode = name in ("Counter法", "字典法", "排序法")
        if supports_unicode:
            for s, t, expected in test_cases_unicode:
                result = fn(s, t)
                if result != expected:
                    print(f"  ✗ {name} (unicode): s='{s}', t='{t}', got={result}, expected={expected}")
                    all_pass = False
        total = len(test_cases_ascii) + (len(test_cases_unicode) if supports_unicode else 0)
        if all_pass:
            print(f"  ✓ {name}: 所有 {total} 个测试用例通过")


# ============================================================
# 性能对比试验
# ============================================================
def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验（测量每种解法在不同规模数据上的运行时间）")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("排序法 O(n log n)",  sol.isAnagram_sort),
        ("双数组法 O(n)",      sol.isAnagram_two_arrays),
        ("单数组法 O(n)",      sol.isAnagram_single_array),
        ("Counter法 O(n)",     sol.isAnagram_counter),
        ("字典法 O(n)",        sol.isAnagram_dict),
    ]

    sizes = [100, 1000, 10000, 50000]
    repeat = 200

    print(f"{'字符串长度':>10} | {'解法':<22} | {'平均耗时 (μs)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        rng = random.Random(42 + size)
        s = ''.join(rng.choice(string.ascii_lowercase) for _ in range(size))
        t_chars = list(s)
        rng.shuffle(t_chars)
        t = ''.join(t_chars)

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(s, t)
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
    print("五种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 支持Unicode | 说明                         |
|------------|-----------|-----------|-------------|------------------------------|
| 排序法     | O(n log n)| O(n)      | 是          | 代码最短，最易写              |
| 双数组法   | O(n)      | O(1)      | 否          | 两个数组分别统计再比较         |
| 单数组法   | O(n)      | O(1)      | 否          | 一增一减，省空间，推荐首选     |
| Counter法  | O(n)      | O(k)      | 是          | Python 内置，unicode 首选    |
| 字典法     | O(n)      | O(k)      | 是          | 手动哈希表，不依赖 Counter    |

进阶问题（Unicode 字符）的解法：
  - 固定大小数组只适用于小写字母、ASCII 等值域有限的情况。
  - Unicode 字符总数超过百万，不可能用数组计数。
  - 此时必须使用哈希表（dict / defaultdict / Counter），
    用字符本身作为键来统计频次，空间取决于实际出现的不同字符数。
  - Python 中 Counter(s) == Counter(t) 是最简洁的答案。

单数组法的剪枝优化：
  - 在遍历 t 时一旦 cnt[idx] 减到负数就立即返回 false，
    说明 t 中某个字符出现次数超过 s，无需继续扫描。
  - 这在"非异位词"情况下能提前终止，平均更快。
""")


if __name__ == "__main__":
    print("=== 有效的字母异位词：五种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
