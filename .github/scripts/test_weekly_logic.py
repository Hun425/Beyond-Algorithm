import datetime
import unittest

import weekly_logic as wl

KST = wl.KST
WEEK_END = datetime.date(2026, 9, 6)


def dt(s):
    return datetime.datetime.fromisoformat(s).replace(tzinfo=KST)


def pr(number, author, created, entries, slugs=(), labels=(), reviews=(), title=""):
    return wl.PR(
        number=number,
        author=author,
        created=dt(created),
        entries=set(entries),
        slugs=set(slugs),
        labels=set(labels),
        reviews=[(a, dt(t)) for a, t in reviews],
        title=title,
        url=f"https://example/pull/{number}",
    )


class WeekRange(unittest.TestCase):
    def test_wednesday_run_reports_previous_mon_to_sun(self):
        start, end = wl.week_range(datetime.date(2026, 9, 9))  # Wed
        self.assertEqual((start, end), (datetime.date(2026, 8, 31), datetime.date(2026, 9, 6)))

    def test_review_deadline_is_tuesday_end_of_day(self):
        _, end = wl.week_range(datetime.date(2026, 9, 9))
        self.assertEqual(wl.review_deadline(end), dt("2026-09-08T23:59:59.999999"))

    def test_submit_deadline_is_sunday_end_of_day(self):
        _, end = wl.week_range(datetime.date(2026, 9, 9))
        self.assertEqual(wl.submit_deadline(end), dt("2026-09-06T23:59:59.999999"))


class Slugs(unittest.TestCase):
    def test_extract_slug_from_url_with_suffix(self):
        text = "## [3718](https://leetcode.com/problems/smallest-missing-multiple-of-k/description/?envType=daily)"
        self.assertEqual(wl.extract_slugs(text), {"smallest-missing-multiple-of-k"})

    def test_extract_slug_none(self):
        self.assertEqual(wl.extract_slugs("no link here"), set())

    def test_slugify_title(self):
        self.assertEqual(wl.slugify("[2026-09-06] Implement Trie (Prefix Tree) - hun425"), "implement-trie-prefix-tree")
        self.assertEqual(wl.slugify("[2026-08-30] 3Sum - CHOYUNSIG"), "3sum")


class Members(unittest.TestCase):
    def test_login_matches_folder_case_insensitively(self):
        members = ["CHOYUNSIG", "hun425", "shiniseong"]
        self.assertEqual(wl.member_key("Hun425", members), "hun425")
        self.assertEqual(wl.member_key("choyunsig", members), "CHOYUNSIG")
        self.assertIsNone(wl.member_key("someone", members))

    def test_solution_entries_only_under_own_folder(self):
        files = [
            "members/hun425/2026-09/09-06-leetcode-208.md",
            "members/hun425/2026-09/09-07-leetcode-1/main.kt",
            "members/hun425/2026-09/09-07-leetcode-1/SOLUTION.md",
            "members/other/2026-09/09-06-x.md",
            "README.md",
        ]
        self.assertEqual(
            wl.solution_entries(files, "hun425"),
            {"2026-09/09-06-leetcode-208.md", "2026-09/09-07-leetcode-1"},
        )


