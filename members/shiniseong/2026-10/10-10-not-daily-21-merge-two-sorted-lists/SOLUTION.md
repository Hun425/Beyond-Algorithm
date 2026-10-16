## [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

### 접근 방법

- 두 연결 리스트는 이미 오름차순으로 정렬되어 있음
- 각 리스트의 첫 번째 노드부터 값을 비교해서 더 작은 노드를 결과 리스트에 연결
- 연결한 노드가 속한 리스트는 다음 노드로 이동
- 이 과정을 둘 중 하나의 리스트가 끝날 때까지 반복
- 한쪽 리스트가 먼저 끝나면 나머지 리스트를 그대로 연결 (미리 정렬되어있기 때문..!)
- 첫 번째 노드를 따로 처리하지 않기 위해 임시 노드 (dummy)를 하나 생성 (AI 도움 받음)
- 마지막에는 임시 노드의 다음 노드부터 반환 (임시 노드 첫 값을 제외하기 위해)

### 코드

```
class Solution {
    fun mergeTwoLists(
        list1: ListNode?,
        list2: ListNode?,
    ): ListNode? {
        val dummy = ListNode(0)
        var tail = dummy

        var left = list1
        var right = list2

        while (left != null && right != null) {
            if (left.`val` <= right.`val`) {
                tail.next = left
                tail = left
                left = left.next
            } else {
                tail.next = right
                tail = right
                right = right.next
            }
        }

        tail.next = left ?: right

        return dummy.next
    }
}
```

### 복잡도

- 시간복잡도: O (N + M) 첫번째 리스트 노드, 두번째 리스트 노트.
- 공간복잡도: 모름

### 회고

- AI 도움을 많이 받음..