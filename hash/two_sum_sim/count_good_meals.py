# 题目：大餐计数 (LeetCode 1711)
# 难度：中等
# 标签：数组、哈希表
#
# 题目需求：
#   大餐是指恰好包含两道不同餐品的一餐，其美味程度之和等于 2 的幂。
#   给你一个整数数组 deliciousness，其中 deliciousness[i] 是第 i 道餐品的美味程度，
#   返回你可以用数组中的餐品做出的不同大餐的数量。结果需要对 10^9 + 7 取余。
#   注意：只要餐品下标不同，就可以认为是不同的餐品，即便美味程度相同。
#
# 约束条件：
#   1. 1 <= deliciousness.length <= 10^5
#   2. 0 <= deliciousness[i] <= 2^20
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
from collections import Counter
import time
import random


MOD = 10**9 + 7
# 两数之和最大 = 2^20 + 2^20 = 2^21，枚举到 2^22 保险
POWERS_OF_TWO = [1 << i for i in range(23)]  # 2^0 ... 2^22


def _is_power_of_two(s: int) -> bool:
    return s > 0 and (s & (s - 1)) == 0


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（两层循环）
    # 思路：枚举所有 (i, j)，i < j，判断 deliciousness[i] + deliciousness[j] 是否为 2 的幂。
    #       判断 2 的幂：s > 0 且 s & (s-1) == 0。
    # 时间复杂度：O(n^2) —— 两层循环。
    # 空间复杂度：O(1) —— 常数额外空间。
    # ----------------------------------------------------------
    def countPairs_brute_force(self, deliciousness: List[int]) -> int:
        n = len(deliciousness)
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if _is_power_of_two(deliciousness[i] + deliciousness[j]):
                    count += 1
        return count % MOD

    # ----------------------------------------------------------
    # 解法二：哈希表一次遍历法 —— 最优解法
    # 思路：
    #   1. 类似两数之和，遍历到第 j 道餐品时，前面的餐品都已经在字典里
    #   2. 枚举所有可能的 2 的幂 p（共 23 个），检查 p - d 是否在字典中
    #   3. 若存在，加上字典里记录的出现次数（说明有那么多道已见过的餐品可与之配对）
    #   4. 将当前 d 加入字典
    # 时间复杂度：O(n * C) —— C = 23（2 的幂个数），等价于 O(n)。
    # 空间复杂度：O(n) —— 哈希表。
    # ----------------------------------------------------------
    def countPairs_hash_map(self, deliciousness: List[int]) -> int:
        freq: dict = {}
        count = 0
        for d in deliciousness:
            for p in POWERS_OF_TWO:
                comp = p - d
                if comp in freq:
                    count += freq[comp]
            freq[d] = freq.get(d, 0) + 1
        return count % MOD

    # ----------------------------------------------------------
    # 解法三：Counter 频率 + 组合计算
    # 思路：
    #   1. 先统计每个美味值的出现次数 → Counter
    #   2. 对每个目标 2 的幂 p：
    #      - 遍历每个值 x，设 y = p - x
    #      - 若 y 不在 Counter 中则跳过
    #      - 若 x == y：组合数 C(f[x], 2) = f[x] * (f[x]-1) // 2（从同值里选两个）
    #      - 若 x < y：配对数 f[x] * f[y]（两组不同值之间的笛卡尔积）
    #   3. 利用 x < y 条件避免重复计数
    # 时间复杂度：O(m * C) —— m 为不同值的个数，C = 23，等价于 O(n)。
    # 空间复杂度：O(m) —— Counter。
    # ----------------------------------------------------------
    def countPairs_counter(self, deliciousness: List[int]) -> int:
        freq = Counter(deliciousness)
        count = 0
        for p in POWERS_OF_TWO:
            for x in freq:
                y = p - x
                if y not in freq:
                    continue
                if x == y:
                    count += freq[x] * (freq[x] - 1) // 2
                elif x < y:
                    count += freq[x] * freq[y]
        return count % MOD


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",     sol.countPairs_brute_force),
        ("哈希表法",   sol.countPairs_hash_map),
        ("Counter法",  sol.countPairs_counter),
    ]

    test_cases = [
        ([1, 3, 5, 7, 9],                                      4),
        ([1, 1, 1, 3, 3, 3, 7],                               15),
        ([0],                                                   0),
        ([1, 1],                                                1),
        ([0, 0],                                                0),   # 0+0=0 不是2的幂
        ([0, 1],                                                1),   # 0+1=1=2^0
        ([2, 2],                                                1),   # 2+2=4=2^2
        ([1, 2, 4, 8, 16],                                     4),   # (1,?)1+1? 无1+1; 枚举
        ([1048576, 1048576],                                    1),   # 2^20 + 2^20 = 2^21
        ([0, 0, 0, 0],                                          0),
        ([1, 1, 1],                                            3),   # C(3,2)=3，每对和为2=2^1
    ]

    # 验证第8个用例
    # [1,2,4,8,16]: 1+? 1+1无,1+2=3,1+4=5,1+8=9,1+16=17; 2+? 2+4=6,2+8=10,2+16=18; 4+? 4+8=12,4+16=20; 8+16=24
    # 2 的幂：1,2,4,8,16,32... 以上没有和为 2 的幂的？那期望是0，我写错了
    # 重新来：[1,3] = 4, [1,7]=8... 让我换成有正确答案的
    test_cases[7] = ([1, 3, 5, 7, 9], 4)  # 重复例1，换一个新的
    # 换：[1, 0, 1, 0] 对：(1,1)=2, (0,1)有4个, (0,0)=0不是
    # 4个(0,1) + 1个(1,1) = 5
    test_cases[7] = ([1, 0, 1, 0], 5)

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
    print("性能对比试验（测量每种解法在不同规模数据上的运行时间）")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("暴力法 O(n^2)",      sol.countPairs_brute_force),
        ("哈希表法 O(n)",      sol.countPairs_hash_map),
        ("Counter法 O(n)",     sol.countPairs_counter),
    ]

    sizes = [100, 1_000, 5_000, 10_000, 50_000, 100_000]
    repeat = 5

    print(f"{'数据规模':>10} | {'解法':<20} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        nums = [random.randint(0, 1 << 20) for _ in range(size)]

        for name, fn in methods:
            if "暴力" in name and size > 1_000:
                print(f"{size:>10} | {name:<20} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums))
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            print(f"{size:>10} | {name:<20} | {avg_ms:>15.3f} | {'':<20}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print(f"""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                                    |
|------------|-----------|-----------|-----------------------------------------|
| 暴力法     | O(n^2)    | O(1)      | 两层循环，n 较大时不可用                  |
| 哈希表法   | O(n)      | O(n)      | 一次遍历，对每个数枚举 23 个 2 的幂，最优  |
| Counter法  | O(n)      | O(m)      | 先统计频率，再用组合数学计算对数           |

核心洞察：
  - 目标值不是单一 target，而是所有 2 的幂；
    由于美味值 <= 2^20，两数之和 <= 2^21，所以只需枚举 2^0 到 2^22 共 23 个值
  - 判断一个数是否为 2 的幂：s > 0 且 (s & (s-1)) == 0
    （注意 0 不是 2 的幂，因为 2^m 对任何整数 m 都大于 0）

Counter 法的组合逻辑：
  - 对每个 2 的幂 p：
    · 若 x == y = p-x：C(f[x], 2) = f[x]*(f[x]-1)//2（从同值中选两个不同餐品）
    · 若 x < y：f[x] * f[y]（两组不同值之间的所有配对）
  - x < y 保证每对值只计一次
""")


if __name__ == "__main__":
    print("=== 大餐计数：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
