## [2996. Smallest Missing Integer Greater Than Sequential Prefix Sum](https://leetcode.com/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/description/?envType=daily-question&envId=2026-08-11)

### 접근 방법

- 앞에서부터 '이전 값 + 1 == 현재 값'인 동안 계속 더해서 가장 긴 nums[0]부터 시작하는 가장 긴 연속된 수의 합을 구한다.
- 그 합부터 시작해서 nums에 없는 숫자가 나올 때 까지 1씩 더한다.

### 코드

```kotlin
class Solution {
    fun missingInteger(nums: IntArray): Int {
        var sum = nums[0]

        for (i in (1..<nums.size)) {
            if (nums[i] != nums[i - 1] + 1) break
            sum += nums[i]
        }

        val set = nums.toSet()

        while (sum in set) {
            sum++
        }
        return sum
    }
}
```

### 복잡도

- 시간복잡도: O (n)
- 공간복잡도: O (n)

### 회고

- 문제 설명이 좀 헷갈렸슴다. 중간부터 연속된 것도 포함되는 줄..