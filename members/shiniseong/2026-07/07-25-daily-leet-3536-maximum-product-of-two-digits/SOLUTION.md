## [3536. Maximum Product of Two Digits](https://leetcode.com/problems/maximum-product-of-two-digits/description/?envType=daily-question&envId=2026-07-25)

### 접근 방법

- 주어진 숫자의 각 자릿수 숫자 배열로 만듭니다.
- 내림차순 정렬 후 앞의 두 숫자를 곱하면 됩니다.

### 코드

```kotlin
class Solution {
    fun maxProduct(n: Int): Int {
        val nums = n.toString()
            .map { it.digitToInt() }
            .sortedDescending()
            .toMutableList()

        val max1 = nums.first()
        nums.removeFirst()
        val max2 = nums.first()

        return max1 * max2
    }
}
```

### 복잡도

- 시간복잡도: O (n)
- 공간복잡도: 모르겠음

### 회고

- 이지헌터가되어버려 죄송합니다.. 이지 굿 이지 짱