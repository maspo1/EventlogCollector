import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QMenuBar, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import seaborn as sns
from scipy import stats  # Import scipy's stats module

# # 실제 회귀직선의 계수와 절편
# true_slope = 10
# true_intercept = 0.115
#
# # 데이터 생성
# np.random.seed(42)
# x = np.random.uniform(58, 60, size=(24*31,))
# y = true_slope * x + true_intercept + np.random.normal(0, 5, size=(24*31,))  # 오차 추가
#
# # 2행 3열의 subplot 생성
# fig, axs = plt.subplots(2, 2, figsize=(15, 10))
#
# # 회귀 모델 학습
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
#
# # 차원 수정
# x_train = x_train.reshape(-1, 1)
# x_test = x_test.reshape(-1, 1)
#
#
# optimizer = Adam(lr=0.001)
# #model.add(Dense(10, activation='relu', input_dim=1))  # 더 깊은 신경망 구조 적용
# #model.compile(loss='mean_squared_error', optimizer=optimizer)
# model = Sequential()
# model.add(Dense(1, input_dim=1))
# model.compile(loss='mean_squared_error', optimizer=optimizer)
# #model.fit(x_train, y_train, epochs=8000, verbose=1, validation_data=(x_test, y_test))
#
# # 잔차 분석 및 표시
# y_pred = model.predict(x_test).flatten()
# residuals = y_test - y_pred
# # sns.residplot(x=x_test, y=residuals, ax=axs[1, 0])
# # axs[1, 0].set_title('Residuals Plot')
# # Z-Score 계산
# z_scores = (residuals - np.mean(residuals)) / np.std(residuals)

class ScatterPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class AnalWindow(QWidget):
    def __init__(self):
        super().__init__()
        # UI 파일을 로드
        uic.loadUi("anal.ui", self)  # UI 파일명을 실제 파일명으로 대체
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
        # Matplotlib 플롯 그리기

        layout.addLayout(self.plots_layout)
        layout.addWidget(self.plotScatter_button)
        layout.addWidget(self.plotScatter_button2)
        layout.addWidget(self.plotScatter_button3)
        central_widget.setLayout(layout)
        self.show()
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        self.canvas.draw()

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        # UI 파일을 로드
        uic.loadUi("tag.ui", self)  # UI 파일명을 실제 파일명으로 대체

class uiExample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)  # UI 파일명을 실제 파일명으로 대체

        # 기존에 만들어진 메뉴 객체 가져오기
        tag_menu = self.menuBar().findChild(QtWidgets.QMenu, "menu")
        # 새로운 윈도우 열기 액션 추가
        open_action = QtWidgets.QAction("태그추출", self)
        open_action.triggered.connect(self.open_second_window)
        tag_menu.addAction(open_action)

        # 기존에 만들어진 메뉴 객체 가져오기
        anal_menu = self.menuBar().findChild(QtWidgets.QMenu, "menu_2")
        # 새로운 윈도우 열기 액션 추가
        open_action = QtWidgets.QAction("태그추출22", self)
        open_action.triggered.connect(self.open_anal_window)
        anal_menu.addAction(open_action)

    def open_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()

    def open_anal_window(self):
        self.anal_window = AnalWindow()
        self.anal_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = uiExample()
    window.show()
    sys.exit(app.exec_())
