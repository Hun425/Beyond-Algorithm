## [3345. Smallest Divisible Digit Product I](https://leetcode.com/problems/smallest-divisible-digit-product-i/description/?envType=daily-question&envId=2026-08-06)

### 접근 방법

- 주어진 숫자 `n`부터 시작하여 각 숫자의 자릿수 곱이 `t`로 나누어지는지 확인합니다.
- 자릿수 곱이 `t`로 나누어지면 해당 숫자를 반환합니다.
- 자릿수 곱이 `t`로 나누어지지 않으면 숫자를 1씩 증가시키며 반복합니다.
- 숫자에 '0'이 포함되어 있으면 자릿수 곱이 0이 되므로 바로 `n`을 반환합니다.

### 코드

```kotlin
class Solution {
    fun smallestNumber(
        n: Int,
        t: Int,
    ): Int {
        var num = n
        if ('0' in num.toString()) return n
        while (true) {
            val product = num.toString().fold(1) { acc, c -> acc * c.digitToInt() }
            if (product % t == 0) return num
            num++
        }
    }
}
```

### 복잡도

- 시간복잡도: 최악의 경우 무한 루프에 빠질 수 있으므로 명확히 정의하기 어렵습니다.. (그래도 일단 케이스는 다 통과해서 답안으로 제출)
- 공간복잡도: 모름

### 회고
