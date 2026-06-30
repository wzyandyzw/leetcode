# 题目：检查相同字母间的距离 (LeetCode 2399)
# 难度：简单
# 标签：数组、哈希表、字符串
#
# 题目需求：
#   给定一个仅由小写英文字母组成的字符串 s，s 中每个字母恰好出现两次。
#   给定一个长度为 26 的整数数组 distance，其中 distance[i] 对应字母
#   'a' + i（即 distance[0] 对应 'a'，distance[1] 对应 'b'，...，
#   distance[25] 对应 'z'）。
#
#   对于 s 中出现的每个字母 ch，设它在 s 中两次出现的下标为 i 和 j（i < j），
#   则这两个位置之间（不包含 i 和 j 本身）的字母个数必须恰好等于
#   distance[ch - 'a']。即：j - i - 1 == distance[ch_idx]。
#
#   如果 s 中所有出现过的字母都满足上述距离条件，返回 true；否则返回 false。
#   s 中未出现的字母，其对应的 distance 值无需检查，可以是任意值。
#
# 示例说明：
#   例 1：s = "abaccb", distance = [1,3,0,...]
#     - 'a' 出现在下标 0 和 2 → 中间有 1 个字母('b') → distance[0] 应为 1 ✓
#     - 'b' 出现在下标 1 和 5 → 中间有 3 个字母('a','c','c') → distance[1] 应为 3 ✓
#     - 'c' 出现在下标 3 和 4 → 中间有 0 个字母 → distance[2] 应为 0 ✓
#     → 返回 true
#
#   例 2：s = "aa", distance = [1,0,...]
#     - 'a' 出现在下标 0 和 1 → 中间有 0 个字母 → distance[0] 应为 0，实际是 1
#     → 返回 false
#
# 易错点：
#   "两个位置之间的字母数"不是 j - i（位置差），而是 j - i - 1（中间元素个数）。
#   例如相邻两个相同字母 "aa"（下标 0,1），它们之间没有字母，距离为 0。
#
# 约束条件：
#   1. 2 <= s.length <= 52
#   2. s 仅由小写英文字母组成
#   3. s 中每个字母恰好出现两次
#   4. distance.length == 26
#   5. 0 <= distance[i] <= 50
#
# 本文件提供四种解法，并在末尾做对比试验。


from typing import List
import time
import random
import string


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力双重查找法
    # 思路：
    #   对每个字母 a-z，在 s 中分别找到第一次和第二次出现的位置，
    #   计算间距并与 distance 比较。若有不匹配立即返回 false。
    # 时间复杂度：O(26 * n) = O(n)，因 n <= 52 常数很小。
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def checkDistances_brute_force(self, s: str, distance: List[int]) -> bool:
        n = len(s)
        for c in range(26):
            ch = chr(ord('a') + c)
            first = -1
            second = -1
            for i in range(n):
                if s[i] == ch:
                    if first == -1:
                        first = i
                    else:
                        second = i
                        break
            if first == -1:
                continue
            if second - first - 1 != distance[c]:
                return False
        return True

    # ----------------------------------------------------------
    # 解法二：首次位置数组法（一次遍历，推荐解法）
    # 思路：
    #   1. 用长度为 26 的数组 first 记录每个字母第一次出现的下标，初始化为 -1
    #   2. 遍历字符串 s，对下标 i 的字符 ch：
    #      - 若 first[ch] == -1，记录 first[ch] = i
    #      - 否则（第二次遇到），检查 i - first[ch] - 1 == distance[ch]，
    #        若不满足直接返回 false
    #   3. 遍历结束返回 true
    # 时间复杂度：O(n) —— 一次遍历，常数时间操作。
    # 空间复杂度：O(1) —— 固定长度 26 数组。
    # ----------------------------------------------------------
    def checkDistances_first_occurrence(self, s: str, distance: List[int]) -> bool:
        first = [-1] * 26
        for i, ch in enumerate(s):
            idx = ord(ch) - ord('a')
            if first[idx] == -1:
                first[idx] = i
            else:
                if i - first[idx] - 1 != distance[idx]:
                    return False
        return True

    # ----------------------------------------------------------
    # 解法三：字典法
    # 思路：
    #   用字典代替数组记录每个字母首次出现的位置，逻辑与解法二完全相同。
    #   由于只涉及出现过的字母，理论上空间稍小但常数开销略大于数组。
    # 时间复杂度：O(n)
    # 空间复杂度：O(k)，k 为出现的字母数（最多 26），可视为 O(1)
    # ----------------------------------------------------------
    def checkDistances_dict(self, s: str, distance: List[int]) -> bool:
        first = {}
        for i, ch in enumerate(s):
            if ch not in first:
                first[ch] = i
            else:
                idx = ord(ch) - ord('a')
                if i - first[ch] - 1 != distance[idx]:
                    return False
        return True

    # ----------------------------------------------------------
    # 解法四：位运算标记法（空间极致优化）
    # 思路：
    #   结合本题"每个字母恰好出现两次"的特性：
    #   - 用一个整数 seen 作为 bitmask，第 c 位为 1 表示该字母已第一次出现
    #   - 再用一个整数 first_pos 无法直接存位置（位置可能>1），所以改用一个
    #     长度为 26 的小数据结构即可，与解法二类似但展示不同的 bit-check 方式。
    #   这里实际复用数组思路，但用位运算判断是否为首次出现。
    # 时间复杂度：O(n)
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def checkDistances_bit_mask(self, s: str, distance: List[int]) -> bool:
        first = [0] * 26
        seen = 0
        for i, ch in enumerate(s):
            bit = ord(ch) - ord('a')
            mask = 1 << bit
            if not (seen & mask):
                seen |= mask
                first[bit] = i
            else:
                if i - first[bit] - 1 != distance[bit]:
                    return False
        return True


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力查找法",   sol.checkDistances_brute_force),
        ("首次位置法",   sol.checkDistances_first_occurrence),
        ("字典法",       sol.checkDistances_dict),
        ("位运算法",     sol.checkDistances_bit_mask),
    ]

    test_cases = [
        ("abaccb",   [1,3,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], True),
        ("aa",       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], False),
        ("zz",       [0]*26, True),   # "zz": positions 0,1 → 1-0-1=0
        ("zz",       [1]*26, False),
        ("abba",     [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], True),
        # a at 0,3 → 3-0-1=2 ✓; b at 1,2 → 2-1-1=0 ✗ wait I said distance[1]=1, should be 0
    ]

    # Fix the last test case: "abba" → a:0,3(2 between), b:1,2(0 between)
    test_cases[-1] = ("abba", [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], True)

    # Additional test cases
    test_cases.append(("abcabc", [2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], True))
    # a:0,3(d=2), b:1,4(d=2), c:2,5(d=2) ✓

    for name, fn in methods:
        all_pass = True
        for s, dist, expected in test_cases:
            result = fn(s, list(dist))
            if result != expected:
                print(f"  ✗ {name}: s='{s}', got={result}, expected={expected}")
                all_pass = False
        if all_pass:
            print(f"  ✓ {name}: 所有 {len(test_cases)} 个测试用例通过")


