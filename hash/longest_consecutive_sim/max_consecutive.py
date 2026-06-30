# 题目：不含特殊楼层的最大连续楼层数 (LeetCode 2274)
# 难度：中等
# 标签：数组、排序
#
# 题目需求：
#   Alice 租用了 [bottom, top] 的所有楼层，其中部分楼层被指定为"特殊楼层"。
#   返回不含特殊楼层的最大连续楼层数。
#
# 约束条件：
#   1. 1 <= special.length <= 10^5
#   2. 1 <= bottom <= special[i] <= top <= 10^9
#   3. special 中所有值互不相同
#
# 核心思路：
#   [bottom, top] 范围高达 10^9，无法逐个楼层扫描。
#   将特殊楼层排序后，连续的"普通段"必然位于：
#     1) bottom 到 special[0]-1
#     2) special[i-1]+1 到 special[i]-1（对每对相邻特殊楼层）
#     3) special[-1]+1 到 top
#   每段长度 = 右端点 - 左端点 + 1，排序后一次扫描即可求出最大值。
#
# 本文件提供三种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：排序 + 一次扫描（推荐最优解法）
    # 思路：
    #   1. 将 special 排序
    #   2. 初始最大段长 = special[0] - bottom（首段）
    #   3. 遍历相邻特殊楼层对，段长 = special[i] - special[i-1] - 1
    #   4. 末段段长 = top - special[-1]
    #   5. 取所有段长的最大值
    # 时间复杂度：O(m log m)，m = special.length。
    # 空间复杂度：O(m)（若允许修改输入可做到 O(1) 额外空间）。
    # ----------------------------------------------------------
    def maxConsecutive_sort_scan(self, bottom: int, top: int, special: List[int]) -> int:
        special.sort()
        best = special[0] - bottom
        for i in range(1, len(special)):
            gap = special[i] - special[i - 1] - 1
            if gap > best:
                best = gap
        tail = top - special[-1]
        if tail > best:
            best = tail
        return best

    # ----------------------------------------------------------
    # 解法二：排序 + 哨兵（写法更统一）
    # 思路：
    #   在特殊楼层序列首尾各加一个"虚拟哨兵" (bottom-1) 和 (top+1)，
    #   这样首段、中段、尾段都可以统一用 s[i]-s[i-1]-1 计算，
    #   无需单独处理边界，代码更简洁不易出错。
    # 时间复杂度：O(m log m)
    # 空间复杂度：O(m)
    # ----------------------------------------------------------
    def maxConsecutive_sentinel(self, bottom: int, top: int, special: List[int]) -> int:
        arr = sorted(special)
        arr = [bottom - 1] + arr + [top + 1]
        best = 0
        for i in range(1, len(arr)):
            gap = arr[i] - arr[i - 1] - 1
            if gap > best:
                best = gap
        return best

    # ----------------------------------------------------------
    # 解法三：原地排序 + 一次扫描（空间优化版）
    # 思路：
    #   与解法一相同，但对输入的 special 做原地排序，避免额外拷贝
    #   （LeetCode 提交时通常允许修改入参）。
    #   注意：首段 = special[0] - bottom，末段 = top - special[-1]，
    #   这两个段长都比中段公式少减 1，因为它们从边界开始/到边界结束。
    # 时间复杂度：O(m log m)
    # 空间复杂度：O(1)（不考虑排序内部栈空间）
    # ----------------------------------------------------------
    def maxConsecutive_in_place(self, bottom: int, top: int, special: List[int]) -> int:
        special.sort()
        best = special[0] - bottom
        prev = special[0]
        for x in special[1:]:
            gap = x - prev - 1
            if gap > best:
                best = gap
            prev = x
        tail = top - special[-1]
        return tail if tail > best else best


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("排序扫描法",   sol.maxConsecutive_sort_scan),
        ("哨兵法",       sol.maxConsecutive_sentinel),
        ("原地排序法",   sol.maxConsecutive_in_place),
    ]

    test_cases = [
        (2, 9,  [4, 6],           3),
        (6, 8,  [7, 6, 8],        0),
        (1, 1,  [1],              0),
        (1, 5,  [3],              2),       # [1,2] and [4,5]
        (1, 10, [2, 5, 7],        3),       # [1]=1, [3,4]=2, [6]=1, [8,10]=3
        (1, 100,[50],             50),      # [1,49]=49 wait, 49-1+1=49; [51,100]=50 → max=50
        (10, 30,[15, 20, 25],     5),       # [10,14]=5, [16,19]=4, [21,24]=4, [26,30]=5 → 5
        (1, 3,  [2],              1),       # [1]=1, [3]=1 → 1
        (1, 2,  [1],              1),       # [2]=1
        (1, 2,  [2],              1),       # [1]=1
    ]

    for name, fn in methods:
        all_pass = True
        for bottom, top, special, expected in test_cases:
            result = fn(bottom, top, list(special))
            if result != expected:
                print(f"  ✗ {name}: bottom={bottom}, top={top}, special={special}, got={result}, expected={expected}")
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
        ("排序扫描法 O(m log m)", sol.maxConsecutive_sort_scan),
        ("哨兵法 O(m log m)",     sol.maxConsecutive_sentinel),
        ("原地排序法 O(m log m)", sol.maxConsecutive_in_place),
    ]

    sizes = [1000, 10000, 100000]
    repeat = 100

    print(f"{'special长度':>12} | {'解法':<26} | {'平均耗时 (μs)':>15}")
    print("-" * 70)

    for size in sizes:
        rng = random.Random(42 + size)
        special = rng.sample(range(1, 10**9), size)
        bottom, top = 1, 10**9

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                data = list(special)
                start = time.perf_counter()
                fn(bottom, top, data)
                elapsed = (time.perf_counter() - start) * 1_000_000
                times.append(elapsed)
            avg_us = sum(times) / len(times)
            print(f"{size:>12} | {name:<26} | {avg_us:>15.3f}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度 | 空间复杂度 | 说明                              |
|------------|-----------|-----------|-----------------------------------|
| 排序扫描法 | O(m log m)| O(m)      | 分首/中/尾三段分别计算，最直观      |
| 哨兵法     | O(m log m)| O(m)      | 首尾加哨兵统一公式，代码最简洁      |
| 原地排序法 | O(m log m)| O(1)额外  | 原地排序省拷贝，空间最优            |

为什么不能用集合/线性扫描？
  - top - bottom + 1 可达 10^9，不可能从 bottom 到 top 逐楼层枚举；
  - 特殊楼层数 m 最多 10^5，比范围小得多，所以以特殊楼层为"锚点"
    计算段长是唯一可行的思路；排序自然是 O(m log m)。

段长公式推导：
  - 首段（bottom 到 special[0]-1）：长度 = (special[0]-1) - bottom + 1
                                        = special[0] - bottom
  - 中段（special[i-1]+1 到 special[i]-1）：长度 = (special[i]-1) - (special[i-1]+1) + 1
                                              = special[i] - special[i-1] - 1
  - 末段（special[-1]+1 到 top）：长度 = top - (special[-1]+1) + 1
                                      = top - special[-1]

哨兵法巧思：
  在 special 前后插入 bottom-1 和 top+1 两个"虚拟特殊楼层"，
  此时每一段都可以用统一公式 s[i] - s[i-1] - 1 计算：
    - 首段：special[0] - (bottom-1) - 1 = special[0] - bottom ✓
    - 中段：special[i] - special[i-1] - 1 ✓
    - 末段：(top+1) - special[-1] - 1 = top - special[-1] ✓
  无需分支处理边界，循环体统一。
""")


if __name__ == "__main__":
    print("=== 不含特殊楼层的最大连续楼层数：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
