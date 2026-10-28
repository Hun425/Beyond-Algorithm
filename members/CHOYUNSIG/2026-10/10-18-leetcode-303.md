## [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/)

### 접근 방법

주어진 배열에서 어떤 구간의 합을 여러 번 구하는 문제이다. 매번 해당 구간을 순회하면서 더하면 한 번 질의할 때마다 $O(n)$ 시간이 필요하다.

배열의 값이 바뀌지 않으므로, 앞에서부터 더한 값을 미리 저장해두면 된다. 이것을 **누적 합(Prefix Sum)** 기법이라고 한다.

아이디어는 다음과 같다.

> 처음부터 어떤 위치까지의 합을 알고 있다면, 두 누적 합의 차이로 그 사이 구간의 합을 구할 수 있다.

`prefixSum[i]`를 배열의 처음부터 `i`개의 원소를 더한 값으로 정의한다. 원소를 하나도 더하지 않은 `prefixSum[0]`은 `0`이다.

1. 배열을 앞에서부터 순회하면서, 직전 누적 합에 현재 원소를 더해 `prefixSum`에 넣는다.
2. `left`부터 `right`까지의 합을 구하려면 `prefixSum[right + 1] - prefixSum[left]`를 계산한다.

예를 들어 `nums = [-2, 0, 3, -5, 2, -1]`이면 누적 합은 `[0, -2, -2, 1, -4, -2, -3]`이다. `sumRange(2, 5)`는 `prefixSum[6] - prefixSum[2] = -3 - (-2) = -1`로 구할 수 있다.

맨 앞에 `0`을 넣었기 때문에 `left = 0`인 경우에도 별도의 예외 처리가 필요하지 않다.

### 코드

```kotlin
class NumArray(nums: IntArray) {
    val prefixSum = run {
        val prefixSum = mutableListOf(0)

        for (num in nums) {
            prefixSum.add(num + prefixSum.last())
        }

        prefixSum
    }

    fun sumRange(left: Int, right: Int): Int {
        return prefixSum[right + 1] - prefixSum[left]
    }
}
```

### 복잡도

$n$이 `nums`의 길이이고, $q$가 `sumRange` 호출 횟수일 때,

- 시간복잡도: 누적 합을 만드는 데 $O(n)$, 각 구간 합 질의는 $O(1)$이므로 전체 $O(n + q)$
- 공간복잡도: 누적 합을 저장하기 위해 $O(n)$

### 회고

배열의 값이 바뀌지 않는다면 누적 합을 사용하여 구간 합을 간단하게 구할 수 있다. 값이 바뀌는 경우에는 어떻게 처리해야 할지 다음 문제와 비교해보면 좋겠습니다.
