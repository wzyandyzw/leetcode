# 题目：连接后等于目标字符串的字符串对 (LeetCode 2023)
# 难度：中等
# 标签：数组、哈希表、字符串、计数
#
# 题目需求：
#   给你一个数字字符串数组 nums 和一个数字字符串 target，
#   请你返回 nums[i] + nums[j]（两个字符串连接）结果等于 target 的下标 (i, j)
#   （需满足 i != j）的数目。
#
# 约束条件：
#   1. 2 <= nums.length <= 100
#   2. 1 <= nums[i].length <= 100
#   3. 2 <= target.length <= 100
#   4. nums[i] 和 target 只包含数字，不包含前导 0
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List
from collections import Counter
import time
import random


class Solution:
    # ----------------------------------------------------------
    # 解法一：暴力法（两层循环）
    # 思路：枚举所有有序对 (i, j)，i != j，直接拼接字符串与 target 比较。
    # 时间复杂度：O(n^2 * L) —— L 为字符串拼接和比较的时间，约等于 target 长度。
    # 空间复杂度：O(1) —— 常数额外空间。
    # ----------------------------------------------------------
    def numOfPairs_brute_force(self, nums: List[str], target: str) -> int:
        n = len(nums)
        count = 0
        for i in range(n):
            for j in range(n):
                if i != j and nums[i] + nums[j] == target:
                    count += 1
        return count

    # ----------------------------------------------------------
    # 解法二：哈希表频率法（每个串作为后缀）
    # 思路：
    #   1. 先用 Counter 统计每个字符串的出现频率
    #   2. 枚举每个字符串 s 作为「后缀」（即拼接在后面的部分）：
    #      - 若 len(s) >= len(target)，跳过
    #      - 若 target 以 s 结尾，则前缀 p = target[:-len(s)]
    #      - 若 p != s，贡献 freq[p] 个前缀（i 可以是任何值为 p 的下标）
    #      - 若 p == s，贡献 freq[p] - 1（排除 i = j 自己）
    # 时间复杂度：O(n * L) —— 每个字符串做一次结尾比较和切片。
    # 空间复杂度：O(n * L) —— Counter 存储。
    # ----------------------------------------------------------
    def numOfPairs_hash_map(self, nums: List[str], target: str) -> int:
        freq = Counter(nums)
        t_len = len(target)
        count = 0
        for s in nums:
            s_len = len(s)
            if s_len >= t_len:
                continue
            if target.endswith(s):
                prefix = target[: t_len - s_len]
                if prefix == s:
                    count += freq[prefix] - 1
                else:
                    count += freq.get(prefix, 0)
        return count

    # ----------------------------------------------------------
    # 解法三：分割点法（枚举 target 的切割位置）—— 最优、最优雅
    # 思路：
    #   1. nums[i] + nums[j] == target 等价于：
    #      存在某个分割点 split（1 <= split < len(target)），使得
    #      nums[i] == target[:split] 且 nums[j] == target[split:]
    #   2. 不同分割点对应不同长度，不会重复计数
    #   3. 对每个 split：
    #      - 设 prefix = target[:split], suffix = target[split:]
    #      - 若 prefix != suffix：有序对数 = freq[prefix] * freq[suffix]
    #      - 若 prefix == suffix：有序对数 = freq[prefix] * (freq[prefix] - 1)（排除 i=j）
    # 时间复杂度：O(n * L + T) —— T = len(target)，L 为字符串平均长度。
    # 空间复杂度：O(n * L) —— Counter 存储。
    # ----------------------------------------------------------
    def numOfPairs_split(self, nums: List[str], target: str) -> int:
        freq = Counter(nums)
        t_len = len(target)
        count = 0
        for split in range(1, t_len):
            prefix = target[:split]
            suffix = target[split:]
            if prefix == suffix:
                c = freq.get(prefix, 0)
                count += c * (c - 1)
            else:
                count += freq.get(prefix, 0) * freq.get(suffix, 0)
        return count


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("暴力法",    sol.numOfPairs_brute_force),
        ("哈希表法",  sol.numOfPairs_hash_map),
        ("分割点法",  sol.numOfPairs_split),
    ]

    test_cases = [
        (["777", "7", "77", "77"],       "7777", 4),
        (["123", "4", "12", "34"],       "1234", 2),
        (["1", "1", "1"],                "11",   6),
        (["12", "12"],                   "1212", 2),
        (["1", "1", "1", "1"],           "11",  12),
        (["7", "7", "7", "7", "7"],      "77",  20),
        (["1", "2", "3"],                "12",   1),
        (["1", "2", "3"],                "21",   1),
        (["1", "2", "3"],                "13",   1),
        (["11", "1", "1"],               "111",  4),
    ]

    for name, fn in methods:
        all_pass = True
        for nums, target_val, expected in test_cases:
            result = fn(list(nums), target_val)
            if result != expected:
                print(f"  ✗ {name}: nums={nums}, target={target_val}, got={result}, expected={expected}")
                all_pass = False
        if all_pass:
            print(f"  ✓ {name}: 所有 {len(test_cases)} 个测试用例通过")


