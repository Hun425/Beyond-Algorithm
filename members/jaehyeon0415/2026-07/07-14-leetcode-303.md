## [303. Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/?envType=problem-list-v2&envId=prefix-sum)

### 접근 방법
- 큰 수를 대비해서 미리 계산해 놈

### 코드
```kotlin
class NumArray(nums: IntArray) {
    val prefixSum = IntArray(nums.size + 1)

    init {
        for (i in nums.indices) {
            prefixSum[i + 1] = prefixSum[i] + nums[i]
        }
    }

    fun sumRange(left: Int, right: Int): Int {
        return prefixSum[right + 1] - prefixSum[left]
    }

}
```

### 복잡도
- 시간복잡도: O(n + sumRange 호출 횟수)
- 공간복잡도: O(n)

### 회고
- prefix sum에 대해서 확실히 알게됨