import sys
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit


class ScatterPlotWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)

    def plot_data(self, x_data, y_data):
        self.ax.clear()
        self.ax.scatter(x_data, y_data)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Scatter Plot')
        self.draw()

class DataGeneratorThread(QThread):
    data_generated = pyqtSignal(list, list)

    def __init__(self):
        super().__init__()

    def run(self):
        x_data = [random.random() for _ in range(50)]
        y_data = [random.random() for _ in range(50)]
        self.data_generated.emit(x_data, y_data)

class RealTimeUpdaterThread(QThread):
    update_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(10):
            self.update_text.emit(f"Updating text {i}\n")
            self.msleep(1000)

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.scatter_widget = ScatterPlotWidget(self)
        layout.addWidget(self.scatter_widget)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_threads)
        layout.addWidget(self.start_button)

        self.second_window = SecondWindow()
        self.second_window.setGeometry(200, 200, 600, 400)
        self.second_window.show()

        self.data_thread = DataGeneratorThread()
        self.data_thread.data_generated.connect(self.update_scatter_plot)

        self.text_thread = RealTimeUpdaterThread()
        self.text_thread.update_text.connect(self.update_text_edit)

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def start_threads(self):
        self.data_thread.start()
        self.text_thread.start()

    def update_scatter_plot(self, x_data, y_data):
        self.second_window.scatter_widget.plot_data(x_data, y_data)

    def update_text_edit(self, text):
        self.text_edit.append(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
