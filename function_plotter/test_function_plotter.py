import pytest
from PySide2.QtWidgets import QApplication
from function_plotter import FunctionPlotter


@pytest.fixture
def app():
    """Fixture to initialize the QApplication."""
    application = QApplication([])
    yield application
    application.quit()


@pytest.fixture
def window(app):
    """Fixture to create the FunctionPlotter window."""
    window = FunctionPlotter()
    yield window
    window.close()


def test_input_validation(window):
    """Test input validation for invalid function strings."""
    invalid_functions = [
        "5*x^3 + 2*x + sin(x)",  # Invalid function
        "5*x^3 + 2*x +",         # Incomplete expression
    ]

    for func in invalid_functions:
        assert window.validate_function(func) is False


def test_plot_functions(window, qtbot):
    """Test plotting valid functions."""
    # Set valid functions
    window.function1_input.setText("5*x^3 + 2*x")
    window.function2_input.setText("3*x^2 - 4*x")

    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)

    # Check if the plot is updated
    assert len(window.ax.lines) > 0