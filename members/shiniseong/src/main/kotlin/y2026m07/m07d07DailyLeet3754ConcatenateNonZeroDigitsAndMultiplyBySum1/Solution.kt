package y2026m07.m07d07DailyLeet3754ConcatenateNonZeroDigitsAndMultiplyBySum1

class Solution {
    fun sumAndMultiply(n: Int): Long {
        val nonZeroDigits = n
            .toString()
            .filter { it != '0' }
            .map { it.digitToInt() }

        val x = nonZeroDigits
            .joinToString("")
            .ifEmpty { "0" }
            .toLong()

        val sum = nonZeroDigits.sum()

        return x * sum
    }
}
