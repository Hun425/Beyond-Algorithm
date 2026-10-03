## [13. Roman to Integer](https://leetcode.com/problems/roman-to-integer/description/)

### 접근 방법

- `when`을 사용해서 각 로마 숫자를 정수 값으로 변환
- 기본적으로 왼쪽부터 하나씩 값을 더함
- 현재 숫자가 다음 숫자보다 작은 경우에는 현재 숫자를 빼줌
- 예를 들어 `IV`는 `I`가 `V`보다 작기 때문에 `-1 + 5`로 계산
- 이 방식으로 `IV`, `IX`, `XL`, `XC`, `CD`, `CM` 같은 경우를 따로 처리하지 않아도 됨

### 코드

```kotlin
class Solution {
    fun romanToInt(s: String): Int {
        fun valueOf(c: Char): Int =
            when (c) {
                'I' -> 1
                'V' -> 5
                'X' -> 10
                'L' -> 50
                'C' -> 100
                'D' -> 500
                'M' -> 1000
                else -> 0
            }

        var result = 0

        for (i in s.indices) {
            val current = valueOf(s[i])

            if (i < s.lastIndex && current < valueOf(s[i + 1])) {
                result -= current
            } else {
                result += current
            }
        }

        return result
    }
}
```

### 복잡도

- 시간복잡도: O (n). 문자열을 처음부터 끝까지 한 번 순회함
- 공간복잡도: 항상 잘 모르겠음..

### 회고

- 다양한 조합을 처리할수 있도록 기본적인 로직을 구현하는 것이 중요함
