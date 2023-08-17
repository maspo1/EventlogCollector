import sys
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ScatterPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Correlation Scatter Plots")
        self.setGeometry(100, 100, 1200, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.plots_layout = QHBoxLayout()
        self.normal_plot = ScatterPlotWidget()
        self.error_plot = ScatterPlotWidget()
        self.missing_plot = ScatterPlotWidget()
        self.plots_layout.addWidget(self.normal_plot)
        self.plots_layout.addWidget(self.error_plot)
        self.plots_layout.addWidget(self.missing_plot)

        self.plotScatter_button = QPushButton("Plot Scatter Chart (normal)")
        self.plotScatter_button2 = QPushButton("Plot Scatter Chart (error)")
        self.plotScatter_button3 = QPushButton("Plot Scatter Chart (missing)")

        self.plotScatter_button.clicked.connect(lambda: self.plotScatterChart(self.generateData("normal"), 'normal'))
        self.plotScatter_button2.clicked.connect(lambda: self.plotScatterChart(self.generateData("error"), 'error'))
        self.plotScatter_button3.clicked.connect(lambda: self.plotScatterChart(self.generateData("missing"), 'missing'))

        layout.addLayout(self.plots_layout)
        layout.addWidget(self.plotScatter_button)
        layout.addWidget(self.plotScatter_button2)
        layout.addWidget(self.plotScatter_button3)
        central_widget.setLayout(layout)

        self.show()

    # ... (generateData, train_data, analyze_data functions)

    def plotScatterChart(self, generatedDict, status):
        ax = self.normal_plot.ax if status == 'normal' else self.error_plot.ax if status == 'error' else self.missing_plot.ax
        ax.clear()  # Clear the plot to remove previous data

        for element_key, element_rows in generatedDict.items():
            x_data = [row[0] for row in element_rows]
            y_data = [row[1] for row in element_rows]
            ax.scatter(x_data, y_data, label=f"{element_key[0]} vs {element_key[1]}")

        ax.set_xlabel("Date")
        ax.set_ylabel("Correlation")
        ax.set_title("Scatter Chart for Tag Correlation (DaeChung-Dam)")
        ax.set_ylim(-1, 1)
        ax.legend()
        self.normal_plot.canvas.draw() if status == 'normal' else self.error_plot.canvas.draw() if status == 'error' else self.missing_plot.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
