package y2026m07.m07d07DailyLeet3754ConcatenateNonZeroDigitsAndMultiplyBySum1

import kotlin.test.Test
import kotlin.test.assertEquals

class SolutionTest {
    private val solution = Solution()

    @Test
    fun example1() {
        // given
        val n = 10203004

        // when
        val actual = solution.sumAndMultiply(n)

        // then
        val expected = 12340L
        assertEquals(expected, actual)
    }

    @Test
    fun example2() {
        // given
        val n = 1000

        // when
        val actual = solution.sumAndMultiply(n)

        // then
        val expected = 1L
        assertEquals(expected, actual)
    }

    @Test
    fun edge1() {
        // given
        val n = 0

        // when
        val actual = solution.sumAndMultiply(n)

        // then
        val expected = 0L
        assertEquals(expected, actual)
    }
}