class JudgeSolving(unittest.TestCase):
    def test_common_problem_solved(self):
        prs = [pr(1, "hun425", "2026-09-06T21:00", ["2026-09/09-06-a.md"], slugs=["implement-trie-prefix-tree"])]
        r = wl.judge_solving("hun425", prs, common_slug="implement-trie-prefix-tree", prev_common_slug=None, prev_prs=[], week_end=WEEK_END)
        self.assertTrue(r.met)
        self.assertEqual(r.how, "common")
        self.assertEqual(r.count, 1)

    def test_two_free_problems(self):
        prs = [
            pr(1, "hun425", "2026-09-05T21:00", ["2026-09/09-05-a.md"], slugs=["a"]),
            pr(2, "hun425", "2026-09-06T21:00", ["2026-09/09-06-b.md"], slugs=["b"]),
        ]
        r = wl.judge_solving("hun425", prs, "common", None, [], week_end=WEEK_END)
        self.assertTrue(r.met)
        self.assertEqual(r.how, "free")
        self.assertEqual(r.count, 2)

    def test_one_free_problem_is_unmet(self):
        prs = [pr(1, "hun425", "2026-09-05T21:00", ["2026-09/09-05-a.md"], slugs=["a"])]
        r = wl.judge_solving("hun425", prs, "common", None, [], week_end=WEEK_END)
        self.assertFalse(r.met)
        self.assertEqual(r.count, 1)

    def test_nothing_submitted(self):
        r = wl.judge_solving("hun425", [], "common", None, [], week_end=WEEK_END)
        self.assertFalse(r.met)
        self.assertEqual(r.count, 0)

    def test_help_retry_of_previous_common_counts(self):
        prev = [pr(1, "hun425", "2026-08-30T21:00", ["2026-08/08-30-x.md"], slugs=["3sum"], labels=["HELP"])]
        prs = [pr(2, "hun425", "2026-09-06T21:00", ["2026-09/09-06-x.md"], slugs=["3sum"])]
        r = wl.judge_solving("hun425", prs, common_slug="trie", prev_common_slug="3sum", prev_prs=prev, week_end=WEEK_END)
        self.assertTrue(r.met)
        self.assertEqual(r.how, "retry")

    def test_help_with_failed_together_still_allows_retry(self):
        prev = [pr(1, "hun425", "2026-08-30T21:00", ["2026-08/08-30-x.md"], slugs=["3sum"], labels=["FAILED", "HELP"])]
        prs = [pr(2, "hun425", "2026-09-06T21:00", ["2026-09/09-06-x.md"], slugs=["3sum"])]
        r = wl.judge_solving("hun425", prs, "trie", "3sum", prev, week_end=WEEK_END)
        self.assertTrue(r.met)
        self.assertEqual(r.how, "retry")

    def test_failed_label_does_not_allow_retry(self):
        prev = [pr(1, "hun425", "2026-08-30T21:00", ["2026-08/08-30-x.md"], slugs=["3sum"], labels=["FAILED"])]
        prs = [pr(2, "hun425", "2026-09-06T21:00", ["2026-09/09-06-x.md"], slugs=["3sum"])]
        r = wl.judge_solving("hun425", prs, "trie", "3sum", prev, week_end=WEEK_END)
        self.assertFalse(r.met)

    def test_retry_requires_own_previous_help_pr(self):
        prev = [pr(1, "other", "2026-08-30T21:00", ["2026-08/08-30-x.md"], slugs=["3sum"], labels=["HELP"])]
        prs = [pr(2, "hun425", "2026-09-06T21:00", ["2026-09/09-06-x.md"], slugs=["3sum"])]
        r = wl.judge_solving("hun425", prs, "trie", "3sum", prev, week_end=WEEK_END)
        self.assertFalse(r.met)

    def test_pr_after_sunday_deadline_ignored(self):
        prs = [pr(1, "hun425", "2026-09-07T00:10", ["2026-09/09-07-a.md"], slugs=["trie"])]
        r = wl.judge_solving("hun425", prs, "trie", None, [], week_end=WEEK_END)
        self.assertFalse(r.met)
        self.assertEqual(r.count, 0)

    def test_other_members_prs_ignored(self):
        prs = [pr(1, "other", "2026-09-06T21:00", ["2026-09/09-06-a.md"], slugs=["trie"])]
        r = wl.judge_solving("hun425", prs, "trie", None, [], week_end=WEEK_END)
        self.assertFalse(r.met)

    def test_slug_fallback_to_title(self):
        prs = [pr(1, "hun425", "2026-09-06T21:00", ["2026-09/09-06-a.md"], title="[2026-09-06] Implement Trie (Prefix Tree) - hun425")]
        r = wl.judge_solving("hun425", prs, "implement-trie-prefix-tree", None, [], week_end=WEEK_END)
        self.assertTrue(r.met)


class JudgeReview(unittest.TestCase):
    def setUp(self):
        self.prs = [
            pr(1, "a", "2026-09-05T10:00", ["2026-09/09-05-x.md"], reviews=[("b", "2026-09-06T10:00"), ("c", "2026-09-09T00:30")]),
            pr(2, "b", "2026-09-06T10:00", ["2026-09/09-06-y.md"], reviews=[("a", "2026-09-08T23:00")]),
            pr(3, "c", "2026-09-07T10:00", ["2026-09/09-07-z.md"], reviews=[("a", "2026-09-07T11:00")]),  # after Sunday: not in scope
        ]

    def test_reviewed_all_before_deadline(self):
        r = wl.judge_review("a", self.prs, WEEK_END)
        self.assertEqual((r.done, r.total), (1, 1))
        self.assertTrue(r.met)

    def test_late_review_does_not_count(self):
        r = wl.judge_review("c", self.prs, WEEK_END)
        self.assertEqual((r.done, r.total), (0, 2))
        self.assertFalse(r.met)

    def test_own_pr_excluded(self):
        r = wl.judge_review("b", self.prs, WEEK_END)
        self.assertEqual((r.done, r.total), (1, 1))
        self.assertTrue(r.met)

    def test_no_prs_to_review_is_met(self):
        r = wl.judge_review("a", [], WEEK_END)
        self.assertEqual((r.done, r.total), (0, 0))
        self.assertTrue(r.met)

    def test_login_case_insensitive(self):
        prs = [pr(1, "a", "2026-09-05T10:00", ["2026-09/09-05-x.md"], reviews=[("B", "2026-09-06T10:00")])]
        self.assertTrue(wl.judge_review("b", prs, WEEK_END).met)


