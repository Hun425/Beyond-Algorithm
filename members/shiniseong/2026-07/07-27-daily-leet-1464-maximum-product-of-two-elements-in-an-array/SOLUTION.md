## [1464. Maximum Product of Two Elements in an Array](https://leetcode.com/problems/maximum-product-of-two-elements-in-an-array/description/?envType=daily-question&envId=2026-07-27)

### 접근 방법

- 줄세우기 후 최대 최소에 -1 적용.

### 코드

```kotlin
class Solution {
    fun maxProduct(nums: IntArray): Int {
        nums.sort()
        val n = nums.size
        return (nums[n - 1] - 1) * (nums[n - 2] - 1)
    }
}
```

### 복잡도

- 시간복잡도: O (n log n)
- 공간복잡도: 모르겠음

### 회고
