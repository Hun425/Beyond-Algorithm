## [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/)

### 접근 방법

- 첫 번째 문자열을 기준으로 잡음
- 첫 번째 문자열의 문자를 앞에서부터 하나씩 확인
- 다른 문자열들도 같은 위치의 문자가 같은지 비교
- 문자열의 길이를 넘어가거나 문자가 다르면 그 전까지를 반환
- 끝까지 모두 같으면 첫 번째 문자열 전체를 반환

### 코드

```kotlin
class Solution {
    fun longestCommonPrefix(strs: Array<String>): String {
        for (i in strs[0].indices) {
            for (str in strs) {
                if (i == str.length || str[i] != strs[0][i]) {
                    return strs[0].substring(0, i)
                }
            }
        }

        return strs[0]
    }
}
```

### 복잡도

- 시간복잡도: O (N × M)
    - N은 문자열의 개수, M은 첫 번째 문자열의 길이
    - 최악의 경우 모든 문자열의 문자를 끝까지 비교해야 함
- 공간복잡도: 모름

### 회고
