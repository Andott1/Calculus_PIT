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

        # Adjust margins to provide more space to the right side for the legend
        self.figure.subplots_adjust(right=0.8)  # Increase this value to provide more space to the right

        # Set legend properties and clip it if necessary
        self.ax.legend(
            loc='upper left',  # Position of the legend
            bbox_to_anchor=(1, 1),  # Position the legend outside the plot (on the right side)
            ncol=1,  # Number of columns in the legend
            frameon=False,  # Turn off the frame for a cleaner look
            fontsize=8,  # Set a smaller font size to reduce the size of the legend
            borderpad=1,  # Padding around the legend box
            labelspacing=1.5,  # Space between legend labels
            columnspacing=1.5  # Space between columns in the legend (if there are multiple columns)
        )

        # Ensure that the legend box is clipped if it's overflowing
        self.ax.margins(0.05)
        
        # Drawing the plot
        self.draw()

    def save_plot(self, file_name):
        # Save the current figure as an image
        self.figure.savefig(file_name)