# ============================================================
# 性能对比试验
# ============================================================
def _random_digit_string(_rnd: random.Random, max_len: int = 5) -> str:
    length = _rnd.randint(1, max_len)
    first = str(_rnd.randint(1, 9))
    rest = "".join(str(_rnd.randint(0, 9)) for _ in range(length - 1))
    return first + rest


def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验（测量每种解法在不同规模数据上的运行时间）")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("暴力法 O(n^2*L)",    sol.numOfPairs_brute_force),
        ("哈希表法 O(n*L)",    sol.numOfPairs_hash_map),
        ("分割点法 O(n*L+T)",  sol.numOfPairs_split),
    ]

    sizes = [50, 100, 500, 1_000, 5_000, 10_000]
    repeat = 10

    print(f"{'数据规模':>10} | {'解法':<22} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        rnd = random.Random(42 + size)
        nums = [_random_digit_string(rnd, max_len=6) for _ in range(size)]
        # 构造一个必然存在解的 target：选两个随机字符串拼接
        i, j = size // 4, 3 * size // 4
        target_val = nums[i] + nums[j]

        for name, fn in methods:
            if "暴力" in name and size > 500:
                print(f"{size:>10} | {name:<22} | {'> 10000':>15} | {'跳过（太慢）':<20}")
                continue

            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(list(nums), target_val)
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
| 解法       | 时间复杂度   | 空间复杂度 | 说明                                     |
|------------|-------------|-----------|------------------------------------------|
| 暴力法     | O(n^2 * L)  | O(1)      | 两层循环拼接字符串比较，n 大时不可用        |
| 哈希表法   | O(n * L)    | O(n*L)    | 统计频率，每个串作为后缀查前缀              |
| 分割点法   | O(n*L + T)  | O(n*L)    | 枚举 target 切割位置，乘法直接计数，最优雅  |

分割点法核心洞察：
  - nums[i] + nums[j] == target 等价于：
    存在 split 使得 nums[i] 恰好是 target 的前 split 个字符，
    nums[j] 恰好是 target 从 split 开始的后缀。
  - 不同 split 的前缀长度不同，一个字符串不可能同时是两种长度的前缀，
    所以不会重复计数，也不会漏计。
  - 这把问题从「两两配对」转化为「按位置查表」，极其简洁。

计数公式：
  - prefix != suffix：freq[prefix] * freq[suffix]
      （前缀组里任意一个配后缀组里任意一个，都是有效有序对）
  - prefix == suffix：freq[prefix] * (freq[prefix] - 1)
      （同组里选两个不同下标：第一个元素有 c 种选法，第二个有 c-1 种，排除自己）
""")


if __name__ == "__main__":
    print("=== 连接后等于目标字符串的字符串对：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
