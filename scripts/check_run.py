"""Validate a prospecting-system run folder and print the stage funnel.

    uv run scripts/check_run.py runs/<run>      # exit 1 if anything is wrong
    uv run scripts/check_run.py --selftest

Checks the contract in skills/prospecting-system/SKILL.md: state.json shape,
spend under cap, every done stage's files exist with their required columns,
lead_id unique. Stdlib only.
"""
import csv
import json
import sys
import tempfile
from pathlib import Path

LEAD = ["lead_id", "account_domain", "source_type"]
# stage key -> {output file: required columns ([] = must exist only)}
STAGES = {
    "01-customer-patterns": {"01-customer-patterns.md": [], "01-seeds.csv": ["domain"]},
    "02-icp-definition": {"02-client-profile.yaml": []},
    "03-lookalike-research": {"03-lookalikes.csv": ["domain"]},
    "04-audience-discovery": {"04-audiences.csv": ["audience_type", "name", "selected"]},
    "05-follower-scrape": {"05-audience-raw": []},
    "06-audience-filter": {"06-judge-prompt.txt": [], "06-audience-qualified.csv": LEAD + ["qualified"]},
    "07-targeted-search": {"07-lane.json": [], "07-accounts.csv": ["domain"]},
    "08-contact-enrichment": {"08-leads.csv": LEAD + ["email_status"]},
    "09-buying-signals": {"09-signals.csv": ["account_domain", "signal_type", "source_url", "event_date"]},
    "10-lead-scoring": {"10-scored.csv": LEAD + ["screen", "fit_score"]},
    "11-lead-prioritization": {"11-prioritized.csv": LEAD + ["priority_score", "tier"]},
    "12-segmentation": {"12-segmented.csv": LEAD + ["segment"]},
    "13-personalization": {"13-personalized.csv": LEAD + ["angle_source"]},
    "14-cold-email": {"14-emails.csv": ["lead_id", "subject", "body"]},
    "15-linkedin-outreach": {"15-linkedin.csv": ["lead_id", "template", "connection_note", "dm"]},
    "16-follow-ups": {"16-sequence.md": [], "16-followups.csv": ["segment", "step", "body"]},
    "17-reply-classification": {"17-replies.csv": ["lead_id", "label", "is_positive"]},
    "18-lead-qualification": {"18-qualified.csv": ["lead_id", "decision", "decision_reason"]},
    "19-account-notes": {"19-account-notes": []},
    "20-pipeline-review": {},
}
STATUSES = {"pending", "done", "skipped", "blocked"}


def check(run: Path) -> list[str]:
    errors = []
    try:
        state = json.loads((run / "state.json").read_text())
    except (OSError, ValueError) as e:
        return [f"state.json unreadable: {e}"]

    cap, spent = state.get("spend_cap_usd"), state.get("spent_usd", 0)
    if not isinstance(cap, (int, float)):
        errors.append("spend_cap_usd missing — the cap is required before any paid stage")
    elif spent > cap:
        errors.append(f"spent_usd {spent} is over spend_cap_usd {cap}")

    for key, st in state.get("stages", {}).items():
        if key not in STAGES:
            errors.append(f"unknown stage '{key}'")
            continue
        if st.get("status") not in STATUSES:
            errors.append(f"{key}: status '{st.get('status')}' not one of {sorted(STATUSES)}")
        if st.get("status") == "blocked" and not st.get("note"):
            errors.append(f"{key}: blocked without a note saying why")
        if st.get("status") != "done":
            continue
        for fname, cols in STAGES[key].items():
            path = run / fname
            if not path.exists():
                errors.append(f"{key}: done but {fname} is missing")
            elif cols:
                with path.open(newline="", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    header = reader.fieldnames or []
                    rows = list(reader)
                missing = [c for c in cols if c not in header]
                if missing:
                    errors.append(f"{key}: {fname} missing columns {missing}")
                if "lead_id" in cols and "lead_id" in header:
                    ids = [r["lead_id"] for r in rows]
                    if "" in ids:
                        errors.append(f"{key}: {fname} has rows with a blank lead_id")
                    if fname != "14-emails.csv" and len(ids) != len(set(ids)):
                        errors.append(f"{key}: {fname} has duplicate lead_id — dedupe before paying for the next stage")
    return errors


def funnel(run: Path) -> None:
    state = json.loads((run / "state.json").read_text())
    print(f"run {state.get('run', run.name)}  spent ${state.get('spent_usd', 0)} of ${state.get('spend_cap_usd')} cap")
    worst = None
    for key in STAGES:
        st = state.get("stages", {}).get(key)
        if not st:
            continue
        rin, rout = st.get("rows_in"), st.get("rows_out")
        keep = f"{rout / rin:5.0%}" if rin and rout is not None else "     "
        print(f"  {key:26} {st.get('status', ''):8} {str(rin or ''):>7} -> {str(rout if rout is not None else ''):>7} {keep}  {st.get('note', '')}")
        # ponytail: "biggest drop" is a plain ratio; stages that are meant to cut hard (06, 07) will often win. Read it, don't obey it.
        if rin and rout is not None and rin >= 20 and (worst is None or rout / rin < worst[1]):
            worst = (key, rout / rin)
    if worst and worst[1] < 1:
        print(f"biggest drop: {worst[0]} keeps {worst[1]:.0%} of its input")


def selftest() -> None:
    with tempfile.TemporaryDirectory() as d:
        run = Path(d)
        (run / "01-customer-patterns.md").write_text("x")
        (run / "01-seeds.csv").write_text("domain\na.com\n")
        (run / "08-leads.csv").write_text("lead_id,account_domain,source_type,email_status\nx,a.com,follower,valid\n")
        state = {"run": "t", "spend_cap_usd": 100, "spent_usd": 10, "stages": {
            "01-customer-patterns": {"status": "done", "rows_in": 5, "rows_out": 5},
            "08-contact-enrichment": {"status": "done", "rows_in": 40, "rows_out": 1}}}
        (run / "state.json").write_text(json.dumps(state))
        assert check(run) == [], check(run)

        (run / "08-leads.csv").write_text("lead_id,account_domain,source_type,email_status\nx,a.com,follower,valid\nx,a.com,search,valid\n")
        assert any("duplicate lead_id" in e for e in check(run))

        state["spent_usd"] = 101
        state["stages"]["05-follower-scrape"] = {"status": "blocked"}
        state["stages"]["03-lookalike-research"] = {"status": "done"}
        (run / "state.json").write_text(json.dumps(state))
        errs = check(run)
        assert any("over spend_cap" in e for e in errs)
        assert any("blocked without a note" in e for e in errs)
        assert any("03-lookalikes.csv is missing" in e for e in errs)
    print("selftest ok")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        selftest()
    else:
        run_dir = Path(sys.argv[1])
        problems = check(run_dir)
        if not any("state.json unreadable" in p for p in problems):
            funnel(run_dir)
        for p in problems:
            print("FAIL", p)
        print("OK" if not problems else f"{len(problems)} problem(s)")
        sys.exit(1 if problems else 0)
