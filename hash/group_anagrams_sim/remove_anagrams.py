# 题目：移除字母异位词后的结果数组 (LeetCode 2273)
# 难度：简单
# 标签：数组、哈希表、字符串、排序
#
# 题目需求：
#   反复删除 words[i]（i>0），其中 words[i] 与 words[i-1] 是字母异位词。
#   按任意顺序删除结果相同，返回最终数组。
#
# 约束条件：
#   1. 1 <= words.length <= 100
#   2. 1 <= words[i].length <= 10
#   3. words[i] 由小写英文字母组成
#
# 核心观察：
#   异位词关系是等价关系（自反、对称、传递）。最终保留的是每个"相邻异位词链"
#   中的第一个词。因此只需从左到右一次遍历：当前词与结果列表最后一个词是异位词
#   则跳过，否则加入结果列表。无需模拟反复删除。
#
# 本文件提供四种解法，并在末尾做对比试验。


from typing import List
import time
import random
import string


class Solution:
    # ----------------------------------------------------------
    # 辅助函数：判断两个字符串是否是字母异位词（计数法）
    # ----------------------------------------------------------
    @staticmethod
    def _anagram_key(s: str) -> tuple:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        return tuple(cnt)

    # ----------------------------------------------------------
    # 解法一：模拟法（忠实模拟题目描述的操作过程）
    # 思路：
    #   反复扫描列表，找到第一个与前驱是异位词的元素并删除，
    #   直到不存在这样的元素为止。每次删除后从头重新扫描。
    # 时间复杂度：O(n^2 * k)，n 为 words 长度，k 为最大串长。
    # 空间复杂度：O(n)（结果列表）
    # ----------------------------------------------------------
    def removeAnagrams_simulation(self, words: List[str]) -> List[str]:
        result = list(words)
        changed = True
        while changed:
            changed = False
            for i in range(1, len(result)):
                if sorted(result[i]) == sorted(result[i - 1]):
                    result.pop(i)
                    changed = True
                    break
        return result

    # ----------------------------------------------------------
    # 解法二：一次遍历 + 排序键（推荐最简洁写法）
    # 思路：
    #   从左到右遍历，维护结果列表。当前词的排序键与结果最后一个词的
    #   排序键相同则跳过（异位词），否则加入结果。
    #   排序键即 ''.join(sorted(s))，互为异位词的字符串排序后相同。
    # 时间复杂度：O(n * k log k)
    # 空间复杂度：O(n * k)
    # ----------------------------------------------------------
    def removeAnagrams_sort_key(self, words: List[str]) -> List[str]:
        result = [words[0]]
        prev_key = ''.join(sorted(words[0]))
        for w in words[1:]:
            cur_key = ''.join(sorted(w))
            if cur_key != prev_key:
                result.append(w)
                prev_key = cur_key
        return result

    # ----------------------------------------------------------
    # 解法三：一次遍历 + 计数元组键（推荐最优解法）
    # 思路：
    #   与解法二相同，但用 26 个字母计数元组代替排序字符串作为键，
    #   生成键的时间从 O(k log k) 降到 O(k)。
    # 时间复杂度：O(n * k)
    # 空间复杂度：O(n * k)
    # ----------------------------------------------------------
    def removeAnagrams_count_key(self, words: List[str]) -> List[str]:
        result = [words[0]]
        prev_key = self._anagram_key(words[0])
        for w in words[1:]:
            cur_key = self._anagram_key(w)
            if cur_key != prev_key:
                result.append(w)
                prev_key = cur_key
        return result

    # ----------------------------------------------------------
    # 解法四：栈法（思路与解法二/三一致，用栈实现）
    # 思路：
    #   遍历每个词，将其排序键与栈顶的排序键比较，相同则跳过，
    #   不同则压入栈。最终栈即结果。
    # 时间复杂度：O(n * k log k)
    # 空间复杂度：O(n * k)
    # ----------------------------------------------------------
    def removeAnagrams_stack(self, words: List[str]) -> List[str]:
        stack = []
        stack_keys = []
        for w in words:
            key = ''.join(sorted(w))
            if not stack_keys or key != stack_keys[-1]:
                stack.append(w)
                stack_keys.append(key)
        return stack


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("模拟法",        sol.removeAnagrams_simulation),
        ("排序键法",      sol.removeAnagrams_sort_key),
        ("计数键法",      sol.removeAnagrams_count_key),
        ("栈法",          sol.removeAnagrams_stack),
    ]

    test_cases = [
        (["abba", "baba", "bbaa", "cd", "cd"], ["abba", "cd"]),
        (["a", "b", "c", "d", "e"],            ["a", "b", "c", "d", "e"]),
        (["a"],                                  ["a"]),
        (["a", "a"],                              ["a"]),
        (["a", "a", "a"],                         ["a"]),
        (["ab", "ba", "cd", "dc", "e"],          ["ab", "cd", "e"]),
        (["abc", "def", "cba", "fed", "ghi"],    ["abc", "def", "cba", "fed", "ghi"]),
        (["cat", "act", "tac", "dog", "god", "odg"], ["cat", "dog"]),
        (["ab", "cd", "dc", "ba"],               ["ab", "cd", "ba"]),
        (["z", "z", "z", "a", "a", "b"],         ["z", "a", "b"]),
    ]

    for name, fn in methods:
        all_pass = True
        for words, expected in test_cases:
            result = fn(list(words))
            if result != expected:
                print(f"  ✗ {name}: words={words}")
                print(f"     got:      {result}")
                print(f"     expected: {expected}")
                all_pass = False
        if all_pass:
            print(f"  ✓ {name}: 所有 {len(test_cases)} 个测试用例通过")


