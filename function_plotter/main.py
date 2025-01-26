from function_plotter import FunctionPlotter
from PySide2.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = FunctionPlotter()
    window.show()
    app.exec_()