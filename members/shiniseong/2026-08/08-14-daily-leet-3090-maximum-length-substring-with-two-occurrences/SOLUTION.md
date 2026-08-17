## [3090. Maximum Length Substring With Two Occurrences](https://leetcode.com/problems/maximum-length-substring-with-two-occurrences/?envType=daily-question&envId=2026-08-14)

### 접근 방법

- 부분 문자열 안에서 각 문자는 최대 두 번만 나타나야 합니다.
- 오른쪽 포인터를 이동시키면서 각 문자의 등장 횟수를 세고, 등장 횟수가 2를 초과하면 왼쪽 포인터를 이동시켜 조건을 만족하도록 합니다.
- 부분 문자열 최대 길이를 갱신하면서 진행합니다.

### 코드

```kotlin
class Solution {
    fun maximumLengthSubstring(
        s: String,
    ): Int {
        val counts = IntArray(26)
        var left = 0
        var maxLength = 0

        for (right in s.indices) {
            val chIdx = s[right] - 'a'
            counts[chIdx]++

            while (counts[chIdx] > 2) {
                val leftChIdx = s[left] - 'a'
                counts[leftChIdx]--
                left++
            }

            maxLength = maxOf(maxLength, right - left + 1)
        }

        return maxLength
    }
}
```

### 복잡도

- 시간복잡도: O (n)
- 공간복잡도: O (1)

### 회고

- 전체 부분 문자열을 구해놓고 2넘는거 있는걸 없애고, 그중에 제일 긴걸 찾는 멍청한 방법으로 시도했다가 AI의 도움을 좀 받았습니다..
