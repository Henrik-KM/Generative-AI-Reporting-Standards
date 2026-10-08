"""Draw Figure 2 (candidate attrition in published campaigns) and its SI source table.

Every value is read from data/figure2_stage_counts.json, where each count carries its
source location in the cited publication. Usage, from the npjcm directory:

    python tools/make_figure2.py
"""
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "figure2_stage_counts.json"
OUT = ROOT / "figures"

# Evidence levels shared by all campaigns; each reported stage is mapped to one of them.
STAGE_TYPES = [
    ("generated", "Generated"),
    ("fast", "Fast filters"),
    ("surrogate", "ML or virtual\nscreen"),
    ("high_fidelity", "High-fidelity\ncomputation"),
    ("attempted", "Experiment\nattempted"),
    ("confirmed", "Experimentally\nconfirmed"),
]
DENOMINATORS = [
    ("generated", "Generated", "o"),
    ("high_fidelity", "High-fidelity inputs", "s"),
    ("attempted", "Experiments", "^"),
]
# Validated categorical palette (dataviz reference; the first three slots pass all-pairs CVD checks).
DOMAIN_COLOURS = {
    "Molecules and polymers": "#2a78d6",
    "Inorganic crystals": "#eb6834",
    "Porous materials": "#1baf7a",
}
MARKERS = {"gentrl": "o", "synthemol": "s", "polyverse": "D", "mattergen": "^",
           "wines": "v", "chen": "P", "mofassemble": "X"}
INK = "#1f1f1e"
SECONDARY = "#52514e"
MUTED = "#8a8984"
GRID = "#e6e5e1"


def load():
    with open(DATA, encoding="utf8") as fh:
        return json.load(fh)


def stage_points(campaign):
    """Return (x, count) for the last reported count at each evidence level."""
    order = {key: i for i, (key, _) in enumerate(STAGE_TYPES)}
    last = {}
    for stage in campaign["stages"]:
        last[stage["type"]] = stage["count"]
    return sorted((order[k], v) for k, v in last.items())


def style_axis(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=INK, length=2.5, width=0.6)


def panel_label(ax, letter, x=-0.07):
    ax.text(x, 1.04, letter, transform=ax.transAxes, fontsize=9, fontweight="bold",
            va="bottom", ha="left", color=INK)


def draw_attrition(ax, data):
    for campaign in data["campaigns"]:
        xs, ys = zip(*stage_points(campaign))
        colour = DOMAIN_COLOURS[campaign["domain"]]
        dashed = campaign["engine"] == "enumeration"
        ax.plot(xs, ys, color=colour, lw=1.3, ls=(0, (3, 2)) if dashed else "-",
                solid_capstyle="round", zorder=2)
        ax.scatter(xs, ys, s=26, marker=MARKERS[campaign["id"]], color=colour,
                   edgecolor="white", linewidth=0.7, zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(0.6, 1e8)
    ax.set_xlim(-0.25, len(STAGE_TYPES) - 0.75)
    ax.set_xticks(range(len(STAGE_TYPES)))
    ax.set_xticklabels([label for _, label in STAGE_TYPES])
    ax.set_ylabel("Candidates remaining")
    ax.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    style_axis(ax)
    handles = []
    for campaign in data["campaigns"]:
        colour = DOMAIN_COLOURS[campaign["domain"]]
        dashed = campaign["engine"] == "enumeration"
        handles.append(Line2D([0], [0], color=colour, lw=1.3, ls=(0, (3, 2)) if dashed else "-",
                              marker=MARKERS[campaign["id"]], ms=4.5, mec="white", mew=0.6,
                              label=campaign["label"]))
    handles.append(Line2D([0], [0], color="none", label=""))
    handles.append(Line2D([0], [0], color=SECONDARY, lw=1.3, label="Generative model"))
    handles.append(Line2D([0], [0], color=SECONDARY, lw=1.3, ls=(0, (3, 2)),
                          label="Enumeration and screening"))
    ax.legend(handles=handles, frameon=False, loc="upper left", bbox_to_anchor=(1.01, 1.0),
              fontsize=6.3, handlelength=2.6, borderaxespad=0)


def draw_denominators(ax, data):
    rows = [c for c in data["campaigns"] if c["endpoint"]]
    for i, campaign in enumerate(rows):
        y = len(rows) - 1 - i
        endpoint = campaign["stages"][-1]["count"]
        colour = DOMAIN_COLOURS[campaign["domain"]]
        xs = []
        for key, _, marker in DENOMINATORS:
            denom = campaign["denominators"].get(key)
            if denom is None:
                continue
            frac = endpoint / denom
            xs.append(frac)
            ax.scatter([frac], [y], marker=marker, s=30, color=colour, edgecolor="white",
                       linewidth=0.7, zorder=3)
        ax.plot([min(xs), max(xs)], [y, y], color=GRID, lw=2.2, zorder=1, solid_capstyle="round")
        span = math.log10(max(xs) / min(xs))
        ax.text(1.6, y, f"{span:.1f}", va="center", ha="left", fontsize=6.3, color=SECONDARY)
    ax.text(1.6, len(rows) - 0.55, "Span", va="bottom", ha="left",
            fontsize=6, color=SECONDARY, linespacing=1.0)
    ax.set_xscale("log")
    ax.set_xlim(1e-8, 1.4)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([c["short"] for c in reversed(rows)])
    ax.set_xlabel("Endpoint count / candidates at the stated stage")
    ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
    style_axis(ax)
    handles = [Line2D([0], [0], color="none", marker=m, ms=5, mfc=SECONDARY, mec="white", label=lab)
               for _, lab, m in DENOMINATORS]
    ax.legend(handles=handles, frameon=False, loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=3,
              fontsize=6.0, handletextpad=0.2, columnspacing=0.9, borderaxespad=0)


def draw_baselines(ax, data):
    base = data["baselines"]
    methods = base["methods"]
    ys = list(range(len(methods)))[::-1]
    for y, m in zip(ys, methods):
        colour = SECONDARY if m["kind"] == "baseline" else DOMAIN_COLOURS["Inorganic crystals"]
        ax.barh(y, m["value"], height=0.62, color=colour, zorder=2)
        ax.text(m["value"] + 0.25, y, f"{m['value']:.1f}%", va="center", ha="left",
                fontsize=6.3, color=INK)
    ax.set_yticks(ys)
    ax.set_yticklabels([m["label"] for m in methods])
    ax.set_xlim(0, 11.5)
    ax.set_xticks([0, 5, 10])
    ax.set_xlabel("On-hull candidates after DFT (%)")
    ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
    style_axis(ax)
    handles = [Line2D([0], [0], color=SECONDARY, lw=5, label="Baseline"),
               Line2D([0], [0], color=DOMAIN_COLOURS["Inorganic crystals"], lw=5, label="Generative model")]
    ax.legend(handles=handles, frameon=False, loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=2,
              fontsize=6.0, handlelength=1.2, handletextpad=0.6, columnspacing=1.2, borderaxespad=0)


def draw(data):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7,
        "axes.labelcolor": INK,
        "axes.labelsize": 7,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })
    fig = plt.figure(figsize=(7.1, 5.3))
    gs_top = GridSpec(1, 1, figure=fig, left=0.09, right=0.99, top=0.96, bottom=0.57)
    gs_bot = GridSpec(1, 2, figure=fig, width_ratios=[1.45, 1.0], wspace=0.75,
                      left=0.165, right=0.975, top=0.41, bottom=0.085)
    ax_a = fig.add_subplot(gs_top[0, 0])
    ax_b = fig.add_subplot(gs_bot[0, 0])
    ax_c = fig.add_subplot(gs_bot[0, 1])
    # Leave room on the right of panel a for its legend.
    pos = ax_a.get_position()
    ax_a.set_position([pos.x0, pos.y0, pos.width * 0.70, pos.height])
    draw_attrition(ax_a, data)
    draw_denominators(ax_b, data)
    draw_baselines(ax_c, data)
    panel_label(ax_a, "a", x=-0.105)
    panel_label(ax_b, "b", x=-0.31)
    panel_label(ax_c, "c", x=-0.62)
    OUT.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"Figure_2.{ext}", dpi=300)


