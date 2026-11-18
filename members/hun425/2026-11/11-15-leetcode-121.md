## [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

### 접근 방법

- 어떤 날 판다고 정하면, 그날의 최대 이익은 **그날 가격 - 이전 날들 중 최저가**
- 왼쪽부터 한 번 훑으면서 지금까지의 최저가를 갱신하고, 매일 그날 팔았을 때의 이익으로 최댓값을 갱신

### 코드

```kotlin
class Solution {
    fun maxProfit(prices: IntArray): Int {
        var minPrice = Int.MAX_VALUE
        var maxProfit = 0
        for (i in prices.indices) {
            val curPrice = prices[i]
            if (curPrice < minPrice) {
                minPrice = curPrice
            }
            maxProfit = maxOf(maxProfit, curPrice - minPrice)
        }
        return maxProfit
    }
}
```

### 복잡도

- 시간복잡도: $O(n)$
- 공간복잡도: $O(1)$

### 회고

- 처음엔 모든 쌍을 비교해서 시간 초과, 다음엔 전체 최저가에 사는 것만 봐서 `[2, 4, 1]` 같은 경우를 놓침
- 판 날을 기준으로 보면 이전 최저가 하나만 들고 다니면 된다는 걸 알게 됨
