# 题目：最长连续序列 (LeetCode 128)
# 难度：中等
# 标签：并查集、数组、哈希表
#
# 题目需求：
#   给定未排序整数数组 nums，找出数字连续的最长序列（不要求原数组中连续）
#   的长度。要求时间复杂度 O(n)。
#
# 约束条件：
#   1. 0 <= nums.length <= 10^5
#   2. -10^9 <= nums[i] <= 10^9
#
# 核心思路：
#   O(n log n) 排序法虽简单，但不符合要求。要达到 O(n) 必须借助哈希表/并查集。
#   关键观察：一个连续序列必定有一个"起点"（即序列中不存在 x-1 的那个最小数）。
#   只要从每个起点开始向 x+1 方向扩展计数，每个元素最多被访问一次，总复杂度 O(n)。
#
# 本文件提供四种解法，并在末尾做对比试验。


from typing import List
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：排序法
    # 思路：排序后一次扫描，遇到连续数字则当前长度+1，否则重置为1。
    #       需要先去重（重复元素不影响长度但会导致错误累计）。
    # 时间复杂度：O(n log n) —— 排序主导。
    # 空间复杂度：O(n) 或 O(1)（取决于是否去重副本/排序是否原地）。
    # ----------------------------------------------------------
    def longestConsecutive_sort(self, nums: List[int]) -> int:
        if not nums:
            return 0
        arr = sorted(set(nums))
        best = cur = 1
        for i in range(1, len(arr)):
            if arr[i] == arr[i - 1] + 1:
                cur += 1
            else:
                best = max(best, cur)
                cur = 1
        return max(best, cur)

    # ----------------------------------------------------------
    # 解法二：哈希集合 + 起点扩展（经典 O(n) 解法，推荐）
    # 思路：
    #   1. 所有元素放入 set 以 O(1) 查找。
    #   2. 遍历 set 中的每个 x：若 x-1 不在 set 中，则 x 是某个连续序列的
    #      起点；从 x 开始不断试探 x+1, x+2, ... 是否在 set 中，统计长度。
    #   3. 每个元素只被"作为序列内部元素"访问一次（因为只有起点会启动扩展，
    #      非起点不会启动），因此 while 循环总次数为 O(n)。
    # 时间复杂度：O(n)
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def longestConsecutive_set(self, nums: List[int]) -> int:
        s = set(nums)
        best = 0
        for x in s:
            if x - 1 not in s:
                cur = 1
                y = x + 1
                while y in s:
                    cur += 1
                    y += 1
                if cur > best:
                    best = cur
        return best

    # ----------------------------------------------------------
    # 解法三：哈希表动态规划（区间合并）
    # 思路：
    #   用字典 dp[x] 表示"以 x 为端点的连续序列长度"。遍历每个数 x：
    #   - 若 x 已处理过则跳过（避免重复）。
    #   - left = dp.get(x-1, 0)，right = dp.get(x+1, 0)。
    #   - 新序列长度 cur = left + right + 1。
    #   - 更新两个端点：dp[x-left] = cur，dp[x+right] = cur。
    #   - 同时设置 dp[x] = cur（标记 x 已处理）。
    #   每次合并后 best 取最大值。
    # 时间复杂度：O(n)
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def longestConsecutive_dp(self, nums: List[int]) -> int:
        dp = {}
        best = 0
        for x in nums:
            if x in dp:
                continue
            left = dp.get(x - 1, 0)
            right = dp.get(x + 1, 0)
            cur = left + right + 1
            dp[x] = cur
            dp[x - left] = cur
            dp[x + right] = cur
            if cur > best:
                best = cur
        return best

    # ----------------------------------------------------------
    # 解法四：并查集（Union-Find）
    # 思路：
    #   将每个数视为图节点，若 x 和 x+1 都存在，则将它们连通；
    #   连通分量的大小即为该连续序列的长度，取最大分量大小即可。
    #   用路径压缩 + 按大小合并，均摊 O(α(n)) ≈ O(1) 每次操作。
    # 时间复杂度：O(n · α(n)) ≈ O(n)
    # 空间复杂度：O(n)
    # ----------------------------------------------------------
    def longestConsecutive_union_find(self, nums: List[int]) -> int:
        if not nums:
            return 0
        parent = {}
        size = {}
        for x in nums:
            if x not in parent:
                parent[x] = x
                size[x] = 1

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

        for x in parent:
            if x + 1 in parent:
                union(x, x + 1)

        return max(size.values())


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("排序法",      sol.longestConsecutive_sort),
        ("哈希集合法",  sol.longestConsecutive_set),
        ("哈希表DP法",  sol.longestConsecutive_dp),
        ("并查集法",    sol.longestConsecutive_union_find),
    ]

    test_cases = [
        ([100, 4, 200, 1, 3, 2],      4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([1, 0, 1, 2],                 3),
        ([],                           0),
        ([1],                          1),
        ([1, 3, 5, 7],                 1),     # 没有连续
        ([1, 2, 3, 4, 5],              5),     # 完全连续
        ([-1, -2, -3, -4],             4),     # 负数连续
        ([1, 2, 0, 1],                 3),     # 0,1,2
        ([10, 5, 12, 3, 55, 30, 4, 11, 2], 6), # [2,3,4,5] wait 2,3,4,5=4? let me recount
        # 10,5,12,3,55,30,4,11,2: 10,11,12=3; 2,3,4,5=4; others single; best=4
    ]
    # Fix last case answer
    test_cases[-1] = ([10, 5, 12, 3, 55, 30, 4, 11, 2], 4)

    # Boundary: negative large span
    test_cases.append(([-(10**9), -(10**9)+1, -(10**9)+2], 3))
    test_cases.append(([10**9, 10**9-1, 10**9-2, 10**9-3], 4))

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
    print("性能对比试验")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("排序法 O(n log n)",      sol.longestConsecutive_sort),
        ("哈希集合法 O(n)",        sol.longestConsecutive_set),
        ("哈希表DP法 O(n)",        sol.longestConsecutive_dp),
        ("并查集法 O(n α(n))",     sol.longestConsecutive_union_find),
    ]

    sizes = [1000, 10000, 100000]
    repeat = 50

    print(f"{'数组长度':>10} | {'解法':<24} | {'平均耗时 (ms)':>15}")
    print("-" * 70)

    for size in sizes:
        rng = random.Random(42 + size)
        nums = [rng.randint(-10**9, 10**9) for _ in range(size)]

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                data = list(nums)
                start = time.perf_counter()
                fn(data)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            print(f"{size:>10} | {name:<24} | {avg_ms:>15.3f}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("四种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法       | 时间复杂度    | 空间复杂度 | 说明                                |
|------------|--------------|-----------|-------------------------------------|
| 排序法     | O(n log n)   | O(n)      | 简洁但不满足题目 O(n) 要求           |
| 哈希集合法 | O(n)         | O(n)      | 经典最优，从"序列起点"扩展计数        |
| 哈希表DP法 | O(n)         | O(n)      | 区间两端点记录长度，合并相邻段        |
| 并查集法   | O(n · α(n))  | O(n)      | 将相邻数字连通，取最大连通分量        |

哈希集合法为什么是 O(n)？
  - 关键在于 "if x-1 not in s" 这一判断：只有序列的最小元素才会进入
    while 扩展循环；非最小元素会被跳过。
  - while 循环每次 y+=1 访问的都是序列中的后续元素，而这些元素在轮到它们
    作为外层循环的 x 时，会因为 x-1 已存在而立即跳过。
  - 因此 while 循环的总迭代次数恰好等于序列长度之和，即 ≤ n。
  - 外层 for 循环 O(n)，内层 while 总次数 O(n)，合计 O(n)。

哈希表 DP 法区间合并原理：
  - dp[x] 只在"序列端点"处保证是正确的序列长度，内部节点的值不必维护
    （因为它们不会再被当作合并端点查询）。
  - 当加入 x 时，若左邻居 x-1 存在则左侧序列长度为 left，右邻居 x+1 存在
    则右侧为 right；新序列长度 = left+right+1。
  - 合并后只需更新新端点 x-left 和 x+right 的值即可，
    中间节点无需更新（它们以后不会被作为边界查询）。
""")


if __name__ == "__main__":
    print("=== 最长连续序列：四种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