def latex_escape(text):
    return (text.replace("&", r"\&").replace("%", r"\%").replace("~", r"\textasciitilde{}")
            .replace("#", r"\#").replace("_", r"\_").replace("µ", r"\textmu{}"))


def write_si_table(data):
    names = {k: v.replace("\n", " ") for k, v in STAGE_TYPES}
    lines = [
        "% Generated by tools/make_figure2.py from data/figure2_stage_counts.json; do not edit by hand.",
        r"\section*{Supplementary Note 4 | Sources for Figure 2}",
        "",
        latex_escape(data["note"]),
        "",
        r"\begin{longtable}{L{0.18\textwidth} L{0.33\textwidth} R{0.10\textwidth} L{0.13\textwidth} L{0.18\textwidth}}",
        r"\caption{Stage counts plotted in Figure 2a,b of the main text}\label{tab:fig2-sources}\\",
        r"\toprule",
        r"\textbf{Campaign} & \textbf{Stage as reported} & \textbf{Count} & \textbf{Evidence level} & \textbf{Source location} \\",
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        r"\textbf{Campaign} & \textbf{Stage as reported} & \textbf{Count} & \textbf{Evidence level} & \textbf{Source location} \\",
        r"\midrule",
        r"\endhead",
        r"\bottomrule",
        r"\endfoot",
    ]
    for campaign in data["campaigns"]:
        for i, stage in enumerate(campaign["stages"]):
            name = rf"{latex_escape(campaign['label'])} \citep{{{campaign['cite']}}}" if i == 0 else ""
            lines.append(f"{name} & {latex_escape(stage['label'])} & {stage['count']:,} & "
                         f"{names[stage['type']]} & {latex_escape(stage['source'])} \\\\")
        lines.append(r"\addlinespace")
    lines.append(r"\end{longtable}")
    base = data["baselines"]
    lines += [
        "",
        rf"Figure~2c reproduces the stability rates reported by Szymanski and Bartel \citep{{{base['cite']}}}, {latex_escape(base['source'])}. "
        r"Each method generated candidates until 500 were absent from the Materials Project, and all 500 were relaxed with DFT; a candidate counts as stable when it lies on or below the Materials Project convex hull. "
        r"The generative models were trained on the MP-20 dataset; MatterGen trained on its larger Alex-MP-20 dataset reached 5.4\%.",
    ]
    (ROOT / "si_figure2_sources.tex").write_text("\n".join(lines) + "\n", encoding="utf8")


if __name__ == "__main__":
    d = load()
    draw(d)
    write_si_table(d)
    print("Figure 2 and Supplementary Note 4 written.")
