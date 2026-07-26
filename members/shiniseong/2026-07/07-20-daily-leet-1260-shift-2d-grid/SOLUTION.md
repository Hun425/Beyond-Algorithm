## [1260. Shift 2D Grid](https://leetcode.com/problems/shift-2d-grid/description/?envType=daily-question&envId=2026-07-20)

### 접근 방법

- 1차원 배열을 잘라서 배치하면 2차원 배열이 되기 때문에 1차원 배열로 생각하고 풀어야 합니다.
- 주어진 배열의 요소 수 만큼 밀면 제자리로 돌아오기 때문에 k % m * n 연산을해서 결과적으로 몇 번 밀어야 되는지 구합니다.
- 나머지 연산을 이용하면 total을 넘어갈 때 순환시킬 수 있습니다.
- 1차원 인덱스를 2차원 행 열로 변환하여 결과값배열에 집어넣습니다.

### 코드

```kotlin
class Solution {
    fun shiftGrid(
        grid: Array<IntArray>,
        k: Int,
    ): List<List<Int>> {
        val m = grid.size
        val n = grid.first().size
        val total = m * n

        val shiftCount = k % total

        val result = Array(m) {
            IntArray(n)
        }

        (0..<m).forEach { y ->
            (0..<n).forEach { x ->
                val currIdx = (y * n) + x
                val shiftedIdx = (currIdx + shiftCount) % total

                val shiftedY = shiftedIdx / n
                val shiftedX = shiftedIdx % n

                result[shiftedY][shiftedX] = grid[y][x]
            }
        }

        return result.map { row ->
            row.toList()
        }
    }
}
```

### 복잡도

- 시간복잡도: O (m * n) = O (n^2)
- 공간복잡도: 모르겠음

### 회고

- 순환하는 로직을 풀때는 나머지 연산이 활용 가능한지 고려합니다.
    - ex. 달팽이 숫자 배열 (https://shin-e-dog.tistory.com/24)
