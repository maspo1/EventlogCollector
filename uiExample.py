import sys, os
import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QMenuBar, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer
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
import time
import random

class GenerateData(QThread):
    signal_Log = pyqtSignal(str)
    signal_Data = pyqtSignal(dict)
    def __init__(self, epoch):
        self.epoch = epoch
        super().__init__()
    def run(self):
        # # 실제 회귀직선의 계수와 절편
        true_slope = 10
        true_intercept = 0.115

        # # 데이터 생성
        np.random.seed(42)
        x = np.random.uniform(58, 60, size=(24 * 31,))
        y = true_slope * x + true_intercept + np.random.normal(0, 5, size=(24 * 31,))  # 오차 추가

        # # 회귀 모델 학습
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        #
        # # 차원 수정
        x_train = x_train.reshape(-1, 1)
        x_test = x_test.reshape(-1, 1)

        # model = Sequential()
        # model.add(Dense(10, activation='relu', input_dim=1))  # 더 깊은 신경망 구조 적용
        # model.compile(loss='mean_squared_error', optimizer=optimizer)
        model = Sequential()
        model.add(Dense(1, input_dim=1))
        model.compile(loss='mean_squared_error', optimizer='Adam')

        # 모델 학습
        for epoch in range(self.epoch):
            history = model.fit(x, y, batch_size=32, verbose=0)
            loss = history.history['loss'][0]  # Get loss from the history
            update_text = f"Epoch(학습량) {epoch + 1}: Loss(손실함수) = {loss:.4f}"
            self.signal_Log.emit(update_text)
            time.sleep(0.1)

        # # 잔차 분석 및 표시
        y_pred = model.predict(x_test).flatten()
        residuals = y_test - y_pred

        # Z-Score 계산
        z_scores = (residuals - np.mean(residuals)) / np.std(residuals)
        data = {
            'x':x,
            'y':y,
            'x_test':x_test,
            'y_test':y_test,
            'x_train':x_train,
            'y_train':y_train,
            'y_pred':y_pred,
            'residuals':residuals,
            'z_scores':z_scores,
            'model':model
        }
        self.signal_Data.emit(data)


class RealTimeUpdaterThread(QThread):
    update_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(10):
            self.update_text.emit(f"Updating text {i}\n")
            self.msleep(1000)
class ScatterPlotWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(20, 20))
        self.ax = self.fig.subplots(2, 2)
        #self.fig, self.ax = plt.subplots(2,2,figsize=(15,10))
        super().__init__(self.fig)
        self.setParent(parent)
        self.canvas = FigureCanvas(self.fig)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    def plot_data(self, dict):
        # 실제 회귀직선의 계수와 절편
        true_slope = 10
        true_intercept = 0.115

        df = pd.DataFrame({'x':dict['x'], 'y':dict['y']})

        model = dict['model']
        x = df['x']
        y = df['y']
        x_test = dict['x_test']
        y_test = dict['y_test']
        x_train = dict['x_train']
        y_train = dict['y_train']
        residuals = dict['residuals']
        y_pred = dict['y_pred']

        #정의
        axs1 = self.ax[0, 0]
        axs2 = self.ax[1, 0]
        axs3 = self.ax[0, 1]
        axs4 = self.ax[1, 1]

        # 1. 원본 산점도와 회귀모델 표시
        axs1.clear()
        axs1.scatter(df['x'], df['y'])
        axs1.set_xlabel('X')
        axs1.set_ylabel('Y')
        axs1.plot(x_train, model.predict(x_train), color='red', label='Regression Line')
        axs1.set_title('Original Scatter Plot and Regression Line')
        axs1.legend()

        # 2. Z-Score표시
        sns.residplot(x=x_test, y=residuals, ax=axs2)
        axs2.set_title('Residuals Plot')
        r2 = r2_score(y_test, y_pred)

        # 유의미한 회귀 모델인 경우
        if r2 >= 0.5:
            # 랜덤한 데이터 생성
            np.random.seed(42)
            x_new = np.random.uniform(58, 60, size=(24 * 31,))
            # y_new = np.random.uniform(580, 600, size=(24 * 31,)) + np.random.normal(0, 10, size=(24 * 31,))
            y_new = true_slope * x + true_intercept + np.random.normal(0, 5, size=(24 * 31,))  # 오차 추가
            x_new = x_new.reshape(-1, 1)  # 차원 수정

            # 훈련된 회귀직선 표시
            regression_line = model.predict(x_new)
            axs3.scatter(x_new, y_new, c='blue', label='Data')
            axs3.plot(x_new, model.predict(x_new.reshape(-1, 1)), color='orange', label='Regression Line')
            axs3.set_title('Regression Line')

            # 유의미한 신뢰대 벗어나는 데이터 표시
            confidence_interval = residuals.std() * 1.96
            outliers = np.where(np.abs(residuals) > confidence_interval)[0]
            axs3.scatter(x_test[outliers], y_test[outliers], c='red', marker='x', label='Outliers')
            axs3.legend()

            # 신뢰대 표시
            axs3.fill_between(x_new.flatten(), regression_line.flatten() - confidence_interval,
                              regression_line.flatten() + confidence_interval, color='gray', alpha=0.3,
                              label='Confidence Interval')
            axs3.legend()

        # 모델의 MSE와 MAE 계산
        mse = np.mean((y_test - y_pred.flatten()) ** 2)
        mae = np.mean(np.abs(y_test - y_pred.flatten()))

        # 오차 검증 정보 표시
        axs4.axis('off')
        axs4.text(0, 0.3, f'R-squared: {r2:.4f}', fontsize=8)
        axs4.text(0, 0.25, f'Standard Error: {np.std(residuals):.4f}', fontsize=8)
        axs4.text(0, 0.2, f'Coefficients1: {model.layers[0].get_weights()[0][0][0]:.4f}', fontsize=8)
        # MSE와 MAE 표시
        axs4.text(0, 0.15, f'MSE: {mse:.4f}', fontsize=8)
        axs4.text(0, 0.1, f'MAE: {mae:.4f}', fontsize=8)

        #self.figure.tight_layout()
        #self.canvas.draw()
        #self.draw()
class AnalWindow(QWidget):
    def __init__(self):
        super().__init__()
        # UI 파일을 로드
        uic.loadUi("anal.ui", self)  # UI 파일명을 실제 파일명으로 대체
        self.setWindowTitle("Analysis Window")
        self.layout = QVBoxLayout(self)
        self.scatter_widget = ScatterPlotWidget()
        self.layout.addWidget(self.scatter_widget)
class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        # UI 파일을 로드
        uic.loadUi("tag.ui", self)  # UI 파일명을 실제 파일명으로 대체
class uiExample(QMainWindow):
    update_signal = pyqtSignal(str)  # 시그널 정의
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
        open_action = QtWidgets.QAction("회귀모델 딥러닝수행", self)
        open_action.triggered.connect(self.start_Linear_Regression)
        anal_menu.addAction(open_action)
        # 새로운 윈도우 열기 액션 추가
        open_action = QtWidgets.QAction("회귀분석", self)
        open_action.triggered.connect(self.open_anal_window)
        anal_menu.addAction(open_action)

        # 연결
        # self.text_thread = RealTimeUpdaterThread()
        # self.text_thread.update_text.connect(self.update_text)
        # self.text_thread.start()
        # self.data_thread = GenerateData()
        # self.data_thread.data_generated.connect(self.update_text)
        # self.data_thread.start()

    def start_Linear_Regression(self):
        line_edit = self.findChild(QtWidgets.QLineEdit, "lineEdit")  # QLineEdit 객체 찾기
        text = line_edit.text()
        self.data_thread = GenerateData(int(text))
        self.data_thread.signal_Log.connect(self.update_log)
        self.data_thread.signal_Data.connect(self.open_anal_window)
        self.data_thread.start()

    def open_anal_window(self, df):
        #딕셔너리를 통째로 넘겨서 Plot안에서 가공
        self.anal_window = AnalWindow()
        self.anal_window.scatter_widget.plot_data(df)
        self.anal_window.show()


    def open_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()
    def update_log(self, log):
        self.logPlainText.appendPlainText(log)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = uiExample()
    window.show()
    sys.exit(app.exec_())
