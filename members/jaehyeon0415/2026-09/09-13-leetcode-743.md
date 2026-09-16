## [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/description/)

### 접근 방법

- 모든 간선들의 경로에 가중치가 있고 최단거리와 관련있다 생각해서 다익스트라로 접근

### 코드

```dart
class Solution {
  int networkDelayTime(List<List<int>> times, int n, int k) {
    int answer = -1;

    // 배열
    final List<List<int>> graph = List.generate(
      n + 1,
      (_) => List<int>.filled(n + 1, 0),
    );

    // times 토대로 초기화
    for (final time in times) {
      graph[time[0]][time[1]] = time[2];
    }

    // TODO: 다익스트라 구현
  }
}
```

### 복잡도

- 시간복잡도:
- 공간복잡도:

### 회고

- 개념 재학습 후 직접 구현해보기
