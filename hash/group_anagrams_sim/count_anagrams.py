# 题目：统计同位异构字符串数目 (LeetCode 2514)
# 难度：困难
# 标签：哈希表、数学、字符串、组合数学、计数
#
# 题目需求：
#   字符串 s 由若干单词（空格分隔）组成。若字符串 t 的每个位置上的单词
#   都是 s 对应位置单词的字母重排（同位异构/字母异位词），则 t 是 s 的
#   "同位异构字符串"。返回这样的 t 的数目，模 10^9+7。
#
# 约束条件：
#   1. 1 <= s.length <= 10^5
#   2. s 仅包含小写字母和空格，相邻单词由单个空格分隔
#
# 核心数学：
#   - 单词间相互独立（顺序固定，仅内部重排），故答案 = 各单词不同排列数之积。
#   - 一个长度为 m 的单词，含重复字母的不同排列数 = m! / (c_a! * c_b! * ... * c_z!)，
#     其中 c_ch 为该单词中字符 ch 的出现次数（多重集排列公式）。
#   - 在模 MOD=10^9+7（素数）下，除法用乘法逆元代替：1/x ≡ x^(MOD-2) (mod MOD)。
#   - 预处理阶乘 fact[i] = i! mod MOD 和阶乘逆元 inv_fact[i] = (i!)^(-1) mod MOD，
#     即可 O(1) 查询任意排列数。
#
# 本文件提供三种解法，并在末尾做对比试验。


from collections import Counter
import time
import random
import string

MOD = 10**9 + 7
MAXN = 10**5 + 10

# 全局预处理阶乘及其逆元（解法一和解法三使用）
_fact = [1] * MAXN
for i in range(1, MAXN):
    _fact[i] = _fact[i - 1] * i % MOD

_inv_fact = [1] * MAXN
_inv_fact[MAXN - 1] = pow(_fact[MAXN - 1], MOD - 2, MOD)
for i in range(MAXN - 2, -1, -1):
    _inv_fact[i] = _inv_fact[i + 1] * (i + 1) % MOD


