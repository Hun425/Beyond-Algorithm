## [Network Delay Time](https://leetcode.com/problems/network-delay-time/)

### 접근 방법

그래프라는 자료구조로 이루어진 네트워크 위에서 어떤 한 정점이 다른 모든 정점하고의 거리(시간)을 재어 가장 최댓값을 보면 되는 문제이다.

이것은 그래프 탐색 기법 중 **다익스트라 방법론**을 사용하는 전형적인 문제이다.

다익스트라 방법론이 이 문제를 푸는 아이디어는 다음과 같다.

> 접근 가능한 정점을 탐색하면서 최소 거리를 하나씩 확정한다.

우선 최소 거리가 확정된 정점의 집합 $V$를 만든다. 시작 정점이 주어지면 $V$에 시작 정점을 넣고 다음 루프를 반복한다.

1. $V$ 바로 접근 가능한 다른 정점들의 거리를 계산해본다.
2. 그 정점들 중 가장 거리가 짧은 정점을 고르면, 그 정점까지의 최단거리가 현재 구한 최단거리보다 짧아질 수 없음을 확정할 수 있다.
3. 확정된 그 정점을 $V$에 넣는다.

이 과정을 더이상 $V$의 크기를 늘릴 수 없을때까지 반복한다.

### 코드

```kotlin
class Solution {
    companion object {
        private const val INF = 1_000_000_000
    }

    fun networkDelayTime(times: Array<IntArray>, n: Int, k: Int): Int {
        val edges = List(n) { mutableListOf<Pair<Int, Int>>() }.apply {
            times.forEach {
                val (u, v, w) = it
                this[u - 1].add(v - 1 to w)
            }
        }

        val minimumTimes = List(n) { INF }.toMutableList()
        val searchQueue = java.util.PriorityQueue<GraphSearchInfo>()

        searchQueue.add(GraphSearchInfo(nodeIndex = k - 1, accumulatedCost = 0))
        minimumTimes[k - 1] = 0

        while (searchQueue.isNotEmpty()) {
            val info = searchQueue.poll() ?: break
            if (minimumTimes[info.nodeIndex] < info.accumulatedCost) continue

            for ((nextNodeIndex, cost) in edges[info.nodeIndex]) {
                val currentMinimumTime = minimumTimes[nextNodeIndex]
                val newMinimumTime = info.accumulatedCost + cost

                if (currentMinimumTime <= newMinimumTime) continue
                minimumTimes[nextNodeIndex] = newMinimumTime
                searchQueue.add(GraphSearchInfo(nodeIndex = nextNodeIndex, accumulatedCost = newMinimumTime))
            }
        }

        return minimumTimes
            .max()
            .takeIf { it < INF } ?: -1
    }

    private data class GraphSearchInfo(
        val nodeIndex: Int,
        val accumulatedCost: Int,
    ) : Comparable<GraphSearchInfo> {
        override fun compareTo(other: GraphSearchInfo): Int {
            return accumulatedCost.compareTo(other.accumulatedCost)
        }
    }
}
```

### 복잡도

- 시간복잡도: 다익스트라 알고리즘 구현법은 여러 종류가 있으며, 현재 코드는 Priority Queue 기법을 사용해 최적화하여 $O((N + E)\log{N})$ 시간복잡도를 가진다. 이 문제는 $O(n^2)$ 방법론이 통과하므로, 해당 방법도 정답이다.
- 공간복잡도: $O(N + E)$

### 회고

인터넷에서 다익스트라 알고리즘을 찾아보는 것을 추천합니다.
이 문제가 어려운지에 대해 의견을 남겨주세요.