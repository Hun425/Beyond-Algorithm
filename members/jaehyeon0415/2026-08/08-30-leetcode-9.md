## [9. Palindrome Number](https://leetcode.com/problems/palindrome-number/)

### 접근 방법

- 뒤집은 숫자와 원본이 같으면 팰린드롬

### 코드

```dart
class Solution {
  bool isPalindrome(int x) {
    int number = x;
    int reversed = 0;

    while (number > 0) {
      reversed = reversed * 10 + number % 10;
      number ~/= 10;
    }

    return x == reversed;
  }
}
```

### 복잡도

- 시간복잡도: ?
- 공간복잡도: O(1)

### 회고

- 문자열로 변환하지 않고 나머지와 몫 연산만으로 숫자를 뒤집을 수 있음
