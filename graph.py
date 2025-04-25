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

    def plot_function(self, x_vals, y_vals, dy_vals, int_vals, title="Function Visualization"):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        self.ax.plot(x_vals, y_vals, label='Function')
        self.ax.plot(x_vals, dy_vals, label='First Derivative', linestyle='--')
        self.ax.plot(x_vals, int_vals, label='Integral', linestyle=':')

        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.legend()
        self.ax.set_title(title, fontsize=10)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid()

        self.draw()

    def save_plot(self, file_name):
        self.figure.savefig(file_name)