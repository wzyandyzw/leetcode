# 题目：第一个出现两次的字母 (LeetCode 2351)
# 难度：简单
# 标签：哈希表、字符串、位运算
#
# 题目需求：
#   给你一个由小写英文字母组成的字符串 s，请你找出并返回第一个出现两次的字母。
#
# 注意：
#   1. 如果 a 的第二次出现比 b 的第二次出现在字符串中的位置更靠前，则认为字母 a 在字母 b 之前出现两次。
#   2. s 包含至少一个出现两次的字母。
#
# 约束条件：
#   1. 2 <= s.length <= 100
#   2. s 由小写英文字母组成
#   3. s 包含至少一个重复字母
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


import time
import random
import string


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（双重循环）
    # 思路：
    #   1. 遍历字符串，对每个位置 i 的字符 ch = s[i]
    #   2. 在 s[0..i-1] 中查找是否存在与 ch 相同的字符
    #   3. 第一个找到的重复字符就是答案（因为是按顺序遍历，第二次出现位置最小）
    # 时间复杂度：O(n^2) —— 最坏情况下每个字符都要和前面所有字符比较。
    # 空间复杂度：O(1) —— 只使用常数额外空间。
    # ----------------------------------------------------------
    def repeatedCharacter_brute_force(self, s: str) -> str:
        n = len(s)
        for i in range(n):
            for j in range(i):
                if s[i] == s[j]:
                    return s[i]
        return ""

    # ----------------------------------------------------------
    # 解法二：哈希集合法（一次遍历）—— 最直观的解法
    # 思路：
    #   1. 使用一个集合 seen 记录已经出现过的字符
    #   2. 遍历字符串，对每个字符 ch：
    #      - 如果 ch 已经在 seen 中，说明这是它第二次出现，直接返回
    #      - 否则将 ch 加入 seen
    #   3. 因为按顺序遍历，第一个遇到的已存在字符就是「第二次出现位置最早」的那个
    # 时间复杂度：O(n) —— 每个字符只访问一次，集合查找 O(1)。
    # 空间复杂度：O(1) —— 最多存储 26 个小写字母，常数空间。
    # ----------------------------------------------------------
    def repeatedCharacter_hash_set(self, s: str) -> str:
        seen = set()
        for ch in s:
            if ch in seen:
                return ch
            seen.add(ch)
        return ""

    # ----------------------------------------------------------
    # 解法三：位运算法（状态压缩）—— 最优空间
    # 思路：
    #   1. 小写字母只有 26 个，可以用一个 32 位整数的每一位来表示对应字母是否出现过
    #      例如第 0 位表示 'a' 是否出现，第 1 位表示 'b' 是否出现，以此类推
    #   2. 遍历字符串，对每个字符 ch，计算其对应的位掩码 mask = 1 << (ord(ch) - ord('a'))
    #   3. 用位与运算 (&) 判断该位是否已经被置为 1（即该字符是否出现过）
    #      - 如果 seen & mask != 0，说明该字符之前出现过，返回 ch
    #      - 否则用位或运算 (|) 将该位置为 1
    # 时间复杂度：O(n) —— 每个字符只访问一次，位运算 O(1)。
    # 空间复杂度：O(1) —— 只用了一个整数变量，空间最优。
    # ----------------------------------------------------------
    def repeatedCharacter_bit_mask(self, s: str) -> str:
        seen = 0
        for ch in s:
            mask = 1 << (ord(ch) - ord('a'))
            if seen & mask:
                return ch
            seen |= mask
        return ""

    # ----------------------------------------------------------
    # 解法四：布尔数组法
    # 思路：
    #   1. 用一个长度为 26 的布尔数组记录每个字母是否出现过
    #   2. 遍历字符串，对每个字符 ch，计算索引 idx = ord(ch) - ord('a')
    #   3. 如果 seen[idx] 为 True，返回 ch；否则设为 True
    # 时间复杂度：O(n) —— 每个字符只访问一次，数组访问 O(1)。
    # 空间复杂度：O(1) —— 固定大小的数组，常数空间。
    # ----------------------------------------------------------
    def repeatedCharacter_bool_array(self, s: str) -> str:
        seen = [False] * 26
        for ch in s:
            idx = ord(ch) - ord('a')
            if seen[idx]:
                return ch
            seen[idx] = True
        return ""


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.repeatedCharacter_brute_force),
        ("哈希集合法", sol.repeatedCharacter_hash_set),
        ("位运算法",   sol.repeatedCharacter_bit_mask),
        ("布尔数组法", sol.repeatedCharacter_bool_array),
    ]

    test_cases = [
        ("abccbaacz", "c"),
        ("abcdd",     "d"),
        ("aa",        "a"),
        ("abba",      "b"),
        ("zz",        "z"),
        ("abcabc",    "a"),
        ("abac",      "a"),
        ("hello",     "l"),
        ("leetcode",  "e"),
        ("abcdcba",   "c"),
    ]

    for name, fn in methods:
        all_pass = True
        for s, expected in test_cases:
            result = fn(s)
            if result != expected:
                print(f"  ✗ {name}: s='{s}', got='{result}', expected='{expected}'")
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
        ("暴力法 O(n^2)",    sol.repeatedCharacter_brute_force),
        ("哈希集合法 O(n)",  sol.repeatedCharacter_hash_set),
        ("位运算法 O(n)",    sol.repeatedCharacter_bit_mask),
        ("布尔数组法 O(n)",  sol.repeatedCharacter_bool_array),
    ]

    sizes = [100, 1_000, 5_000, 10_000, 50_000, 100_000]
    repeat = 1000

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (μs)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        chars = [random.choice(string.ascii_lowercase) for _ in range(size)]
        duplicate_pos = random.randint(size // 2, size - 1)
        chars[duplicate_pos] = chars[duplicate_pos // 2]
        s = ''.join(chars)

        for name, fn in methods:
            if "暴力" in name and size > 5_000:
                print(f"{size:>10} | {name:<20} | {'> 100000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(s)
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
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                    |
|------------|-----------|-----------|-----------------------------------------|
| 暴力法     | O(n^2)    | O(1)      | 双重循环比较，n 较大时不可用              |
| 哈希集合法 | O(n)      | O(1)      | 一次遍历，集合记录已见字符，最直观         |
| 位运算法   | O(n)      | O(1)      | 用整数位标记字母，空间最优，速度最快       |
| 布尔数组法 | O(n)      | O(1)      | 用固定长度数组记录，实现简单清晰           |

为什么一次遍历就能找到答案？
  - 题目要求的是「第二个出现位置最靠前」的字母
  - 从左到右遍历时，第一个遇到的「已经见过」的字符，
    它的第二次出现位置就是当前位置，这一定是最早的第二次出现位置
  - 因为任何其他字母的第二次出现位置都不可能比当前位置更早

位运算法的核心原理：
  - 26 个小写字母 → 只需要 26 个 bit，一个 32 位整数足够
  - mask = 1 << (ord(ch) - ord('a'))：将对应位置 1
  - seen & mask：判断该位是否已经是 1（之前出现过）
  - seen |= mask：将该位置为 1（标记为已出现）
  - 位运算速度极快，且不需要额外的数据结构开销
""")


if __name__ == "__main__":
    print("=== 第一个出现两次的字母：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
