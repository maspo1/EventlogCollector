import sys
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'NanumGothic'
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

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

    def generateData(self, status):
        name_col1 = ['Quantity used', 'discharge', 'inflow', 'flow', 'power generation']
        name_col2 = ['fall', 'humidity', 'Temperatures', 'water level', 'low water level']
        data = []
        start_date = datetime.strptime("2023-07-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-07-31", "%Y-%m-%d")

        # 7월 달의 31일에 해당하는 데이터 생성
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            # 각 이름별로 데이터 생성
            for name1 in name_col1:
                for name2 in name_col2:
                    if status == "normal":
                        value = random.uniform(0.7, 0.9)  # -0.5부터 0.5 사이의 랜덤 값 생성
                        entry = [name1, name2, date_str, round(value, 3)]  # 데이터를 이중 리스트 형태로 생성
                        data.append(entry)  # 데이터 리스트에 추가
                    elif status == "error":
                        if random.random() < 0.5:  # 10% 확률로 NaN 값 생성
                            value = float("nan")
                        else:
                            value = random.uniform(0.7, 0.9)
                        entry = [name1, name2, date_str, round(value, 3)]  # 데이터를 이중 리스트 형태로 생성
                        data.append(entry)  # 데이터 리스트에 추가
                    elif status == "missing":
                        if random.random() < 0.1:  # 10% 확률로 -1부터 0.1 사이의 값 생성
                            value = random.uniform(-1.0, 0.1)
                        else:
                            value = random.uniform(0.7, 0.9)
                        entry = [name1, name2, date_str, round(value, 3)]  # 데이터를 이중 리스트 형태로 생성
                        data.append(entry)  # 데이터 리스트에 추가

            current_date += timedelta(days=1)

        # 무작위로 2개의 이름 추출
        random_names = random.sample(name_col1, 2)
        random_names2 = random.sample(name_col2, 2)

        # 추출된 이름과 일치하는 데이터 추출
        selected_data = [entry for entry in data if entry[0] in random_names]
        selected_data = [entry for entry in selected_data if entry[1] in random_names2]
        data_Dict = {}  # 결과를 저장할 딕셔너리 생성

        # 데이터를 순회하면서 딕셔너리에 추가
        for entry in selected_data:
            key = tuple(entry[:2])  # 0번째와 1번째를 키로 사용
            value = entry[2:]  # 2번째와 3번째를 리스트로 묶어서 값으로 사용

            if key in data_Dict:
                data_Dict[key].append(value)
            else:
                data_Dict[key] = [value]
        return data_Dict

    def train_data(self):
        # 데이터 학습을 수행하는 코드
        pass

    def analyze_data(self):
        pass

    def plotScatterChart(self, generatedDict, status):
        ax = self.normal_plot.ax if status == 'normal' else self.error_plot.ax if status == 'error' else self.missing_plot.ax
        ax.clear()  # Clear the plot to remove previous data
        for element_key, element_rows in generatedDict.items():
            x_data = [row[0] for row in element_rows]
            y_data = [row[1] for row in element_rows]
            label_added = False  # 라벨을 이미 추가했는지 여부를 나타내는 변수
            nan_y_data = [np.nanmin(y_data) - 0.5 for y in y_data]
            if not label_added:
                ax.scatter(x_data, y_data, label=f"{element_key[0]} ↔ {element_key[1]}")
                label_added = True
            for y in y_data:
                if np.isnan(y):
                    ax.scatter(x_data, nan_y_data, c='green', marker='x',s =100)
        ax.set_xlabel("Date")
        ax.set_ylabel("Correlation")
        ax.set_title("Scatter Chart (정상)") if status == 'normal' else ax.set_title("Scatter Chart (오류)") if status == 'error' else ax.set_title("Scatter Chart (결측)")
        ax.set_ylim(-1, 1)
        ax.legend()
        ax.get_figure().canvas.draw()  # Update the canvas


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
