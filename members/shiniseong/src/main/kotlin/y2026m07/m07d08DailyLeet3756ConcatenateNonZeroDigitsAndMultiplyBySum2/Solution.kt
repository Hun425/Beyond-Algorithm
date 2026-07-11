package y2026m07.m07d08DailyLeet3756ConcatenateNonZeroDigitsAndMultiplyBySum2

class Solution {
    fun sumAndMultiply(
        s: String,
        queries: Array<IntArray>,
    ): IntArray = queries.map { query ->
        val start = query[0]
        val end = query[1] + 1

        val substring = s.substring(start, end)
        sumAndMultiPlyNonZero(substring)
    }
        .toTypedArray()
        .toIntArray()

    private fun sumAndMultiPlyNonZero(nString: String): Int {
        val nonZeroDigits = nString
            .filter { it != '0' }
            .map { it.digitToInt() }

        val x = nonZeroDigits
            .joinToString("")
            .ifEmpty { "0" }
            .toBigInteger()

        val sum = nonZeroDigits.sum()

        val result = x * sum.toBigInteger()

        return (result % MOD.toBigInteger()).toInt()
    }

    companion object {
        private const val MOD = 1_000_000_000 + 7
    }
}
