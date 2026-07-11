## [3754. Concatenate Non-Zero Digits and Multiply by Sum I](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-i/)

### 접근 방법

1. 숫자를 문자열로 바꾸어 0이 아닌 숫자 배열로 변환
2. 0이 아닌 숫자 배열을 하나의 문자열로 concat 후 숫자로 변환하여 x에 할당
3. 0이 아닌 숫자 배열을 하나로 합쳐 sum에 할당
4. x * sum 리턴

### 코드

```kotlin
class Solution {
    fun sumAndMultiply(n: Int): Long {
        val nonZeroDigits = n
            .toString()
            .filter { it != '0' }
            .map { it.digitToInt() }

        val x = nonZeroDigits
            .joinToString("")
            .ifEmpty { "0" }
            .toLong()

        val sum = nonZeroDigits.sum()

        return x * sum
    }
}
```

### 복잡도

- 시간복잡도: O(log n), n의 크기 만큼이 아닌 자릿수에 비례한 순회를해서?
- 공간복잡도: 모름

### 회고

- 없음
