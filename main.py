from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QTextEdit
import numpy as np
import sympy as sp
from scipy.integrate import quad, cumulative_trapezoid
from graph import PlotWidget 

class FunctionVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Function Visualizer")
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Enter function (in terms of x; ex. \"2*x**2 + 4*x + 1\"):"))
        self.function_entry = QLineEdit()
        layout.addWidget(self.function_entry)
        
        layout.addWidget(QLabel("X Range (min, max):"))
        range_layout = QHBoxLayout()
        self.x_min_entry = QLineEdit()
        self.x_max_entry = QLineEdit()
        range_layout.addWidget(self.x_min_entry)
        range_layout.addWidget(self.x_max_entry)
        layout.addLayout(range_layout)
        
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot)
        layout.addWidget(self.plot_button)

        self.save_button = QPushButton("Save Plot")
        self.save_button.clicked.connect(self.save_plot)
        layout.addWidget(self.save_button)

        # Use the PlotWidget instead of directly using Matplotlib
        self.plot_widget = PlotWidget()
        layout.addWidget(self.plot_widget)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("Function details will appear here...")
        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def parse_function(self, func_str):
        x = sp.Symbol('x')
        try:
            func = sp.sympify(func_str)
            return func, x
        except sp.SympifyError:
            self.warning(warning="Invalid function syntax.\nExample: 3*x**2 + 2*x - 4")
            return None, None
    
    def numerical_derivative(self, func, x_val, dx=1e-5):
        return (func.subs('x', x_val + dx).evalf() - func.subs('x', x_val - dx).evalf()) / (2 * dx)
    
    def plot(self):
        func_str = self.function_entry.text()
        try:
            x_min = float(self.x_min_entry.text())
            x_max = float(self.x_max_entry.text())
        except ValueError:
            self.warning(warning="Invalid range input.")
            return
        
        func, x = self.parse_function(func_str)
        if func is None:
            return
            
        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = np.array([func.subs(x, val).evalf() for val in x_vals], dtype=np.float64)
        dy_vals = np.array([self.numerical_derivative(func, val) for val in x_vals], dtype=np.float64)
        int_vals = cumulative_trapezoid(y_vals, x_vals, initial=0)

        # Symbolic derivatives and integral for display
        func_diff = sp.diff(func, x)
        func_integral = sp.integrate(func, x)

        # Update label with formatted math expressions
        self.result_box.setPlainText(
            f"Original Function:\n  f(x) = {sp.simplify(func)}\n\n"
            f"First Derivative:\n  f'(x) = {sp.simplify(func_diff)}\n\n"
            f"Integral:\n  ∫f(x)dx = {sp.simplify(func_integral)} + C"
        )

        # Use the PlotWidget to plot
        self.plot_widget.plot_function(x_vals, y_vals, dy_vals, int_vals)

    def save_plot(self):
        """Opens a file dialog to save the plot as an image."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
        
        if file_name:
            self.plot_widget.save_plot(file_name)
            print(f"Plot saved as: {file_name}")

    def warning(self, warning):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(warning)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        

if __name__ == "__main__":
    app = QApplication([])
    window = FunctionVisualizer()
    window.show()
    app.exec_()