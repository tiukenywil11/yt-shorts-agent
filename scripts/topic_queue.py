#!/usr/bin/env python3
"""Topic queue: creative/topic-queue.csv is the source of truth; the .xlsx is generated for viewing.

  python scripts/topic_queue.py list [--status Queued] [--pillar Money]
  python scripts/topic_queue.py next [-n 3]        # candidates for the next Short (you choose; sources are NOT yet citations)
  python scripts/topic_queue.py link <num> <project-folder>   # e.g. link 8 08-phone-screen-time
  python scripts/topic_queue.py sync               # set status from what exists in projects/<folder>/
  python scripts/topic_queue.py xlsx               # regenerate creative/topic-queue.xlsx (read-only output)
  python scripts/topic_queue.py set <num> <status> # manual: Published, Dropped, or a correction

Status ladder (sync): Queued -> Researching (idea.md) -> Scripted (script.json has timings)
 -> Stills (output/stills/*) -> Rendered (draft/preview/final mp4) -> Produced (publish.md).
Published and Dropped are manual and sync never overwrites them.
"""
import argparse, csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "creative" / "topic-queue.csv"
XLSX = ROOT / "creative" / "topic-queue.xlsx"
FIELDS = ["num", "title", "pillar", "series", "status", "project", "trend_score", "origin",
          "source_type", "action", "guardrail", "verification", "verified_source", "url", "caveats"]
STATUSES = ["Queued", "Researching", "Scripted", "Stills", "Rendered", "Produced", "Published", "Dropped"]
MANUAL = {"Published", "Dropped"}
TARGETS = {"Money": "~35%", "Mind": "~25%", "Body": "~20%", "Ready": "~20%"}


def load():
    with CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save(rows):
    with CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def find(rows, num):
    for r in rows:
        if r["num"] == str(num):
            return r
    sys.exit(f"No topic #{num}")


def derive(project):
    """Status implied by files on disk, or None if the project folder is missing."""
    p = ROOT / "projects" / project
    if not p.is_dir():
        return None
    out = p / "output"
    if (p / "publish.md").exists():
        return "Produced"
    if any((out / n).exists() for n in ("draft.mp4", "preview.mp4", "final.mp4")):
        return "Rendered"
    stills = out / "stills"
    if stills.is_dir() and any(stills.iterdir()):
        return "Stills"
    try:
        segs = json.loads((p / "script.json").read_text(encoding="utf-8")).get("segments", [])
        if segs and all("startSec" in s for s in segs):
            return "Scripted"
    except (OSError, ValueError):
        pass
    return "Researching" if (p / "idea.md").exists() else None


def cmd_list(a):
    for r in load():
        if (a.status and r["status"] != a.status) or (a.pillar and r["pillar"] != a.pillar):
            continue
        print(f'{r["num"]:>3}  {r["status"]:<11} {r["pillar"]:<6} {r["series"]:<12} {r["title"]}  [{r["verification"]}]')


def cmd_next(a):
    rows = [r for r in load() if r["status"] == "Queued"]
    counts = {}
    for r in load():
        if r["status"] != "Dropped":
            counts[r["pillar"]] = counts.get(r["pillar"], 0) + 1
    print("Pillar mix so far (target): " + ", ".join(f"{k} {counts.get(k, 0)} ({t})" for k, t in TARGETS.items()))
    print("Candidates (a human picks; read the primary source before writing idea.md):\n")
    for r in rows[: a.n]:
        print(f'#{r["num"]} {r["title"]}  [{r["pillar"]} / {r["series"]}]')
        print(f'   verification: {r["verification"]} - {r["verified_source"] or r["source_type"]}')
        print(f'   url: {r["url"] or "-"}')
        print(f'   try-it-today: {r["action"]}')
        print(f'   guardrail: {r["guardrail"]}')
        print(f'   caveats: {r["caveats"] or "-"}\n')


def cmd_link(a):
    rows = load()
    r = find(rows, a.num)
    if not (ROOT / "projects" / a.project).is_dir():
        sys.exit(f"projects/{a.project} does not exist")
    r["project"] = a.project
    save(rows)
    print(f'#{a.num} -> {a.project}')


