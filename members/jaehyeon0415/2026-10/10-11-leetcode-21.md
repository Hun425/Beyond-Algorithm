## [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/)

### 접근 방법

- 정렬된 배열이므로 같은 값은 연속해서 나타난다.
- 배열을 순회하며 마지막으로 저장한 값과 다르면 앞쪽에 덮어쓴다. 
- 중복 없는 원소 개수 `k`를 반환하며, 앞의 `k`개 원소가 결과가 된다.

### 코드

```dart
class Solution {
  int removeDuplicates(List<int> nums) {
    if (nums.isEmpty) return 0;

    var k = 1;

    for (var i = 1; i < nums.length; i++) {
      if (nums[i] != nums[k - 1]) {
        nums[k] = nums[i];
        k++;
      }
    }

    return k;
  }
}
```

### 복잡도

- 시간복잡도: O(n)
- 공간복잡도: O(1)

### 회고

- 중복 원소를 실제로 삭제할 필요 없이 앞쪽에 고유한 값만 모으면 된다.
- 탐색 위치와 저장 위치를 분리하는 두 포인터 접근을 배웠다.