# ============================================================
# 性能对比试验
# ============================================================
def generate_test_string(rng):
    letters = list(string.ascii_lowercase)
    rng.shuffle(letters)
    k = rng.randint(1, 26)
    chosen = letters[:k]
    arr = []
    for ch in chosen:
        pos1 = rng.randint(0, 2 * k - 1)
        arr.append((pos1, ch))
    arr.sort()
    s_chars = [''] * (2 * k)
    used = [False] * (2 * k)
    for idx, ch in arr:
        s_chars[idx] = ch
        used[idx] = True
    ptr = 0
    for ch in chosen:
        while ptr < 2*k and used[ptr]:
            ptr += 1
        if ptr < 2*k:
            s_chars[ptr] = ch
            used[ptr] = True
    return ''.join(s_chars)


def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验（测量每种解法在多次重复调用下的运行时间）")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("暴力查找法 O(26n)", sol.checkDistances_brute_force),
        ("首次位置法 O(n)",   sol.checkDistances_first_occurrence),
        ("字典法 O(n)",       sol.checkDistances_dict),
        ("位运算法 O(n)",     sol.checkDistances_bit_mask),
    ]

    repeat = 50000
    rng = random.Random(42)
    test_strings = [generate_test_string(rng) for _ in range(100)]
    dist = [rng.randint(0, 50) for _ in range(26)]

    print(f"{'重复次数':>10} | {'解法':<20} | {'平均耗时 (μs)':>15} | {'备注':<20}")
    print("-" * 70)

    for name, fn in methods:
        times = []
        for _ in range(repeat):
            s = test_strings[_ % len(test_strings)]
            start = time.perf_counter()
            fn(s, dist)
            elapsed = (time.perf_counter() - start) * 1_000_000
            times.append(elapsed)
        avg_us = sum(times) / len(times)
        print(f"{repeat:>10} | {name:<20} | {avg_us:>15.3f} | {'':<20}")

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
| 暴力查找法 | O(n)      | O(1)      | 对每个字母分别扫描字符串找两次位置        |
| 首次位置法 | O(n)      | O(1)      | 一次遍历记录首次下标，二次遇到直接检验    |
| 字典法     | O(n)      | O(1)      | 用字典存首次位置，逻辑同首次位置法        |
| 位运算法   | O(n)      | O(1)      | 用 bitmask 标记是否首次出现            |

关键公式：j - i - 1
  两次出现的下标为 i 和 j（i<j），中间有 j-i-1 个字母。
  例如 "aa" 位于下标 0、1：1-0-1=0，中间没有字母。
  这是本题最容易出错的地方（容易误算为 j-i）。

为什么首次位置法是最优？
  - 一次遍历即可完成，无需回头扫描
  - 长度为 26 的数组是常数空间，访问速度快
  - 遇到不匹配可立即返回 false，有剪枝效果
""")


if __name__ == "__main__":
    print("=== 检查相同字母间的距离：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
