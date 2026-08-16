## [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)

### 접근 방법

만약 $k$ 값이 너무 크면 굉장히 짧은 시간 내로 바나나를 모두 먹어치울 것이고, 너무 작으면 `h` 시간 내로 바나나를 전부 먹지 못할 것이다. 즉 적절한 $k$ 값을 수직선 위에 찍는다고 하면, 그 값의 왼쪽으로는 `h` 시간 내로 바나나를 먹지 못하고, 오른쪽으로는 바나나를 모두 먹어치울 수 있다. 바로 그 지점이 이 문제의 정답이다.

이렇게 **단조적인 구간 특성**을 지니는 변수 공간에서 어떤 조건을 만족하는 특정 값을 찾을 땐 **이분 탐색**을 사용하여 구할 수 있다.

이분 탐색의 절차는 다음과 같다.

1. 우선 정답이 될 수 있는 $k$ 값의 범위는 $10^{10}$을 넘지 않을 것임이 자명하다. 따라서 우리는 정답 값을 탐색할 범위를 $1 \leq k \leq 10^{10}$의 범위로 잡는다. ($l = 1$, $r = 10^{10}$)
2. 우리가 찾고자 하는 범위 $l \leq k \leq r$에 대해서, $l$과 $r$의 중간 값인 $m = \frac{l + r}{2}$를 찍어본다. 만약 $k = m$이라면 $h$ 시간 내로 바나나를 다 먹을 수 있는지를 계산해본다.
3. 만약 바나나를 다 먹을 수 있다면 우리는 $k$ 값으로 $m$보다 작은 값을 시도해볼 수 있다. 만약 바나나를 다 못 먹는다면 우리는 $k$ 값을 $m$보다 크게 잡아야 한다. 따라서, 우리는 다음 탐색 구간을 $m$값을 기준으로 왼쪽을 탐색할지($r = m$) 오른쪽을 탐색할지($l = m$)를 결정할 수 있다.
4. 2~3 과정을 $l$과 $r$이 만날때까지 수행한다.

### 코드

```kotlin
import kotlin.math.min

class Solution {
    fun minEatingSpeed(piles: IntArray, h: Int): Int {
        var s = 1L
        var e = 10_000_000_000L

        while (s <= e) {
            val m = (s + e) / 2
            val hours = getCompleteHours(piles, m)

            if (hours > h) {
                s = m + 1
            } else {
                e = m - 1
            }
        }

        return s.toInt()
    }

    fun getCompleteHours(piles: IntArray, k: Long): Long {
        return piles.sumOf { it / k + min(it % k, 1) }
    }
}
```

### 복잡도

- 시간복잡도: $O(n\log{|k|})$, 단 $|k|$는 가능한 $k$ 값의 범위 크기
- 공간복잡도: 입력의 크기에 의해, $O(n)$

### 회고

해당 문제가 어려운지를 남겨주세요.