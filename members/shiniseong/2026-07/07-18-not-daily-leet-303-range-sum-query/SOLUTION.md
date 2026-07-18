## [303. Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/description/?envType=problem-list-v2&envId=prefix-sum)

### 접근 방법

- 배열을 잘라서 풀이.

### 코드

```kotlin
class NumArray(
    private val nums: IntArray,
) {
    fun sumRange(
        left: Int,
        right: Int,
    ): Int = nums
        .slice(left..right)
        .sum()
}
```

### 복잡도

- 시간복잡도: (슬라이스(n) + sum(n)) * 호출 횟수(q) 2nq = O(nq)
- 공간복잡도: 모르겠음

### 회고

- 윤식님이 누적합 배우라고 던져주신 문제인데.. 그냥 kotlin 반복자 api로 해결함.. 다시 풀어 봐야할 필요가 있음. 
