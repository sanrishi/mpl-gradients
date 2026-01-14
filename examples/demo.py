"""
Complete demonstration of mpl-gradients library features.
"""
import matplotlib.pyplot as plt
import numpy as np
from mpl_gradients import LinearGradient

def fill_between_chart_1(ax):
    x = np.linspace(0, 10, 100)
    y = x * np.exp(-x)
    gradient = LinearGradient("Blues_r", direction="vertical")
    ax.plot(x, y, color="darkblue", lw=1.5, label="line")
    fb_pc = ax.fill_between(x, y, alpha=1, lw=0)
    fb_pc.set_agg_filter(gradient)
    ax.legend(loc="upper right")
    ax.set_title("Built-in Colormap\n(Blues_r)")

def fill_between_chart_2(ax):
    x = np.linspace(0, 3, 100) * np.pi
    y = np.sin(x)
    
    # VISUAL PROOF: Turn on the grid!
    ax.grid(True, linestyle="--", alpha=0.5, color="black", zorder=0)

    gradient = LinearGradient.from_colors(
        ["red", "#ffffff00", "green"],
        preserve_alpha=False
    )
    ax.plot(x, y, color="k", lw=1.5, label="line", zorder=3)
    fb_pc = ax.fill_between(x, y, color="blue", alpha=1, lw=0, zorder=2)
    fb_pc.set_agg_filter(gradient)
    ax.legend(loc="upper right")
    ax.set(xlim=(0, 3 * np.pi), ylim=(-1.1, 1.1))
    ax.set_title("Transparent Middle\n(Grid visible = truly transparent!)", fontsize=10)

def bar_chart(ax):
    np.random.seed(19680801)
    x = np.linspace(0, 1, 11, endpoint=True)
    y = np.random.rand(11)
    colors = plt.cm.Blues_r(np.linspace(0, 0.6, 100))
    gradient = LinearGradient.from_colors(colors, direction="diagonal")
    ax.set(xlim=(-0.1, 1.1), ylim=(0, 1))
    rects = ax.bar(x, y, width=0.07, align="center", label="bar", color=colors[0])
    for rect in rects:
        rect.set_agg_filter(gradient)
    ax.legend(loc="upper right")
    ax.set_title("Diagonal Gradient Bars")

def background(ax):
    ax.patch.set_alpha(0.5)
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, 100))
    gradient = LinearGradient.from_colors(colors, direction="horizontal")
    ax.patch.set_agg_filter(gradient)
    np.random.seed(19680801)
    x = np.linspace(0, 1, 11, endpoint=True)
    y = np.random.rand(11)
    bar_colors = plt.cm.Blues_r(np.linspace(0, 0.6, 100))
    bar_gradient = LinearGradient.from_colors(bar_colors, direction="diagonal")
    ax.set(xlim=(-0.1, 1.1), ylim=(0, 1))
    rects = ax.bar(x, y, width=0.07, align="center", label="bar", color=bar_colors[0])
    for rect in rects:
        rect.set_agg_filter(bar_gradient)
    ax.legend(loc="upper right")
    ax.set_title("Gradient Background\n+ Gradient Bars")

def main():
    """Create comprehensive demo figure."""
    fig, axs = plt.subplots(2, 2, figsize=(10, 10), dpi=150)
    fig.suptitle("mpl-gradients Demo (v0.2.0)", fontsize=16, fontweight="bold")
    
    fill_between_chart_1(axs[0, 0])
    fill_between_chart_2(axs[0, 1])
    bar_chart(axs[1, 0])
    background(axs[1, 1])

    plt.tight_layout()
    
    # FINAL LAYOUT FIX:
    # top=0.88   -> Leaves room for the main title
    # hspace=0.4 -> Adds gap between the top and bottom rows (Fixes the crash!)
    plt.subplots_adjust(top=0.88, hspace=0.4)
    
    plt.savefig("gradient_demo.png", dpi=150, bbox_inches="tight")
    print("✓ Saved gradient_demo.png")
    plt.show()

if __name__ == "__main__":
    main()