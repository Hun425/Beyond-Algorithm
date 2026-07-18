## [303. Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/description/?envType=problem-list-v2&envId=prefix-sum)

### 접근 방법

- 배열을 잘라서 풀이.

### 코드

```kotlin
class NumArray(nums: IntArray) {
    private val prefixSum = IntArray(nums.size + 1)

    init {
        prefixSum[0] = 0
        for (idx in 1..nums.size) {
            prefixSum[idx] = prefixSum[idx - 1] + nums[idx - 1]
        }
    }

    fun sumRange(
        left: Int,
        right: Int,
    ): Int = prefixSum[right + 1] - prefixSum[left]
}
```

### 복잡도

- 시간복잡도: 처음 누적합 연산 O(n). sumRagne 시간 복잡도 O(1). 호출 q번 고려시 O(q) => O(n)
- 공간복잡도: 모르겠음

### 회고

- 윤식님을 받들어 다시 풀어봄. 대 윤 식