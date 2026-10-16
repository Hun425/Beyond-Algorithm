## [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

### 접근 방법

- 두 리스트가 이미 정렬되어 있으므로 현재 노드의 값을 비교해 작은 노드부터 연결한다.
- 한쪽 리스트가 끝나면 남은 리스트를 그대로 연결한다.

### 코드

```dart
class Solution {
  ListNode? mergeTwoLists(ListNode? list1, ListNode? list2) {
    final ListNode head = ListNode(0);
    ListNode temp = head;

    while (list1 != null && list2 != null) {
      if (list1.val <= list2.val) {
        temp.next = list1;
        list1 = list1.next;
      } else {
        temp.next = list2;
        list2 = list2.next;
      }
      temp = temp.next!;
    }

    temp.next = list1 ?? list2;
    return head.next;
  }
}
```

### 복잡도

- 시간복잡도: O(n + m)
- 공간복잡도: O(1)

### 회고

- 더미 노드를 사용하면 첫 노드를 별도로 처리할 필요가 없다.
- 남은 리스트를 한 번에 연결해 구현을 단순화할 수 있다.