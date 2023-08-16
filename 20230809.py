from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sys, os
import concurrent.futures
import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta
from functools import partial

corrList = []

def generateData(num_tags):
    '''
        2, 4, 6, 8, 10번 태그를 추출한다.
    '''
    num_tags = num_tags
    maindf = pd.DataFrame()

    for i in range(num_tags):
        np.random.seed(np.random.randint(30))
        n = 60
        data = np.random.uniform(1, 10, size=(n, 1))

        inclination = np.random.uniform(0.1,0.9)
        data = inclination * data
        df = pd.DataFrame(data, columns=[f"Tag{i}"])  # 컬럼명 설정
        maindf = pd.concat([maindf, df], axis=1)

    # 두 변수 간의 상관관계 약화
    for i in range(1, num_tags):
        maindf[f"Tag{i}"] = maindf[f"Tag{i}"] + np.random.uniform(-0.5, 0.5, size=n)

    return maindf

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('toy.ui')
form_class = uic.loadUiType(form)[0]


class Worker(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, num_tags, run_count):
        super().__init__()
        self.num_tags = int(num_tags)
        self.extract_period = int(run_count)
    def run(self):
        dataList = []
        for i in range(self.extract_period):
            dataList.append(generateData(self.num_tags))
        idx = 0
        for k in range(len(dataList)):
            for i in range(self.extract_period):
                for j in range(i+1, self.extract_period):
                    tag1 = f"Tag{i}"
                    tag2 = f"Tag{j}"
                    if tag1 == tag2:  # 같은 태그일 경우 스킵
                        continue
                    corr = dataList[k][f"Tag{i}"].corr(dataList[k][f"Tag{j}"], method='pearson')
                    if abs(corr) > 0.8:
                        idx += 1
                        result = f"[ Tag{i} <-> Tag{j} ] ==> {corr}"
                        corrList.append([f"Tag{i}",f"Tag{j}",f"{corr}"])
                        self.update_signal.emit(result)
        print(corrList)
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.setWindowTitle("발전통합운영시스템 빅데이터 상관분석")
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.graph)

    def run(self):
        self.worker_thread = Worker(self.lineEdit.text(), self.lineEdit_2.text())
        self.worker_thread.update_signal.connect(self.update_text)
        self.worker_thread.start()
    def update_text(self,text):
        self.plainTextEdit.appendPlainText(text)

    def graph(self):
        # xValue = 날짜를 생성할 카운트
        # yValue = 상관계수 데이터
        if len(corrList) !=0:
            # 데이터 시각화 (산점도)
            start_date = datetime.today()
            date_list = [start_date + timedelta(days=x) for x in range(int(self.lineEdit_2.text()))]
            date_format = "%m-%d"  # 원하는 날짜 형식으로 설정
            #날짜 생성
            date_labels = [date.strftime(date_format) for date in date_list]
            #데이터 생성
            data_labels = [np.random.uniform(0.8, 0.85) for _ in range(int(self.lineEdit_2.text()))]
            data_labels2 = [np.random.uniform(0.8, 0.95) for _ in range(int(self.lineEdit_2.text()))]
            #data_labels2 = corrList
            fig = Figure(figsize=(8, 6))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.scatter(date_labels, data_labels, label=f"Tag1 Correlation at")
            ax.scatter(date_labels, data_labels2, label=f"Tag2 Correlation at")
            ax.set_ylim(0,1)
            ax.set_xlabel('Day')
            ax.set_ylabel('Correlation')
            ax.set_title(f"Correlation Analysis Scatter Chart")
            ax.legend()

            # QPixmap으로 변환하여 QLabel에 표시
            canvas = FigureCanvas(fig)
            canvas.draw()
            width, height = fig.get_size_inches() * fig.get_dpi()
            pixmap = QPixmap(int(width), int(height))
            canvas.render(pixmap)
            self.label_2.setPixmap(pixmap)
        else:
            QMessageBox.warning(self,'Warning','산점도는 분석 후에 표시됩니다.',QMessageBox.Ok)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    sys.exit(app.exec_())