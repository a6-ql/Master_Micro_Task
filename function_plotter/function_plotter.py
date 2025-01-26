import re
import numpy as np
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import math
import numpy as np

class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Input fields for functions
        self.function1_input = QLineEdit(self)
        self.function1_input.setPlaceholderText("Enter first function of x, e.g., 5*x^3 + 2*x")
        self.layout.addWidget(self.function1_input)

        self.function2_input = QLineEdit(self)
        self.function2_input.setPlaceholderText("Enter second function of x, e.g., 3*x^2 - 4*x")
        self.layout.addWidget(self.function2_input)

        # Plot button
        self.plot_button = QPushButton("Plot Functions", self)
        self.plot_button.clicked.connect(self.plot_functions)
        self.layout.addWidget(self.plot_button)

        # Matplotlib figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def validate_function(self, func_str):
        """Validate the function input."""
        # Allowed operators and functions
        allowed_pattern = re.compile(r'^[0-9x\+\-\/\*\^\.\(\)\s]*(log10\(.*\))?(sqrt\(.*\))?.*$')
        if not allowed_pattern.match(func_str):
            return False
        return True

    def parse_function(self, func_str):
        """Parse the function string into a callable function."""
        try:
            # Replace ^ with ** for Python syntax
            func_str = func_str.replace('^', '**')
            # Validate and create lambda function
            if self.validate_function(func_str):
                # Define the environment for eval
                eval_env = {
                    'log10': np.log10,  # Use math.log10 for log10
                    'sqrt': np.sqrt # Use math.sqrt for sqrt
                #    'x': None             # Placeholder for x
                }
                # Create the lambda function
                return lambda x: eval(func_str, {'x': x, **eval_env})
            else:
                return None
        except Exception as e:
            print(f"Error parsing function: {e}")
            return None

    def plot_functions(self):
        """Plot the two functions."""
        # Get user input
        func1_str = self.function1_input.text().strip()
        func2_str = self.function2_input.text().strip()

        # Validate input
        if not func1_str or not func2_str:
            QMessageBox.warning(self, "Input Error", "Please enter both functions.")
            return

        # Parse functions
        func1 = self.parse_function(func1_str)
        func2 = self.parse_function(func2_str)

        if func1 is None or func2 is None:
            QMessageBox.warning(self, "Input Error", "Invalid function input. Please check your syntax.")
            return

        # Generate x values
        x = np.linspace(-10, 10, 400)
        y1 = func1(x)
        y2 = func2(x)

        # Clear previous plot
        self.ax.clear()

        # Plot functions
        self.ax.plot(x, y1, label="Function 1")
        self.ax.plot(x, y2, label="Function 2")

        # Find intersection point
        intersection_idx = np.argwhere(np.diff(np.sign(y1 - y2))).flatten()
        if intersection_idx.size > 0:
            intersection_x = x[intersection_idx]
            intersection_y = y1[intersection_idx]
            self.ax.plot(intersection_x, intersection_y, 'ro', label="Intersection")
            self.ax.annotate(f'({intersection_x[0]:.2f}, {intersection_y[0]:.2f})',
                             xy=(intersection_x[0], intersection_y[0]), xytext=(10, 20),
                             textcoords='offset points', arrowprops=dict(arrowstyle='->'))

        # Add labels and legend
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()
        self.ax.grid(True)

        # Refresh canvas
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    window = FunctionPlotter()
    window.show()
    app.exec_()
