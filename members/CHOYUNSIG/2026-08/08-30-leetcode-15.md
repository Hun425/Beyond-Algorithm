## [3Sum](https://leetcode.com/problems/3sum/)

### 접근 방법

`i`와 `j`를 먼저 정하고, 적절한 `k`를 이분 탐색으로 찾아본다.

### 코드

```kotlin
class Solution {
    fun threeSum(nums: IntArray): List<List<Int>> {
        val sortedNums = nums.sorted()
        val result = mutableSetOf<List<Int>>()

        for (i in 0 ..< sortedNums.size - 2) {
            for (j in i + 1 ..< sortedNums.size - 1) {
                val remain = -(sortedNums[i] + sortedNums[j])
                val k = sortedNums.searchIndex(value = remain, fromIndex = j + 1) ?: continue
                result.add(listOf(sortedNums[i], sortedNums[j], sortedNums[k]))
            }
        }

        return result.toList()
    }

    private fun List<Int>.searchIndex(value: Int, fromIndex: Int): Int? {
        var (s, e) = fromIndex to this.lastIndex

        while (s <= e) {
            val m = (s + e) / 2

            if (this[m] < value) {
                s = m + 1
            } else {
                e = m - 1
            }
        }

        return s.takeIf { it in fromIndex ..< size && this[it] == value }
    }
}
```

### 복잡도

- 시간복잡도: $O(n^{2}\log{n})$
- 공간복잡도: 답안 공간에 의해 $O(n^{2})$

### 회고

이 문제가 어려운지에 대해 의견을 남겨주세요.