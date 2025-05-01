import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure()
        super().__init__(self.figure)
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)

    def plot_function(self, x_vals, y_vals_list, dy_vals_list, int_vals, title="Function Visualization"):
        # Clear the figure before plotting
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        # Plot the original function
        self.ax.plot(x_vals, y_vals_list[0], label='Original Function', color='b')

        # Plot all derivatives
        for i in range(1, len(y_vals_list)):
            self.ax.plot(x_vals, y_vals_list[i], label=f'{i}th Derivative', linestyle='--')

        # Plot the integral (if provided)
        if int_vals is not None:
            self.ax.plot(x_vals, int_vals, label='Integral', linestyle=':')

        # Draw a horizontal and vertical line through the origin
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

        # Set title and labels
        self.ax.set_title(title, fontsize=10)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid()

        # Set legend properties and clip it if necessary
        self.ax.legend(
            loc='upper right',  # or 'upper left', 'lower left', etc.
            fontsize=8,
            frameon=False,
            borderpad=1,
            labelspacing=1.2
        )

        # Ensure that the legend box is clipped if it's overflowing
        self.ax.margins(0.05)
        
        # Drawing the plot
        self.draw()

    def save_plot(self, file_name):
        # Save the current figure as an image
        self.figure.savefig(file_name)