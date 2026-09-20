"""
Build the adherence dashboard, per docs/dashboard-build-spec.md (originally
delivered as dashboard-build-spec.md — see that file for the full brief).

Queries Supabase, writes a single self-contained dashboard.html at the repo
root. Static: no server, no auth, no interactivity, no live refresh, no
external libraries/fonts/scripts. All CSS inline in a <style> block, all
charts hand-built inline SVG. dashboard.html is a generated artifact and is
gitignored — re-run this any time the underlying data changes.

Usage:
    python scripts/build_dashboard.py
"""

import html
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from db import get_connection

OUT_PATH = Path(__file__).resolve().parent.parent / "dashboard.html"

TV_AVG_DAYS = 12


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------------------
# Data fetchers — one round trip per logical question, nothing templated
# into a chart until the number is in hand.
# ---------------------------------------------------------------------------

def fetch_action_items(cur):
    cur.execute(
        """
        select o.name, ai.owner_role, ai.owner_name, ai.description, ai.due_date,
               ai.completed_at, ai.is_blocker, ai.status
        from action_items ai
        join opportunities o on o.id = ai.opportunity_id
        order by o.name, ai.due_date
        """
    )
    return cur.fetchall()


def fetch_exit_criteria(cur):
    cur.execute(
        """
        select a.name, vr.version, vr.payload
        from validation_records vr
        join opportunities o on o.id = vr.opportunity_id
        join accounts a on a.id = o.account_id
        where (vr.opportunity_id, vr.version) in (
            select opportunity_id, max(version) from validation_records group by opportunity_id
        )
        order by a.name
        """
    )
    return cur.fetchall()


def fetch_call_counts(cur):
    cur.execute("select call_type, opportunity_id from calls")
    return cur.fetchall()


def fetch_records_by_opportunity(cur):
    cur.execute(
        "select distinct opportunity_id from validation_records where status = 'complete'"
    )
    return {r[0] for r in cur.fetchall()}


def fetch_days_in_stage(cur):
    cur.execute(
        """
        select a.name, o.stage, date_part('day', now() - o.stage_entered_at)::int
        from opportunities o join accounts a on a.id = o.account_id
        order by a.name
        """
    )
    return cur.fetchall()


def fetch_calls_and_activities(cur):
    cur.execute(
        """
        select o.id, a.name, o.ae_name, c.call_type, c.occurred_at
        from calls c join opportunities o on o.id = c.opportunity_id
        join accounts a on a.id = o.account_id
        where c.call_type = 'technical_validation'
        order by a.name, c.occurred_at
        """
    )
    tv_calls = cur.fetchall()
    cur.execute(
        """
        select opportunity_id, activity_type, actor, occurred_at
        from activities
        where activity_type in ('email', 'meeting') and actor <> 'system'
        """
    )
    activities = cur.fetchall()
    return tv_calls, activities


def fetch_baselines(cur):
    cur.execute("select metric, segment, metric_period, value, unit, note from baselines")
    rows = defaultdict(list)
    for metric, segment, period, value, unit, note in cur.fetchall():
        rows[metric].append({"segment": segment, "period": period, "value": float(value), "unit": unit, "note": note})
    return rows


def fetch_competitive(cur):
    cur.execute(
        """
        select a.name, vr.payload -> 'competitive'
        from validation_records vr
        join opportunities o on o.id = vr.opportunity_id
        join accounts a on a.id = o.account_id
        where (vr.opportunity_id, vr.version) in (
            select opportunity_id, max(version) from validation_records group by opportunity_id
        )
        """
    )
    rows = []
    for name, competitive in cur.fetchall():
        for c in (competitive or []):
            rows.append((name, c.get("vendor"), c.get("evaluation_status")))
    return rows


def fetch_deal_outcomes(cur):
    cur.execute("select stage, count(*) from opportunities group by stage")
    return cur.fetchall()


# ---------------------------------------------------------------------------
# Small SVG/HTML chart primitives — thin marks, 4px rounded data-ends, a 2px
# surface gap between bars, hairline gridlines, direct labels (never hover —
# this file has no interactivity by spec).
# ---------------------------------------------------------------------------

