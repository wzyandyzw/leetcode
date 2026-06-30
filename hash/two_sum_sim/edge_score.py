# 题目：边积分最高的节点 (LeetCode 2374)
# 难度：中等
# 标签：图、哈希表、数组
#
# 题目需求：
#   给你一个有向图，n 个节点编号 0~n-1，每个节点恰有一条出边。
#   图由长度为 n 的数组 edges 表示，edges[i] 表示从节点 i 到 edges[i] 的有向边。
#   节点 i 的边积分定义为：所有指向 i 的边的源节点编号之和。
#   返回边积分最高的节点；若多个节点边积分相同，返回编号最小的那个。
#
# 约束条件：
#   1. n == edges.length
#   2. 2 <= n <= 10^5
#   3. 0 <= edges[i] < n
#   4. edges[i] != i
#
# 核心思路：
#   边积分 = 所有入边的源节点编号之和。
#   对每条边 i → edges[i]，把 i 累加到 score[edges[i]] 即可。
#   遍历完所有边后，找 score 最大的下标（同分取最小下标）。
#
# 本文件提供三种解法，并在末尾做对比试验。


from typing import List
from collections import defaultdict
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：数组两次遍历法（标准最优解法）
    # 思路：
    #   1. 初始化长度为 n 的 score 数组为 0
    #   2. 第一遍遍历：对每条边 i→edges[i]，执行 score[edges[i]] += i
    #   3. 第二遍遍历：找出 score 数组中最大值对应的最小下标
    # 时间复杂度：O(n) —— 两次线性遍历。
    # 空间复杂度：O(n) —— score 数组。
    # ----------------------------------------------------------
    def edgeScore_array(self, edges: List[int]) -> int:
        n = len(edges)
        score = [0] * n
        for src in range(n):
            dst = edges[src]
            score[dst] += src
        max_score = -1
        ans = 0
        for i in range(n):
            if score[i] > max_score:
                max_score = score[i]
                ans = i
        return ans

    # ----------------------------------------------------------
    # 解法二：字典法（适用于稀疏图场景）
    # 思路：
    #   用字典 defaultdict(int) 只记录有入边的节点的边积分，
    #   遍历结束后在字典的键中找边积分最大、编号最小的节点。
    #   注意：没有入边的节点边积分为 0，但题目保证至少存在一条边，
    #   且至少有一个节点边积分 > 0（因为 n>=2 且 edges[i]!=i），所以不需要考虑这些节点。
    # 时间复杂度：O(n) —— 一次遍历 + 一次对字典键的遍历。
    # 空间复杂度：O(k)，k 为有入边的节点数，最坏 O(n)。
    # ----------------------------------------------------------
    def edgeScore_dict(self, edges: List[int]) -> int:
        score = defaultdict(int)
        for src, dst in enumerate(edges):
            score[dst] += src
        max_score = -1
        ans = 0
        for node, s in score.items():
            if s > max_score or (s == max_score and node < ans):
                max_score = s
                ans = node
        return ans

    # ----------------------------------------------------------
    # 解法三：Pythonic 简洁写法（利用内置 max 函数的 key）
    # 思路：
    #   逻辑与解法一完全相同，但用 Python 内置函数写得更紧凑：
    #   - 用 enumerate + max，key 取 (-score[i], i) 可实现"分数高优先，同分编号小优先"
    #   - 或者 key 取 (score[i], -i) 后取最大也可以，但这里用第一种比较直观
    # 时间复杂度：O(n)
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def edgeScore_pythonic(self, edges: List[int]) -> int:
        n = len(edges)
        score = [0] * n
        for src, dst in enumerate(edges):
            score[dst] += src
        return max(range(n), key=lambda i: (score[i], -i))


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("数组两次遍历法", sol.edgeScore_array),
        ("字典法",         sol.edgeScore_dict),
        ("Pythonic写法",   sol.edgeScore_pythonic),
    ]

    test_cases = [
        ([1, 0, 0, 0, 0, 7, 7, 5], 7),
        ([2, 0, 0, 2],              0),
        ([1, 2, 0],                 0),   # 0←2, 1←0, 2←1; score[0]=2, score[1]=0, score[2]=1 → 0最大
        ([1, 0],                    0),   # 0←1, 1←0; score[0]=1, score[1]=0 → 0
        ([1, 2, 3, 4, 0],           0),   # 一个环 0→1→2→3→4→0，score[1]=0, score[2]=1, score[3]=2, score[4]=3, score[0]=4 → 0
        ([3, 3, 3, 2, 2],           2),   # 0,1,2→3 score[3]=3; 3,4→2 score[2]=7 → 2最大
        ([1, 1, 1, 1],              1),   # 全部指向1，score[1]=0+1+2+3=6，其余为0
    ]

    for name, fn in methods:
        all_pass = True
        for edges, expected in test_cases:
            result = fn(list(edges))
            if result != expected:
                print(f"  ✗ {name}: edges={edges}, got={result}, expected={expected}")
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
        ("数组两次遍历法 O(n)", sol.edgeScore_array),
        ("字典法 O(n)",         sol.edgeScore_dict),
        ("Pythonic写法 O(n)",   sol.edgeScore_pythonic),
    ]

    sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000]
    repeat = 20

    print(f"{'数据规模':>10} | {'解法':<22} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        random.seed(42 + size)
        edges = [0] * size
        for i in range(size):
            dst = random.randint(0, size - 1)
            if dst == i:
                dst = (dst + 1) % size
            edges[i] = dst

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                data = list(edges)
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
| 解法           | 时间复杂度 | 空间复杂度 | 说明                                  |
|----------------|-----------|-----------|---------------------------------------|
| 数组两次遍历法 | O(n)      | O(n)      | 最直接、最稳定、缓存友好，推荐解法      |
| 字典法         | O(n)      | O(k)≤O(n) | 稀疏图下节省空间，但哈希有常数开销      |
| Pythonic写法   | O(n)      | O(n)      | 代码最简洁，利用 max 的 key 特性        |

题目的图结构性质：
  - 每个节点恰有一条出边，所以图的每个连通分量是一个环，环上挂着若干指向环的树（内向基环树）
  - 这一性质在本题中没有被用到，因为只需要计算入度加权和，直接遍历即可
  - 若题目再增加"找环"等要求，则需要用到拓扑排序 / 快慢指针等技巧

同分取小编号的处理：
  - 数组法从前往后遍历，只在 score[i] > max_score 时更新 ans，
    自然保证了"首次遇到的最大值保留，后来的同分不覆盖"
  - Pythonic 写法利用 key=(score[i], -i)，max 在比较元组时，
    先比 score[i]（大者优先），再比 -i（即小编号优先），同样正确
""")


if __name__ == "__main__":
    print("=== 边积分最高的节点：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
