## [658. Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/)

### 접근 방법

- 배열이 오름차순 정렬되어 있으므로 **정답은 항상 길이 $k$의 연속 구간**
- 시작하는 인덱스만 찾으면 되니까 이진탐색

### 코드

```kotlin
class Solution {
    fun findClosestElements(arr: IntArray, k: Int, x: Int): List<Int> {
      
        var lo = 0
        var hi = arr.size - k

        while (lo < hi) {
            val mid = (lo + hi) / 2
            
            if (x - arr[mid] > arr[mid + k] - x) {
                lo = mid + 1
            } else {
                hi = mid
            }
        }

        return arr.slice(lo until lo + k)
    }
}
```

### 복잡도

- 시간복잡도: $O(\log n)$ 
- 공간복잡도: $O(k)$

### 회고

- 오랜만에 구현해보는 이진탐색 
