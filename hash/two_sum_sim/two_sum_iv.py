# 题目：两数之和 IV - 输入二叉搜索树 (LeetCode 653)
# 难度：简单
# 标签：树、深度优先搜索、广度优先搜索、二叉搜索树、哈希表、双指针
#
# 题目需求：
#   给定一个二叉搜索树 root 和一个目标结果 k，
#   如果 BST 中存在两个元素且它们的和等于给定的目标结果，则返回 true。
#
# 约束条件：
#   1. 二叉树的节点个数的范围是 [1, 10^4]
#   2. -10^4 <= Node.val <= 10^4
#   3. root 为二叉搜索树
#   4. -10^5 <= k <= 10^5
#
# 本文件在同一个 Solution 类里提供三种解法，并在末尾做对比试验。


from typing import List, Optional
from collections import deque
import time
import random


# ============================================================
# 二叉树节点定义
# ============================================================
class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================
# 辅助函数：按 LeetCode 层序格式（含 None）构建二叉树
# ============================================================
def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


class Solution:
    # ----------------------------------------------------------
    # 解法一：DFS 遍历 + BST 查找
    # 思路：
    #   1. DFS 遍历每一个节点
    #   2. 对每个节点的值 val，在 BST 中搜索 k - val
    #   3. 搜索时要确保找到的节点不是当前节点自身
    # 时间复杂度：O(n log n) —— 每个节点做一次 O(log n) 的 BST 搜索（平衡时）。
    # 空间复杂度：O(h) —— 递归栈深度，h 为树高；最坏 O(n)。
    # ----------------------------------------------------------
    def findTarget_dfs_search(self, root: Optional[TreeNode], k: int) -> bool:
        def search(node: Optional[TreeNode], target: int, exclude: TreeNode) -> bool:
            if node is None:
                return False
            if node.val == target and node is not exclude:
                return True
            if target < node.val:
                return search(node.left, target, exclude)
            else:
                return search(node.right, target, exclude)

        def dfs(node: Optional[TreeNode]) -> bool:
            if node is None:
                return False
            if search(root, k - node.val, node):
                return True
            return dfs(node.left) or dfs(node.right)

        return dfs(root)

    # ----------------------------------------------------------
    # 解法二：哈希集 + DFS（简洁高效）
    # 思路：
    #   1. 深度优先遍历每个节点
    #   2. 用 set 记录已访问过的节点值
    #   3. 访问当前节点前，先检查 k - node.val 是否已在 set 中；
    #      若在则返回 True，否则将当前值加入 set
    #   注意：必须先查再加，避免同一节点被用两次（因为 BST 中值可能不重复）
    # 时间复杂度：O(n) —— 每个节点访问一次，set 查找/插入 O(1)。
    # 空间复杂度：O(n) —— set 最多存 n 个值。
    # ----------------------------------------------------------
    def findTarget_hash_set(self, root: Optional[TreeNode], k: int) -> bool:
        seen = set()

        def dfs(node: Optional[TreeNode]) -> bool:
            if node is None:
                return False
            if k - node.val in seen:
                return True
            seen.add(node.val)
            return dfs(node.left) or dfs(node.right)

        return dfs(root)

    # ----------------------------------------------------------
    # 解法三：中序遍历 + 双指针（利用 BST 有序性）—— 推荐解法
    # 思路：
    #   1. BST 的中序遍历结果是一个严格（非递减）升序序列
    #   2. 对有序数组用双指针：左指针从最小值出发，右指针从最大值出发
    #   3. 若两数之和 == k，返回 True；
    #      若和 < k，左指针右移；若和 > k，右指针左移
    # 时间复杂度：O(n) —— 中序遍历 O(n)，双指针 O(n)。
    # 空间复杂度：O(n) —— 存储中序遍历结果。
    # ----------------------------------------------------------
    def findTarget_inorder_two_pointers(self, root: Optional[TreeNode], k: int) -> bool:
        inorder: List[int] = []

        def traverse(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            traverse(node.left)
            inorder.append(node.val)
            traverse(node.right)

        traverse(root)

        left, right = 0, len(inorder) - 1
        while left < right:
            s = inorder[left] + inorder[right]
            if s == k:
                return True
            elif s < k:
                left += 1
            else:
                right -= 1
        return False


# ============================================================
# 正确性测试用例
# ============================================================
def test_correctness():
    sol = Solution()

    methods = [
        ("DFS+BST查找",     sol.findTarget_dfs_search),
        ("哈希集+DFS",      sol.findTarget_hash_set),
        ("中序+双指针",     sol.findTarget_inorder_two_pointers),
    ]

    test_cases = [
        ([5, 3, 6, 2, 4, None, 7], 9,  True),
        ([5, 3, 6, 2, 4, None, 7], 28, False),
        ([1],                       2,  False),
        ([2, 1, 3],                 4,  True),
        ([2, 1, 3],                 3,  True),
        ([2, 1, 3],                 5,  True),
        ([1, None, 3],              4,  True),
        ([0, -1, 2, -3, None, None, 4], -4, True),
        ([0, -1, 2, -3, None, None, 4], 1,  True),
        ([1, 0, 4, -2, None, 3],   7,  True),
    ]

    for name, fn in methods:
        all_pass = True
        for tree_list, k_val, expected in test_cases:
            tree = build_tree(list(tree_list))
            result = fn(tree, k_val)
            if result != expected:
                print(f"  ✗ {name}: tree={tree_list}, k={k_val}, got={result}, expected={expected}")
                all_pass = False
        if all_pass:
            print(f"  ✓ {name}: 所有 {len(test_cases)} 个测试用例通过")


# ============================================================
# 性能对比试验
# ============================================================
def _generate_bst(n: int, seed: int) -> TreeNode:
    """生成一棵近似平衡的 BST（用随机值排序后递归中点分割）。"""
    random.seed(seed)
    values = sorted(random.sample(range(-10_000_000, 10_000_000), n))

    def build(sorted_vals: List[int]) -> Optional[TreeNode]:
        if not sorted_vals:
            return None
        mid = len(sorted_vals) // 2
        node = TreeNode(sorted_vals[mid])
        node.left = build(sorted_vals[:mid])
        node.right = build(sorted_vals[mid + 1:])
        return node

    return build(values)


def benchmark():
    print("\n" + "=" * 70)
    print("性能对比试验（测量每种解法在不同规模数据上的运行时间）")
    print("=" * 70)

    sol = Solution()
    methods = [
        ("DFS+BST查找 O(n log n)", sol.findTarget_dfs_search),
        ("哈希集+DFS O(n)",        sol.findTarget_hash_set),
        ("中序+双指针 O(n)",       sol.findTarget_inorder_two_pointers),
    ]

    sizes = [500, 2_000, 5_000, 10_000]
    repeat = 5

    print(f"{'数据规模':>10} | {'解法':<25} | {'平均耗时 (ms)':>15} | {'备注':<20}")
    print("-" * 70)

    for size in sizes:
        root = _generate_bst(size, seed=42 + size)
        # 构造一个必定存在的 k：取两个叶子的值相加
        # 为简单起见，固定取最小值+最大值
        node_min, node_max = root, root
        while node_min.left:
            node_min = node_min.left
        while node_max.right:
            node_max = node_max.right
        k_val = node_min.val + node_max.val

        for name, fn in methods:
            times = []
            for _ in range(repeat):
                start = time.perf_counter()
                fn(root, k_val)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            avg_ms = sum(times) / len(times)
            print(f"{size:>10} | {name:<25} | {avg_ms:>15.3f} | {'':<20}")

        print("-" * 70)


# ============================================================
# 理论复杂度小结
# ============================================================
def summary():
    print("\n" + "=" * 70)
    print("三种解法的理论复杂度小结")
    print("=" * 70)
    print("""
| 解法          | 时间复杂度   | 空间复杂度 | 说明                                     |
|---------------|-------------|-----------|------------------------------------------|
| DFS+BST查找   | O(n log n)  | O(h)      | 每个节点做一次 BST 二分查找，注意排除自身  |
| 哈希集+DFS    | O(n)        | O(n)      | 一次遍历，边查边加，简洁高效               |
| 中序+双指针   | O(n)        | O(n)      | 利用 BST 有序性，中序后双指针夹逼           |

为什么哈希集和中序+双指针都很高效？
  - 哈希集：代码最短，利用 set O(1) 查找，不需要先遍历一次再处理
  - 中序+双指针：理论上空间可优化到 O(h)（用 Morris 遍历或迭代器）
  - DFS+BST查找：虽然利用了 BST 性质，但每个节点都从根搜索，常数较大

关键注意点：
  1. 不能把同一个节点用两次：先查再加（哈希集法）或用 is 排除（查找法）
  2. BST 的中序遍历是升序序列，这是所有 BST 题目的核心性质
  3. 题目没有说节点值唯一，所以不能因为找到 k - val == val 就认为一定存在
""")


if __name__ == "__main__":
    print("=== 两数之和 IV - 输入 BST：三种解法 + 对比试验 ===\n")
    print("【1】正确性测试")
    test_correctness()

    print("\n【2】性能对比")
    benchmark()

    print("\n【3】理论小结")
    summary()
