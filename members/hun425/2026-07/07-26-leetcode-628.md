## [628. Maximum Product of Three Numbers](https://leetcode.com/problems/maximum-product-of-three-numbers/)

### 접근 방법

- 세 수의 곱이 최대가 되는 경우는 딱 두 가지뿐
  - 가장 큰 세 수의 곱
  - 가장 작은 두 수(음수 × 음수 = 양수) × 가장 큰 수
- 정렬 후 두 후보를 비교해서 큰 값을 반환

### 코드

```kotlin
class Solution {
    fun maximumProduct(nums: IntArray): Int {
        nums.sort()
        val n = nums.size
        return maxOf(nums[n - 1] * nums[n - 2] * nums[n - 3], nums[0] * nums[1] * nums[n - 1])
    }
}
```

### 복잡도

- 시간복잡도: O(n log n)
- 공간복잡도: O(1)

### 회고

- 음수 두 개의 곱이 양수가 되는 케이스를 놓치지 않는 게 핵심이었다
