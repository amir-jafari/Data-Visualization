import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons

x = np.linspace(0, 10, 50)
y = np.sin(x ** 2) * np.exp(x)

fig = plt.figure()
ax = fig.subplots()
plt.subplots_adjust(left=0.3, bottom=0.25)
p, = ax.plot(x, y, color='b', label='Plot 1')

ax_button = fig.add_axes([0.25, 0.1, 0.08, 0.05])
grid_button = Button(ax_button, 'Grid', color='white', hovercolor='grey')


def grid(val):
    ax.grid()
    fig.canvas.draw()


grid_button.on_clicked(grid)

ax_color = plt.axes([0.02, 0.5, 0.2, 0.3])
color_button = RadioButtons(ax_color, ['red', 'green', 'blue', 'black'], active=2, activecolor='r')


def color(labels):
    p.set_color(labels)
    fig.canvas.draw()


color_button.on_clicked(color)

y1 = -1 * np.sin(x ** 2) * np.exp(x)
p1, = ax.plot(x, y1, color='b', label='Plot 2', visible=False)
plots = [p, p1]
activated = [True, False]
labels = ['Plot 1', 'Plot 2']

ax_check = plt.axes([0.7, 0.05, 0.08, 0.1])
plot_button = CheckButtons(ax_check, labels, activated)


def select_plot(label):
    index = labels.index(label)
    plots[index].set_visible(not plots[index].get_visible())
    fig.canvas.draw()


plot_button.on_clicked(select_plot)
plt.show()