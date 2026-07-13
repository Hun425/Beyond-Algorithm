import datetime
import os
import re

KST = datetime.timezone(datetime.timedelta(hours=9))
GOAL = 2

today = datetime.datetime.now(KST).date()
this_monday = today - datetime.timedelta(days=today.weekday())
week_start = this_monday - datetime.timedelta(days=7)
week_end = this_monday - datetime.timedelta(days=1)

# members/<유저>/<YYYY-MM>/<MM-DD>-... 경로에서 날짜 파싱
entries = {}
unrecognized = []
for member in sorted(os.listdir("members"), key=str.lower):
    mdir = os.path.join("members", member)
    if not os.path.isdir(mdir):
        continue
    entries[member] = []
    for month in os.listdir(mdir):
        mpath = os.path.join(mdir, month)
        ym = re.match(r"^(\d{4})-\d{2}$", month)
        if not ym:
            unrecognized.append(f"{mpath} (월 폴더가 YYYY-MM 형식이 아님)")
            continue
        if not os.path.isdir(mpath):
            unrecognized.append(f"{mpath} (월 위치에 폴더가 아닌 파일)")
            continue
        year = int(ym.group(1))
        for entry in os.listdir(mpath):
            md = re.match(r"^(\d{2})-(\d{2})", entry)
            if not md:
                unrecognized.append(f"{mpath}/{entry} (MM-DD 접두어 없음)")
                continue
            try:
                d = datetime.date(year, int(md.group(1)), int(md.group(2)))
            except ValueError:
                unrecognized.append(f"{mpath}/{entry} (날짜가 유효하지 않음)")
                continue
            entries[member].append((d, entry))

table = ["| 멤버 | 풀이 | 목표(주 2회) |", "|---|---|---|"]
details = []
for member, items in entries.items():
    week_items = sorted(e for e in items if week_start <= e[0] <= week_end)
    mark = "✅" if len(week_items) >= GOAL else "❌"
    table.append(f"| {member} | {len(week_items)}회 | {mark} |")
    if week_items:
        details.append(f"- **{member}**: " + ", ".join(e[1] for e in week_items))

range_str = f"{week_start} ~ {week_end}"
table_md = "\n".join(table)

body = f"## 📊 주간 문제풀이 리포트\n\n**기간**: {range_str} (월~일)\n\n{table_md}\n"
if details:
    body += "\n### 풀이 목록\n" + "\n".join(details) + "\n"
if unrecognized:
    body += (
        "\n### ⚠️ 형식 미인식 (집계 제외)\n"
        "아래 항목은 `MM-DD` 접두어 규칙에 맞지 않아 집계에서 빠졌어요. "
        "풀이가 맞다면 이름을 규칙에 맞게 바꿔주세요.\n"
        + "\n".join(f"- `{u}`" for u in unrecognized)
        + "\n"
    )

with open("report.md", "w", encoding="utf-8") as f:
    f.write(body)
with open("range.txt", "w", encoding="utf-8") as f:
    f.write(range_str)

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

print(range_str)
