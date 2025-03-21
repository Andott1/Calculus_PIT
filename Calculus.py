import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.integrate import quad
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class FunctionVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Function Visualizer")
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Enter function (in terms of x):"))
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
        
        self.setLayout(layout)
    
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
        
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, label='Function')
        plt.plot(x_vals, dy_vals, label='First Derivative', linestyle='--')
        plt.plot(x_vals, int_vals, label='Integral', linestyle=':')
        
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.legend()
        plt.title("Function Visualization")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()
        plt.show()
        
if __name__ == "__main__":
    app = QApplication([])
    window = FunctionVisualizer()
    window.show()
    app.exec_()
