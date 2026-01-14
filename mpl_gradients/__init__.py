"""
mpl-gradients: Linear gradient fills for Matplotlib using AGG filters.

This package provides gradient fill support for Matplotlib charts by leveraging
AGG filters. Gradients only work with AGG-based backends (not SVG/PDF).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgba

__version__ = "0.1.0"
__all__ = ["LinearGradient", "colors2cmap", "apply_gradient"]


def colors2cmap(colors, pos=None, name="__"):
    """
    Creates a LinearSegmentedColormap from a list of colors and positions.
    
    Parameters
    ----------
    colors : list
        List of color specifications (names, hex, RGB tuples, RGBA tuples, etc.)
    pos : array-like, optional
        Positions for each color in [0, 1]. If None, colors are evenly spaced.
    name : str, optional
        Name for the colormap
        
    Returns
    -------
    LinearSegmentedColormap
        A colormap that interpolates between the given colors
        
    Examples
    --------
    >>> # Simple two-color gradient
    >>> cmap = colors2cmap(["red", "blue"])
    
    >>> # Multi-color with custom positions
    >>> cmap = colors2cmap(
    ...     ["red", "yellow", "green"],
    ...     pos=[0, 0.3, 1.0]
    ... )
    
    >>> # Transparent middle (for preserve_alpha=False)
    >>> cmap = colors2cmap(["red", "#ffffff00", "green"])
    """
    if pos is None:
        pos = np.linspace(0, 1, len(colors), endpoint=True)

    r_target, g_target, b_target, a_target = [], [], [], []
    for c in colors:
        r, g, b, a = to_rgba(c)
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
            "alpha": list(zip(pos, a_target, a_target)),
        },
    )


class LinearGradient:
    """
    Apply a linear gradient fill to matplotlib artists using AGG filters.
    
    This class creates gradient effects by modifying the pixel colors of rendered
    artists. It only works with AGG-based backends (the default for most uses).
    Vector backends like SVG and PDF will ignore the gradient.
    
    Parameters
    ----------
    cmap : str or Colormap
        Colormap name (e.g., "viridis", "Blues") or Colormap instance
    direction : str, default "vertical"
        Gradient direction: "vertical", "horizontal", or "diagonal"
    preserve_alpha : bool, default True
        If True, only apply gradient to RGB channels, preserving original alpha.
        If False, gradient affects RGBA channels (use this for transparent gradients).
        
    Examples
    --------
    >>> # Basic vertical gradient using matplotlib colormap
    >>> gradient = LinearGradient("Blues", direction="vertical")
    >>> bars = ax.bar([1, 2, 3], [4, 5, 6])
    >>> for bar in bars:
    ...     bar.set_agg_filter(gradient)
    
    >>> # Custom two-color gradient
    >>> gradient = LinearGradient.from_colors(["red", "yellow"])
    >>> fill = ax.fill_between(x, y)
    >>> fill.set_agg_filter(gradient)
    
    >>> # Transparent middle gradient (IMPORTANT: preserve_alpha=False)
    >>> gradient = LinearGradient.from_colors(
    ...     ["red", "#ffffff00", "green"],
    ...     preserve_alpha=False  # Required for transparency!
    ... )
    
    Notes
    -----
    - Only works with AGG backend (default for most matplotlib uses)
    - Vector backends (SVG, PDF) will ignore gradients
    - For transparent color stops, you MUST set preserve_alpha=False
    """
    
    def __init__(self, cmap, direction="vertical", preserve_alpha=True):
        # Handle string input (e.g., "viridis")
        if isinstance(cmap, str):
            try:
                self.cmap = plt.get_cmap(cmap)
            except (ValueError, AttributeError):
                # Fallback for matplotlib >= 3.5
                import matplotlib as mpl
                self.cmap = mpl.colormaps[cmap]
        else:
            # Accept any colormap-like object
            self.cmap = cmap

        if direction not in ("vertical", "horizontal", "diagonal"):
            raise ValueError(
                f"Invalid direction '{direction}'. "
                "Must be 'vertical', 'horizontal', or 'diagonal'."
            )
        
        self.direction = direction
        self.preserve_alpha = preserve_alpha

    @classmethod
    def from_colors(cls, colors, pos=None, direction="vertical", 
                    cmap_name="__", preserve_alpha=True):
        """
        Create a LinearGradient from a list of colors.
        
        This is the recommended way to create custom gradients with specific colors.
        
        Parameters
        ----------
        colors : list
            List of colors (names, hex codes, or RGBA tuples).
            Examples: ["red", "blue"], ["#ff0000", "#0000ff"], 
                     [(1,0,0,1), (0,0,1,1)]
        pos : array-like, optional
            Positions for each color in [0, 1]. If None, colors are evenly spaced.
            Example: [0, 0.3, 1.0] for red at start, yellow at 30%, green at end.
        direction : str, default "vertical"
            Gradient direction: "vertical", "horizontal", or "diagonal"
        cmap_name : str, optional
            Internal name for the colormap (usually not needed)
        preserve_alpha : bool, default True
            Whether to preserve original alpha channel.
            Set to False for transparent color stops like "#ffffff00"
            
        Returns
        -------
        LinearGradient
        
        Examples
        --------
        >>> # Simple two-color gradient
        >>> gradient = LinearGradient.from_colors(["red", "yellow"])
        
        >>> # Multi-stop gradient with positions
        >>> gradient = LinearGradient.from_colors(
        ...     colors=["red", "yellow", "green"],
        ...     pos=[0, 0.5, 1.0]
        ... )
        
        >>> # Transparent middle (CRITICAL: preserve_alpha=False)
        >>> gradient = LinearGradient.from_colors(
        ...     ["red", "#ffffff00", "green"],
        ...     preserve_alpha=False  # <-- REQUIRED for transparency!
        ... )
        
        >>> # Horizontal gradient
        >>> gradient = LinearGradient.from_colors(
        ...     ["navy", "cyan"],
        ...     direction="horizontal"
        ... )
        """
        cmap = colors2cmap(colors, pos, name=cmap_name)
        return cls(cmap, direction=direction, preserve_alpha=preserve_alpha)

    def __call__(self, im, dpi):
        """
        Apply the gradient filter to an image array.
        
        This is called automatically by matplotlib's AGG filter system.
        Users typically don't call this directly.
        
        Parameters
        ----------
        im : ndarray
            Image array of shape (h, w, 4) in RGBA format
        dpi : float
            DPI of the figure (unused but required by AGG filter interface)
            
        Returns
        -------
        tuple
            (modified_image, x_offset, y_offset)
        """
        h, w = im.shape[:2]

        if self.direction == "vertical":
            # Create vertical gradient: varies with height (top to bottom)
            vals = np.linspace(0, 1, h, endpoint=True)
            colors = self.cmap(vals)  # Shape: (h, 4)
            gradient = colors[:, np.newaxis, :]  # Broadcast: (h, 1, 4) -> (h, w, 4)

        elif self.direction == "horizontal":
            # Create horizontal gradient: varies with width (left to right)
            vals = np.linspace(0, 1, w, endpoint=True)
            colors = self.cmap(vals)  # Shape: (w, 4)
            gradient = colors[np.newaxis, :, :]  # Broadcast: (1, w, 4) -> (h, w, 4)

        elif self.direction == "diagonal":
            # Create diagonal gradient: varies with both dimensions
            y_indices = np.linspace(0, 1, h)[:, None]
            x_indices = np.linspace(0, 1, w)[None, :]
            factor = (x_indices + y_indices) / 2
            gradient = self.cmap(factor)  # Shape: (h, w, 4)

        # Apply gradient
        if self.preserve_alpha:
            # Only change RGB, keep original alpha (typical use case)
            im[:, :, :3] = gradient[:, :, :3]
        else:
            # Replace RGBA entirely (needed for transparent color stops)
            im[:, :, :4] = gradient

        return im, 0, 0
    
    def __repr__(self):
        return (f"LinearGradient(cmap={self.cmap.name}, "
                f"direction='{self.direction}', "
                f"preserve_alpha={self.preserve_alpha})")


def apply_gradient(artist, gradient):
    """
    Helper function to apply gradient to a single artist or collection.
    
    This is a convenience function that handles both single artists and
    collections (like BarContainer).
    
    Parameters
    ----------
    artist : Artist or iterable of Artists
        Matplotlib artist(s) to apply gradient to
    gradient : LinearGradient
        Gradient filter to apply
        
    Examples
    --------
    >>> bars = ax.bar([1, 2, 3], [4, 5, 6])
    >>> gradient = LinearGradient("viridis")
    >>> apply_gradient(bars, gradient)
    
    >>> # Equivalent to manually iterating:
    >>> for bar in bars:
    ...     bar.set_agg_filter(gradient)
    """
    try:
        # Try to iterate (for BarContainer, etc.)
        for item in artist:
            item.set_agg_filter(gradient)
    except TypeError:
        # Single artist
        artist.set_agg_filter(gradient)