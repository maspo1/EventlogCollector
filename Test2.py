import sys
import concurrent.futures
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject

def calculate_correlation(data1, data2, index1, index2):
    correlation = data1.corrwith(data2).iloc[0]
    return f"Correlation ({index1}, {index2}): {correlation:.4f}\n"

class Worker(QObject):
    update_signal = pyqtSignal(str)

    def process(self, data1, data2, index1, index2):
        result = calculate_correlation(data1, data2, index1, index2)
        self.update_signal.emit(result)

def main():
    num_samples = 100
    num_threads = 4

    data_list = []
    for _ in range(num_samples):
        data = pd.DataFrame({'A': np.random.rand(100), 'B': np.random.rand(100)})
        data_list.append(data)

    app = QApplication(sys.argv)
    window = RealTimeConsole(data_list, num_threads)
    window.show()
    sys.exit(app.exec_())

class RealTimeConsole(QMainWindow):
    def __init__(self, data_list, num_threads):
        super().__init__()

        self.setWindowTitle('Real-Time Console')
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.save_button = QPushButton('Save to CSV', self)
        self.save_button.clicked.connect(self.save_to_csv)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.worker = Worker()
        self.worker_threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.worker.update_signal.connect(self.update_console)

        futures = []
        for i, data1 in enumerate(data_list, start=1):
            for j, data2 in enumerate(data_list, start=1):
                future = self.worker_threadpool.submit(self.worker.process, data1, data2, i, j)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            future.result()

    def update_console(self, text):
        self.text_edit.appendPlainText(text)

    def save_to_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "CSV 파일 저장", "", "CSV 파일 (*.csv);;모든 파일 (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write("Index1,Index2,Correlation\n")
                    for item in self.text_edit.toPlainText().split('\n'):
                        if item:
                            f.write(item.replace("Correlation", "").replace(":", "").replace("(", "").replace(")", "").replace(",", "") + "\n")
                print("파일 저장이 완료되었습니다!")
            except Exception as e:
                print("파일 저장 중 오류가 발생했습니다:", e)

if __name__ == '__main__':
    main()