class Solution:
    # ----------------------------------------------------------
    # 解法一：预处理阶乘 + 逆元（推荐最优解法）
    # 思路：
    #   预处理 fact[0..MAXN] 和 inv_fact[0..MAXN]。
    #   对每个单词：ans = ans * fact[m] * Π inv_fact[cnt[ch]] mod MOD。
    # 时间复杂度：O(MAXN) 预处理 + O(n) 处理（n 为 s 长度）。
    # 空间复杂度：O(MAXN)（常数级别，固定 10^5）。
    # ----------------------------------------------------------
    def countAnagrams_precompute(self, s: str) -> int:
        ans = 1
        for word in s.split():
            m = len(word)
            ans = ans * _fact[m] % MOD
            cnt = [0] * 26
            for ch in word:
                cnt[ord(ch) - ord('a')] += 1
            for c in cnt:
                if c > 0:
                    ans = ans * _inv_fact[c] % MOD
        return ans

    # ----------------------------------------------------------
    # 解法二：逐单词求逆元（不做全局预处理）
    # 思路：
    #   对每个单词现场计算 m!，以及对每个重复字母出现次数 c 用 pow(c!, MOD-2)
    #   求逆元相乘。不依赖全局预处理，写法更自洽，但每个单词要算若干次 pow，
    #   在单词多且每个单词短的情况下有常数开销。
    # 时间复杂度：O(n * log MOD)，每个字符对应一次乘法，逆元调用 O(log MOD)。
    # 空间复杂度：O(1)（不含局部变量）。
    # ----------------------------------------------------------
    def countAnagrams_per_word(self, s: str) -> int:
        ans = 1
        for word in s.split():
            m = len(word)
            f = 1
            for i in range(2, m + 1):
                f = f * i % MOD
            ans = ans * f % MOD
            for c in Counter(word).values():
                if c > 1:
                    inv = 1
                    fc = 1
                    for i in range(2, c + 1):
                        fc = fc * i % MOD
                    inv = pow(fc, MOD - 2, MOD)
                    ans = ans * inv % MOD
        return ans

    # ----------------------------------------------------------
    # 解法三：预处理阶乘 + Counter 统计（写法更 Pythonic）
    # 思路：
    #   与解法一相同，但用 collections.Counter 统计字符频次，代码更简洁。
    #   Counter 对每个单词遍历一次；对长度 10^5 的字符串总复杂度仍 O(n)。
    # 时间复杂度：O(n)（Counter 构建 + 查表）。
    # 空间复杂度：O(k)，k 为单个单词内不同字符数（≤26）。
    # ----------------------------------------------------------
    def countAnagrams_counter(self, s: str) -> int:
        ans = 1
        for word in s.split():
            ans = ans * _fact[len(word)] % MOD
            for c in Counter(word).values():
                ans = ans * _inv_fact[c] % MOD
        return ans


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("预处理+数组法",   sol.countAnagrams_precompute),
        ("逐单词法",        sol.countAnagrams_per_word),
        ("预处理+Counter法", sol.countAnagrams_counter),
    ]

    test_cases = [
        ("too hot",                                         18),
        ("aa",                                              1),
        ("a",                                               1),
        ("ab",                                              2),
        ("abc",                                             6),
        ("abc def",                                         6 * 6),
        ("aab",                                             3),       # 3!/(2!1!)=3
        ("aaa",                                             1),       # 3!/(3!)=1
        ("aaab",                                            4),       # 4!/(3!1!)=4
        ("aabb",                                            6),       # 4!/(2!2!)=6
        ("too hot too",                                     18 * 3),
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
def _random_sentence(rng: random.Random, total_chars: int) -> str:
    words = []
    remaining = total_chars
    while remaining > 0:
        wlen = min(remaining, rng.randint(1, 10))
        words.append(''.join(rng.choice(string.ascii_lowercase) for _ in range(wlen)))
        remaining -= wlen + 1
    return ' '.join(words)


def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("预处理+数组法 O(n)",     sol.countAnagrams_precompute),
        ("逐单词法 O(n log MOD)", sol.countAnagrams_per_word),
        ("预处理+Counter O(n)",   sol.countAnagrams_counter),
    ]

    sizes = [1000, 10000, 100000]
    repeat = 100

    print(f"{'总字符数':>10} | {'解法':<28} | {'平均耗时 (μs)':>15}")
    print("-" * 70)

    for size in sizes:
        rng = random.Random(42 + size)
        s = _random_sentence(rng, size)

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(s)
                elapsed = (time.perf_counter() - start) * 1_000_000
                times.append(elapsed)
            avg_us = sum(times) / len(times)
            print(f"{size:>10} | {name:<28} | {avg_us:>15.3f}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print(f"""
| 解法           | 时间复杂度     | 空间复杂度 | 说明                         |
|----------------|---------------|-----------|------------------------------|
| 预处理+数组法  | O(MAXN + n)   | O(MAXN)   | 预处理阶乘逆元，查询最快      |
| 逐单词法       | O(n log MOD)  | O(1)      | 不做预处理，每次求逆元        |
| 预处理+Counter | O(MAXN + n)   | O(MAXN)   | 代码更 Pythonic，略慢于数组法 |

MOD = {MOD}（质数），采用费马小定理计算逆元：a^(MOD-2) ≡ a^(-1) (mod MOD)。

多重集排列公式：
  长度为 m、各字符出现次数为 c_1, c_2, ..., c_k 的字符串，
  其不同排列数目为：m! / (c_1! * c_2! * ... * c_k!)

预处理技巧：
  1. fact[i]    = fact[i-1] * i mod MOD
  2. inv_fact[n] = fact[n]^(MOD-2) mod MOD   （用快速幂算最大项的逆元）
  3. inv_fact[i] = inv_fact[i+1] * (i+1) mod MOD  （倒推）
  这样所有阶乘逆元 O(n) 一次算完，比单独 pow 更快。
""")


if __name__ == "__main__":
    print("=== 统计同位异构字符串数目：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