# ============================================================
# 性能对比试验
# ============================================================
def _random_word(rng: random.Random) -> str:
    length = rng.randint(1, 10)
    return ''.join(rng.choice(string.ascii_lowercase) for _ in range(length))


def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("模拟法 O(n^2 k)",     sol.removeAnagrams_simulation),
        ("排序键法 O(n k log k)", sol.removeAnagrams_sort_key),
        ("计数键法 O(n k)",     sol.removeAnagrams_count_key),
        ("栈法 O(n k log k)",   sol.removeAnagrams_stack),
    ]

    sizes = [100, 500, 1000, 5000]
    repeat = 500

    print(f"{'数组长度':>10} | {'解法':<26} | {'平均耗时 (μs)':>15}")
    print("-" * 70)

    for size in sizes:
        rng = random.Random(42 + size)
        words = [_random_word(rng) for _ in range(size)]

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                data = list(words)
                start = time.perf_counter()
                fn(data)
                elapsed = (time.perf_counter() - start) * 1_000_000
                times.append(elapsed)
            avg_us = sum(times) / len(times)
            print(f"{size:>10} | {name:<26} | {avg_us:>15.3f}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("四种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度     | 空间复杂度 | 说明                              |
|------------|---------------|-----------|-----------------------------------|
| 模拟法     | O(n^2 * k)    | O(n)      | 忠实模拟反复删除，最坏多次扫描     |
| 排序键法   | O(n * k log k)| O(n)      | 一次遍历 + 排序键，最简洁          |
| 计数键法   | O(n * k)      | O(n)      | 一次遍历 + 计数元组键，理论最优    |
| 栈法       | O(n * k log k)| O(n)      | 本质同排序键法，栈式写法           |

为什么"一次遍历"是正确的？
  - 题目保证"按任意顺序删除结果相同"。这意味着最终每个"连续异位词链"
    中只保留第一个词。
  - 异位词是等价关系（a~a, a~b ⇒ b~a, a~b∧b~c ⇒ a~c）。
  - 当从左到右遍历时，当前词若与结果末尾词是异位词，那么它与整条链
    的词都是异位词，删除它不会影响后续判定（它没有引入"新的"键）。
  - 因此每个词只需与结果末尾词比较一次即可，无需回退。

为什么模拟法低效？
  - 每次删除后从头重新扫描，最坏情况下（所有词互为异位词）要删除 n-1 次，
    每次扫描长度递减，总比较次数 O(n^2)。
  - 但 n ≤ 100 时即使 O(n^2) 也很快，所以暴力法依然可行。
""")


if __name__ == "__main__":
    print("=== 移除字母异位词后的结果数组：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
