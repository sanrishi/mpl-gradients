import pytest
import matplotlib.pyplot as plt
from mpl_gradients import apply_gradient  # <--- importing the CORRECT name

def test_import():
    """Test that the library imports without crashing."""
    # We check for 'apply_gradient', not 'gradient_fill'
    assert apply_gradient is not None

def test_run_without_error():
    """Test that the function runs on a dummy plot without crashing."""
    fig, ax = plt.subplots()
    bars = ax.bar([1, 2, 3], [1, 2, 3])
    
    # Try running your function
    try:
        # We use 'apply_gradient' here too
        apply_gradient(bars, direction="vertical", colors=["red", "blue"])
        assert True
    except Exception as e:
        pytest.fail(f"apply_gradient raised an exception: {e}")
