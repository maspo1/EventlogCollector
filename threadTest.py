import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import pandas as pd
import numpy as np
import scipy.stats as stats


# 가상의 데이터 생성 (2800개 태그, 각 태그에 60개의 데이터)


np.random.seed(0)
n = 10
num_tags = 2500000
data = np.random.rand(n, num_tags)
df = pd.DataFrame(data)
counter = 0

class WorkerThread(QThread):
    update_signal = pyqtSignal(str)
    def run(self):
        # P-VALUE 검정
        idx = 0
        for i in range(num_tags):
            for j in range(i+1, num_tags):
                idx +=1
                correlation_coefficient, p_value = stats.pearsonr(df[i], df[j])
                if abs(correlation_coefficient) > 0.5 and abs(correlation_coefficient) < 1 and p_value <= 0.05:
                    result = f'[ {idx} ]  Corr:{round(correlation_coefficient,3)} P-Value:{round(p_value,3)}'
                    self.update_signal.emit(result)

class RealTimeConsole(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Real-Time Console')
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(self.update_console)
        self.worker_thread.start()

        self.show()

    def update_console(self, text):
        self.text_edit.appendPlainText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    console = RealTimeConsole()
    sys.exit(app.exec_())
