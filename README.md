<p align="center">
  <img src="assets/lab18-banner.png" width="100%" alt="Banner for AMS 261 Lab 18, Mission 18, Rover Field Test: directional derivatives and the gradient. A plot shows the isotherms of T(x, y) = 20 minus 4x squared minus y squared, the point P = (2, −3), the gradient arrow at P in blue and the two zero-change headings as green dashed lines.">
</p>

# AMS 261 Labs

![practice: not graded](https://img.shields.io/badge/practice-not%20graded-22D3EE?labelColor=0A0E14)
![time: ~30 min](https://img.shields.io/badge/time-~30%20min-22D3EE?labelColor=0A0E14)

Practice notebooks for AMS 261 (Multivariable Calculus) at SUNY Korea.
Each lab follows one lecture. It lets you predict, compute, plot and check the ideas of that lecture in Python.

## Labs

| Lab | Topic | Open |
|:---|:---|:---|
| Lab 18 | Directional Derivatives and the Gradient | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tancao1128/ams261-labs/blob/main/labs/AMS261-Lecture18.ipynb) [![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tancao1128/ams261-labs/main?labpath=labs%2FAMS261-Lecture18.ipynb) [Download](https://raw.githubusercontent.com/tancao1128/ams261-labs/main/labs/AMS261-Lecture18.ipynb) |

## Preview

In Lab 18, a heat-seeking rover sits on a metal plate. The temperature is T(x, y) = 20 − 4x² − y² (°C, with x and y in cm). At the point P = (2, −3), the gradient is ∇T(P) = ⟨−16, 6⟩. The animation turns the heading φ once around the compass. Left: the rate of change D<sub>u</sub>T(P) = −16 cos φ + 6 sin φ. Right: the gradient (blue), the opposite direction (red), the two zero-change headings (green) and the heading u (amber).

<p align="center">
  <img src="assets/lab18-preview.gif" width="720" alt="Animation of a heading sweep at the point P = (2, −3). On the left, a cosine curve of the directional derivative against the heading angle phi, with a moving amber dot. On the right, a compass showing the gradient in blue, the negative gradient in red, the two zero-change headings in green dashed lines and the current heading u in amber.">
</p>

## How to open a lab

- **Colab (recommended).** Click the Colab badge. Sign in with a Google account. Choose *Runtime → Run all*, or run the cells one by one with Shift+Enter. To keep your work, choose *File → Save a copy in Drive*.
- **Binder.** Click the Binder badge. No account is needed. The first launch can take a few minutes. Binder does not save your work, so download the notebook before you close the tab.
- **Download.** Use the *Download* link (right-click → *Save link as…*). Open the `.ipynb` file in Jupyter or VS Code. You need Python 3 with the packages in `requirements.txt`.

## Ground rules

- **Labs are ungraded practice.** Nothing here counts toward your grade. Homework is submitted on Gradescope as usual.
- **AI use.** Each lab contains a short student AI contract and a verification rule in its *AI Learning Companion* section. If you use an AI tool, paste that contract first and follow it.

## License

© Tan H. Cao, for AMS 261 students. All rights reserved.
