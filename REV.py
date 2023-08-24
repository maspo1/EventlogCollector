import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import mplcursors

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matplotlib in PyQt Example")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.canvas = FigureCanvas(plt.figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)

        self.plot_data()

    def plot_data(self):
        # 날짜 범위 생성
        date_range = pd.date_range(start='2023-07-01', end='2023-07-31', freq='H')

        # 기준 데이터 생성
        data1 = np.random.uniform(60, 61, len(date_range))

        # 상관계수 목표치
        correlation_target = 0.9

        # 두 번째 데이터 생성
        data2 = correlation_target * data1 + np.random.uniform(-0.5, 0.5, len(date_range))

        # 데이터프레임 생성
        df = pd.DataFrame({'Date': date_range, 'Data1': data1, 'Data2': data2})

        # 그래프 그리기
        self.canvas.figure.clear()  # 기존의 그래프를 지우고 새로운 그래프 생성

        ax1 = self.canvas.figure.add_subplot(3, 2, 1)
        ax1.scatter(df['Date'], df['Data1'], label='Data1', alpha=0.5)
        ax1.scatter(df['Date'], df['Data2'], label='Data2', alpha=0.5)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Data')
        ax1.legend()

        ax2 = self.canvas.figure.add_subplot(3, 2, 2)
        ax2.scatter(df['Data1'], df['Data2'], label='Scatter Plot', alpha=0.5)
        ax2.set_xlabel('Data1')
        ax2.set_ylabel('Data2')
        ax2.legend()

        ax3 = self.canvas.figure.add_subplot(3, 2, 3)
        ax3.plot(df['Date'], df['Data2'] - df['Data1'], label='Residuals')
        ax3.axhline(y=2, color='red', linestyle='--', label='Z-Score Threshold')
        ax3.axhline(y=-2, color='red', linestyle='--')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Residuals / Z-Score')
        ax3.legend()

        ax4 = self.canvas.figure.add_subplot(3, 2, 4)
        ax4.hist(df['Data2'] - df['Data1'], bins=20, density=True, alpha=0.7, color='blue', label='Z-Scores')
        ax4.set_xlabel('Z-Score')
        ax4.set_ylabel('Density')
        ax4.legend()

        ax5 = self.canvas.figure.add_subplot(3, 2, 5)
        ax5.scatter(df['Date'], df['Data1'], label='Data1', alpha=0.5)
        ax5.scatter(df['Date'], df['Data2'], label='Data2', alpha=0.5)
        ax5.set_xlabel('Date')
        ax5.set_ylabel('Data')
        ax5.legend()

        ax6 = self.canvas.figure.add_subplot(3, 2, 6)
        ax6.scatter(df['Data1'], df['Data2'], label='Scatter Plot', alpha=0.5)
        ax6.set_xlabel('Data1')
        ax6.set_ylabel('Data2')
        ax6.legend()

        plt.tight_layout()

        # mplcursors 라이브러리를 사용하여 툴팁 활성화
        mplcursors.cursor(hover=True)

        # 주석 추가 및 좌표 표시
        annotations = []

        for ax in self.canvas.figure.get_axes():
            sc = ax.collections[0]

            def on_move(event):
                for annot, ind in annotations:
                    annot.set_visible(False)
                annotations.clear()

                cont, ind = sc.contains(event)
                if cont:
                    for i in ind["ind"]:
                        x, y = sc.get_offsets()[i]
                        annot = ax.annotate(f'x={x:.2f}, y={y:.2f}',
                                            xy=(x, y), xycoords='data',
                                            xytext=(10, 10), textcoords='offset points',
                                            bbox=dict(boxstyle="round", fc="w"),
                                            arrowprops=dict(arrowstyle="->"))
                        annotations.append((annot, i))
                        annot.set_visible(True)

            self.canvas.mpl_connect('motion_notify_event', on_move)

        self.canvas.draw()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
