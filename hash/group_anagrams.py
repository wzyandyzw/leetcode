# 题目：字母异位词分组 (LeetCode 49)
# 难度：中等
# 标签：哈希表、字符串、排序
#
# 题目需求：
#   给你一个字符串数组 strs，将字母异位词组合在一起。可以按任意顺序返回结果列表。
#   字母异位词指字母相同但排列不同的字符串。
#
# 约束条件：
#   1. 1 <= strs.length <= 10^4
#   2. 0 <= strs[i].length <= 100
#   3. strs[i] 仅包含小写字母
#
# 核心思路：
#   字母异位词的充要条件是：各字符出现次数完全相同。
#   因此可以设计一个"哈希键"使得互为异位词的字符串具有相同键：
#     - 方案 A：对字符串排序，排序结果作为键
#     - 方案 B：统计 26 个字母出现次数，拼成元组作为键
#     - 方案 C：给每个字母分配唯一质数，用乘积作为键（算术基本定理保证唯一性）
#
# 本文件提供三种解法，并在末尾做对比试验。


from typing import List
from collections import defaultdict
import time
import random
import string


class Solution:
    # ----------------------------------------------------------
    # 解法一：排序法（最直观、最常用）
    # 思路：
    #   将每个字符串按字符排序，排序后的字符串作为字典的键。
    #   互为异位词的字符串排序后必然相同，因此会落入同一个键下。
    # 时间复杂度：O(n * k log k)，n 为字符串数，k 为最大串长。
    # 空间复杂度：O(n * k) —— 字典存储所有字符串。
    # ----------------------------------------------------------
    def groupAnagrams_sort(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)
        return list(groups.values())

    # ----------------------------------------------------------
    # 解法二：字符计数法（时间复杂度更优）
    # 思路：
    #   统计每个字符串中 a~z 每个字母出现的次数，将长度为 26 的计数
    #   元组作为键。互为异位词的字符串有相同的字符计数，因此键相同。
    #   对长度为 k 的字符串，计数是 O(k)，比拼对排序的 O(k log k) 更优。
    # 时间复杂度：O(n * k)
    # 空间复杂度：O(n * k)
    # ----------------------------------------------------------
    def groupAnagrams_count(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            cnt = [0] * 26
            for ch in s:
                cnt[ord(ch) - ord('a')] += 1
            groups[tuple(cnt)].append(s)
        return list(groups.values())

    # ----------------------------------------------------------
    # 解法三：质数乘积法（数学方法）
    # 思路：
    #   给 26 个小写字母各分配一个素数 primes[0..25]。
    #   每个字符串的键 = 各字母对应素数的乘积。
    #   由算术基本定理，素数分解唯一，因此互为异位词的字符串乘积相同，
    #   不同字符组成的字符串乘积不同（无碰撞）。
    #   Python 原生大整数不会溢出，但长串乘积极大，乘法代价不可忽略。
    # 时间复杂度：O(n * k)
    # 空间复杂度：O(n * k)
    # ----------------------------------------------------------
    def groupAnagrams_prime(self, strs: List[str]) -> List[List[str]]:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                  31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                  73, 79, 83, 89, 97, 101]
        groups = defaultdict(list)
        for s in strs:
            key = 1
            for ch in s:
                key *= primes[ord(ch) - ord('a')]
            groups[key].append(s)
        return list(groups.values())


# ============================================================
# 辅助函数：比较两个分组结果是否相同（忽略组内和组间顺序）
# ============================================================
def _results_equal(res1: List[List[str]], res2: List[List[str]]) -> bool:
    def normalize(result):
        return sorted([sorted(group) for group in result])
    return normalize(res1) == normalize(res2)


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("排序法",   sol.groupAnagrams_sort),
        ("计数法",   sol.groupAnagrams_count),
        ("质数法",   sol.groupAnagrams_prime),
    ]

    test_cases = [
        (["eat", "tea", "tan", "ate", "nat", "bat"],
         [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
        ([""], [[""]]),
        (["a"], [["a"]]),
        (["", ""], [["", ""]]),
        (["ab", "ba", "abc", "cba", "bac"], [["ab", "ba"], ["abc", "cba", "bac"]]),
        (["ddddddddddg", "dgggggggggg"], [["ddddddddddg"], ["dgggggggggg"]]),
        (["abc", "def", "ghi"], [["abc"], ["def"], ["ghi"]]),
        (["aab", "aba", "baa", "abb", "bba", "bab"], [["aab", "aba", "baa"], ["abb", "bba", "bab"]]),
    ]

    for name, fn in methods:
        all_pass = True
        for strs, expected in test_cases:
            result = fn(list(strs))
            if not _results_equal(result, expected):
                print(f"  ✗ {name}: strs={strs}")
                print(f"     got:      {sorted([sorted(g) for g in result])}")
                print(f"     expected: {sorted([sorted(g) for g in expected])}")
                all_pass = False
        if all_pass:
            print(f"  ✓ {name}: 所有 {len(test_cases)} 个测试用例通过")


# ============================================================
# 性能对比试验
# ============================================================
def _random_string(rng: random.Random, max_len: int = 100) -> str:
    length = rng.randint(1, max_len)
    return ''.join(rng.choice(string.ascii_lowercase) for _ in range(length))


def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验（测量每种解法在不同规模数据上的运行时间）")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("排序法 O(nk log k)", sol.groupAnagrams_sort),
        ("计数法 O(nk)",       sol.groupAnagrams_count),
        ("质数法 O(nk)",       sol.groupAnagrams_prime),
    ]

    sizes = [100, 500, 1000, 5000, 10000]
    repeat = 3

    print(f"{'字符串数':>10} | {'解法':<22} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        rng = random.Random(42 + size)
        strs = [_random_string(rng) for _ in range(size)]

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                data = list(strs)
                start = time.perf_counter()
                fn(data)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            print(f"{size:>10} | {name:<22} | {avg_ms:>15.3f} | {'':<20}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法     | 时间复杂度   | 空间复杂度 | 说明                                  |
|----------|-------------|-----------|---------------------------------------|
| 排序法   | O(n k log k)| O(nk)     | 最直观，代码最短，面试常用写法          |
| 计数法   | O(n k)      | O(nk)     | 避免排序开销，理论复杂度更优            |
| 质数法   | O(n k)      | O(nk)     | 数学优美，但 Python 大整数乘法有开销    |

为什么字母异位词可以用哈希表分组？
  - 两个字符串是异位词 ⇔ 它们的字符多重集相等 ⇔ 存在一个规范化表示
    （canonical form）使它们映射到同一个键。
  - 排序字符串、字符计数元组、素数乘积都是合法的规范化表示。

计数法的优势：
  - 对长度为 k 的字符串，排序需要 O(k log k)，而计数只需 O(k)。
  - 当 k 较大时（如本题 k=100），计数法优势明显。
  - 计数元组是固定长度 26 的整数元组，哈希稳定。

质数法的注意事项：
  - 虽然算术基本定理保证唯一性，但在非 Python 语言中乘积可能溢出
    （例如 26 个素数前 26 个乘积已远超 64 位整数），需要额外处理。
  - Python 原生支持大整数，但大整数乘法本身不是 O(1)，实际未必更快。
""")


if __name__ == "__main__":
    print("=== 字母异位词分组：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