def hbar_chart(rows, width=620, bar_h=20, gap=12, max_val=None, color="var(--accent)", unit="", label_w=190):
    """rows: list of (label, value, note_str_or_None). value may be None -> renders an 'awaiting volume' ghost bar."""
    numeric = [r[1] for r in rows if r[1] is not None]
    if max_val is None:
        max_val = max(numeric) if numeric else 1
    max_val = max_val or 1
    # Reserve room for the longest value+note text so the full-length bar's
    # label can't run past the viewBox edge — measured roughly at 6.5px/char
    # for the 12px label font, floored/ceilinged to a sane range.
    longest_note = max((len(f"{v:g}{unit} · {n}" if n else f"{v:g}{unit}") for _l, v, n in rows if v is not None), default=6)
    value_zone = min(260, max(60, int(longest_note * 6.5) + 20))
    chart_w = width - label_w - value_zone
    h = len(rows) * (bar_h + gap) + gap
    parts = [f'<svg viewBox="0 0 {width} {h}" width="100%" height="{h}" role="img" aria-label="bar chart">']
    y = gap
    parts.append(f'<line x1="{label_w}" y1="0" x2="{label_w}" y2="{h}" class="axis-line"/>')
    for label, value, note in rows:
        parts.append(f'<text x="0" y="{y + bar_h * 0.72}" class="bar-label">{esc(label)}</text>')
        if value is None:
            parts.append(
                f'<rect x="{label_w}" y="{y}" width="{chart_w}" height="{bar_h}" rx="4" class="awaiting-bar"/>'
            )
            parts.append(f'<text x="{label_w + 10}" y="{y + bar_h * 0.72}" class="awaiting-label">awaiting volume</text>')
        else:
            w = max(3, (value / max_val) * chart_w)
            parts.append(f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="4" fill="{color}"/>')
            val_txt = f"{value:g}{unit}"
            note_txt = f" · {esc(note)}" if note else ""
            parts.append(f'<text x="{label_w + w + 8:.1f}" y="{y + bar_h * 0.72}" class="bar-value">{val_txt}{note_txt}</text>')
        y += bar_h + gap
    parts.append("</svg>")
    return "".join(parts)


def grouped_bar_chart(groups, series_labels, series_colors, width=640, bar_h=16, group_gap=22, bar_gap=3, max_val=None, unit=""):
    """groups: list of (group_label, [v1, v2, ...]) — one bar per series, grouped by row."""
    all_vals = [v for _, vals in groups for v in vals if v is not None]
    if max_val is None:
        max_val = max(all_vals) if all_vals else 1
    max_val = max_val or 1
    label_w = 150
    chart_w = width - label_w - 90
    n_series = len(series_labels)
    row_h = n_series * (bar_h + bar_gap) + group_gap
    h = len(groups) * row_h + 30
    parts = [f'<svg viewBox="0 0 {width} {h}" width="100%" height="{h}" role="img" aria-label="grouped bar chart">']
    legend_x = label_w
    for i, (lab, color) in enumerate(zip(series_labels, series_colors)):
        lx = legend_x + i * 150
        parts.append(f'<rect x="{lx}" y="4" width="10" height="10" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{lx + 16}" y="13" class="legend-label">{esc(lab)}</text>')
    y = 30
    for glabel, vals in groups:
        gy0 = y
        parts.append(f'<text x="0" y="{gy0 + row_h * 0.4}" class="bar-label">{esc(glabel)}</text>')
        for v, color in zip(vals, series_colors):
            if v is None:
                parts.append(f'<rect x="{label_w}" y="{y}" width="{chart_w}" height="{bar_h}" rx="4" class="awaiting-bar"/>')
                parts.append(f'<text x="{label_w + 8}" y="{y + bar_h * 0.72}" class="awaiting-label-sm">awaiting volume</text>')
            else:
                w = max(3, (v / max_val) * chart_w)
                parts.append(f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="4" fill="{color}"/>')
                parts.append(f'<text x="{label_w + w + 8:.1f}" y="{y + bar_h * 0.72}" class="bar-value-sm">{v:g}{unit}</text>')
            y += bar_h + bar_gap
        y += group_gap - bar_gap
    parts.append("</svg>")
    return "".join(parts)


def stat_tile(label, value, sub=None, status=None):
    status_cls = f" stat-{status}" if status else ""
    sub_html = f'<div class="stat-sub">{esc(sub)}</div>' if sub else ""
    return f'''<div class="stat-tile{status_cls}">
      <div class="stat-label">{esc(label)}</div>
      <div class="stat-value">{esc(value)}</div>
      {sub_html}
    </div>'''


def badge(text, kind="muted"):
    return f'<span class="badge badge-{kind}">{esc(text)}</span>'


# ---------------------------------------------------------------------------
# Panel A — adherence, real, computed from the database
# ---------------------------------------------------------------------------

def build_panel_a(cur, today):
    items = fetch_action_items(cur)

    # Action items by owner role x status
    by_role = defaultdict(lambda: defaultdict(int))
    for _name, role, _owner, _desc, _due, _comp, _blk, status in items:
        by_role[role][status] += 1
    role_order = ["ae", "sc", "customer"]
    role_labels = {"ae": "AE", "sc": "SolCon", "customer": "Customer"}
    status_order = ["open", "completed", "completed_unverified", "missed"]
    status_colors = {"open": "#898781", "completed": "#0ca30c", "completed_unverified": "#eda100", "missed": "#d03b3b"}
    groups = []
    for role in role_order:
        counts = by_role.get(role, {})
        groups.append((role_labels[role], [counts.get(s, 0) for s in status_order]))
    total_committed = sum(sum(c.values()) for c in by_role.values())
    action_items_chart = grouped_bar_chart(
        groups, [s.replace("_", " ") for s in status_order],
        [status_colors[s] for s in status_order], width=640,
    )

    # On-time completion rate per AE / per SolCon
    def on_time_stats(role):
        by_owner = defaultdict(lambda: {"on_time": 0, "resolved": 0})
        for _name, r, owner, _desc, due, comp, _blk, status in items:
            if r != role:
                continue
            if status in ("completed", "missed"):
                by_owner[owner]["resolved"] += 1
                if status == "completed" and comp is not None and comp.date() <= due:
                    by_owner[owner]["on_time"] += 1
        rows = []
        for owner, c in sorted(by_owner.items()):
            n = c["resolved"]
            rate = f"{round(100 * c['on_time'] / n)}%" if n else "—"
            rows.append((owner, n, rate))
        return rows

    ae_on_time = on_time_stats("ae")
    sc_on_time = on_time_stats("sc")

    # Open items past due
    past_due = []
    for name, role, owner, desc, due, _comp, blk, status in items:
        if status == "open" and due < today:
            past_due.append((name, role, owner, desc, due, (today - due).days, blk))
    past_due.sort(key=lambda r: -r[5])

    # Exit criteria per deal
    crit_rows = fetch_exit_criteria(cur)
    CRITERIA_LABELS = [
        "Objections resolved", "Economic buyer ID'd", "Integration agreed",
        "Next step scheduled", "Success criteria captured",
    ]
    exit_grid = []
    legacy_deals = []
    for name, version, payload in crit_rows:
        criteria = payload.get("stage_exit_criteria")
        if criteria is None:
            legacy_deals.append(name)
            continue
        exit_grid.append((name, version, criteria))

    # Record coverage: TV calls whose deal has >=1 complete record, over all TV calls
    tv_calls, activities = fetch_calls_and_activities(cur)
    covered_opps = fetch_records_by_opportunity(cur)
    tv_call_total = len(tv_calls)
    tv_call_covered = sum(1 for opp_id, *_ in tv_calls if opp_id in covered_opps)
    coverage_pct = round(100 * tv_call_covered / tv_call_total) if tv_call_total else 0

    # Days in stage per deal, TV-stage deals only
    stage_rows = fetch_days_in_stage(cur)
    tv_stage_rows = [(name, days) for name, stage, days in stage_rows if stage == "Technical Validation"]
    tv_stage_rows.sort(key=lambda r: -r[1])
    stage_chart_rows = [(name, days, "over baseline" if days > TV_AVG_DAYS else "within baseline") for name, days in tv_stage_rows]

    # Post-demo touches per AE
    touches_by_opp = defaultdict(list)
    for opp_id, name, ae, _ct, occurred in tv_calls:
        window_end_days = 14
        acts_in_window = [
            a for a in activities
            if a[0] == opp_id and 0 <= (a[3] - occurred).total_seconds() / 86400 <= window_end_days
        ]
        first_touch_hours = None
        if acts_in_window:
            first = min(a[3] for a in acts_in_window)
            first_touch_hours = round((first - occurred).total_seconds() / 3600)
        touches_by_opp[(ae, name)].append((len(acts_in_window), first_touch_hours))

    by_ae = defaultdict(list)
    for (ae, name), windows in touches_by_opp.items():
        by_ae[ae].append((name, windows))

    touches_table = []
    for ae, deals in sorted(by_ae.items()):
        all_windows = [w for _n, ws in deals for w in ws]
        n_windows = len(all_windows)
        n_deals = len(deals)
        avg_touches = sum(w[0] for w in all_windows) / n_windows if n_windows else 0
        hours = sorted(w[1] for w in all_windows if w[1] is not None)
        median_hours = hours[len(hours) // 2] if hours else None
        flag = avg_touches <= 0.7
        touches_table.append((ae, n_deals, n_windows, round(avg_touches, 1), median_hours, flag))

    return {
        "action_items_chart": action_items_chart,
        "total_committed": total_committed,
        "ae_on_time": ae_on_time,
        "sc_on_time": sc_on_time,
        "past_due": past_due,
        "exit_grid": exit_grid,
        "legacy_deals": legacy_deals,
        "criteria_labels": CRITERIA_LABELS,
        "coverage_pct": coverage_pct,
        "tv_call_total": tv_call_total,
        "tv_call_covered": tv_call_covered,
        "stage_chart_rows": stage_chart_rows,
        "touches_table": touches_table,
    }


# ---------------------------------------------------------------------------
# Panel B — measurement design. Baseline real, treatment/holdout awaiting.
# ---------------------------------------------------------------------------

def build_panel_b(cur, panel_a):
    baselines = fetch_baselines(cur)

    # 1. Stage duration, all four stages + total cycle
    stages = ["Discovery", "Technical Validation", "Commercial Negotiation", "Legal/Close"]
    stage_baseline = {}
    for row in baselines["stage_duration"]:
        if row["period"] == "Q3":
            stage_baseline[row["segment"]] = row["value"]
    stage_groups = []
    for s in stages:
        stage_groups.append((s, [stage_baseline.get(s), None, None]))
    total_baseline = sum(stage_baseline.values())
    stage_groups.append(("Total cycle", [total_baseline, None, None]))
    stage_chart = grouped_bar_chart(
        stage_groups, ["Baseline (Q3)", "Treatment", "Holdout"],
        ["var(--accent)", "var(--awaiting-ink)", "var(--awaiting-ink)"], width=660, unit="d",
    )
    # Displacement guard — functional now, inert until treatment data exists.
    treatment_tv = None  # would come from a treatment cohort's own stage_duration once seeded
    treatment_total = None
    displacement_warning = (
        treatment_tv is not None and treatment_total is not None
        and treatment_tv < stage_baseline.get("Technical Validation", 0)
        and treatment_total >= total_baseline
    )

    # 2. Win rate — baseline bucket real; record-covered/holdout awaiting (n too thin to report as a rate)
    win_rate_rows = [(r["segment"], r["value"], None) for r in baselines["win_rate_by_tv_days"]]
    win_rate_chart = hbar_chart(win_rate_rows, unit="%", color="var(--accent)", max_val=100)

    # 3. Deal outcomes — real stage counts as a footnote, not a rate
    outcome_rows = fetch_deal_outcomes(cur)
    outcome_footnote = ", ".join(f"{count} {stage}" for stage, count in outcome_rows)

    # 4. Competitive win rate — note the data source, list what's captured so far
    competitive_rows = fetch_competitive(cur)
    live_mentions = [r for r in competitive_rows if r[2] == "actively_evaluating"]

    # 5. CS time to first value — baseline only
    ttfv_rows = [(r["segment"], r["value"], None) for r in baselines["cs_ttfv"]]
    ttfv_chart = hbar_chart(ttfv_rows, unit="d", color="var(--accent)")
    ttfv_corr = baselines["cs_ttfv_correlation"][0]["value"]

    # 6. Behavior — baseline is a real population-level quartile split; this
    # system only has 5 reps, which isn't a quartile in any meaningful sense,
    # so the chart stays baseline-only and each rep's real (tiny-n) average
    # is listed separately underneath rather than forced into a fake
    # quartile bucket next to it.
    touch_baseline = {r["segment"]: r["value"] for r in baselines["post_demo_touches"]}
    quartile_map = {"top": "Top quartile", "middle": "Middle", "bottom": "Bottom quartile"}
    behavior_rows = [(quartile_map[q], touch_baseline[q], None) for q in ("top", "middle", "bottom")]
    behavior_chart = hbar_chart(behavior_rows, unit=" touches", color="var(--accent)")
    behavior_observed = [
        (ae, avg, f"n={n_windows}")
        for ae, _n_deals, n_windows, avg, _med, _flag in panel_a["touches_table"]
    ]

    # 7. First-touch latency — real observed medians, explicitly tiny-n
    latency_rows = [
        (ae, med, f"n={n_windows}")
        for ae, _n_deals, n_windows, _avg, med, _flag in panel_a["touches_table"]
        if med is not None
    ]
    latency_chart = hbar_chart(
        [(ae, med, note) for ae, med, note in latency_rows], unit="h", color="#eda100",
    ) if latency_rows else "<p class='muted'>No first-touch data yet.</p>"

    return {
        "stage_chart": stage_chart,
        "displacement_warning": displacement_warning,
        "win_rate_chart": win_rate_chart,
        "outcome_footnote": outcome_footnote,
        "live_mentions": live_mentions,
        "ttfv_chart": ttfv_chart,
        "ttfv_corr": ttfv_corr,
        "behavior_chart": behavior_chart,
        "behavior_observed": behavior_observed,
        "latency_chart": latency_chart,
        "sc_summary_pct": baselines["sc_summary_completion"][0]["value"],
    }


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------

STYLE = """
:root {
  color-scheme: light;
  --surface-1: #fcfcfb;
  --page: #f3f1f9;
  --text-primary: #171521;
  --text-secondary: #52514e;
  --muted: #898781;
  --hairline: #e1e0d9;
  --border: rgba(11,11,11,0.10);
  --accent: #4a3aa7;
  --accent-ink: #ffffff;
  --accent-wash: #efe9fb;
  --topbar: #1f1633;
  --awaiting-ink: #cfcbe8;
  --good: #0ca30c;
  --warning: #eda100;
  --critical: #d03b3b;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --surface-1: #1c1a24;
    --page: #131019;
    --text-primary: #f5f3ff;
    --text-secondary: #c3c2b7;
    --muted: #8f8ca3;
    --hairline: #322d44;
    --border: rgba(255,255,255,0.10);
    --accent: #9085e9;
    --accent-ink: #171225;
    --accent-wash: #241d3a;
    --topbar: #0f0c18;
    --awaiting-ink: #3a3552;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface-1: #1c1a24;
  --page: #131019;
  --text-primary: #f5f3ff;
  --text-secondary: #c3c2b7;
  --muted: #8f8ca3;
  --hairline: #322d44;
  --border: rgba(255,255,255,0.10);
  --accent: #9085e9;
  --accent-ink: #171225;
  --accent-wash: #241d3a;
  --topbar: #0f0c18;
  --awaiting-ink: #3a3552;
}
* { box-sizing: border-box; }
body { background: var(--page); color: var(--text-primary); font-family: system-ui, -apple-system, "Segoe UI", sans-serif; margin: 0; padding: 0; }
.topbar { background: var(--topbar); color: #fff; padding: 14px 24px; display: flex; align-items: center; gap: 14px; }
.topbar .logo { width: 26px; height: 26px; border-radius: 7px; background: var(--accent); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex: none; }
.topbar .product { font-weight: 600; letter-spacing: 0.2px; }
.topbar .tabs { display: flex; gap: 18px; margin-left: 24px; font-size: 13.5px; color: #cfc9e8; flex-wrap: wrap; }
.topbar .tabs span.active { color: #fff; font-weight: 600; border-bottom: 2px solid var(--accent); padding-bottom: 3px; }
.wrap { max-width: 1120px; margin: 0 auto; padding: 20px 20px 64px; }
.header-card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 20px 24px; margin: 20px 0 28px; }
.header-card h1 { margin: 0 0 6px; font-size: 21px; }
.header-card p { margin: 4px 0; color: var(--text-secondary); font-size: 13.5px; line-height: 1.5; }
.disclosure { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
section.panel { margin-bottom: 36px; }
.panel-title { display: flex; align-items: baseline; gap: 10px; margin: 0 0 14px; }
.panel-title h2 { font-size: 17px; margin: 0; }
.panel-title .kicker { font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.6px; color: var(--muted); font-weight: 600; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-bottom: 16px; }
.card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; overflow-x: auto; }
.card h3 { margin: 0 0 10px; font-size: 13.5px; color: var(--text-secondary); font-weight: 600; }
.card-wide { grid-column: 1 / -1; }
.stat-tile { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; }
.stat-label { font-size: 12px; color: var(--text-secondary); }
.stat-value { font-size: 28px; font-weight: 600; margin-top: 4px; }
.stat-sub { font-size: 12px; color: var(--muted); margin-top: 4px; }
.stat-warning .stat-value { color: var(--warning); }
.stat-critical .stat-value { color: var(--critical); }
table { border-collapse: collapse; width: 100%; font-size: 13px; }
th, td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--hairline); }
th { color: var(--muted); font-weight: 600; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.3px; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11.5px; font-weight: 600; }
.badge-good { background: color-mix(in srgb, var(--good) 16%, transparent); color: var(--good); }
.badge-warning { background: color-mix(in srgb, var(--warning) 20%, transparent); color: #8a5c00; }
.badge-critical { background: color-mix(in srgb, var(--critical) 16%, transparent); color: var(--critical); }
.badge-muted { background: var(--hairline); color: var(--text-secondary); }
:root:not([data-theme="light"]) .badge-warning { color: var(--warning); }
.bar-label, .legend-label { font-size: 12.5px; fill: var(--text-secondary); }
.bar-value, .bar-value-sm { font-size: 12px; fill: var(--text-secondary); font-variant-numeric: tabular-nums; }
.axis-line { stroke: var(--hairline); stroke-width: 1; }
.awaiting-bar { fill: var(--awaiting-ink); opacity: 0.55; }
.awaiting-label, .awaiting-label-sm { font-size: 11.5px; fill: var(--muted); font-style: italic; }
.exit-grid-table td.met { color: var(--good); font-weight: 700; }
.exit-grid-table td.unmet { color: var(--critical); font-weight: 700; }
.exit-reason { display: block; font-size: 11px; color: var(--muted); font-weight: 400; margin-top: 2px; }
.muted { color: var(--muted); font-size: 12.5px; }
.legacy-note { font-size: 12px; color: var(--muted); margin-top: 8px; }
/* Panel B — unmistakably distinct: violet-tinted surface, dashed border, persistent banner */
.panel-b-wrap { background: repeating-linear-gradient(135deg, var(--accent-wash), var(--accent-wash) 12px, var(--page) 12px, var(--page) 24px); border: 2px dashed var(--accent); border-radius: 16px; padding: 18px; }
.panel-b-banner { background: var(--topbar); color: #fff; border-radius: 10px; padding: 12px 16px; margin-bottom: 16px; font-size: 13px; display: flex; gap: 10px; align-items: center; }
.panel-b-banner .tag { background: var(--accent); border-radius: 999px; padding: 3px 10px; font-weight: 700; font-size: 11px; letter-spacing: 0.4px; flex: none; }
.panel-b-wrap .card { background: var(--surface-1); border-color: var(--accent); }
.panel-b-wrap .card h3::after { content: " — MEASUREMENT DESIGN"; color: var(--accent); font-size: 10px; letter-spacing: 0.4px; font-weight: 700; }
.warn-banner { background: color-mix(in srgb, var(--critical) 12%, transparent); border: 1px solid var(--critical); color: var(--critical); border-radius: 8px; padding: 10px 14px; font-size: 12.5px; margin-bottom: 10px; }
.footnote { font-size: 12px; color: var(--muted); margin-top: 8px; }
footer.page-footer { text-align: center; color: var(--muted); font-size: 12px; padding: 24px 0; }
@media (max-width: 640px) {
  .topbar .tabs { display: none; }
  .card { overflow-x: auto; }
}
"""


def render_action_items_card(pa):
    return f'''<div class="card card-wide">
      <h3>Action items by owner role</h3>
      {pa['action_items_chart']}
      <p class="footnote">{pa['total_committed']} items committed in total (open + completed + completed unverified + missed).
      "Completed unverified" is counted separately from "completed" on purpose — see <code>scripts/check_closure.py</code>: it's evidence found but only weakly corresponding to the item, not a confirmed close.</p>
    </div>'''


def render_on_time_card(pa):
    def rows_html(rows):
        if not rows:
            return "<tr><td colspan='3' class='muted'>No resolved items yet.</td></tr>"
        out = ""
        for owner, n, rate in rows:
            out += f"<tr><td>{esc(owner)}</td><td class='num'>{rate}</td><td class='num'>n={n}</td></tr>"
        return out

    return f'''<div class="card">
      <h3>On-time completion rate — AE</h3>
      <table><thead><tr><th>Owner</th><th class="num">Rate</th><th class="num">Sample</th></tr></thead>
      <tbody>{rows_html(pa['ae_on_time'])}</tbody></table>
      <p class="footnote">On time = completed on or before due date, as a share of items no longer open (completed + missed). Sample sizes are tiny — read the n, not just the rate.</p>
    </div>
    <div class="card">
      <h3>On-time completion rate — SolCon</h3>
      <table><thead><tr><th>Owner</th><th class="num">Rate</th><th class="num">Sample</th></tr></thead>
      <tbody>{rows_html(pa['sc_on_time'])}</tbody></table>
    </div>'''


def render_past_due_card(pa, today):
    if not pa["past_due"]:
        return f'''<div class="card card-wide"><h3>Open items past due</h3><p class="muted">Nothing open is past due as of {today.isoformat()}.</p></div>'''
    rows = ""
    for name, role, owner, desc, due, days_over, blk in pa["past_due"]:
        blocker_badge = badge("blocker", "critical") if blk else ""
        rows += f'''<tr><td>{esc(name)}</td><td>{esc(owner)} ({esc(role)})</td><td>{esc(desc)}</td>
          <td class="num">{due.isoformat()}</td><td class="num">{days_over}d</td><td>{blocker_badge}</td></tr>'''
    return f'''<div class="card card-wide">
      <h3>Open items past due</h3>
      <table><thead><tr><th>Deal</th><th>Owner</th><th>Description</th><th class="num">Due</th><th class="num">Overdue</th><th>Flag</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>'''


def render_exit_criteria_card(pa):
    if not pa["exit_grid"]:
        return ""
    header = "".join(f"<th>{esc(c)}</th>" for c in pa["criteria_labels"])
    rows = ""
    for name, version, criteria in pa["exit_grid"]:
        met_count = sum(1 for c in criteria if c["met"])
        cells = ""
        for c in criteria:
            if c["met"]:
                cells += '<td class="met">✓</td>'
            else:
                reason = f'<span class="exit-reason">{esc(c["reason"])}</span>' if c.get("reason") else ""
                cells += f'<td class="unmet">✗{reason}</td>'
        rows += f'<tr><td>{esc(name)} <span class="muted">v{version}</span> · {met_count}/5</td>{cells}</tr>'
    legacy_note = ""
    if pa["legacy_deals"]:
        legacy_note = (
            f'<p class="legacy-note">Not shown: {esc(", ".join(pa["legacy_deals"]))} — '
            f"record predates the stage_exit_criteria field in the current contract, not a coverage gap.</p>"
        )
    return f'''<div class="card card-wide exit-grid-table">
      <h3>Exit criteria per deal</h3>
      <table><thead><tr><th>Deal</th>{header}</tr></thead><tbody>{rows}</tbody></table>
      {legacy_note}
    </div>'''


def render_coverage_card(pa):
    status = "critical" if pa["coverage_pct"] < 40 else ("warning" if pa["coverage_pct"] < 70 else None)
    return stat_tile(
        "Record coverage",
        f"{pa['coverage_pct']}%",
        sub=f"{pa['tv_call_covered']} of {pa['tv_call_total']} technical validation calls belong to a deal with a complete Record",
        status=status,
    )


def render_days_in_stage_card(pa):
    if not pa["stage_chart_rows"]:
        return '<div class="card card-wide"><h3>Days in Technical Validation</h3><p class="muted">No deals currently in Technical Validation.</p></div>'
    chart = hbar_chart(pa["stage_chart_rows"], unit="d", color="var(--accent)")
    return f'''<div class="card card-wide">
      <h3>Days in Technical Validation, vs the {TV_AVG_DAYS}-day Apex average</h3>
      {chart}
    </div>'''


def render_touches_card(pa):
    rows = ""
    for ae, n_deals, n_windows, avg, median_h, flag in pa["touches_table"]:
        flag_badge = badge(f"≤ baseline bottom quartile (0.7)", "critical") if flag else ""
        med_txt = f"{median_h}h" if median_h is not None else "—"
        rows += f'''<tr><td>{esc(ae)}</td><td class="num">{n_deals}</td><td class="num">n={n_windows}</td>
          <td class="num">{avg:g}</td><td class="num">{med_txt}</td><td>{flag_badge}</td></tr>'''
    return f'''<div class="card card-wide">
      <h3>Post-demo touches per AE — 14 days following each technical validation call</h3>
      <table><thead><tr><th>AE</th><th class="num">Deals</th><th class="num">Call windows</th>
        <th class="num">Avg touches</th><th class="num">Median hrs to first touch</th><th>Flag</th></tr></thead>
      <tbody>{rows}</tbody></table>
      <p class="footnote">n is call-windows, not deals, where a deal has more than one technical validation call. With six synthetic deals these counts are tiny — read the rate next to its n, not on its own.</p>
    </div>'''


def render_panel_b(pb):
    warn_html = ""
    if pb["displacement_warning"]:
        warn_html = '<div class="warn-banner">⚠ Technical Validation is improving while total cycle time is not — this system may be moving work to a later stage rather than removing it.</div>'

    live_mentions_html = ""
    if pb["live_mentions"]:
        items = "; ".join(f"{esc(n)} vs {esc(v)}" for n, v, _s in pb["live_mentions"])
        live_mentions_html = f"<p class='footnote'>Captured so far: {items}.</p>"

    return f'''<section class="panel">
      <div class="panel-title"><span class="kicker">Panel B</span><h2>The measurement design</h2></div>
      <div class="panel-b-wrap">
        <div class="panel-b-banner"><span class="tag">AWAITING VOLUME</span>
          Baselines are real Apex historical data from the GTM assessment packet. Treatment and holdout columns are placeholders — this system has not yet run against enough deals to populate them. Nothing on this panel is a result.</div>

        <div class="card-grid">
          <div class="card card-wide">
            <h3>1. Stage duration, all four stages + total cycle</h3>
            {warn_html}
            {pb['stage_chart']}
            <p class="footnote">This is the displacement guard. If Technical Validation drops while total cycle time doesn't, the system moved work rather than removing it — the warning above fires automatically once treatment data exists.</p>
          </div>

          <div class="card">
            <h3>2. Win rate by days in Technical Validation</h3>
            {pb['win_rate_chart']}
            <p class="footnote">Baseline only. Record-covered vs. holdout win rate isn't shown as a rate yet — with one closed deal so far, a rate would be one coin flip wearing statistics.</p>
          </div>

          <div class="card">
            <h3>3. Deal outcomes</h3>
            <p class="muted">Record-covered vs. holdout split: awaiting volume.</p>
            <p class="footnote">Current stage mix across all deals: {esc(pb['outcome_footnote'])}.</p>
          </div>

          <div class="card">
            <h3>4. Competitive win rate</h3>
            <p class="muted">Awaiting volume.</p>
            <p class="footnote">This data doesn't exist in the CRM today — it's only available at all because the Record captures competitor mentions from the call itself.</p>
            {live_mentions_html}
          </div>

          <div class="card">
            <h3>5. CS time to first value</h3>
            {pb['ttfv_chart']}
            <p class="footnote">Baseline only, r={pb['ttfv_corr']:g} between cycle length and time to first value. Not instrumented yet on this system's side.</p>
          </div>

          <div class="card card-wide">
            <h3>6. Behavior — post-demo touches by AE quartile</h3>
            {pb['behavior_chart']}
            <p class="footnote">Targets: bottom quartile to 1.5, middle to 1.8. Baseline only — five reps isn't a population you can split into quartiles, so no "observed quartile" bar is shown next to it. SolCon summary-doc completion rate baseline: ~{pb['sc_summary_pct']:g}%.</p>
            <table><thead><tr><th>Rep (individual, not quartile-matched)</th><th class="num">Avg touches</th><th class="num">Sample</th></tr></thead>
              <tbody>{"".join(f"<tr><td>{esc(ae)}</td><td class='num'>{avg:g}</td><td class='num'>{esc(n)}</td></tr>" for ae, avg, n in pb['behavior_observed'])}</tbody></table>
          </div>

          <div class="card card-wide">
            <h3>7. First-touch latency — median hours from technical validation call to first touch</h3>
            {pb['latency_chart']}
            <p class="footnote">Isolates speed from volume — the most direct read on whether the drafted email is actually landing faster. Treatment vs. holdout split: awaiting volume; these are this session's observed numbers only, each tagged with its n.</p>
          </div>
        </div>
      </div>
    </section>'''


def build_html(pa, pb, today):
    coverage_card = render_coverage_card(pa)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Adherence &amp; Measurement</title>
<style>{STYLE}</style>
</head>
<body>
<div class="topbar">
  <div class="logo">A</div>
  <div class="product">Pipeline Intelligence</div>
  <div class="tabs"><span class="active">Insights</span><span>Deals</span><span>Calls</span><span>Coaching</span></div>
</div>
<div class="wrap">
  <div class="header-card">
    <h1>Adherence &amp; Measurement Dashboard</h1>
    <p>This is the artifact behind a pipeline review, not a standalone tool. Panel A is real, computed from the live database behind the six synthetic deals in this prototype. Panel B's baselines are real Apex historical data from the GTM assessment packet; its treatment and holdout columns are placeholders awaiting real rollout volume — see the banner on that panel.</p>
    <div class="disclosure">
      {badge("Underlying deal data: synthetic", "muted")}
      {badge("Panel A: real, computed", "good")}
      {badge("Panel B baselines: real (packet)", "muted")}
      {badge("Panel B treatment/holdout: awaiting volume", "warning")}
    </div>
  </div>

  <section class="panel">
    <div class="panel-title"><span class="kicker">Panel A</span><h2>Adherence</h2></div>
    <div class="card-grid">
      {render_action_items_card(pa)}
      {render_on_time_card(pa)}
      {render_past_due_card(pa, today)}
      {render_exit_criteria_card(pa)}
      {coverage_card}
      {render_days_in_stage_card(pa)}
      {render_touches_card(pa)}
    </div>
  </section>

  {render_panel_b(pb)}

  <footer class="page-footer">Generated {today.isoformat()} by scripts/build_dashboard.py. Static file — re-run the script to refresh.</footer>
</div>
</body>
</html>'''


def main():
    # UTC, not local time — matches scripts/seed_structure.py's REFERENCE_DATE
    # convention (Postgres's now() is UTC; local time can disagree by a day).
    today = datetime.now(timezone.utc).date()
    with get_connection() as conn:
        with conn.cursor() as cur:
            panel_a = build_panel_a(cur, today)
            panel_b = build_panel_b(cur, panel_a)

    html_out = build_html(panel_a, panel_b, today)
    OUT_PATH.write_text(html_out)
    print(f"Wrote {OUT_PATH} ({len(html_out):,} bytes)")
    print(f"Record coverage: {panel_a['tv_call_covered']}/{panel_a['tv_call_total']} technical validation calls ({panel_a['coverage_pct']}%)")


if __name__ == "__main__":
    main()
