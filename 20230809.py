import pandas as pd

# 두 개의 삼중 리스트 예시 데이터
data_list_1 = [
    [['apple', '2023-07-01'], [0.5, 0.5, 0.5]],
    [['banana', '2023-07-02'], [0.3, 0.4, 0.6]],
    [['orange', '2023-07-03'], [0.8, 0.2, 0.7]]
]

data_list_2 = [
    [['grape', '2023-07-01'], [0.1, 0.2, 0.3]],
    [['kiwi', '2023-07-02'], [0.9, 0.8, 0.7]],
    [['pear', '2023-07-03'], [0.4, 0.5, 0.6]]
]

# 데이터프레임을 저장할 리스트 초기화
data_frames = []

# 첫 번째 삼중 리스트 처리
for entry in data_list_1:
    company_name, date = entry[0]
    values = entry[1]

    data = {
        'Company': company_name,
        'Date': date,
        'Values': values
    }

    df = pd.DataFrame(data)
    data_frames.append(df)

# 두 번째 삼중 리스트 처리
for entry in data_list_2:
    company_name, date = entry[0]
    values = entry[1]

    data = {
        'Company': company_name,
        'Date': date,
        'Values': values
    }

    df = pd.DataFrame(data)
    data_frames.append(df)

# 모든 데이터프레임을 하나로 합치기
result_df = pd.concat(data_frames, ignore_index=True)

print(result_df)