def cmd_set(a):
    if a.status not in STATUSES:
        sys.exit("Status must be one of: " + ", ".join(STATUSES))
    rows = load()
    find(rows, a.num)["status"] = a.status
    save(rows)


def cmd_sync(a):
    rows = load()
    changed = 0
    for r in rows:
        if not r["project"] or r["status"] in MANUAL:
            continue
        s = derive(r["project"])
        if s and s != r["status"]:
            print(f'#{r["num"]} {r["title"]}: {r["status"]} -> {s}')
            r["status"] = s
            changed += 1
    save(rows)
    print(f"sync: {changed} change(s)")


def cmd_xlsx(a):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    rows = load()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Queue"
    heads = ["#", "Title", "Pillar", "Series", "Status", "Project folder", "Trend score (11-06 snapshot)", "Origin",
             "Source type", "Try-it-today action", "Guardrail", "Verification", "Verified source", "URL", "Caveats"]
    ws.append(heads)
    for r in rows:
        ts = float(r["trend_score"]) if r["trend_score"] else None
        ws.append([int(r["num"]), r["title"], r["pillar"], r["series"], r["status"], r["project"], ts, r["origin"],
                   r["source_type"], r["action"], r["guardrail"], r["verification"], r["verified_source"], r["url"], r["caveats"]])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3A5F")
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for col, w in zip("ABCDEFGHIJKLMNO", [5, 46, 9, 13, 12, 28, 14, 40, 40, 40, 40, 16, 60, 40, 60]):
        ws.column_dimensions[col].width = w
    fills = {"Verified": "C6EFCE", "Partly verified": "FFEB9C", "Not found": "FFC7CE"}
    for i, row in enumerate(ws.iter_rows(min_row=2), start=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
        if row[6].value is not None:
            row[6].number_format = "0.00"
        f = fills.get(row[11].value)
        if f:
            row[11].fill = PatternFill("solid", fgColor=f)
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUSES) + '"')
    ws.add_data_validation(dv)
    dv.add("E2:E200")
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:O{len(rows) + 1}"
    s = wb.create_sheet("Pillar balance")
    s.append(["Pillar", "Count", "Share", "Target"])
    for k, (pl, t) in enumerate(TARGETS.items(), 2):
        s.append([pl, f"=COUNTIF(Queue!C2:C200,A{k})", f"=B{k}/COUNTA(Queue!C2:C200)", t])
        s[f"C{k}"].number_format = "0%"
    n = wb.create_sheet("Notes")
    for line in [
        "GENERATED from creative/topic-queue.csv by scripts/topic_queue.py xlsx. Edits here are overwritten: edit the CSV or use topic_queue.py.",
        "Status: " + ", ".join(STATUSES) + ". sync derives it from projects/<folder>/; Published and Dropped are manual.",
        "Verification is from web-search abstracts/snippets, not full-text reads. Re-read the primary source before writing idea.md.",
        "Trend score: from creative/trending-habit-topics-2026-11.xlsx (2026-11-06 snapshot); blank if the topic was not ranked.",
        "Pillar targets: docs/business/MONETIZATION_STRATEGY.md."]:
        n.append([line])
    n.column_dimensions["A"].width = 130
    wb.save(XLSX)
    print(f"wrote {XLSX.relative_to(ROOT)}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--status"); s.add_argument("--pillar"); s.set_defaults(f=cmd_list)
    s = sub.add_parser("next"); s.add_argument("-n", type=int, default=3); s.set_defaults(f=cmd_next)
    s = sub.add_parser("link"); s.add_argument("num", type=int); s.add_argument("project"); s.set_defaults(f=cmd_link)
    s = sub.add_parser("set"); s.add_argument("num", type=int); s.add_argument("status"); s.set_defaults(f=cmd_set)
    sub.add_parser("sync").set_defaults(f=cmd_sync)
    sub.add_parser("xlsx").set_defaults(f=cmd_xlsx)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
