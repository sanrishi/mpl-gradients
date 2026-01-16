import pytest
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_gradients import apply_gradient, LinearGradient

# 1. SETUP FIXTURE
@pytest.fixture
def ax():
    """Creates a fresh plot for every test."""
    fig, ax = plt.subplots()
    return ax

# 2. PARAMETERIZED TEST: Directions
@pytest.mark.parametrize("direction", ["vertical", "horizontal", "diagonal"])
def test_gradient_directions(ax, direction):
    """Test that LinearGradient accepts all valid directions."""
    bars = ax.bar([1, 2], [10, 20])
    
    # Correct Usage: Create the object FIRST
    grad = LinearGradient("viridis", direction=direction)
    
    # Then apply it
    apply_gradient(bars, grad)
    
    # Check if it didn't crash
    assert len(bars) == 2

# 3. TEST: Custom Colors (using .from_colors)
def test_custom_colors(ax):
    """Test creating a gradient from a custom list of colors."""
    bars = ax.bar([1], [1])
    
    # Correct Usage: Use the class method
    grad = LinearGradient.from_colors(["red", "blue"], direction="vertical")
    
    apply_gradient(bars, grad)

# 4. TEST: Transparent Colors (preserve_alpha=False)
def test_transparency_handling(ax):
    """Test that we can set preserve_alpha=False for transparent gradients."""
    rect = Rectangle((0,0), 1, 1)
    ax.add_patch(rect)
    
    # Create a gradient with transparency
    grad = LinearGradient.from_colors(
        ["red", "#ffffff00"], 
        preserve_alpha=False
    )
    
    apply_gradient(rect, grad)
    # If the function runs without error, the test passes

# 5. TEST: Error Handling (The "Sad Path")
def test_raises_error_on_invalid_direction():
    """Test that the class raises ValueError for bad directions."""
    
    with pytest.raises(ValueError):
        # This should fail because 'circular' is not supported
        LinearGradient("viridis", direction="circular")

def test_apply_to_single_artist(ax):
    """Test applying to a single patch (not a list)."""
    rect = Rectangle((0,0), 1, 1)
    ax.add_patch
