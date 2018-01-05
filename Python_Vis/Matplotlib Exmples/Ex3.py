import matplotlib.pyplot as plt
from numpy.random import rand


fig, ax = plt.subplots()
for color in ['red', 'green', 'blue']:
    n = 100
    x, y = rand(2, n)
    scale = 200.0 * rand(n)
    ax.scatter(x, y, c=color, s=scale, label=color, alpha=10, edgecolors='none')

ax.legend()
ax.grid(True)

plt.show()