import os
import pandas as pd
import csv
import concurrent.futures

# 폴더에서 파일 이름 가져오기
folder_path = './hourData'
file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# 비교 결과를 저장할 딕셔너리
correlation_results = {}
list1 = []
list2 = []
count = 0

# 모든 파일 조합에 대한 상관계수 계산
with concurrent.futures.ThreadPoolExecutor() as executor:
    for i in range(len(file_names)):
        for j in range(i + 1, len(file_names)):

            file1 = file_names[i]
            file2 = file_names[j]

            data1 = pd.read_csv(os.path.join(folder_path, file1))
            data2 = pd.read_csv(os.path.join(folder_path, file2))

            # 여기서는 첫 번째 열을 사용하여 상관계수를 계산한다고 가정
            # 필요에 따라 다른 열이나 처리 방법을 선택
            col1 = data1.iloc[:, 1]
            col2 = data2.iloc[:, 1]

            # 상관계수 계산 (피어슨 방법)
            correlation = col1.corr(col2, method='pearson')

            # 결과 출력
            print(f"[{count}] {file1} vs {file2} = {correlation}")
            # 파일 열기
            with open('corr_20230830.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([file1.split('_')[0], file2.split('_')[0], correlation])
            count +=1
    #         correlation_results[f"{file1} vs {file2}"] = correlation
    #
    # # 결과 출력
    # for key, value in correlation_results.items():
    #     print(f"The correlation between {key} is {value}")
