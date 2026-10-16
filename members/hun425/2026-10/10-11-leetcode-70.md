## [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)

### 접근 방법

- 마지막 걸음이 1칸 아니면 2칸이라 `f(n) = f(n-1) + f(n-2)`
- 직전 두 값만 있으면 돼서 변수 두 개로 처리

### 코드

```kotlin
class Solution {
    fun climbStairs(n: Int): Int {
        var prev = 1 // f(0)
        var curr = 1 // f(1)

        repeat(n - 1) {
            val next = prev + curr
            prev = curr
            curr = next
        }
        return curr
    }
}
```

### 복잡도

- 시간복잡도: $O(n)$
- 공간복잡도: $O(1)$

### 회고

- 그냥 피보나치임
