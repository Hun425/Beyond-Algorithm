## [3756. Concatenate Non-Zero Digits and Multiply by Sum II](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/?envType=daily-question&envId=2026-07-08)

### 접근 방법

1. x, sum 을 좌측에서 부터 미리 연산하여 준비.
2. 자릿수 보정에 쓰일 수 있도록 10의 제곱도 미리 연산.
3. 이 때, MOD연산을 미리 적용. (나머지 연산의 분배법칙)
4. prefixX에 나머지 연산이 적용되어 있어, 오른쪽 파트에서 왼쪽 파트를 뺼 때 음수가 될 수 있으므로 나머지를 더하여 보정.

### 문제점

### 코드

```kotlin
package y2026m07.m07d08DailyLeet3756ConcatenateNonZeroDigitsAndMultiplyBySum2

class Solution {
    fun sumAndMultiply(
        s: String,
        queries: Array<IntArray>,
    ): IntArray {
        val length = s.length
        val nonZeroCount = IntArray(length + 1)
        val digitSum = LongArray(length + 1)
        val prefixX = LongArray(length + 1)
        val powerOfTen = LongArray(length + 1)
        powerOfTen[0] = 1L

        s.forEachIndexed { idx, ch ->
            val digit = ch.digitToInt()
            digitSum[idx + 1] = digitSum[idx] + digit
            powerOfTen[idx + 1] = powerOfTen[idx] * 10L % MOD

            if (digit == 0) {
                nonZeroCount[idx + 1] = nonZeroCount[idx]
                prefixX[idx + 1] = prefixX[idx]
            } else {
                nonZeroCount[idx + 1] = nonZeroCount[idx] + 1
                prefixX[idx + 1] = (prefixX[idx] * 10L + digit) % MOD
            }
        }

        return queries.map { query ->
            val left = query[0]
            val right = query[1]

            val gapNonZeroCount = nonZeroCount[right + 1] - nonZeroCount[left]
            val xLeftPart = prefixX[left] * powerOfTen[gapNonZeroCount] % MOD
            val x = (prefixX[right + 1] - xLeftPart + MOD) % MOD
            val sum = digitSum[right + 1] - digitSum[left]

            (x * sum % MOD).toInt()
        }.toIntArray()
    }

    companion object {
        private const val MOD = 1_000_000_007L
    }
}

```

### 복잡도

- 시간복잡도: O (s.length + queries.size + queries.size) = O (n)
- 공간복잡도: 모름

### 회고

- 없음

### 기타

- 303 문제를 풀고도, 완전히 혼자 풀지는 못함.. 윤식님 답안과 AI의 도움을 너무 많이 받았음.
- Failed로 표기해놓고 오답 복습 필요.
