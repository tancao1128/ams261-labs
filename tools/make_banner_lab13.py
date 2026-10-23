#!/usr/bin/env python3
"""Build the Lab 13 banner (assets/lab13-banner.svg and assets/lab13-banner.png).

Run from anywhere:  python3 tools/make_banner_lab13.py
Needs only numpy and matplotlib. The output is deterministic: the same
input always gives byte-identical files (fixed fonts, fixed SVG hash salt,
no dates in the metadata).

The right-hand panel is drawn from the lecture's own hook. It shows the hill
z = sqrt(16 - 4x^2 - y^2) of Mission 13 (x, y in km, z in hundreds of m):
on the left, the contour map at heights 0, 2 and 4 on equal axes; on the
right, the east-west and north-south profiles through the summit.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.patches import Rectangle

# ---------------------------------------------------------------- tokens
NAVY_DARK = "#0A0E14"
NAVY = "#0F1A2B"
CYAN = "#22D3EE"
INK = "#1E293B"
BLUE = "#2563EB"      # contour at height 2
GREEN = "#059669"     # contour at height 0 (edge of the domain)
SLICE = "#7C3AED"     # profile curves
AMBER = "#D97706"     # highlight
CONTOUR = "#94A3B8"
SCREEN = "#F8FAFC"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"


# ------------------------------------------------------------ the maths
def hill(x, y):
    """Height of the hill in hundreds of metres; nan outside the domain."""
    r = 16.0 - 4.0 * x**2 - y**2
    return np.where(r >= 0, np.sqrt(np.clip(r, 0, None)), np.nan)


def reaches(h):
    """East and north reach (km) of the contour at height h: 4x^2 + y^2 = 16 - h^2."""
    c = 16.0 - h**2
    return np.sqrt(c) / 2.0, np.sqrt(c)


assert np.allclose(reaches(0), (2.0, 4.0))                      # domain edge 4x^2 + y^2 = 16
assert np.allclose(reaches(2), (np.sqrt(3), np.sqrt(12)))       # 4x^2 + y^2 = 12
assert np.allclose(reaches(4), (0.0, 0.0))                      # the summit (0, 0)
assert abs(float(hill(np.array(0.0), np.array(0.0))) - 4.0) < 1e-12
east_gap = reaches(0)[0] - reaches(2)[0]
north_gap = reaches(0)[1] - reaches(2)[1]
assert abs(east_gap - 0.2679) < 1e-4 and abs(north_gap - 0.5359) < 1e-4
assert abs(north_gap / east_gap - 2.0) < 1e-12                   # twice as close east-west

# ------------------------------------------------------- matplotlib setup
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "path",           # text becomes outlines: same look everywhere
        "svg.hashsalt": "ams261-lab13-banner",
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
            "AMS 261  ·  LAB 13  ·  HILL SURVEY",
            color=NAVY_DARK, fontsize=fs(24), fontweight="bold",
            va="center", ha="left", zorder=4)

    # left text block
    x0 = 52
    ax.text(x0, 196, "MISSION 13 //", color=WHITE, fontsize=fs(54),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.text(x0, 152, "HILL SURVEY", color=CYAN, fontsize=fs(40),
            fontweight="bold", va="baseline", ha="left", zorder=4)
    ax.plot([x0, x0 + 90], [130, 130], color=CYAN, lw=3, solid_capstyle="butt", zorder=4)
    ax.text(x0, 98, "Functions of several", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 64, "variables", color=WHITE, fontsize=fs(30),
            va="baseline", ha="left", zorder=4)
    ax.text(x0, 26, "Ungraded practice  ·  about 30 minutes", color=MUTED,
            fontsize=fs(23), va="baseline", ha="left", zorder=4)

    # ---- right-hand panel: the light plot screen
    px0, px1, py0, py1 = 600.0, 1156.0, 24.0, 244.0
    pw, ph = px1 - px0, py1 - py0
    ax.add_patch(Rectangle((px0 - 5, py0 - 5), pw + 10, ph + 10, fc=NAVY,
                           ec=CYAN, lw=1.8, zorder=2))
    ax.add_patch(Rectangle((px0, py0), pw, ph, fc=SCREEN, ec="none", zorder=2.5))

    halo = [patheffects.withStroke(linewidth=4, foreground=SCREEN)]

    # (a) contour map on equal axes: x in [-2.6, 2.6] km, y in [-4.6, 4.6] km
    y_half = 4.6
    mh = ph - 16.0                         # map height in px
    x_half = y_half * 0.58                 # map width/height ratio chosen so the scale is equal
    mw = mh * x_half / y_half
    mx0, my0 = px0 + 14.0, py0 + 8.0
    max_ = fig.add_axes([mx0 / W, my0 / H, mw / W, mh / H], zorder=3)
    max_.set_facecolor(SCREEN)
    max_.set_xlim(-x_half, x_half)
    max_.set_ylim(-y_half, y_half)
    max_.set_aspect("equal", adjustable="box")
    max_.set_xticks([])
    max_.set_yticks([])
    for s in max_.spines.values():
        s.set_visible(False)
    max_.axhline(0, color=CONTOUR, lw=0.8, alpha=0.5, zorder=1)
    max_.axvline(0, color=CONTOUR, lw=0.8, alpha=0.5, zorder=1)
    t = np.linspace(0, 2 * np.pi, 400)
    for h in (1.0, 3.0):                   # thin grey contours between the three survey heights
        a, b = reaches(h)
        max_.plot(a * np.cos(t), b * np.sin(t), color=CONTOUR, lw=1.3, zorder=2)
    a0, b0 = reaches(0)
    max_.plot(a0 * np.cos(t), b0 * np.sin(t), color=GREEN, lw=2.8, zorder=3)
    a2, b2 = reaches(2)
    max_.plot(a2 * np.cos(t), b2 * np.sin(t), color=BLUE, lw=2.8, zorder=3)
    max_.plot(0, 0, marker="*", ms=13, color=INK, mec=SCREEN, mew=1.2, zorder=4)

    # (b) profiles through the summit
    qx0 = mx0 + mw + 48.0
    qx1 = px1 - 14.0
    qy0, qy1 = py0 + 30.0, py1 - 30.0
    pax = fig.add_axes([qx0 / W, qy0 / H, (qx1 - qx0) / W, (qy1 - qy0) / H], zorder=3)
    pax.set_facecolor(SCREEN)
    pax.set_xlim(-4.3, 4.3)
    pax.set_ylim(0, 4.6)
    pax.set_xticks([])
    pax.set_yticks([])
    for s in pax.spines.values():
        s.set_visible(False)
    pax.axhline(0, color=INK, lw=1.2, zorder=1)
    for h, col in ((0, GREEN), (2, BLUE), (4, INK)):
        pax.axhline(h, color=col, lw=0.9, ls=(0, (3, 3)), alpha=0.7, zorder=1)
    s = np.linspace(-4, 4, 801)
    pax.plot(s, hill(np.zeros_like(s), s), color=CONTOUR, lw=2.4, zorder=2)      # north-south
    se = np.linspace(-2, 2, 801)
    pax.plot(se, hill(se, np.zeros_like(se)), color=SLICE, lw=3.0, zorder=3)     # east-west
    pax.plot(0, 4, marker="*", ms=13, color=INK, mec=SCREEN, mew=1.2, zorder=4)

    # labels
    mtxt = dict(fontsize=fs(19), fontweight="bold", path_effects=halo, zorder=8)
    fig.text((mx0 + mw + 4) / W, (my0 + mh * 0.90) / H, "h = 0", color=GREEN,
             ha="left", va="center", **mtxt)
    fig.text((mx0 + mw + 4) / W, (my0 + mh * 0.73) / H, "h = 2", color=BLUE,
             ha="left", va="center", **mtxt)
    fig.text((mx0 + mw + 4) / W, (my0 + mh * 0.56) / H, "h = 4 ★", color=INK,
             ha="left", va="center", **mtxt)
    fig.text((qx0 + qx1) / 2 / W, (qy1 + 6) / H, "summit (0, 0) · height 4",
             color=INK, ha="center", va="bottom", **mtxt)
    pax.text(2.15, 0.9, "E–W", color=SLICE, ha="left", va="center", **mtxt)
    pax.text(2.85, 3.05, "N–S", color="#64748B", ha="left", va="center", **mtxt)
    fig.text((qx0 + qx1) / 2 / W, (qy0 - 6) / H, "profiles through the summit",
             color=INK, ha="center", va="top", **mtxt)
    return fig


def main():
    root = Path(__file__).resolve().parent.parent
    out = root / "assets"
    out.mkdir(exist_ok=True)
    fig = build()
    fig.savefig(out / "lab13-banner.svg", format="svg", facecolor=NAVY_DARK,
                metadata={"Date": None, "Creator": "make_banner_lab13.py"})
    fig.savefig(out / "lab13-banner.png", format="png", dpi=200, facecolor=NAVY_DARK,
                metadata={"Software": None})
    plt.close(fig)
    print("wrote", out / "lab13-banner.svg")
    print("wrote", out / "lab13-banner.png")
    print(f"east gap {east_gap:.3f} km, north gap {north_gap:.3f} km, ratio {north_gap / east_gap:.1f}")


if __name__ == "__main__":
    main()
