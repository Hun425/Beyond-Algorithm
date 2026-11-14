## [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/)

### 접근 방법

앞선 [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) 문제에서 배열의 값을 바꾸는 연산이 추가된 문제이다.

누적 합을 사용하면 구간 합은 빠르게 구할 수 있지만, 어떤 원소의 값이 바뀌었을 때 그 원소를 포함하는 뒤쪽 누적 합들을 모두 수정해야 한다. 이 경우 한 번 갱신할 때마다 최악의 경우 $O(n)$ 시간이 필요하다.

이렇게 **원소의 갱신과 구간 합 질의를 함께 처리**할 때 사용할 수 있는 자료구조가 **세그먼트 트리**이다.

세그먼트 트리가 이 문제를 푸는 아이디어는 다음과 같다.

> 배열의 구간을 절반씩 나누어 트리로 만들고, 각 노드에 자신이 담당하는 구간의 합을 저장한다.

각 노드는 `[left, right)` 구간을 담당한다. 즉 `left`는 포함하고 `right`는 포함하지 않는다.

트리를 만드는 절차는 다음과 같다.

1. 루트 노드는 배열 전체인 `[0, nums.size)`를 담당한다.
2. 원소가 하나뿐인 구간이라면 리프 노드로 만들고 해당 원소의 값을 저장한다.
3. 그렇지 않으면 중간 위치 `m`을 기준으로 `[left, m)`과 `[m, right)`를 담당하는 자식 노드를 만든다.
4. 현재 노드의 값은 두 자식 노드의 값을 더한 값으로 정한다.

어떤 원소를 갱신할 때는 해당 인덱스가 포함된 자식으로만 내려가며, 전체 노드를 수정할 필요 없이 루트에서 해당 리프까지의 경로만 수정하면 된다.

구간 합을 구할 때는 현재 노드의 구간과 질의 구간의 관계를 확인한다.

1. 현재 노드의 구간이 질의 구간에 완전히 포함되면, 미리 저장한 합을 그대로 반환한다.
2. 두 구간이 전혀 겹치지 않으면 `0`을 반환한다.
3. 일부만 겹치면, 두 자식 노드에 대해 같은 방법으로 구간 합을 구해 더한다.

예를 들어 `[1, 3, 5]`에서 `update(1, 2)`를 호출하면 원소 `3`을 담당하는 리프의 값이 `2`로 바뀌고, 그 리프의 조상 노드들만 합을 다시 계산한다. 이후 전체 구간의 합은 루트에 저장된 `8`을 반환하면 된다.

### 코드

```kotlin
class NumArray(nums: IntArray) {
    private class Node private constructor(
        nums: IntArray,
        val left: Int,
        val right: Int,
    ) {
        constructor(nums: IntArray) : this(nums, 0, nums.size)

        val children: Pair<Node, Node>? // 리프 노드인 경우 자식이 없다.

        var value: Int private set

        init {
            if (right - left == 1) {
                children = null
                value = nums[left]
            } else {
                val m = (left + right) / 2
                val leftNode = Node(nums, left, m)
                val rightNode = Node(nums, m, right)
                children = leftNode to rightNode
                value = leftNode.value + rightNode.value
            }
        }

        fun update(index: Int, value: Int) {
            if (children == null) {
                this.value = value
                return
            }

            val (leftNode, rightNode) = children

            listOf(leftNode, rightNode).forEach { node ->
                if (node.left <= index && index < node.right) {
                    node.update(index, value)
                }
            }

            this.value = leftNode.value + rightNode.value
        }

        fun sumRange(left: Int, right: Int): Int {
            return when {
                left <= this.left && this.right <= right -> value
                this.right <= left || right <= this.left -> 0
                children == null -> throw IllegalStateException()
                else -> children.first.sumRange(left, right) + children.second.sumRange(left, right)
            }
        }
    }

    private val root = Node(nums)

    fun update(index: Int, `val`: Int) {
        root.update(index, `val`)
    }

    fun sumRange(left: Int, right: Int): Int {
        return root.sumRange(left, right + 1)
    }
}
```

### 복잡도

$n$이 `nums`의 길이이고, $q$가 `update`와 `sumRange`의 총 호출 횟수일 때,

- 시간복잡도: 트리 생성은 $O(n)$, 각 갱신과 구간 합 질의는 $O(\log{n})$이므로 전체 $O(n + q\log{n})$. 구간 합 질의는 완전히 포함되거나 겹치지 않는 구간에서 탐색을 끝내므로 모든 리프를 방문하지 않는다.
- 공간복잡도: 트리 저장에 $O(n)$, 재귀 호출 스택에 $O(\log{n})$이 필요하므로 전체 $O(n)$

### 회고

같은 구간 합 문제라도 값의 갱신이 추가되면 적절한 자료구조가 달라진다. 세그먼트 트리는 구간을 나누고 자식의 결과를 합치는 구조이므로, 합 대신 최솟값이나 최댓값을 저장하는 문제에도 응용할 수 있다.

현재 코드는 노드 객체로 구현했지만 배열로도 구현할 수 있다. 구간 합을 처리하는 다른 자료구조로는 펜윅 트리(Binary Indexed Tree)도 있으므로, 함께 찾아보는 것을 추천합니다.
