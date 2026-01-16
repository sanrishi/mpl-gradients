



[![PyPI version](https://badge.fury.io/py/mpl-gradients.svg)](https://badge.fury.io/py/mpl-gradients)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<img width="700" height="353" alt="image" src="https://github.com/user-attachments/assets/4a6ce8e4-724d-4254-a7c8-176cab27db0c" />

A zero-dependency plotting utility that implements vectorized gradient rendering for Matplotlib Figure and Axes objects. Unlike other styling libraries that require heavy dependencies (like Pillow or Qt), mpl-gradients leverages NumPy broadcasting to generate gradient arrays directly within the Matplotlib canvas.

<img width="826" height="415" alt="image" src="https://github.com/user-attachments/assets/1d17679a-6162-43f2-aab5-5e53642d1482" />

 This approach ensures compatibility with all Matplotlib backends while maintaining a minimal footprint. Key features include support for variable alpha channels (transparency), arbitrary gradient angles, and multi-color transitions, all optimized for rendering speed.
 
<img width="826" height="363" alt="image" src="https://github.com/user-attachments/assets/cf069f22-03ce-49ba-ae66-1ad764b45b02" />




## 📦 Installation

```bash
pip install mpl-gradients

## Features
* **Vertical Gradients:** Fade from Top to Bottom.
* **Horizontal Gradients:** Fade from Left to Right.
* **Diagonal Gradients:** Fade from Corner to Corner.
* **Alpha Blending:** Correctly handles transparency.

## Installation

You can install directly from GitHub:

```bash
pip install mpl-gradients
```

## Quick start 
```python
import matplotlib.pyplot as plt
from mpl_gradients import LinearGradient

fig, ax = plt.subplots()
ax.bar([0, 1, 2], [10, 20, 15])

# Create a gradient (Top-Left Navy -> Bottom-Right Lime)
gradient = LinearGradient("navy", "lime", direction="diagonal")

# Apply to bars
for bar in ax.containers[0]:
    bar.set_agg_filter(gradient)

plt.show()
```
## Requirements
Python 3.9+

Matplotlib

Numpy

## New in v0.2.1: Transparency Support

You can now create gradients that fade to transparent!

By default, gradients preserve the original alpha of the plot (`preserve_alpha=True`).
To create transparent gradients (e.g., Red -> Transparent), set `preserve_alpha=False`.

```python
from mpl_gradients import LinearGradient

# Create a gradient that fades from Red to Transparent to Green
gradient = LinearGradient.from_colors(
    ["red", "#ffffff00", "green"],
    preserve_alpha=False
)

# Apply it
ax.fill_between(x, y, color="blue").set_agg_filter(gradient)
