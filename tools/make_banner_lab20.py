#!/usr/bin/env python3
"""Build the Lab 20 banner (assets/lab20-banner.svg and assets/lab20-banner.png).

Run from anywhere:  python3 tools/make_banner_lab20.py
Needs only numpy and matplotlib. The output is deterministic: the same
input always gives byte-identical files (fixed fonts, fixed SVG hash salt,
no dates in the metadata).

The right-hand panel is drawn from data. It shows the level curves of
Example 5 of Lecture 20, f(x, y) = xy(x - 2)(y + 3). The zero level set is
four lines. Its four corners (0, 0), (0, -3), (2, 0), (2, -3) are saddle
points, and the centre (1, -3/2) is a relative maximum with value 9/4.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

# ---------------------------------------------------------------- tokens
NAVY_DARK = "#0A0E14"
NAVY = "#0F1A2B"
CYAN = "#22D3EE"
INK = "#1E293B"
RED = "#DC2626"       # relative maximum (f_xx < 0)
GREEN = "#059669"     # zero level set f = 0
AMBER = "#D97706"     # saddle points
CONTOUR = "#94A3B8"
SCREEN = "#F8FAFC"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"

# ------------------------------------------------------------ the maths


def f(x, y):
    return x * y * (x - 2.0) * (y + 3.0)


def grad_f(x, y):
    return np.array([(2.0 * x - 2.0) * (y**2 + 3.0 * y), (x**2 - 2.0 * x) * (2.0 * y + 3.0)])


def hessian_D(x, y):
    fxx = 2.0 * (y**2 + 3.0 * y)
    fyy = 2.0 * (x**2 - 2.0 * x)
    fxy = (2.0 * x - 2.0) * (2.0 * y + 3.0)
    return fxx, fxx * fyy - fxy**2


SADDLES = [(0.0, 0.0), (0.0, -3.0), (2.0, 0.0), (2.0, -3.0)]
PEAK = (1.0, -1.5)
for p in SADDLES + [PEAK]:
    assert np.allclose(grad_f(*p), 0.0), p          # every marked point is critical
for p in SADDLES:
    assert abs(hessian_D(*p)[1] - (-36.0)) < 1e-12   # D = -36 < 0: saddle
    assert abs(f(*p)) < 1e-12
fxx_peak, D_peak = hessian_D(*PEAK)
assert abs(fxx_peak + 4.5) < 1e-12 and abs(D_peak - 9.0) < 1e-12   # D > 0, f_xx < 0: max
assert abs(f(*PEAK) - 2.25) < 1e-12                                 # value 9/4

# ------------------------------------------------------- matplotlib setup
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "path",           # text becomes outlines: same look everywhere
        "svg.hashsalt": "ams261-lab20-banner",
        "path.simplify": False,
    }
)

W, H = 1200.0, 300.0          # drawing units (1 unit = 1 px at 1x; PNG is saved at 2x)
PT = 0.72                     # one unit in points (12 in = 1200 units, 72 pt per in)


def fs(units):
    """Font size in points for a text height given in drawing units."""
    return units * PT


def build():
    fig = plt.figure(figsize=(W / 100, H / 100), facecolor=NAVY_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # background: vertical navy gradient
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    cmap = LinearSegmentedColormap.from_list("hud", [NAVY, NAVY_DARK])
    ax.imshow(grad, extent=[0, W, 0, H], origin="upper", cmap=cmap,
              aspect="auto", zorder=0, interpolation="bilinear")

    # faint grid on the left side
    for x in np.arange(0, 620, 40):
        ax.plot([x, x], [0, 250], color=CYAN, alpha=0.05, lw=1, zorder=1)
    for y in np.arange(10, 251, 40):
        ax.plot([0, 620], [y, y], color=CYAN, alpha=0.05, lw=1, zorder=1)

    # corner brackets
    inset, ln, lw = 9, 30, 3.2
    for cx, sx in ((inset, 1), (W - inset, -1)):
        for cy, sy in ((inset, 1), (H - inset, -1)):
            ax.plot([cx + sx * ln, cx, cx], [cy, cy, cy + sy * ln],
                    color=CYAN, lw=lw, solid_capstyle="butt",
                    solid_joinstyle="miter", zorder=5)

    # top bar
    bar_x0, bar_x1, bar_y0, bar_y1 = 48.0, W - 48.0, 254.0, 290.0
    ax.add_patch(Rectangle((bar_x0, bar_y0), bar_x1 - bar_x0, bar_y1 - bar_y0,
                           fc=CYAN, ec="none", zorder=3))
    ax.text(bar_x0 + 16, (bar_y0 + bar_y1) / 2 - 1,
            "AMS 261  ·  LAB 20  ·  SUMMIT & SADDLE",
            color=NAVY_DARK, fontsize=fs(24), fontweight="bold",
            va="center", ha="left", zorder=4)

    # left text block
    x0 = 52
    ax.text(x0, 196, "MISSION 20 //", color=WHITE, fontsize=fs(54),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.text(x0, 152, "SUMMIT & SADDLE", color=CYAN, fontsize=fs(40),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.plot([x0, x0 + 90], [130, 130], color=CYAN, lw=3, solid_capstyle="butt", zorder=4)
    ax.text(x0, 98, "Extrema of functions", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 64, "of two variables", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 26, "Ungraded practice  ·  about 30 minutes", color=MUTED,
            fontsize=fs(23), va="baseline", ha="left", zorder=4)

    # ---- right-hand panel: the light plot screen
    px0, px1, py0, py1 = 600.0, 1156.0, 24.0, 244.0
    pw, ph = px1 - px0, py1 - py0
    ax.add_patch(Rectangle((px0 - 5, py0 - 5), pw + 10, ph + 10, fc=NAVY,
                           ec=CYAN, lw=1.8, zorder=2))

    # The rectangle [0,2] x [-3,0] sits in the middle. The x-scale is stretched
    # so the four saddles and the peak fill the wide panel.
    xa, xb = -2.4, 4.4
    ya, yb = -4.6, 1.6
    pax = fig.add_axes([px0 / W, py0 / H, pw / W, ph / H], zorder=3)
    pax.set_facecolor(SCREEN)
    pax.set_xlim(xa, xb)
    pax.set_ylim(ya, yb)
    pax.set_xticks([])
    pax.set_yticks([])
    for s in pax.spines.values():
        s.set_visible(False)

    X, Y = np.meshgrid(np.linspace(xa, xb, 900), np.linspace(ya, yb, 450))
    Z = f(X, Y)
    levels = [-10, -4, -1.5, 0.6, 1.2, 1.7, 2.1, 4, 10]
    pax.contour(X, Y, Z, levels=levels, colors=CONTOUR, linewidths=1.4,
                linestyles="solid", zorder=2)
    # zero level set: the four lines x = 0, x = 2, y = 0, y = -3
    for xv in (0.0, 2.0):
        pax.plot([xv, xv], [ya, yb], color=GREEN, lw=2.2, ls=(0, (5, 3)), zorder=3)
    for yv in (0.0, -3.0):
        pax.plot([xa, xb], [yv, yv], color=GREEN, lw=2.2, ls=(0, (5, 3)), zorder=3)

    halo = [patheffects.withStroke(linewidth=4, foreground=SCREEN)]

    for (sx, sy) in SADDLES:
        pax.plot(sx, sy, marker="X", ms=15, mfc=AMBER, mec=SCREEN, mew=1.6, zorder=6)
    pax.plot(*PEAK, marker="^", ms=16, mfc=RED, mec=SCREEN, mew=1.6, zorder=6)

    pax.text(PEAK[0], PEAK[1] - 0.45, "summit  f = ?", color=RED,
             fontsize=fs(21), fontweight="bold", ha="center", va="top",
             path_effects=halo, zorder=8)
    pax.text(2.2, 0.25, "saddle", color=AMBER, fontsize=fs(21),
             fontweight="bold", ha="left", va="bottom", path_effects=halo, zorder=8)
    pax.text(xa + 0.15, yb - 0.2, "f = xy(x−2)(y+3)", color=INK,
             fontsize=fs(21), fontweight="bold", ha="left", va="top",
             path_effects=halo, zorder=8)

    return fig


def main():
    root = Path(__file__).resolve().parent.parent
    out = root / "assets"
    out.mkdir(exist_ok=True)
    fig = build()
    fig.savefig(out / "lab20-banner.svg", format="svg", facecolor=NAVY_DARK,
                metadata={"Date": None, "Creator": "make_banner_lab20.py"})
    fig.savefig(out / "lab20-banner.png", format="png", dpi=200, facecolor=NAVY_DARK,
                metadata={"Software": None})
    plt.close(fig)
    print("wrote", out / "lab20-banner.svg")
    print("wrote", out / "lab20-banner.png")
    print(f"peak value {f(*PEAK):.4f}, D at peak {D_peak:.1f}, D at saddles -36")


if __name__ == "__main__":
    main()
