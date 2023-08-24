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
true_slope = 10
true_intercept = 0.115

# # 데이터 생성
np.random.seed(42)
x = np.random.uniform(58, 60, size=(24*31,))
y = true_slope * x + true_intercept + np.random.normal(0, 5, size=(24*31,))  # 오차 추가

# # 회귀 모델 학습
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
#
# # 차원 수정
x_train = x_train.reshape(-1, 1)
x_test = x_test.reshape(-1, 1)

#optimizer = Adam(lr=0.001)
#model = Sequential()
#model.add(Dense(10, activation='relu', input_dim=1))  # 더 깊은 신경망 구조 적용
#model.compile(loss='mean_squared_error', optimizer=optimizer)
model = Sequential()
model.add(Dense(1, input_dim=1))
model.compile(loss='mean_squared_error', optimizer='Adam')
model.fit(x_train, y_train, epochs=100, verbose=1, validation_data=(x_test, y_test))

# # 잔차 분석 및 표시
y_pred = model.predict(x_test).flatten()
residuals = y_test - y_pred

# Z-Score 계산
z_scores = (residuals - np.mean(residuals)) / np.std(residuals)

class ScatterPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(2, 2, figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_plots(self, data):
        # 데이터를 받아와서 서브플롯에 그래프를 그리는 참고코드!!
        # for i in range(2):
        #     for j in range(2):
        #         ax = self.ax[i, j]
        #         ax.clear()  # 이전 그래프를 지웁니다
        #         x = [1, 2, 3, 4, 5]
        #         y = [value * (i * 2 + j + 1) for value in data]
        #         ax.scatter(x, y)
        #         ax.set_title(f"Subplot {i + 1}, {j + 1}")
        #         ax.set_xlabel("X")
        #         ax.set_ylabel("Y")
        # 원본 산점도와 회귀모델 표시
        axs1 = self.ax[0,0]
        axs1.clear()  # 이전 그래프를 지웁니다
        axs2 = self.ax[1,0]
        axs3 = self.ax[0,1]
        axs4 = self.ax[1,1]
        # 1. 원본 산점도와 회귀모델 표시
        axs1.scatter(x, y)
        axs1.plot(x, model.predict(x), color='red', label='Regression Line')
        axs1.set_title('Original Scatter Plot and Regression Line')
        axs1.legend()
        # 2. Z-Score표시
        # sns.residplot(x=x_test, y=residuals, ax=axs2)
        # axs2.set_title('Residuals Plot')

        r2 = r2_score(y_test, y_pred)

        # # 유의미한 회귀 모델인 경우
        # if r2 >= 0.5:
        #     # 랜덤한 데이터 생성
        #     np.random.seed(42)
        #     x_new = np.random.uniform(58, 60, size=(24 * 31,))
        #     # y_new = np.random.uniform(580, 600, size=(24 * 31,)) + np.random.normal(0, 10, size=(24 * 31,))
        #     y_new = true_slope * x + true_intercept + np.random.normal(0, 5, size=(24 * 31,))  # 오차 추가
        #     x_new = x_new.reshape(-1, 1)  # 차원 수정
        #
        #     # 훈련된 회귀직선 표시
        #     regression_line = model.predict(x_new)
        #     axs3.scatter(x_new, y_new, c='blue', label='Data')
        #     axs3.plot(x_new, model.predict(x_new.reshape(-1, 1)), color='orange', label='Regression Line')
        #     axs3.set_title('Regression Line')
        #
        #     # 유의미한 신뢰대 벗어나는 데이터 표시
        #     confidence_interval = residuals.std() * 1.96
        #     outliers = np.where(np.abs(residuals) > confidence_interval)[0]
        #     axs3.scatter(x_test[outliers], y_test[outliers], c='red', marker='x', label='Outliers')
        #     axs3.legend()
        #
        #     # 신뢰대 표시
        #     axs3.fill_between(x_new.flatten(), regression_line.flatten() - confidence_interval,
        #                            regression_line.flatten() + confidence_interval, color='gray', alpha=0.3,
        #                            label='Confidence Interval')
        #     axs3.legend()
        #
        # # 모델의 MSE와 MAE 계산
        # mse = np.mean((y_test - y_pred.flatten()) ** 2)
        # mae = np.mean(np.abs(y_test - y_pred.flatten()))
        #
        # # 오차 검증 정보 표시
        # axs4.axis('off')
        # axs4.text(0, 0.3, f'R-squared: {r2:.4f}', fontsize=8)
        # axs4.text(0, 0.25, f'Standard Error: {np.std(residuals):.4f}', fontsize=8)
        # axs4.text(0, 0.2, f'Coefficients1: {model.layers[0].get_weights()[0][0][0]:.4f}', fontsize=8)
        # # MSE와 MAE 표시
        # axs4.text(0, 0.15, f'MSE: {mse:.4f}', fontsize=8)
        # axs4.text(0, 0.1, f'MAE: {mae:.4f}', fontsize=8)

        self.figure.tight_layout()
        self.canvas.draw()

class AnalWindow(QWidget):
    def __init__(self):
        super().__init__()
        # UI 파일을 로드
        uic.loadUi("anal.ui", self)  # UI 파일명을 실제 파일명으로 대체
        self.setWindowTitle("Main Window")
        self.layout = QVBoxLayout(self)
        self.scatter_widget = ScatterPlotWidget(self)
        self.layout.addWidget(self.scatter_widget)
    def update_plots(self):
        data = [10, 20, 30, 40, 50]  # 예시 데이터
        self.scatter_widget.update_plots(data)

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
        self.anal_window.update_plots()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = uiExample()
    window.show()
    sys.exit(app.exec_())
