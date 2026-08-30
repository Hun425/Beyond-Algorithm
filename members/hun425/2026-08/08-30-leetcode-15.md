## [15. 3Sum](https://leetcode.com/problems/3sum/)

### 접근 방법

- 세 수를 모두 탐색하면 $O(n^3)$ 이라 $n = 3000$ 에서 터짐 → **탐색 할 숫자 개수를 3에서 2로 줄이는 게 핵심**
- 2개 고르고 1개는 이진탐색으로 결정

### 코드

```kotlin
class Solution {
    fun threeSum(nums: IntArray): List<List<Int>> {
        nums.sort()
        val result = HashSet<List<Int>>()

        for (i in 0 until nums.size - 2) {
            for (j in i + 1 until nums.size - 1) {
                val target = -(nums[i] + nums[j])
                val k = binarySearch(nums, j + 1, nums.size - 1, target)
                if (k != -1) {
                    result.add(listOf(nums[i], nums[j], nums[k]))
                }
            }
        }
        return result.toList()
    }

    private fun binarySearch(nums: IntArray, from: Int, to: Int, target: Int): Int {
        var low = from
        var high = to
        while (low <= high) {
            val mid = (low + high) / 2
            when {
                nums[mid] == target -> return mid
                nums[mid] < target -> low = mid + 1
                else -> high = mid - 1
            }
        }
        return -1
    }
}
```

### 복잡도

- 시간복잡도: $O(n^2 \log n)$ 
- 공간복잡도: $O(k)$ 

### 회고

- 근데 더 좋은 방법이 있을거 같긴 함
