"""주간 리포트 생성 (수요일 00:05 KST 실행).

산출물:
  report.md              이슈 본문
  range.txt              집계 기간 문자열
  README.md              현황 블록 갱신
  .github/warnings.json  경고 누적 상태

입력:
  .github/excuses.json   유예 목록 (PR + approve로 추가)

환경변수:
  GH_TOKEN      gh CLI 인증 (Actions에서는 secrets.GITHUB_TOKEN)
  REPORT_DATE   실행일을 강제 (YYYY-MM-DD, 로컬 검증용)
  DRY_RUN=1     파일을 쓰지 않고 이슈 본문만 출력
"""
import datetime
import json
import os
import subprocess
import sys

import weekly_logic as wl

REPO = os.environ.get("GITHUB_REPOSITORY", "Hun425/Beyond-Algorithm")
STATE_PATH = ".github/warnings.json"
EXCUSES_PATH = ".github/excuses.json"
COMMON_ISSUE_QUERY = "공통 문제 in:title"
REPORT_ISSUE_QUERY = "주간 문제풀이 리포트 in:title"
TEXT_EXT = (".md", ".txt", ".kt", ".py", ".java", ".js", ".ts", ".go", ".rs", ".cpp", ".c")


# ---------- GitHub 조회 ----------

def gh_json(*args):
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
    return json.loads(out) if out.strip() else []


def fetch_file(path, ref):
    try:
        return subprocess.run(
            ["gh", "api", "-H", "Accept: application/vnd.github.raw+json",
             f"repos/{REPO}/contents/{path}?ref={ref}"],
            check=True, capture_output=True, text=True,
        ).stdout
    except subprocess.CalledProcessError:
        return ""


def fetch_prs(since, members):
    raw = gh_json(
        "pr", "list", "--repo", REPO, "--state", "all", "--limit", "200",
        "--search", f"created:>={since.isoformat()}",
        "--json", "number,title,author,createdAt,labels,files,reviews,url,headRefOid",
    )
    prs = []
    for r in raw:
        author = wl.member_key(r["author"]["login"], members)
        if not author:
            continue
        files = [f["path"] for f in r.get("files", [])]
        entries = wl.solution_entries(files, author)
        slugs = set()
        for f in files:
            if f.startswith(f"members/{author}/") and f.lower().endswith(TEXT_EXT):
                slugs |= wl.extract_slugs(fetch_file(f, r["headRefOid"]))
        prs.append(wl.PR(
            number=r["number"],
            author=author,
            created=wl.to_kst(r["createdAt"]),
            entries=entries,
            slugs=slugs,
            labels={l["name"] for l in r.get("labels", [])},
            reviews=[(rv["author"]["login"], wl.to_kst(rv["submittedAt"]))
                     for rv in r.get("reviews", []) if rv.get("author") and rv.get("submittedAt")],
            title=r["title"],
            url=r["url"],
            files=files,
        ))
    return prs


def fetch_common_issue(week_start, week_end):
    """그 주(월~일)에 생성된 공통 문제 이슈 중 가장 최근 것."""
    raw = gh_json("issue", "list", "--repo", REPO, "--state", "all", "--limit", "30",
                  "--search", COMMON_ISSUE_QUERY, "--json", "number,title,body,createdAt,url")
    found = None
    for r in raw:
        d = wl.to_kst(r["createdAt"]).date()
        if week_start <= d <= week_end and (found is None or r["number"] > found["number"]):
            found = r
    if not found:
        return None
    slugs = wl.extract_slugs(found.get("body", ""))
    if not slugs:
        return None
    return {"number": found["number"], "url": found["url"], "slug": sorted(slugs)[0]}


def fetch_previous_report_body():
    raw = gh_json("issue", "list", "--repo", REPO, "--state", "all", "--limit", "5",
                  "--search", REPORT_ISSUE_QUERY, "--json", "number,body,createdAt")
    if not raw:
        return ""
    return max(raw, key=lambda r: r["number"]).get("body", "")


# ---------- 렌더링 ----------

def solve_text(r):
    if r.how == "common":
        return f"✅ 공통 ({r.count}개)"
    if r.how == "retry":
        return f"✅ 리트라이 ({r.count}개)"
    if r.how == "free":
        return f"✅ 자유 {r.count}개"
    return f"❌ {r.count}개"


def review_text(r):
    mark = "✅" if r.met else "❌"
    return f"{mark} {r.done}/{r.total}"


def warn_text(n):
    return f"{n}회" + (" ☕" if n >= wl.COFFEE_THRESHOLD else "")


