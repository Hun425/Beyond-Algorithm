package y2026m07.m07d08DailyLeet3756ConcatenateNonZeroDigitsAndMultiplyBySum2

import kotlin.test.Test
import kotlin.test.assertEquals

class SolutionTest {
    private val solution = Solution()

    @Test
    fun example1() {
        // given
        val s = "10203004"
        val queries = arrayOf(
            intArrayOf(0, 7),
            intArrayOf(1, 3),
            intArrayOf(4, 6),
        )

        // when
        val actual = solution.sumAndMultiply(
            s = s,
            queries = queries,
        )

        // then
        val expected = intArrayOf(12340, 4, 9)
        assertEquals(expected.joinToString(), actual.joinToString())
    }

    @Test
    fun example2() {
        // given
        val s = "1000"
        val queries = arrayOf(
            intArrayOf(0, 3),
            intArrayOf(1, 1),
        )

        // when
        val actual = solution.sumAndMultiply(
            s = s,
            queries = queries,
        )

        // then
        val expected = intArrayOf(1, 0)
        assertEquals(expected.joinToString(), actual.joinToString())
    }

    @Test
    fun example3() {
        // given
        val s = "9876543210"
        val queries = arrayOf(
            intArrayOf(0, 9),
        )

        // when
        val actual = solution.sumAndMultiply(
            s = s,
            queries = queries,
        )

        // then
        val expected = intArrayOf(444444137)
        assertEquals(expected.joinToString(), actual.joinToString())
    }

    @Test
    fun edge1() {
        // given
        val s = "0000000"
        val queries = arrayOf(
            intArrayOf(0, 6),
        )

        // when
        val actual = solution.sumAndMultiply(
            s = s,
            queries = queries,
        )

        // then
        val expected = intArrayOf(0)
        assertEquals(expected.joinToString(), actual.joinToString())
    }

    @Test
    fun exception1() {
        // given
        val s = "941983443"
        val queries = arrayOf(
            intArrayOf(1, 8)
        )

        // when
        val actual = solution.sumAndMultiply(
            s = s,
            queries = queries,
        )

        // then
        val expected = intArrayOf(511403941)
        assertEquals(expected.joinToString(), actual.joinToString())
    }

    @Test
    fun exception2() {
        // given
        val s = "9223538386222334255"
        val queries = arrayOf(
            intArrayOf(0, 18)
        )

        // when
        val actual = solution.sumAndMultiply(
            s = s,
            queries = queries,
        )

        // then
        val expected = intArrayOf(632582266)
        assertEquals(expected.joinToString(), actual.joinToString())
    }
}
