## [문제명](문제 링크)

### 접근 방법

k의 배수가 주어진 배열에 있는지 없는지 빠르게 찾는게 중요. 처음엔 true를 값으로 하는 해시 맵을 만들어 풀었으나, true만 담겨있는 맵을 만들고 정작 존재 여부는 null로 하는 것이 바람직하지 않다고
여겨, AI 의 도움을 받아 HashSet을 사용하는 풀이로 변경.

### 코드

```kotlin
class Solution {
    fun missingMultiple(
        nums: IntArray,
        k: Int,
    ): Int {
        val hashSet = nums.toHashSet()
        var multiple = k

        while (multiple in hashSet) {
            multiple += k
        }

        return multiple
    }
}
```

### 복잡도

- 시간복잡도: O (n) - nums -> HashSet 변환.
- 공간복잡도: O (n)

### 회고

