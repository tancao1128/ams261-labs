#!/usr/bin/env python3
"""Build the Lab 18 banner (assets/lab18-banner.svg and assets/lab18-banner.png).

Run from anywhere:  python3 tools/make_banner.py
Needs only numpy and matplotlib. The output is deterministic: the same
input always gives byte-identical files (fixed fonts, fixed SVG hash salt,
no dates in the metadata).

The right-hand panel is drawn from data. It shows the isotherms of
T(x, y) = 20 - 4x^2 - y^2, the point P = (2, -3), the gradient direction
and the two zero-change headings.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.patches import FancyArrowPatch, Rectangle

# ---------------------------------------------------------------- tokens
NAVY_DARK = "#0A0E14"
NAVY = "#0F1A2B"
CYAN = "#22D3EE"
INK = "#1E293B"
BLUE = "#2563EB"      # gradient
GREEN = "#059669"     # zero change
CONTOUR = "#94A3B8"
SCREEN = "#F8FAFC"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"

# ------------------------------------------------------------ the maths
P = np.array([2.0, -3.0])


def T(x, y):
    return 20.0 - 4.0 * x**2 - y**2


def grad_T(x, y):
    return np.array([-8.0 * x, -2.0 * y])


g = grad_T(*P)
assert np.allclose(g, [-16.0, 6.0])
g_hat = g / np.hypot(*g)
heading_grad = np.degrees(np.arctan2(g[1], g[0])) % 360
zero_dirs = [np.array([-g_hat[1], g_hat[0]]), np.array([g_hat[1], -g_hat[0]])]
zero_headings = sorted(np.degrees(np.arctan2(d[1], d[0])) % 360 for d in zero_dirs)
assert abs(heading_grad - 159.44) < 0.01, heading_grad
assert abs(zero_headings[0] - 69.44) < 0.01 and abs(zero_headings[1] - 249.44) < 0.01
assert abs(T(*P) - (-5.0)) < 1e-12          # P lies on 4x^2 + y^2 = 25

# ------------------------------------------------------- matplotlib setup
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "path",           # text becomes outlines: same look everywhere
        "svg.hashsalt": "ams261-lab18-banner",
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
    from matplotlib.colors import LinearSegmentedColormap

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
            "AMS 261  ·  LAB 18  ·  ROVER FIELD TEST",
            color=NAVY_DARK, fontsize=fs(24), fontweight="bold",
            va="center", ha="left", zorder=4)

    # left text block
    x0 = 52
    ax.text(x0, 196, "MISSION 18 //", color=WHITE, fontsize=fs(54),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.text(x0, 152, "ROVER FIELD TEST", color=CYAN, fontsize=fs(40),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.plot([x0, x0 + 90], [130, 130], color=CYAN, lw=3, solid_capstyle="butt", zorder=4)
    ax.text(x0, 98, "Directional derivatives", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 64, "and the gradient", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 26, "Ungraded practice  ·  about 30 minutes", color=MUTED,
            fontsize=fs(23), va="baseline", ha="left", zorder=4)

    # ---- right-hand panel: the light plot screen
    px0, px1, py0, py1 = 600.0, 1156.0, 24.0, 244.0
    pw, ph = px1 - px0, py1 - py0
    # frame behind the screen
    ax.add_patch(Rectangle((px0 - 5, py0 - 5), pw + 10, ph + 10, fc=NAVY,
                           ec=CYAN, lw=1.8, zorder=2))

    y_half = 6.2
    x_half = y_half * pw / ph            # equal scale: same units per pixel in x and y
    pax = fig.add_axes([px0 / W, py0 / H, pw / W, ph / H], zorder=3)
    pax.set_facecolor(SCREEN)
    pax.set_xlim(-x_half, x_half)
    pax.set_ylim(-y_half, y_half)
    pax.set_aspect("equal", adjustable="box")
    pax.set_xticks([])
    pax.set_yticks([])
    for s in pax.spines.values():
        s.set_visible(False)

    xs = np.linspace(-x_half, x_half, 900)
    ys = np.linspace(-y_half, y_half, 450)
    X, Y = np.meshgrid(xs, ys)
    Z = T(X, Y)
    cs = [4, 9, 16, 36, 49, 64, 100, 144, 196, 256, 324, 400, 484, 576, 676]
    pax.contour(X, Y, Z, levels=sorted(20 - c for c in cs), colors=CONTOUR,
                linewidths=1.5, linestyles="solid", zorder=2)
    pax.contour(X, Y, Z, levels=[T(*P)], colors=INK, linewidths=2.4, linestyles="solid", zorder=3)
    pax.axhline(0, color=CONTOUR, lw=0.8, alpha=0.5, zorder=1)
    pax.axvline(0, color=CONTOUR, lw=0.8, alpha=0.5, zorder=1)

    halo = [patheffects.withStroke(linewidth=4, foreground=SCREEN)]

    # zero-change headings (green, dashed)
    L0 = 2.75
    for d in zero_dirs:
        tip = P + L0 * d
        pax.plot([P[0], tip[0]], [P[1], tip[1]], color=GREEN, lw=3.0,
                 ls=(0, (4, 2.6)), solid_capstyle="butt", zorder=5)

    # gradient arrow: scaled unit direction (blue)
    La = 3.6
    tipg = P + La * g_hat
    pax.add_patch(FancyArrowPatch(tuple(P), tuple(tipg), arrowstyle="-|>",
                                  mutation_scale=26, lw=3.6, color=BLUE,
                                  shrinkA=0, shrinkB=0, zorder=6))

    # point P
    pax.plot(*P, "o", ms=9, mfc=INK, mec=SCREEN, mew=2, zorder=7)

    # labels
    pax.text(tipg[0] - 0.3, tipg[1] + 0.25, r"$\nabla T(P)$", color=BLUE,
             fontsize=fs(25), fontweight="bold", ha="right", va="bottom",
             path_effects=halo, zorder=8)
    pax.text(P[0] + 0.5, P[1] - 0.15, "P (2, −3)", color=INK,
             fontsize=fs(22), fontweight="bold", ha="left", va="top",
             path_effects=halo, zorder=8)
    up = P + L0 * zero_dirs[0] if zero_dirs[0][1] > 0 else P + L0 * zero_dirs[1]
    pax.text(up[0] + 0.3, up[1] + 0.1, "zero change", color=GREEN,
             fontsize=fs(21), fontweight="bold", ha="left", va="bottom",
             path_effects=halo, zorder=8)

    return fig


def main():
    root = Path(__file__).resolve().parent.parent
    out = root / "assets"
    out.mkdir(exist_ok=True)
    fig = build()
    fig.savefig(out / "lab18-banner.svg", format="svg", facecolor=NAVY_DARK,
                metadata={"Date": None, "Creator": "make_banner.py"})
    fig.savefig(out / "lab18-banner.png", format="png", dpi=200, facecolor=NAVY_DARK,
                metadata={"Software": None})
    plt.close(fig)
    print("wrote", out / "lab18-banner.svg")
    print("wrote", out / "lab18-banner.png")
    print(f"grad heading {heading_grad:.2f}, zero headings "
          f"{zero_headings[0]:.2f} and {zero_headings[1]:.2f}")


if __name__ == "__main__":
    main()
