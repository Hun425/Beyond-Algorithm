## [3731. Find Missing Elements](https://leetcode.com/problems/find-missing-elements/description/?envType=daily-question&envId=2026-08-04)

### 접근 방법

- 최소 값과 최대값을 구한 후, 최소값부터 최대값까지의 범위에서 nums에 없는 값을 찾아 반환.

### 코드

```kotlin
class Solution {
    fun findMissingElements(
        nums: IntArray,
    ): List<Int> {
        val min = nums.minOrNull() ?: return emptyList()
        val max = nums.maxOrNull() ?: return emptyList()

        return (min..max).mapNotNull { num ->
            if (num !in nums) num else null
        }
    }
}
```

### 복잡도

- 시간복잡도: O (n)
- 공간복잡도: O (m) (min과 max 사이의 범위)

### 회고
