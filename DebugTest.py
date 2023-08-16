import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
import numpy as np
import matplotlib as plt
import scipy.stats as stats


# 가상의 데이터 생성 (2800개 태그, 각 태그에 60개의 데이터)
np.random.seed(0)
n = 10
num_tags = 50
data = np.random.rand(n, num_tags)
df = pd.DataFrame(data)
counter = 0

print("데이터 생성완료")

class Worker(QThread):
    result_signal = pyqtSignal(tuple)

    def __init__(self, tag1, tag2):
        super().__init__()
        self.tag1 = tag1
        self.tag2 = tag2

    def run(self):
        #P-VALUE 검정
        correlation_coefficient, p_value = stats.pearsonr(df[self.tag1],df[self.tag2])
        if abs(correlation_coefficient) > 0.5 and abs(correlation_coefficient) < 1 and p_value <=0.05:
            result = (self.tag1, self.tag2, round(correlation_coefficient, 3), round(p_value,3))
            self.result_signal.emit(result)

class ThreadController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker_threads = []

    def start_threads(self):
        threads = []
        for i in range(num_tags):
            for j in range(i + 1, num_tags):
                # 새로운 QThread 객체를 생성하여 실행함
                thread = Worker(i,j)
                thread.result_signal.connect(self.update_text_edit)
                threads.append(thread)
                thread.start()
        for thread in threads:
            thread.wait()

    def update_text_edit(self, result):
        text = f"Correlation between {result[0]} and {result[1]}(Corr계수): {result[2]} P-Value(신뢰도) : {result[3]}"
        # 메인 윈도우의 update_text_edit 메서드 호출
        self.main_window.update_text_edit(text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-time Result Update")

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.button = QPushButton("Calculate Correlation", self)
        self.button.clicked.connect(self.start_calculation)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.thread_controller = ThreadController()
        self.thread_controller.main_window = self

    def start_calculation(self):
        self.text_edit.clear()
        self.thread_controller.start_threads()

    def update_text_edit(self, result):
        self.text_edit.append(result)
        QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
