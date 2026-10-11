#!/usr/bin/env python3
"""Build the Lab 15 banner (assets/lab15-banner.svg and assets/lab15-banner.png).

Run from anywhere:  python3 tools/make_banner_lab15.py
Needs only numpy and matplotlib. The output is deterministic: the same
input always gives byte-identical files (fixed fonts, fixed SVG hash salt,
no dates in the metadata).

The right-hand panel is drawn from data. It shows the surface of
Example 2 on the Lecture 15 page, f(x, y) = -x^2/2 - y^2 + 25/8, the point
(1/2, 1, 2), the two slices y = 1 and x = 1/2, and the two tangent lines
whose slopes are f_x(1/2, 1) = -1/2 and f_y(1/2, 1) = -2.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

# ---------------------------------------------------------------- tokens
NAVY_DARK = "#0A0E14"
NAVY = "#0F1A2B"
CYAN = "#22D3EE"
INK = "#1E293B"
SLICE = "#7C3AED"     # slice curves
TANGENT = "#059669"   # tangent lines
PROBE = "#D97706"     # the probe point
CONTOUR = "#94A3B8"
SCREEN = "#F8FAFC"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"

# ------------------------------------------------------------ the maths
A, B = 0.5, 1.0                      # the point (a, b) of Example 2


def f(x, y):
    return -x**2 / 2.0 - y**2 + 25.0 / 8.0


def f_x(x, y):
    return -x


def f_y(x, y):
    return -2.0 * y


Z0 = f(A, B)
SX, SY = f_x(A, B), f_y(A, B)
assert abs(Z0 - 2.0) < 1e-12                 # the point (1/2, 1, 2) lies on the surface
assert abs(SX - (-0.5)) < 1e-12 and abs(SY - (-2.0)) < 1e-12
# The tangent slopes agree with difference quotients from the definition.
for h in (1e-4, -1e-4):
    assert abs((f(A + h, B) - Z0) / h - SX) < 1e-3
    assert abs((f(A, B + h) - Z0) / h - SY) < 1e-3

# ------------------------------------------------------- matplotlib setup
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "path",           # text becomes outlines: same look everywhere
        "svg.hashsalt": "ams261-lab15-banner",
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
            "AMS 261  ·  LAB 15  ·  SLICE PROBE",
            color=NAVY_DARK, fontsize=fs(24), fontweight="bold",
            va="center", ha="left", zorder=4)

    # left text block
    x0 = 52
    ax.text(x0, 196, "MISSION 15 //", color=WHITE, fontsize=fs(54),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.text(x0, 152, "SLICE PROBE", color=CYAN, fontsize=fs(40),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.plot([x0, x0 + 90], [130, 130], color=CYAN, lw=3, solid_capstyle="butt", zorder=4)
    ax.text(x0, 98, "Partial derivatives", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 64, "as slopes of slices", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 26, "Ungraded practice  ·  about 30 minutes", color=MUTED,
            fontsize=fs(23), va="baseline", ha="left", zorder=4)

    # ---- right-hand panel: the light plot screen
    px0, px1, py0, py1 = 600.0, 1156.0, 24.0, 244.0
    pw, ph = px1 - px0, py1 - py0
    ax.add_patch(Rectangle((px0 - 5, py0 - 5), pw + 10, ph + 10, fc=SCREEN,
                           ec=CYAN, lw=1.8, zorder=2))

    qx0 = px0 + 205.0                    # the 3D view uses the right part of the screen
    pax = fig.add_axes([qx0 / W, py0 / H - 0.10, (px1 - qx0) / W, ph / H + 0.16],
                       projection="3d", zorder=3, computed_zorder=False)
    pax.set_facecolor(SCREEN)
    pax.patch.set_alpha(0.0)
    for axis in (pax.xaxis, pax.yaxis, pax.zaxis):
        axis.set_pane_color((0.973, 0.980, 0.988, 0.0))
        axis.line.set_color((0, 0, 0, 0))
        axis.set_ticks([])
    pax.grid(False)
    pax.view_init(elev=22, azim=-112)
    pax.set_box_aspect((1.5, 1.5, 1.0), zoom=1.05)

    xs = np.linspace(-2, 2, 41)
    ys = np.linspace(-1.6, 1.6, 33)        # keeps the lowest part of the surface inside the screen
    X, Y = np.meshgrid(xs, ys)
    pax.plot_wireframe(X, Y, f(X, Y), rstride=2, cstride=2, color=CONTOUR,
                       linewidth=0.6, zorder=1)

    # the two slices of the surface through the point
    t = np.linspace(-2, 2, 200)
    pax.plot(t, np.full_like(t, B), f(t, B), color=SLICE, lw=3.0, zorder=4)
    t = np.linspace(-1.6, 1.6, 200)
    pax.plot(np.full_like(t, A), t, f(A, t), color=SLICE, lw=3.0, ls=(0, (5, 2.5)), zorder=4)

    # tangent lines with slopes f_x and f_y
    s = np.linspace(-1.4, 1.4, 2)
    pax.plot(A + s, np.full_like(s, B), Z0 + SX * s, color=TANGENT, lw=3.6, zorder=5)
    s = np.linspace(-0.75, 0.75, 2)
    pax.plot(np.full_like(s, A), B + s, Z0 + SY * s, color=TANGENT, lw=3.6,
             ls=(0, (3, 1.6)), zorder=5)

    pax.scatter([A], [B], [Z0], s=70, color=PROBE, edgecolor=INK, linewidth=1.2,
                depthshade=False, zorder=6)
    pax.set_xlim(-2, 2)
    pax.set_ylim(-1.6, 1.6)
    pax.set_zlim(-2.0, 3.2)

    # labels in the screen (drawn on the flat axes, so they never overlap the 3D view)
    lx = px0 + 16
    ax.text(lx, py1 - 26, r"$z = -\frac{x^2}{2} - y^2 + \frac{25}{8}$", color=INK, fontsize=fs(21),
            ha="left", va="center", zorder=8)
    ax.text(lx, py1 - 72, "probe (1/2, 1, 2)", color=PROBE, fontsize=fs(18),
            fontweight="bold", ha="left", va="center", zorder=8)
    ax.text(lx, py1 - 112, r"$f_x = \,?$", color=TANGENT, fontsize=fs(21),
            fontweight="bold", ha="left", va="center", zorder=8)
    ax.text(lx, py1 - 134, "solid: slice y = 1", color=SLICE, fontsize=fs(16),
            ha="left", va="center", zorder=8)
    ax.text(lx, py1 - 170, r"$f_y = \,?$", color=TANGENT, fontsize=fs(21),
            fontweight="bold", ha="left", va="center", zorder=8)
    ax.text(lx, py1 - 192, "dashed: slice x = 1/2", color=SLICE, fontsize=fs(16),
            ha="left", va="center", zorder=8)
    return fig


def main():
    root = Path(__file__).resolve().parent.parent
    out = root / "assets"
    out.mkdir(exist_ok=True)
    fig = build()
    fig.savefig(out / "lab15-banner.svg", format="svg", facecolor=NAVY_DARK,
                metadata={"Date": None, "Creator": "make_banner_lab15.py"})
    fig.savefig(out / "lab15-banner.png", format="png", dpi=200, facecolor=NAVY_DARK,
                metadata={"Software": None})
    plt.close(fig)
    print("wrote", out / "lab15-banner.svg")
    print("wrote", out / "lab15-banner.png")
    print(f"f(1/2, 1) = {Z0}, f_x = {SX}, f_y = {SY}")


if __name__ == "__main__":
    main()
