from PyQt5.QtWidgets import QScrollArea, QDesktopWidget, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QTextEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
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

        # New field for higher-order derivative
        layout.addWidget(QLabel("Derivative Order (e.g., 1 for first derivative):"))
        self.derivative_order_entry = QLineEdit()
        self.derivative_order_entry.setPlaceholderText("Enter derivative order")
        layout.addWidget(self.derivative_order_entry)

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot)
        layout.addWidget(self.plot_button)

        self.save_button = QPushButton("Save Plot")
        self.save_button.clicked.connect(self.save_plot)
        layout.addWidget(self.save_button)

        # Set up right layout for the graph and result box
        right_layout = QHBoxLayout()

        # Create the plot widget
        self.plot_widget = PlotWidget()
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a QScrollArea to make the plot widget scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.plot_widget)  # Set the plot widget as the scrollable widget
        scroll_area.setWidgetResizable(True)  # Allow the widget to resize within the scroll area

        # Set a fixed minimum size for the plot widget to ensure scrolling is triggered
        self.plot_widget.setMinimumSize(800, 600)  # Set the size depending on your graph's expected dimensions

        right_layout.addWidget(scroll_area)

        # Result Box
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("Function details will appear here...")
        self.result_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Allow the result box to expand vertically but not horizontally
        right_layout.addWidget(self.result_box)

        layout.addLayout(right_layout)
        self.setLayout(layout)

        # Resize window based on screen size (percentage) but allow resizing
        self.resize_window_to_percentage()

        self.center_window()

    def resize_window_to_percentage(self):
        # Get the screen's dimensions
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Define the desired window size as a percentage of the screen size
        window_width_percentage = 0.8  # 80% of the screen width
        window_height_percentage = 0.7  # 70% of the screen height

        # Calculate the window's size based on the percentages
        window_width = int(screen_width * window_width_percentage)
        window_height = int(screen_height * window_height_percentage)

        # Set initial window size but allow manual resizing
        self.resize(window_width, window_height)

    def center_window(self):
        # Get the screen's dimensions
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Get the window's current size after it is shown
        window_width = self.frameGeometry().width()
        window_height = self.frameGeometry().height()

        # Calculate the top-left position to center the window
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        # Move the window to the calculated position
        self.move(x_pos, y_pos)

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

        # Get the derivative order from the input
        try:
            derivative_order = int(self.derivative_order_entry.text())
        except ValueError:
            self.warning(warning="Invalid derivative order input.")
            return

        # List to store all derivatives and their numerical values
        derivatives = [func]
        x_vals = np.linspace(x_min, x_max, 400)

        # Initialize lists for the values of the function and its derivatives
        y_vals_list = []
        dy_vals_list = []

        # Calculate the original function's values for each x_val
        y_vals_list.append(np.array([float(func.subs(x, val).evalf()) for val in x_vals], dtype=np.float64))
        dy_vals_list.append(np.array([self.numerical_derivative(func, val) for val in x_vals], dtype=np.float64))

        # Calculate derivatives from 1 up to the desired order and add them to lists
        for i in range(1, derivative_order + 1):
            func_diff = sp.diff(derivatives[-1], x)  # Calculate next derivative
            derivatives.append(func_diff)

            # Calculate the numerical values for the derivative
            dy_vals = np.array([self.numerical_derivative(derivatives[i], val) for val in x_vals], dtype=np.float64)
            dy_vals_list.append(dy_vals)

            # Also add the values for the current derivative
            y_vals_list.append(np.array([float(derivatives[i].subs(x, val).evalf()) for val in x_vals], dtype=np.float64))

        # Calculate the symbolic integral of the original function
        func_integral = sp.integrate(func, x)
        
        # Calculate the integral values
        int_vals = cumulative_trapezoid(y_vals_list[0], x_vals, initial=0)

        # Update the result box with the original function, derivatives, and integral
        derivative_text = ""
        for i in range(1, derivative_order + 1):
            derivative_text += f"Derivative [{i}]:\n  f^{i}(x) = {sp.simplify(derivatives[i])}\n\n"

        # Simplify the function and derivative text
        simplified_func = sp.simplify(func)
        simplified_integral = sp.simplify(func_integral)

        # Convert the expression to string and replace symbols
        formatted_func = str(simplified_func).replace('**', '^').replace('*', '')
        formatted_integral = str(simplified_integral).replace('**', '^').replace('*', '')

        # Construct the derivative text similarly, if applicable
        derivative_text = derivative_text.replace('**', '^').replace('*', '')

        # Set the formatted text to the result box
        self.result_box.setPlainText(
            f"Original Function:\n  f(x) = {formatted_func}\n\n"
            + derivative_text
            + f"Integral:\n  ∫f(x)dx = {formatted_integral} + C"
        )

        # Plot the original function and all derivatives
        self.plot_widget.plot_function(x_vals, y_vals_list, dy_vals_list, int_vals)

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

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")

        screen_geometry = QDesktopWidget().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        window_width = int(screen_width * 0.55)  # 50% of screen width
        window_height = int(screen_height * 0.55)  # 30% of screen height

        self.setFixedSize(window_width, window_height)
        self.setStyleSheet("background-color: #FFFFFF; color: black; font-size: 20px;")
        layout = QVBoxLayout()
        
        # Replace text with an image
        splash_image = QPixmap("Assets/Splash Screen.png")  # Path to your image
        scaled_image = splash_image.scaled(window_width, window_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        image_label = QLabel(self)
        image_label.setPixmap(scaled_image)
        image_label.setAlignment(Qt.AlignCenter)  # Center the image
        layout.addWidget(image_label)
        
        # Retain the start button
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.launch_main)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)

    def launch_main(self):
        self.close()
        self.main = FunctionVisualizer()  # Assuming you have a class FunctionVisualizer
        self.main.show()
        

if __name__ == "__main__":
    app = QApplication([])
    splash = SplashScreen()
    splash.show()
    app.exec_()