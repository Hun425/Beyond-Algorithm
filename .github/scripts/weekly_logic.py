"""주간 리포트 판정 로직 (순수 함수, GitHub API 호출 없음).

이행 기준 (둘 중 하나):
  1. 그 주 공통 문제를 풀었다 (또는 직전 주 공통 문제를 HELP 라벨로 냈고 이번 주에 다시 풀었다)
  2. 자유 문제를 2개 이상 풀었다
리뷰 기준: 그 주 다른 멤버의 풀이 PR 전부에 화요일 23:59 KST까지 리뷰를 남겼다
경고: 풀이/리뷰 중 하나라도 미이행이면 그 주 1회 누적. 커피 체크 시 0회로 초기화.
"""
import copy
import datetime
import re
from dataclasses import dataclass, field

KST = datetime.timezone(datetime.timedelta(hours=9))
FREE_GOAL = 2
RETRY_LABEL = "HELP"
COFFEE_THRESHOLD = 2
END_OF_DAY = datetime.time(23, 59, 59, 999999)


@dataclass
class PR:
    number: int
    author: str  # members/ 폴더 이름으로 정규화된 값
    created: datetime.datetime  # KST
    entries: set  # 본인 폴더 아래 풀이 항목 ("YYYY-MM/entry")
    slugs: set = field(default_factory=set)  # 풀이 파일에서 찾은 leetcode slug
    labels: set = field(default_factory=set)
    reviews: list = field(default_factory=list)  # [(login, submitted KST)]
    title: str = ""
    url: str = ""
    files: list = field(default_factory=list)  # PR이 건드린 전체 경로


@dataclass
class SolveResult:
    count: int
    met: bool
    how: str  # "common" | "retry" | "free" | "none"
    prs: list


@dataclass
class ReviewResult:
    done: int
    total: int
    met: bool
    missed: list  # 리뷰하지 않은 PR 목록


# ---------- 날짜 ----------

def week_range(today):
    """수요일 실행 기준 직전 월~일."""
    this_monday = today - datetime.timedelta(days=today.weekday())
    return this_monday - datetime.timedelta(days=7), this_monday - datetime.timedelta(days=1)


def submit_deadline(week_end):
    return datetime.datetime.combine(week_end, END_OF_DAY, tzinfo=KST)


def review_deadline(week_end):
    return datetime.datetime.combine(week_end + datetime.timedelta(days=2), END_OF_DAY, tzinfo=KST)


def to_kst(iso):
    return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(KST)


# ---------- slug ----------

SLUG_RE = re.compile(r"leetcode\.com/problems/([a-z0-9-]+)")


def extract_slugs(text):
    return set(SLUG_RE.findall(text or ""))


def slugify(title):
    """PR 제목 '[YYYY-MM-DD] 문제명 - id' 에서 문제명을 slug 형태로 변환 (본문에 링크가 없을 때의 대비책)."""
    t = re.sub(r"^\s*\[[^\]]*\]\s*", "", title or "")
    t = re.sub(r"\s+-\s+\S+\s*$", "", t)
    t = re.sub(r"^\d+\.\s*", "", t)
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return t


# ---------- 멤버 / 파일 ----------

def member_key(login, members):
    low = (login or "").lower()
    for m in members:
        if m.lower() == low:
            return m
    return None


def solution_entries(files, member):
    prefix = f"members/{member}/"
    out = set()
    for f in files:
        if not f.startswith(prefix):
            continue
        parts = f[len(prefix):].split("/")
        if len(parts) >= 2:
            out.add(f"{parts[0]}/{parts[1]}")
    return out


# ---------- 판정 ----------

def _in_week(pr, week_end):
    start = datetime.datetime.combine(week_end - datetime.timedelta(days=6), datetime.time(0), tzinfo=KST)
    return start <= pr.created <= submit_deadline(week_end)


def _pr_slugs(pr):
    s = set(pr.slugs)
    if pr.title:
        s.add(slugify(pr.title))
    return s


def judge_solving(member, prs, common_slug, prev_common_slug, prev_prs, week_end):
    mine = [p for p in prs if p.author == member and p.entries and _in_week(p, week_end)]
    count = len(set().union(*(p.entries for p in mine)) if mine else set())
    slugs = set().union(*(_pr_slugs(p) for p in mine)) if mine else set()

    if common_slug and common_slug in slugs:
        return SolveResult(count, True, "common", mine)

    retry_allowed = prev_common_slug and any(
        p.author == member and RETRY_LABEL in p.labels and prev_common_slug in _pr_slugs(p)
        for p in prev_prs
    )
    if retry_allowed and prev_common_slug in slugs:
        return SolveResult(count, True, "retry", mine)

    if count >= FREE_GOAL:
        return SolveResult(count, True, "free", mine)
    return SolveResult(count, False, "none", mine)


def judge_review(member, prs, week_end):
    deadline = review_deadline(week_end)
    targets = [p for p in prs if p.author != member and p.entries and _in_week(p, week_end)]
    missed = [
        p for p in targets
        if not any(login.lower() == member.lower() and at <= deadline for login, at in p.reviews)
    ]
    done = len(targets) - len(missed)
    return ReviewResult(done, len(targets), not missed, missed)


# ---------- 경고 누적 ----------

def apply_warnings(state, range_str, unmet, coffee_paid, members):
    """같은 주차로 다시 실행되면 직전 주차 값(base)에서 다시 계산하므로 두 번 누적되지 않는다."""
    state = copy.deepcopy(state or {})
    if state.get("as_of") == range_str and "base" in state:
        counts = dict(state["base"])
    else:
        counts = dict(state.get("counts", {}))
    base = dict(counts)
    for m in members:
        counts.setdefault(m, 0)
    for m in coffee_paid:
        counts[m] = 0
    for m in unmet:
        counts[m] = counts.get(m, 0) + 1
    return {"as_of": range_str, "base": base, "counts": counts}


COFFEE_RE = re.compile(r"^\s*[-*]\s*\[[xX]\].*<!--\s*coffee:(\S+?)\s*-->", re.MULTILINE)


def parse_coffee_checks(body):
    return set(COFFEE_RE.findall(body or ""))


# ---------- 유예 ----------

def excused_members(excuses, week_start, week_end, members=None):
    """유예 기간이 그 주(월~일)와 하루라도 겹치는 멤버 → {폴더명: 사유}.

    excuses.json 항목: {"member": "hun425", "from": "YYYY-MM-DD", "to": "YYYY-MM-DD", "reason": "..."}
    """
    out = {}
    for e in excuses or []:
        try:
            start = datetime.date.fromisoformat(e["from"])
            end = datetime.date.fromisoformat(e["to"])
            member = e["member"]
        except (KeyError, TypeError, ValueError):
            continue
        if members:
            member = member_key(member, members)
            if not member:
                continue
        if start <= week_end and end >= week_start:
            out[member] = e.get("reason", "")
    return out
