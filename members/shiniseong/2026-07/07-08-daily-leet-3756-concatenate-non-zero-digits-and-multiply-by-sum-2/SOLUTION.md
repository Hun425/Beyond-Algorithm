## [3756. Concatenate Non-Zero Digits and Multiply by Sum II](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/?envType=daily-question&envId=2026-07-08)

### 접근 방법

1. 쿼리의 엘레멘트 대로 주어진 문자열 substring후 Leetcode 3754 번 스타일로 연산.
2. 수학적 원리는 잘 모르겠지만 나머지연산을 자릿수별로 미리해도 결과가 똑같길래 적용해 봤음...

### 문제점

1. 몇개 테스트에서 계속 실패함 (원인을 모르겠습니다..)

### 코드

```kotlin
import kotlin.math.pow

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

        val sum = nonZeroDigits.sum()

        val xSource = nonZeroDigits
            .joinToString("")
            .ifEmpty { "0" }

        val result = xSource.reversed().mapIndexed { index, ch ->
            val number = ch.digitToInt() * (10.0.pow(index)) % MOD
            (number * sum) % MOD
        }.sum()

        return (result % MOD).toInt()
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
