#!/usr/bin/env python3
"""Build the Lab 21 banner (assets/lab21-banner.svg and assets/lab21-banner.png).

Run from anywhere:  python3 tools/make_banner_lab21.py
Needs only numpy and matplotlib. The output is deterministic: the same
input always gives byte-identical files (fixed fonts, fixed SVG hash salt,
no dates in the metadata).

The right-hand panel is drawn from data (Lecture 21, Example 1). It shows
the fence x^2/9 + y^2/16 = 1, the level curves 4xy = k, the tangent level
curve 4xy = 24, the point P = (3/sqrt 2, 2 sqrt 2) and the parallel
gradients grad f = 24 grad g there.
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
GREEN = "#059669"     # tangent line
AMBER = "#D97706"     # grad g
PURPLE = "#7C3AED"    # the fence (constraint curve)
CONTOUR = "#94A3B8"
SCREEN = "#F8FAFC"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"

# ------------------------------------------------------------ the maths
# Lecture 21, Example 1: maximize f = 4xy on the fence x^2/9 + y^2/16 = 1 (x, y > 0).
P = np.array([3.0 / np.sqrt(2.0), 2.0 * np.sqrt(2.0)])
LAM = 24.0


def f(x, y):
    return 4.0 * x * y


def g(x, y):
    return x**2 / 9.0 + y**2 / 16.0


def grad_f(x, y):
    return np.array([4.0 * y, 4.0 * x])


def grad_g(x, y):
    return np.array([2.0 * x / 9.0, y / 8.0])


gf, gg = grad_f(*P), grad_g(*P)
assert abs(g(*P) - 1.0) < 1e-12              # P lies on the fence
assert abs(f(*P) - 24.0) < 1e-12             # the maximum value is 24
assert np.allclose(gf, LAM * gg)             # grad f = 24 grad g at P
_t = np.linspace(1e-4, np.pi / 2 - 1e-4, 200001)
assert abs(f(3 * np.cos(_t), 4 * np.sin(_t)).max() - 24.0) < 1e-6   # scan agrees
u_hat = gf / np.hypot(*gf)                   # common unit normal
t_hat = np.array([-u_hat[1], u_hat[0]])      # tangent direction of the fence at P

# ------------------------------------------------------- matplotlib setup
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "path",           # text becomes outlines: same look everywhere
        "svg.hashsalt": "ams261-lab21-banner",
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
            "AMS 261  ·  LAB 21  ·  FENCE LINE",
            color=NAVY_DARK, fontsize=fs(24), fontweight="bold",
            va="center", ha="left", zorder=4)

    # left text block
    x0 = 52
    ax.text(x0, 196, "MISSION 21 //", color=WHITE, fontsize=fs(54),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.text(x0, 152, "FENCE LINE", color=CYAN, fontsize=fs(40),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.plot([x0, x0 + 90], [130, 130], color=CYAN, lw=3, solid_capstyle="butt", zorder=4)
    ax.text(x0, 98, "Lagrange multipliers:", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 64, "the peak on the fence", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 26, "Ungraded practice  ·  about 30 minutes", color=MUTED,
            fontsize=fs(23), va="baseline", ha="left", zorder=4)

    # ---- right-hand panel: the light plot screen
    px0, px1, py0, py1 = 600.0, 1156.0, 24.0, 244.0
    pw, ph = px1 - px0, py1 - py0
    # frame behind the screen
    ax.add_patch(Rectangle((px0 - 5, py0 - 5), pw + 10, ph + 10, fc=NAVY,
                           ec=CYAN, lw=1.8, zorder=2))

    y_half = 5.0
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

    xs = np.linspace(-x_half, x_half, 1200)
    ys = np.linspace(-y_half, y_half, 500)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    pax.contour(X, Y, Z, levels=[-24, -12, 6, 12, 18, 36], colors=CONTOUR,
                linewidths=1.4, linestyles="solid", zorder=2)
    pax.contour(X, Y, Z, levels=[24.0], colors=INK, linewidths=2.4, linestyles="solid", zorder=3)
    pax.axhline(0, color=CONTOUR, lw=0.8, alpha=0.5, zorder=1)
    pax.axvline(0, color=CONTOUR, lw=0.8, alpha=0.5, zorder=1)

    s = np.linspace(0, 2 * np.pi, 600)
    pax.plot(3 * np.cos(s), 4 * np.sin(s), color=PURPLE, lw=3.2, zorder=4)

    halo = [patheffects.withStroke(linewidth=4, foreground=SCREEN)]

    # tangent line of the fence at P (green, dashed)
    L0 = 2.2
    a0, a1 = P - L0 * t_hat, P + L0 * t_hat
    pax.plot([a0[0], a1[0]], [a0[1], a1[1]], color=GREEN, lw=2.6,
             ls=(0, (4, 2.6)), solid_capstyle="butt", zorder=5)

    # grad f (blue, long) and grad g (amber, short) point the same way
    tipf = P + 2.1 * u_hat
    tipg = P + 1.05 * u_hat
    pax.add_patch(FancyArrowPatch(tuple(P), tuple(tipf), arrowstyle="-|>",
                                  mutation_scale=26, lw=3.6, color=BLUE,
                                  shrinkA=0, shrinkB=0, zorder=6))
    pax.add_patch(FancyArrowPatch(tuple(P), tuple(tipg), arrowstyle="-|>",
                                  mutation_scale=22, lw=4.2, color=AMBER,
                                  shrinkA=0, shrinkB=0, zorder=7))

    # the point P
    pax.plot(*P, "o", ms=9, mfc=INK, mec=SCREEN, mew=2, zorder=8)

    # labels
    pax.text(tipf[0] + 0.35, tipf[1] + 0.05, r"$\nabla f = \lambda\,\nabla g$", color=BLUE,
             fontsize=fs(23), fontweight="bold", ha="left", va="center",
             path_effects=halo, zorder=9)
    pax.text(P[0] - 0.6, P[1] - 0.5, "P", color=INK,
             fontsize=fs(22), fontweight="bold", ha="right", va="top",
             path_effects=halo, zorder=9)
    pax.text(-3.4, -4.3, "fence", color=PURPLE, fontsize=fs(21), fontweight="bold",
             ha="right", va="center", path_effects=halo, zorder=9)
    pax.text(7.6, 0.95, "4xy = k?", color=INK, fontsize=fs(21), fontweight="bold",
             ha="left", va="bottom", path_effects=halo, zorder=9)

    return fig


def main():
    root = Path(__file__).resolve().parent.parent
    out = root / "assets"
    out.mkdir(exist_ok=True)
    fig = build()
    fig.savefig(out / "lab21-banner.svg", format="svg", facecolor=NAVY_DARK,
                metadata={"Date": None, "Creator": "make_banner_lab21.py"})
    fig.savefig(out / "lab21-banner.png", format="png", dpi=200, facecolor=NAVY_DARK,
                metadata={"Software": None})
    plt.close(fig)
    print("wrote", out / "lab21-banner.svg")
    print("wrote", out / "lab21-banner.png")
    print(f"P = ({P[0]:.4f}, {P[1]:.4f}), f(P) = {f(*P):.4f}, lambda = {gf[0] / gg[0]:.4f}")


if __name__ == "__main__":
    main()
