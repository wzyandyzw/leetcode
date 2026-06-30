# 题目：找到和为给定整数的三个连续整数 (LeetCode 2177)
# 难度：中等
# 标签：数学、模拟
#
# 题目需求：
#   给定整数 num，返回三个连续整数，它们的和为 num；若无法表示则返回空数组。
#
# 约束条件：
#   0 <= num <= 10^15
#
# 数学推导：
#   设三个连续整数为 n-1, n, n+1，则它们的和 = (n-1) + n + (n+1) = 3n。
#   因此 num 必须能被 3 整除；令 n = num/3，则答案为 [n-1, n, n+1]。
#   若 num % 3 != 0，则无解。
#
# 本文件提供三种解法（含暴力枚举、数学公式），并在末尾做验证。


from typing import List
import time


class Solution:
    # ----------------------------------------------------------
    # 解法一：数学公式法（最优，O(1)）
    # 思路：
    #   三个连续整数 (n-1)+n+(n+1) = 3n = num ⟹ n = num/3。
    #   若 num 能被 3 整除，返回 [n-1, n, n+1]；否则返回 []。
    # 时间复杂度：O(1)
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def sumOfThree_math(self, num: int) -> List[int]:
        if num % 3 != 0:
            return []
        n = num // 3
        return [n - 1, n, n + 1]

    # ----------------------------------------------------------
    # 解法二：代数等价法（同样 O(1)，另一种写法）
    # 思路：
    #   设三个连续整数为 x, x+1, x+2，和为 3x+3 = num ⟹ x = (num-3)/3。
    #   必须 (num-3) 能被 3 整除（等价于 num 能被 3 整除，因为 3 本身整除 3），
    #   返回 [x, x+1, x+2]。
    # 时间复杂度：O(1)
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def sumOfThree_algebra(self, num: int) -> List[int]:
        if (num - 3) % 3 != 0:
            return []
        x = (num - 3) // 3
        return [x, x + 1, x + 2]

    # ----------------------------------------------------------
    # 解法三：暴力枚举法（仅用于对照验证，num 大时极慢或不可行）
    # 思路：
    #   从可能的起点 x 开始枚举，判断 x+(x+1)+(x+2)==num。
    #   x 的范围：x 最小可以是 (num-3)/3 附近，但此题 num 可达 10^15，
    #   暴力法完全不可行；仅作为正确性参考。
    # 时间复杂度：O(num) —— 实际无法处理大数据，仅用于测试小数字。
    # 空间复杂度：O(1)
    # ----------------------------------------------------------
    def sumOfThree_brute(self, num: int) -> List[int]:
        if num < 3:
            if num == 0:
                return [-1, 0, 1]
            return []
        start = max(-(10**6), (num // 3) - 2)
        end = min(10**6, (num // 3) + 2)
        for x in range(start, end + 1):
            if x + (x + 1) + (x + 2) == num:
                return [x, x + 1, x + 2]
        return []


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("数学公式法", sol.sumOfThree_math),
        ("代数等价法", sol.sumOfThree_algebra),
    ]

    test_cases = [
        (33, [10, 11, 12]),
        (4,  []),
        (0,  [-1, 0, 1]),
        (3,  [0, 1, 2]),
        (6,  [1, 2, 3]),
        (9,  [2, 3, 4]),
        (1,  []),
        (2,  []),
        (15, [4, 5, 6]),
        (3*10**15 - 3, [10**15 - 2, 10**15 - 1, 10**15]),
        (10**15, [] if 10**15 % 3 != 0 else [(10**15)//3 - 1, (10**15)//3, (10**15)//3 + 1]),
    ]

    for name, fn in methods:
        all_pass = True
        for num, expected in test_cases:
            result = fn(num)
            if result != expected:
                print(f"  ✗ {name}: num={num}, got={result}, expected={expected}")
                all_pass = False
        if all_pass:
            print(f"  ✓ {name}: 所有 {len(test_cases)} 个测试用例通过")

    # 暴力法仅在小数字上与公式法对照
    brute_ok = True
    for num in range(0, 200):
        r1 = sol.sumOfThree_math(num)
        r2 = sol.sumOfThree_brute(num)
        if r1 != r2:
            print(f"  ✗ 暴力法不一致: num={num}, math={r1}, brute={r2}")
            brute_ok = False
    if brute_ok:
        print(f"  ✓ 暴力法: 在 0~199 范围内与公式法结果一致")


# ============================================================
# 性能对比试验（大数据边界）
# ============================================================
def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验（num = 10^15 边界值）")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("数学公式法 O(1)", sol.sumOfThree_math),
        ("代数等价法 O(1)", sol.sumOfThree_algebra),
    ]

    test_nums = [0, 33, 10**15 - 1, 10**15, 3 * 10**15]
    repeat = 100000

    print(f"{'num':>20} | {'解法':<20} | {'平均耗时 (ns)':>15}")
    print("-" * 70)

    for num in test_nums:
        for name, fn in methods:
            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(num)
                elapsed = (time.perf_counter() - start) * 1e9
                times.append(elapsed)
            avg_ns = sum(times) / len(times)
            print(f"{num:>20} | {name:<20} | {avg_ns:>15.2f}")
        print("-" * 70)


# ============================================================
# 理论推导小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("理论推导小结")
    print("=" * 70)
    print("""
设三个连续整数为 n-1, n, n+1（以中间数 n 为变量更对称）：
  和 = (n-1) + n + (n+1) = 3n

令 3n = num，得：
  n = num / 3

有解条件：
  num 必须能被 3 整除（即 num % 3 == 0）。

若有解，答案为：[n-1, n, n+1] = [num/3 - 1, num/3, num/3 + 1]。
若无解，返回 []。

为什么这种题可以 O(1) 解决？
  - "三个连续整数之和"是严格的等差数列问题，本质上只有一个自由度 n，
    一个方程直接确定唯一解（或判定无解），无需搜索或枚举。
  - 类似地，k 个连续整数之和为 S 时，设中间为 n，和 = k·n（k 奇数）
    或首项为 a，和 = k·a + k(k-1)/2（k 偶数），都能直接解方程。

验证示例：
  num=33 → 33%3==0，n=11 → [10,11,12]，和 10+11+12=33 ✓
  num=4  → 4%3=1≠0，无解 ✓
  num=0  → 0%3==0，n=0 → [-1,0,1]，和 -1+0+1=0 ✓
""")


if __name__ == "__main__":
    print("=== 找到和为给定整数的三个连续整数：三种解法 + 验证 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
