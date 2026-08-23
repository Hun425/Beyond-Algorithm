## [Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/)

### 접근 방법

**이분 탐색**하여 초기 탐색 위치를 잡고, **투 포인터** 방식으로 배열을 스캔해나간다.
모두 스터디 기존 출제 문제로 접했던 알고리즘이다.

### 코드

```kotlin
import kotlin.math.abs

class Solution {
    fun findClosestElements(arr: IntArray, k: Int, x: Int): List<Int> {
        val initialIndexPair = searchInitialIndexPair(arr, x)
        val closestElements = getKthClosestElementsFromInitialIndexPair(arr, k, x, initialIndexPair)

        return closestElements
    }

    private fun searchInitialIndexPair(
        arr: IntArray,
        x: Int,
    ): Pair<Int, Int> {
        var (s, e) = 0 to arr.lastIndex

        while (s <= e) {
            val m = (s + e) / 2

            if (arr[m] <= x) {
                s = m + 1
            } else {
                e = m - 1
            }
        }

        return e to s
    }

    private fun getKthClosestElementsFromInitialIndexPair(
        arr: IntArray,
        k: Int,
        x: Int,
        initialIndexPair: Pair<Int, Int>,
    ): List<Int> {
        infix fun Int.closerThan(other: Int) =
            abs(this - x) < abs(other - x) || (abs(this - x) == abs(other - x) && this < other)

        val result = mutableListOf<Int>()
        var (s, e) = initialIndexPair

        repeat(k) {
            when {
                s < 0 -> {
                    if (e <= arr.lastIndex) result.add(arr[e++])
                }

                e > arr.lastIndex -> {
                    result.add(arr[s--])
                }

                arr[s] closerThan arr[e] -> {
                    result.add(arr[s--])
                }

                else -> {
                    result.add(arr[e++])
                }
            }
        }

        return result.sorted()
    }
}
```

### 복잡도

$n$이 `arr`의 길이일 때,

- 시간복잡도: $O(\log{n} + k\log{k})$
- 공간복잡도: 입력에 의해 $O(n)$

### 회고

해당 문제가 어려운지 의견을 남겨주세요.
