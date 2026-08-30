## [9. Palindrome Number](https://leetcode.com/problems/palindrome-number/description/)

### 접근 방법

- 숫자가 회문인지 확인
- 음수인 경우와 끝자리가 0이면서 0이아닌 케이스를 얼리 리턴
- 문자열로 변환 후 뒤집어서 비교

### 코드

```kotlin
class Solution {
    fun isPalindrome(x: Int): Boolean {
        if (x < 0) return false
        val str = x.toString()
        if (str.endsWith("0") && str != "0") return false
        return str == str.reversed()
    }
}
```

### 복잡도

- 시간복잡도: 잘 모르겠음
- 공간복잡도: 잘 모르겠음

### 회고

- 문자열 변환 없이 풀 수 있는 방법이 있는지 궁금합니다.