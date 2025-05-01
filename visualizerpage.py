from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QGraphicsView, QGraphicsScene, QCheckBox
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.integrate import quad

class VisualizerPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Visualizer")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("background-color: #FFFFFF;")

        # Title Label
        title_label = QLabel("Graphique Visualizer", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Amaranth", 40, QFont.Bold))
        title_label.setStyleSheet("color: black;")

        # Left Section (1/3 of the width)
        left_widget = QWidget(self)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20, 20, 20, 20)

        # Empty space (upper 1/3)
        left_layout.addStretch(1)

        # User input section (lower 2/3)
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        # Function Input
        function_label = QLabel("Enter function (in terms of x):")
        function_label.setFont(QFont("Poppins", 18))
        self.function_entry = QLineEdit()
        self.function_entry.setFont(QFont("Poppins", 18))
        input_layout.addWidget(function_label)
        input_layout.addWidget(self.function_entry)

        # X Range Input
        range_label = QLabel("X Range (min, max):")
        range_label.setFont(QFont("Poppins", 18))
        range_layout = QHBoxLayout()
        self.x_min_entry = QLineEdit()
        self.x_min_entry.setFont(QFont("Poppins", 18))
        self.x_max_entry = QLineEdit()
        self.x_max_entry.setFont(QFont("Poppins", 18))
        range_layout.addWidget(self.x_min_entry)
        range_layout.addWidget(self.x_max_entry)
        input_layout.addWidget(range_label)
        input_layout.addLayout(range_layout)

        # Selection for Graph
        selection_label = QLabel("Choose what to plot:")
        selection_label.setFont(QFont("Poppins", 18))
        self.function_checkbox = QCheckBox("Function")
        self.function_checkbox.setFont(QFont("Poppins", 18))
        self.derivative_checkbox = QCheckBox("Derivative")
        self.derivative_checkbox.setFont(QFont("Poppins", 18))
        self.integral_checkbox = QCheckBox("Integral")
        self.integral_checkbox.setFont(QFont("Poppins", 18))

        input_layout.addWidget(selection_label)
        input_layout.addWidget(self.function_checkbox)
        input_layout.addWidget(self.derivative_checkbox)
        input_layout.addWidget(self.integral_checkbox)

        # Plot Button
        self.plot_button = QPushButton("Plot")
        self.plot_button.setFont(QFont("Poppins", 18))
        self.plot_button.clicked.connect(self.plot)
        input_layout.addWidget(self.plot_button)

        left_layout.addLayout(input_layout)
        left_layout.addStretch(2)

        left_widget.setLayout(left_layout)

        # Graph area (2/3 of the width)
        self.graph_widget = QWidget(self)
        self.graph_layout = QVBoxLayout()
        self.graph_area = QGraphicsView(self.graph_widget)
        self.graph_layout.addWidget(self.graph_area)
        self.graph_widget.setLayout(self.graph_layout)

        # Main Layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(self.graph_widget, 2)

        # Overall Layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(main_layout)
        self.setLayout(layout)

    def plot(self):
        func_str = self.function_entry.text()
        try:
            x_min = float(self.x_min_entry.text())
            x_max = float(self.x_max_entry.text())
        except ValueError:
            print("Error: Invalid range input.")
            return

        func, x = self.parse_function(func_str)
        if func is None:
            return

        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = np.array([float(func.subs(x, val)) for val in x_vals])
        dy_vals = np.array([self.numerical_derivative(func, val) for val in x_vals])
        int_vals = np.array([self.numerical_integral(func, val) for val in x_vals])

        # Clear previous graph
        self.graph_area.scene().clear() if self.graph_area.scene() else None

        # Plot using Matplotlib
        plt.figure(figsize=(8, 6))
        if self.function_checkbox.isChecked():
            plt.plot(x_vals, y_vals, label='Function')
        if self.derivative_checkbox.isChecked():
            plt.plot(x_vals, dy_vals, label='First Derivative', linestyle='--')
        if self.integral_checkbox.isChecked():
            plt.plot(x_vals, int_vals, label='Integral', linestyle=':')

        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.legend()
        plt.title("Graphique Visualization")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()

        # Convert matplotlib plot to Qt image
        plt_canvas = self.canvas_from_plt(plt)
        scene = QGraphicsScene()
        scene.addPixmap(plt_canvas)
        self.graph_area.setScene(scene)

    def canvas_from_plt(self, plt):
        from PyQt5.QtGui import QImage, QPixmap
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        canvas = FigureCanvas(plt.gcf())
        canvas.draw()
        width, height = canvas.get_width_height()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
        pixmap = QPixmap(image)
        return pixmap

    def parse_function(self, func_str):
        x = sp.Symbol('x')
        try:
            func = sp.sympify(func_str)
            return func, x
        except sp.SympifyError:
            print("Error: Invalid function syntax.")
            return None, None

    def numerical_derivative(self, func, x_val, dx=1e-5):
        return (float(func.subs('x', x_val + dx)) - float(func.subs('x', x_val - dx))) / (2 * dx)

    def numerical_integral(self, func, x_val):
        return quad(lambda x: float(func.subs('x', x)), 0, x_val)[0]
