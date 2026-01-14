import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgba

def colors2cmap(colors, pos=None, name="__"):
    """
    Creates a LinearSegmentedColormap from a list of colors and positions.
    """
    if pos is None:
        pos = np.linspace(0, 1, len(colors), endpoint=True)

    r_target, g_target, b_target, a_target = [], [], [], []
    for c in colors:
        r, g, b, a = to_rgba(c)  # <--- Fix 1: Capture Alpha
        r_target.append(r)
        g_target.append(g)
        b_target.append(b)
        a_target.append(a)

    return LinearSegmentedColormap(
        name,
        {
            "red": list(zip(pos, r_target, r_target)),
            "green": list(zip(pos, g_target, g_target)),
            "blue": list(zip(pos, b_target, b_target)),
            "alpha": list(zip(pos, a_target, a_target)), # <--- Fix 1: Use Alpha
        },
    )

class LinearGradient:
    def __init__(self, cmap, direction="vertical"):
        """
        Apply a linear gradient to the artist.
        """
        # Handle string input (e.g., "viridis")
        if isinstance(cmap, str):
            try:
                self.cmap = plt.get_cmap(cmap)
            except ValueError:
                # Fallback for very new MPL versions if get_cmap fails
                import matplotlib as mpl
                self.cmap = mpl.colormaps[cmap]
        elif isinstance(cmap, LinearSegmentedColormap):
            self.cmap = cmap
        else:
            # Fallback for other colormap types
            self.cmap = cmap

        self.direction = direction

    @classmethod
    def from_colors(cls, colors, pos=None, direction="vertical", cmap_name="__"):
        cmap = colors2cmap(colors, pos, name=cmap_name)
        return cls(cmap, direction=direction)

    def __call__(self, im, dpi):
        h, w, _ = im.shape

        # Fix 2: Vectorization (No loops!)
        if self.direction == "vertical":
            vals = np.linspace(0, 1, h, endpoint=True)
            colors = self.cmap(vals) # Shape: (h, 4)
            
            # Broadcast to image shape: (h, 1, 4) -> (h, w, 4)
            gradient = colors[:, np.newaxis, :] 
            im[:, :, :] = gradient # Apply to R, G, B, and A

        elif self.direction == "horizontal":
            vals = np.linspace(0, 1, w, endpoint=True)
            colors = self.cmap(vals) # Shape: (w, 4)
            
            # Broadcast to image shape: (1, w, 4) -> (h, w, 4)
            gradient = colors[np.newaxis, :, :]
            im[:, :, :] = gradient

        elif self.direction == "diagonal":
            y_indices = np.linspace(0, 1, h)[:, None]
            x_indices = np.linspace(0, 1, w)[None, :]
            factor = (x_indices + y_indices) / 2
            
            colors = self.cmap(factor) # Shape: (h, w, 4)
            im[:, :, :] = colors
        
        else:
            raise ValueError(f"Unknown direction: {self.direction}")

        return im, 0, 0