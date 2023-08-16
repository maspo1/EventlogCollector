import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


def generateData(extract_period):
    '''
        generateData는 extract_period를 통해서 60개의 데이터는 일별로 생성합니다.
        상관관계 약화는 아래의 코드를 사용합니다.

        for i in range(1, extract_period):
        # maindf[f"{i}"] = maindf[f"{i}"] + np.random.uniform(-0.5, 0.5, size=n)
    '''
    extract_period = extract_period
    maindf = pd.DataFrame()

    for i in range(extract_period):
        np.random.seed(np.random.randint(30))
        n = 60
        data = np.random.uniform(1, 10, size=(n, 1))
        inclination = np.random.uniform(0.1, 0.9)
        data = inclination * data
        df = pd.DataFrame(data, columns=[f"{i}"])  # 컬럼명 설정
        maindf = pd.concat([maindf, df], axis=1)

    return maindf

    # 두 변수 간의 상관관계 약화
    # 매일 생성되는 데이터는 비슷한 값을 가짐
    # for i in range(1, extract_period):
        # maindf[f"{i}"] = maindf[f"{i}"] + np.random.uniform(-0.5, 0.5, size=n)

dataDict ={}
for i in range(10):
    dataDict[f'DCDTAG{i}'] = generateData(30)

tags = list(dataDict.keys())  # 태그 리스트 생성

# 상관계수 계산 및 평균 상관계수 계산
total_correlation = 0
num_combinations = 0
dataList = []

overCorrelation = []

#태그전체별 상관계수
for i in range(len(tags)):
    for j in range(i + 1, len(tags)):
        tag1 = tags[i]
        tag2 = tags[j]

        df1 = dataDict[tag1]
        df2 = dataDict[tag2]

        correlation = df1.corrwith(df2, axis=0).mean()  # 전체 데이터에 대한 상관계수 계산 및 평균
        if correlation > 0.7 and correlation < 1:
            overCorrelation.append([tag1,tag2])
            print(f"평균 상관계수: {correlation:.6f} (Tag{tag1} <-> Tag{tag2})")

print(overCorrelation)


def columnCorrelation(dataDict, overCorrelation):
    dict = {}
    for i in range(len(overCorrelation)):
        tag1 = overCorrelation[i][0]
        tag2 = overCorrelation[i][1]
        df1 = dataDict[tag1]
        df2 = dataDict[tag2]

        for idx in range(len(df1.columns)):
            col1 = df1.columns[idx]
            col2 = df2.columns[idx]
            correlation = df1[col1].corr(df2[col2])  # 같은 인덱스의 열 간 상관계수 계산
            print(f"상관계수: {tag1} <{col1}일> <==> {tag2} <{col2}일> {correlation:.6f}")
            dataDict[f"{tag1}<->{tag2}"].append([col1, correlation])
    return dataDict
#열별 상관계수
def columnCorrelation2():
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            tag1 = tags[i]
            tag2 = tags[j]

            df1 = dataDict[tag1]
            df2 = dataDict[tag2]

            for idx in range(len(df1.columns)):
                col1 = df1.columns[idx]
                col2 = df2.columns[idx]

                correlation = df1[col1].corr(df2[col2])  # 같은 인덱스의 열 간 상관계수 계산
                print(f"상관계수: {tag1} <{col1}일> <==> {tag2} <{col2}일> {correlation:.6f}")
def plot_scatter(data, overCorrelation):
    overCorrelation = overCorrelation
    selList = []

    #관계가 있는 태그의 이름을 유일하게 분리
    for item in data:
        sel = item[2]
        selList.append(sel)
    selList = list(set(selList))
    print(selList)

    dataDict = {}

    # target_list의 요소를 순회하면서 다른 리스트에 있는지 검사
    for element in data:
        if element[2] in selList:
            dataDict[f"{element[2]}"] = element
    print(dataDict)



    # for i in range(len(selList)):
    #     # 데이터 분리
    #     dates = [item[0] for item in selected_data]
    #     correlation_values = [item[1] for item in selected_data]
    #     tagNames = [item[2] for item in selected_data]
    #     # 산점도 그리기
    #     fig, ax = plt.subplots(figsize=(8, 6))
    #     ax.scatter(dates, correlation_values, color='gold', label=f"{tagNames} Correlation")
    #     ax.set_xlabel('Date')
    #     ax.set_ylabel('Correlation')
    #     ax.set_title('Tag Scatter Chart')
    #     ax.set_xticklabels(dates, rotation=45)
    #     ax.legend()
    #     plt.tight_layout()
    #     plt.show()


    # # 산점도 그리기
    # fig, ax = plt.subplots(figsize=(8, 6))
    # ax.scatter(dates, correlation_values, color='gold', label=f"{tagName} Correlation")
    # ax.set_xlabel('Date')
    # ax.set_ylabel('Correlation')
    # ax.set_title('Tag Scatter Chart')
    # ax.set_xticklabels(dates, rotation=45)
    # ax.legend()
    # plt.tight_layout()
    # plt.show()


#------------------------실행>>
data = columnCorrelation(dataDict, overCorrelation)
#plot_scatter(data,overCorrelation)
print(data)
