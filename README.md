# mpl-gradients
![Gradient Demo](assets/polished_demo.png)
A lightweight library to add linear gradient fills to Matplotlib charts.

## Usage

```python
import matplotlib.pyplot as plt
from gradients import LinearGradient

# Create a gradient (vertical, horizontal, or diagonal)
grad = LinearGradient("navy", "lime", direction="diagonal")

# Apply to your bar chart
bars = plt.bar([0, 1], [10, 20])
for bar in bars:
    bar.set_agg_filter(grad)

plt.show()