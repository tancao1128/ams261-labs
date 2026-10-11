#!/usr/bin/env python3
"""Build assets/lab18-preview.gif: a heading sweep at P = (2, -3).

Run from anywhere:  python3 tools/make_preview_gif.py
Needs numpy, matplotlib and Pillow. The output is deterministic.

For T(x, y) = 20 - 4x^2 - y^2 we have grad T(P) = <-16, 6>, so
D_u T(P) = -16 cos(phi) + 6 sin(phi) for u = (cos phi, sin phi).
Left: this cosine curve with a moving amber dot.
Right: a compass with grad T, -grad T, the two zero-change headings and u.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch
from PIL import Image

NAVY_DARK = "#0A0E14"
NAVY = "#0F1A2B"
CYAN = "#22D3EE"
INK = "#1E293B"
BLUE = "#2563EB"
RED = "#DC2626"
GREEN = "#059669"
AMBER = "#D97706"
CONTOUR = "#94A3B8"
LIGHT = "#CBD5E1"      # text on the navy frame
SCREEN = "#F8FAFC"
WHITE = "#F1F5F9"

g = np.array([-16.0, 6.0])
AMP = float(np.hypot(*g))                       # sqrt(292) = 17.09
PHI_GRAD = float(np.degrees(np.arctan2(g[1], g[0])) % 360)      # 159.44
PHI_ZERO = [(PHI_GRAD - 90) % 360, (PHI_GRAD + 90) % 360]       # 69.44, 249.44
PHI_MIN = (PHI_GRAD + 180) % 360                                # 339.44
assert abs(PHI_GRAD - 159.44) < 0.01
assert abs(sorted(PHI_ZERO)[0] - 69.44) < 0.01 and abs(sorted(PHI_ZERO)[1] - 249.44) < 0.01


def D(phi_deg):
    p = np.radians(phi_deg)
    return g[0] * np.cos(p) + g[1] * np.sin(p)


plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans"})

N_FRAMES = 40
FPS = 8
W_IN, H_IN, DPI = 8.4, 4.4, 100                 # 840 x 440 px


def vec(deg, r=1.0):
    a = np.radians(deg)
    return r * np.cos(a), r * np.sin(a)


def draw_frame(phi):
    fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=NAVY_DARK)

    # HUD frame
    fa = fig.add_axes([0, 0, 1, 1])
    fa.set_xlim(0, W_IN * DPI)
    fa.set_ylim(0, H_IN * DPI)
    fa.axis("off")
    w, h = W_IN * DPI, H_IN * DPI
    fa.plot([5, w - 5, w - 5, 5, 5], [5, 5, h - 5, h - 5, 5], color=CYAN, lw=0.8, alpha=0.55)
    for cx, sx in ((5, 1), (w - 5, -1)):
        for cy, sy in ((5, 1), (h - 5, -1)):
            fa.plot([cx + sx * 18, cx, cx], [cy, cy, cy + sy * 18], color=CYAN, lw=2.2,
                    solid_capstyle="butt")
    sign = "+" if D(phi) >= 0 else "−"
    fa.text(26, h - 30, f"HEADING  φ = {phi:06.2f}°", color=WHITE, fontsize=14,
            fontweight="bold", va="center", ha="left")
    fa.text(w - 26, h - 30, rf"$D_{{\mathbf{{u}}}}T(P)$ = {sign}{abs(D(phi)):05.2f}",
            color=CYAN, fontsize=14, fontweight="bold", va="center", ha="right")
    fa.text(26, 20, "P = (2, −3)    ∇T(P) = ⟨−16, 6⟩",
            color=LIGHT, fontsize=10, va="center", ha="left")
    fa.text(w - 26, 20, "AMS 261  ·  LAB 18", color=LIGHT, fontsize=10, va="center", ha="right")

    # ---- left screen: cosine curve
    ax = fig.add_axes([0.085, 0.19, 0.45, 0.63], facecolor=SCREEN)
    t = np.linspace(0, 360, 721)
    ax.plot(t, D(t), color=INK, lw=2.2, zorder=3)
    ax.axhline(0, color=CONTOUR, lw=1, zorder=1)
    ax.set_xlim(0, 360)
    ax.set_ylim(-20, 20)
    ax.set_xticks([0, 90, 180, 270, 360])
    ax.set_yticks([-16, -8, 0, 8, 16])
    ax.tick_params(colors=LIGHT, labelsize=9, length=3)
    ax.grid(color=CONTOUR, alpha=0.3, lw=0.7)
    for s in ax.spines.values():
        s.set_color(CONTOUR)
    ax.set_xlabel("heading φ (degrees)", color=LIGHT, fontsize=10, labelpad=2)
    ax.set_ylabel(r"$D_{\mathbf{u}}T(P)$", color=LIGHT, fontsize=11, labelpad=0)
    # special headings on the curve
    ax.plot([PHI_GRAD], [AMP], "o", ms=8, mfc=BLUE, mec=SCREEN, mew=1.5, zorder=4)
    ax.plot([PHI_MIN], [-AMP], "o", ms=8, mfc=RED, mec=SCREEN, mew=1.5, zorder=4)
    ax.plot(PHI_ZERO, [0, 0], "o", ms=8, mfc=GREEN, mec=SCREEN, mew=1.5, zorder=4)
    # moving dot and drop line
    ax.plot([phi, phi], [0, D(phi)], color=AMBER, lw=1.6, ls=":", zorder=4)
    ax.plot([phi], [D(phi)], "o", ms=11, mfc=AMBER, mec=NAVY_DARK, mew=1.5, zorder=6, clip_on=False)

    # ---- right screen: compass
    cx_ = fig.add_axes([0.585, 0.19, 0.385, 0.63], facecolor=SCREEN)
    R = 1.55
    cx_.set_xlim(-R, R)
    cx_.set_ylim(-R, R)
    cx_.set_aspect("equal", adjustable="box")
    cx_.set_xticks([])
    cx_.set_yticks([])
    for s in cx_.spines.values():
        s.set_color(CONTOUR)
    cx_.add_patch(Circle((0, 0), 1.0, fc="none", ec=CONTOUR, lw=1.4, zorder=1))
    for a in range(0, 360, 30):
        x0, y0 = vec(a, 0.94)
        x1, y1 = vec(a, 1.0)
        cx_.plot([x0, x1], [y0, y1], color=CONTOUR, lw=1.2, zorder=1)
    for a in (0, 90, 180, 270):
        x, y = vec(a, 1.36)
        cx_.text(x, y, f"{a}°", color=CONTOUR, fontsize=9, ha="center", va="center")
    cx_.axhline(0, color=CONTOUR, lw=0.6, alpha=0.5, zorder=0)
    cx_.axvline(0, color=CONTOUR, lw=0.6, alpha=0.5, zorder=0)

    # zero-change headings: green dashed
    for a in PHI_ZERO:
        x, y = vec(a, 1.0)
        cx_.plot([0, x], [0, y], color=GREEN, lw=2.2, ls=(0, (4, 2.4)), zorder=3)
        xt, yt = vec(a, 1.2)
        cx_.text(xt, yt, "D=0", color=GREEN, fontsize=9, fontweight="bold",
                 ha="center", va="center", zorder=5)
    # minus gradient: red dash-dot
    x, y = vec(PHI_MIN, 1.0)
    cx_.plot([0, x], [0, y], color=RED, lw=2.4, ls=(0, (6, 2, 1.5, 2)), zorder=3)
    xt, yt = vec(PHI_MIN, 1.2)
    cx_.text(xt, yt, r"$-\nabla T$", color=RED, fontsize=11, fontweight="bold",
             ha="center", va="center", zorder=5)
    # gradient: blue solid arrow
    x, y = vec(PHI_GRAD, 1.0)
    cx_.add_patch(FancyArrowPatch((0, 0), (x, y), arrowstyle="-|>", mutation_scale=16,
                                  lw=2.6, color=BLUE, shrinkA=0, shrinkB=0, zorder=4))
    xt, yt = vec(PHI_GRAD, 1.2)
    cx_.text(xt, yt, r"$\nabla T$", color=BLUE, fontsize=11, fontweight="bold",
             ha="center", va="center", zorder=5)
    # u: amber arrow, shorter, label inside the circle
    x, y = vec(phi, 0.66)
    cx_.add_patch(FancyArrowPatch((0, 0), (x, y), arrowstyle="-|>", mutation_scale=18,
                                  lw=3.2, color=AMBER, shrinkA=0, shrinkB=0, zorder=6))
    xt, yt = vec(phi, 0.80)
    cx_.text(xt, yt, "u", color=AMBER, fontsize=13, fontweight="bold", fontstyle="italic",
             ha="center", va="center", zorder=7,
             bbox=dict(boxstyle="round,pad=0.12", fc=SCREEN, ec="none", alpha=0.85))
    cx_.plot([0], [0], "o", ms=5, mfc=INK, mec=INK, zorder=8)

    fig.canvas.draw()
    img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy(), "RGB")
    plt.close(fig)
    return img


def main():
    root = Path(__file__).resolve().parent.parent
    out = root / "assets"
    out.mkdir(exist_ok=True)
    phis = [360.0 * k / N_FRAMES for k in range(N_FRAMES)]
    frames = [draw_frame(p) for p in phis]

    # One shared palette for all frames: smaller file and no colour flicker.
    sample = Image.new("RGB", (frames[0].width, frames[0].height * 4))
    for i, k in enumerate((0, 10, 20, 30)):
        sample.paste(frames[k], (0, i * frames[0].height))
    pal = sample.quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]

    path = out / "lab18-preview.gif"
    q[0].save(path, save_all=True, append_images=q[1:], duration=int(round(1000 / FPS)),
              loop=0, optimize=False, disposal=1)
    print("wrote", path, f"({path.stat().st_size / 1024:.0f} KB, {len(q)} frames)")


if __name__ == "__main__":
    main()
