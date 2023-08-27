import sys
import concurrent.futures
import pandas as pd
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
import scipy.stats as stats

num_threads = 4
np.random.seed(0)
n = 10
num_tags = 100000
data = np.random.rand(n, num_tags)
df = pd.DataFrame(data)
counter = 0

def calculate_correlation(data1, data2, index1, index2):
    correlation_coefficient, p_value = stats.pearsonr(data1, data2)
    return correlation_coefficient, p_value

class Worker(QObject):
    update_signal = pyqtSignal(str)
    def process(self, data1, data2, index1, index2):
        result = calculate_correlation(data1, data2, index1, index2)
        if abs(result[0]) > 0.5 and abs(result[0]) < 1 and abs(result[1]) <=0.05:
            result = f'Corr:{round(result[0], 3)} P-Value:{round(result[1], 3)}'
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

        self.worker = Worker()
        self.worker_threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.worker.update_signal.connect(self.update_console)

        futures = []
        #data는 df이다

        for i in range(num_tags):
            for j in range(i+1, num_tags):
                future = self.worker_threadpool.submit(self.worker.process, df[i], df[j], i, j)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            future.result()

    def update_console(self, text):
        self.text_edit.appendPlainText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RealTimeConsole()
    window.show()
    sys.exit(app.exec_())
