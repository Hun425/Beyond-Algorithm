## [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

### 접근 방법

- 가장 마지막에 열린 괄호가 가장 먼저 닫혀야 함 → **스택**
- 여는 괄호면 push, 닫는 괄호면 pop 해서 짝이 맞는지 확인
- 끝까지 돌았을 때 스택이 비어 있어야 유효

### 코드

```kotlin
class Solution {
    fun isValid(s: String): Boolean {
        val pair = mapOf(')' to '(', ']' to '[', '}' to '{')
        val stack = ArrayDeque<Char>()

        for (c in s) {
            if (c in pair) {
                if (stack.removeLastOrNull() != pair[c]) return false
            } else {
                stack.addLast(c)
            }
        }
        return stack.isEmpty()
    }
}
```

### 복잡도

- 시간복잡도: $O(n)$
- 공간복잡도: $O(n)$

### 회고

- 스택이 비었는데 닫는 괄호가 오는 경우를 `removeLastOrNull()` 하나로 같이 처리할 수 있어서 깔끔했다
