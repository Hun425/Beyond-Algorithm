## [628. Maximum Product of Three Numbers](https://leetcode.com/problems/maximum-product-of-three-numbers/description/?envType=daily-question&envId=2026-07-26)

### 접근 방법

- 양수만 존재하는 경우, 음수만 존재하는 경우, 양수와 음수가 섞여 있는 경우를 나누어 생각할 수 있다.

### 코드

```kotlin
class Solution {
    fun maximumProduct(nums: IntArray): Int {
        nums.sort()
        val n = nums.size
        // 가장 큰 수의 세 곱
        val case1 = nums[n - 1] * nums[n - 2] * nums[n - 3]
        // 음수 두개와 양수 하나케이스를 고려한 곱
        val case2 = nums[0] * nums[1] * nums[n - 1]
        // 두 경우 중 최대값을 반환
        return maxOf(case1, case2)
    }
}
```

### 복잡도

- 시간복잡도: O (n log n) (정렬)
- 공간복잡도: 모르겠음

### 회고
