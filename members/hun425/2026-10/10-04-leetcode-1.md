## [1. Two Sum](https://leetcode.com/problems/two-sum/)

### 접근 방법

- 두 수를 다 고르면 $O(n^2)$ → **하나를 고르면 나머지 하나(`target - num`)는 정해짐**
- 지나온 값들을 `값 → 인덱스`로 `HashMap`에 넣어두고, 현재 값의 짝이 이미 있으면 바로 반환
- 짝을 먼저 확인하고 나서 넣으니까 같은 원소를 두 번 쓰는 경우도 자연스럽게 막힘

### 코드

```kotlin
class Solution {
    fun twoSum(nums: IntArray, target: Int): IntArray {
        val seen = HashMap<Int, Int>()

        for ((i, num) in nums.withIndex()) {
            val j = seen[target - num]
            if (j != null) return intArrayOf(j, i)
            seen[num] = i
        }
        return intArrayOf()
    }
}
```

### 복잡도

- 시간복잡도: $O(n)$
- 공간복잡도: $O(n)$

### 회고

- 3Sum에서 "탐색할 개수를 줄이는 게 핵심"이었던 거랑 같은 맥락 — 2개 중 1개는 해시로 바로 찾기
