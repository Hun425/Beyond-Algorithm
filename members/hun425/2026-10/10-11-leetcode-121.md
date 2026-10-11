## [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

### 접근 방법

- 파는 날 기준으로 보면 그 전까지 최저가에 샀어야 함
- `minPrice` 들고 다니면서 `price - minPrice` 최댓값 갱신

### 코드

```kotlin
class Solution {
    fun maxProfit(prices: IntArray): Int {
        var minPrice = Int.MAX_VALUE
        var maxProfit = 0

        for (price in prices) {
            minPrice = minOf(minPrice, price)
            maxProfit = maxOf(maxProfit, price - minPrice)
        }
        return maxProfit
    }
}
```

### 복잡도

- 시간복잡도: $O(n)$
- 공간복잡도: $O(1)$

### 회고

- 최솟값 하나만 들고 다니면 끝
