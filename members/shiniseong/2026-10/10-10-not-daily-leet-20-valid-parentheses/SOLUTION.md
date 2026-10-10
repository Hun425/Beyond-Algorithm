## [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

### 접근 방법

- 괄호는 가장 나중에 열린 괄호부터 닫혀야 함
- 따라서 마지막에 넣은 값을 먼저 꺼내는 스택을 사용
- 여는 괄호가 나오면 스택에 추가
- 닫는 괄호가 나오면 스택의 마지막 괄호와 짝이 맞는지 확인
- 스택이 비어 있거나 짝이 맞지 않으면 false 반환
- 모든 문자를 확인한 후 스택이 비어 있으면 true 반환

### 코드

```
class Solution {
    fun isValid(s: String): Boolean {
        val stack = mutableListOf<Char>()

        s.forEach { char ->
            if (char.isOpen()) {
                stack.add(char)
            } else if (stack.isEmpty() || stack.removeAt(stack.lastIndex) != PAIRS[char]) {
                return false
            }
        }

        return stack.isEmpty()
    }

    private fun Char.isOpen(): Boolean = this in OPENS

    companion object {
        private val OPENS = setOf('(', '{', '[')
        private val PAIRS = mapOf(')' to '(', '}' to '{', ']' to '[')
    }
}
```

### 복잡도

- 시간복잡도: O (N)
    - N은 문자열의 길이
    - 문자열을 처음부터 끝까지 한 번만 순회
    - 스택의 마지막 요소를 추가하거나 제거하는 작업은 O (1)
- 공간복잡도: O (N)
    - 최악의 경우 모든 문자가 여는 괄호일 때 스택에 저장

### 회고

- 