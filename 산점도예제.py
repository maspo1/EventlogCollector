import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel(self)
        layout.addWidget(self.label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_graph()

    def create_graph(self):
        # 가상의 데이터 생성 예시 (특정 1시간 데이터)
        num_tags = 50
        num_days = 30
        hour_of_interest = 6  # 특정한 1시간 (0 ~ 23)

        data = pd.DataFrame({
            f"Tag{i}": [i * (j + 1) for j in range(num_days * 24)] for i in range(1, num_tags + 1)
        })

        # 특정 1시간 데이터 추출
        hour_data = data.iloc[hour_of_interest::24]

        # 상관계수 계산
        correlations = hour_data.corr()

        # 그래프 생성
        fig = Figure(figsize=(8, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.scatter(range(1, num_days + 1), range(1, num_days + 1), label=f"Tag1 Correlation at {hour_of_interest}h")
        ax.set_xlabel('Day')
        ax.set_ylabel('Correlation')
        ax.set_title(f"Tag1 Correlation at {hour_of_interest}h over {num_days} days")
        ax.legend()

        # QPixmap으로 변환하여 QLabel에 표시
        canvas = FigureCanvas(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()
        pixmap = QPixmap(int(width), int(height))
        canvas.render(pixmap)
        self.label.setPixmap(pixmap)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