def render(range_str, week_end, common, results, counts, prev_common, skipped):
    header = "| 멤버 | 풀이 | 리뷰 | 이번 주 | 누적 경고 |"
    sep = "|---|---|---|---|---|"
    rows = []
    for m, (s, rv, ex) in results.items():
        if ex is not None:
            status = f"🛌 유예 ({ex})" if ex else "🛌 유예"
        else:
            status = "이행" if s.met and rv.met else "**미이행**"
        rows.append(f"| {m} | {solve_text(s)} | {review_text(rv)} | {status} | {warn_text(counts[m])} |")
    table_md = "\n".join([header, sep, *rows])

    common_line = f"[{common['slug']}]({common['url']}) (#{common['number']})" if common else "없음"
    body = [
        "## 📊 주간 문제풀이 리포트", "",
        f"**기간**: {range_str} (월~일)",
        f"**공통 문제**: {common_line}",
        f"**리뷰 마감**: {wl.review_deadline(week_end):%Y-%m-%d %H:%M} KST", "",
        table_md, "",
        "> 이행 기준: 공통 문제 1개 **또는** 자유 문제 2개 / 다른 멤버 PR 전부 리뷰. "
        "하나라도 빠지면 그 주 경고 1회. 2회 누적 시 커피 ☕ (유예 승인된 주는 제외)",
    ]
    if prev_common:
        body.append(f"> 직전 주 공통 문제 `{prev_common['slug']}`를 HELP 라벨로 냈다면 이번 주 리트라이로 인정")

    solved = [(m, s.prs) for m, (s, _, _) in results.items() if s.prs]
    if solved:
        body += ["", "### 풀이 목록"]
        for m, prs in solved:
            links = ", ".join(f"[#{p.number}]({p.url})" for p in sorted(prs, key=lambda p: p.number))
            body.append(f"- **{m}**: {links}")

    missed = [(m, rv.missed) for m, (_, rv, ex) in results.items() if rv.missed and ex is None]
    if missed:
        body += ["", "### 리뷰 누락 (화요일 23:59 KST 기준)"]
        for m, prs in missed:
            body.append(f"- **{m}**: " + ", ".join(f"[#{p.number}]({p.url})" for p in sorted(prs, key=lambda p: p.number)))

    coffee = [m for m in results if counts[m] >= wl.COFFEE_THRESHOLD]
    if coffee:
        body += ["", "### ☕ 커피 체크", "커피를 샀으면 체크해 주세요. 다음 리포트에서 0회로 초기화됩니다."]
        body += [f"- [ ] **{m}** 커피 샀음 <!-- coffee:{m} -->" for m in coffee]

    if skipped:
        body += ["", "### ⚠️ 집계 제외 PR", "본인 `members/{id}/` 폴더 아래에 파일이 없어 풀이로 세지 않았어요."]
        body += [f"- [#{p.number}]({p.url}) ({p.author})" for p in skipped]

    readme_rows = "\n".join(
        f"| {m} | {'🛌 유예' if ex is not None else solve_text(s)} | {review_text(rv)} | {warn_text(counts[m])} |"
        for m, (s, rv, ex) in results.items()
    )
    readme_table = "| 멤버 | 풀이 | 리뷰 | 누적 경고 |\n|---|---|---|---|\n" + readme_rows
    return "\n".join(body) + "\n", readme_table


def update_readme(range_str, table_md):
    MS, ME = "<!-- WEEKLY-REPORT:START -->", "<!-- WEEKLY-REPORT:END -->"
    block = f"{MS}\n**기간**: {range_str}\n\n{table_md}\n{ME}"
    readme = ""
    if os.path.exists("README.md"):
        with open("README.md", encoding="utf-8") as f:
            readme = f.read()
    if MS in readme and ME in readme:
        readme = readme.split(MS)[0] + block + readme.split(ME)[1]
    else:
        readme = readme.rstrip() + "\n\n## 📊 주간 문제풀이 현황\n\n" + block + "\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)


# ---------- main ----------

def main():
    dry = os.environ.get("DRY_RUN") == "1"
    today = (datetime.date.fromisoformat(os.environ["REPORT_DATE"])
             if os.environ.get("REPORT_DATE") else datetime.datetime.now(wl.KST).date())
    week_start, week_end = wl.week_range(today)
    prev_start, prev_end = week_start - datetime.timedelta(days=7), week_start - datetime.timedelta(days=1)
    range_str = f"{week_start} ~ {week_end}"

    members = sorted((m for m in os.listdir("members") if os.path.isdir(os.path.join("members", m))), key=str.lower)

    prs = fetch_prs(prev_start - datetime.timedelta(days=1), members)
    this_prs = [p for p in prs if week_start <= p.created.date() <= week_end]
    prev_prs = [p for p in prs if prev_start <= p.created.date() <= prev_end]
    common = fetch_common_issue(week_start, week_end)
    prev_common = fetch_common_issue(prev_start, prev_end)
    coffee_paid = wl.parse_coffee_checks(fetch_previous_report_body())
    excuses = []
    if os.path.exists(EXCUSES_PATH):
        with open(EXCUSES_PATH, encoding="utf-8") as f:
            excuses = json.load(f)
    excused = wl.excused_members(excuses, week_start, week_end, members)

    results = {}
    for m in members:
        s = wl.judge_solving(m, this_prs, common and common["slug"], prev_common and prev_common["slug"], prev_prs, week_end)
        rv = wl.judge_review(m, this_prs, week_end)
        results[m] = (s, rv, excused.get(m))
    unmet = {m for m, (s, rv, ex) in results.items() if ex is None and not (s.met and rv.met)}
    skipped = [p for p in this_prs if not p.entries and any(f.startswith("members/") for f in p.files)]

    state = {}
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as f:
            state = json.load(f)
    state = wl.apply_warnings(state, range_str, unmet, coffee_paid, members)

    body, readme_table = render(range_str, week_end, common, results, state["counts"], prev_common, skipped)

    if dry:
        print(body)
        print("coffee_paid:", sorted(coffee_paid), "| state:", json.dumps(state, ensure_ascii=False), file=sys.stderr)
        return

    with open("report.md", "w", encoding="utf-8") as f:
        f.write(body)
    with open("range.txt", "w", encoding="utf-8") as f:
        f.write(range_str)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
    update_readme(range_str, readme_table)
    print(range_str)


if __name__ == "__main__":
    main()