class Warnings(unittest.TestCase):
    def test_increment_unmet(self):
        state = {"as_of": "old", "counts": {"a": 1, "b": 0}}
        new = wl.apply_warnings(state, "new", unmet={"a", "b"}, coffee_paid=set(), members=["a", "b"])
        self.assertEqual(new["counts"], {"a": 2, "b": 1})
        self.assertEqual(new["as_of"], "new")

    def test_coffee_resets_before_increment(self):
        state = {"as_of": "old", "counts": {"a": 2}}
        new = wl.apply_warnings(state, "new", unmet={"a"}, coffee_paid={"a"}, members=["a"])
        self.assertEqual(new["counts"], {"a": 1})

    def test_rerun_same_week_is_idempotent(self):
        state = {"as_of": "old", "counts": {"a": 0}}
        once = wl.apply_warnings(state, "new", unmet={"a"}, coffee_paid=set(), members=["a"])
        twice = wl.apply_warnings(once, "new", unmet={"a"}, coffee_paid=set(), members=["a"])
        self.assertEqual(twice["counts"], {"a": 1})

    def test_new_member_starts_at_zero(self):
        new = wl.apply_warnings({}, "new", unmet=set(), coffee_paid=set(), members=["z"])
        self.assertEqual(new["counts"], {"z": 0})


class CoffeeParsing(unittest.TestCase):
    def test_checked_boxes_only(self):
        body = (
            "- [x] **a** 커피 샀음 <!-- coffee:a -->\n"
            "- [ ] **b** 커피 샀음 <!-- coffee:b -->\n"
            "- [X] **c** 커피 샀음 <!-- coffee:c -->\n"
        )
        self.assertEqual(wl.parse_coffee_checks(body), {"a", "c"})

    def test_no_section(self):
        self.assertEqual(wl.parse_coffee_checks("hello"), set())


if __name__ == "__main__":
    unittest.main()


class Excuses(unittest.TestCase):
    WEEK = (datetime.date(2026, 9, 7), datetime.date(2026, 9, 13))

    def test_overlapping_range_excuses_member(self):
        excuses = [{"member": "hun425", "from": "2026-09-12", "to": "2026-09-12", "reason": "결혼식"}]
        self.assertEqual(wl.excused_members(excuses, *self.WEEK), {"hun425": "결혼식"})

    def test_multi_week_range_covers_each_week(self):
        excuses = [{"member": "hun425", "from": "2026-09-07", "to": "2026-09-20", "reason": "출장"}]
        self.assertIn("hun425", wl.excused_members(excuses, *self.WEEK))
        self.assertIn("hun425", wl.excused_members(excuses, datetime.date(2026, 9, 14), datetime.date(2026, 9, 20)))
        self.assertEqual(wl.excused_members(excuses, datetime.date(2026, 9, 21), datetime.date(2026, 9, 27)), {})

    def test_non_overlapping_range_ignored(self):
        excuses = [{"member": "hun425", "from": "2026-09-01", "to": "2026-09-06", "reason": "x"}]
        self.assertEqual(wl.excused_members(excuses, *self.WEEK), {})

    def test_member_name_case_insensitive_and_reason_optional(self):
        excuses = [{"member": "Hun425", "from": "2026-09-10", "to": "2026-09-10"}]
        self.assertEqual(wl.excused_members(excuses, *self.WEEK, members=["hun425"]), {"hun425": ""})

    def test_malformed_entry_skipped(self):
        excuses = [{"member": "hun425", "from": "not-a-date", "to": "2026-09-10"}, {"member": "a"}]
        self.assertEqual(wl.excused_members(excuses, *self.WEEK), {})


class ExcusePRReview(unittest.TestCase):
    def test_excuse_pr_is_a_review_target(self):
        prs = [wl.PR(number=1, author="a", created=dt("2026-09-05T10:00"), entries=set(), is_excuse=True)]
        r = wl.judge_review("b", prs, WEEK_END)
        self.assertEqual((r.done, r.total), (0, 1))
        self.assertFalse(r.met)

    def test_excuse_pr_reviewed_in_time(self):
        prs = [wl.PR(number=1, author="a", created=dt("2026-09-05T10:00"), entries=set(), is_excuse=True,
                     reviews=[("b", dt("2026-09-06T10:00"))])]
        self.assertTrue(wl.judge_review("b", prs, WEEK_END).met)

    def test_excuse_pr_not_counted_as_solution(self):
        prs = [wl.PR(number=1, author="a", created=dt("2026-09-05T10:00"), entries=set(), is_excuse=True)]
        r = wl.judge_solving("a", prs, "x", None, [], week_end=WEEK_END)
        self.assertEqual(r.count, 0)
        self.assertFalse(r.met)

    def test_is_excuse_pr_by_files(self):
        self.assertTrue(wl.is_excuse_pr([".github/excuses.json"]))
        self.assertFalse(wl.is_excuse_pr(["members/a/2026-09/09-05-x.md"]))
