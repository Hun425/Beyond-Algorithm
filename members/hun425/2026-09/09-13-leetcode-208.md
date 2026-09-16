## [208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)

### 접근 방법

- 노드마다 `children`(소문자 26개라 배열)과 `isEnd` 두 개만 들고 있음
- `insert`: 글자 따라 내려가다 자식 없으면 만들고, 마지막 노드에 `isEnd = true`
- `search`/`startsWith`는 순회가 같아서 `find` 하나로 뺌
  - `search` = 노드 있음 + `isEnd`
  - `startsWith` = 노드 있음

### 코드

```kotlin
class Trie() {
    private class Node {
        val children = arrayOfNulls<Node>(26)
        var isEnd = false
    }

    private val root = Node()

    fun insert(word: String) {
        var node = root
        for (c in word) {
            val i = c - 'a'
            node = node.children[i] ?: Node().also { node.children[i] = it }
        }
        node.isEnd = true
    }

    fun search(word: String): Boolean = find(word)?.isEnd == true

    fun startsWith(prefix: String): Boolean = find(prefix) != null

    private fun find(s: String): Node? {
        var node = root
        for (c in s) {
            node = node.children[c - 'a'] ?: return null
        }
        return node
    }
}
```

### 복잡도

- 시간복잡도: $O(L)$ — 세 연산 모두 문자열 길이만큼
- 공간복잡도: $O(\text{총 글자 수} \times 26)$

### 회고

- 결국 트리에 길 만들고 단어 끝에만 `true` 찍는 게 전부
