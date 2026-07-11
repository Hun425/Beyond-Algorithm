## [3756. Concatenate Non-Zero Digits and Multiply by Sum II](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/?envType=daily-question&envId=2026-07-08)

### 접근 방법

1. 쿼리의 엘레멘트 대로 주어진 문자열 substring후 Leetcode 3754 번 스타일로 연산.

### 문제점

1. 큰수를 Int -> Long -> BigInteger등 으로 대응하였으나, 문제의 조건을 제대로 이해하지 못하였음.
2. 1 <= m == s.length <= 10^5의 길이가 들어올 수 있기때문에 데이터타입을 변경하는 식으로는 해결하지 못하고 결국 timeout 처리됨.

### 코드

```kotlin
class Solution {
    fun sumAndMultiply(
        s: String,
        queries: Array<IntArray>,
    ): IntArray = queries.map { query ->
        val start = query[0]
        val end = query[1] + 1

        val substring = s.substring(start, end)
        sumAndMultiPlyNonZero(substring)
    }
        .toTypedArray()
        .toIntArray()

    private fun sumAndMultiPlyNonZero(nString: String): Int {
        val nonZeroDigits = nString
            .filter { it != '0' }
            .map { it.digitToInt() }

        val x = nonZeroDigits
            .joinToString("")
            .ifEmpty { "0" }
            .toBigInteger()

        val sum = nonZeroDigits.sum()

        val result = x * sum.toBigInteger()

        return (result % MOD.toBigInteger()).toInt()
    }

    companion object {
        private const val MOD = 1_000_000_000 + 7
    }
}
```

### 복잡도

- 시간복잡도: 모름
- 공간복잡도: 망함

### 회고

- 없음

### 기타

- 아직 전부 풀이한 문제가 아닙니다. 답안을 보지 않고 풀기위해 큰수를 어떻게 다룰지 고민중 입니다.
