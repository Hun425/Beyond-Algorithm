## [3756. Concatenate Non-Zero Digits and Multiply by Sum II](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/?envType=daily-question&envId=2026-07-08)

### 접근 방법

1. 수학적 원리는 잘 모르겠지만 나머지연산을 자릿수별로 미리해도 결과가 똑같길래 적용해 봤음...

### 문제점

1. 많은 케이스를 통과하게 되었으나 결국 * 10으로 누적해나가는 과정에서 연산 문제가 발생함. 미쳐버리겠슴다..

### 코드

```kotlin
package y2026m07.m07d08DailyLeet3756ConcatenateNonZeroDigitsAndMultiplyBySum2

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

        var sum = 0.toBigInteger()
        nonZeroDigits.forEach { ch ->
            sum = (sum + ch.digitToInt().toBigInteger()) % MOD
        }

        val xSource = nonZeroDigits
            .ifEmpty { "0" }

        var x = 0.toBigInteger()
        xSource.forEach { ch ->
            x = (x * 10.toBigInteger()) % MOD
            x += ch.digitToInt().toBigInteger() * sum
            x %= MOD
        }

        return (x % MOD).toInt()
    }

    companion object {
        private val MOD = (1_000_000_000 + 7).toBigInteger()
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
