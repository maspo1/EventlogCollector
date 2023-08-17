import numpy as np
import matplotlib.pyplot as plt

# 주어진 데이터 딕셔너리
data = {
    'apple': [['2023-07-01', 0.5], ['2023-07-02', np.nan], ['2023-07-03', 0.7]],
    'tesla': [['2023-07-01', 0.5], ['2023-07-02', np.nan], ['2023-07-03', 0.8]]
}

# 데이터 추출
companies = list(data.keys())
dates = [entry[0] for entry in data[companies[0]]]
values = {company: [entry[1] for entry in data[company]] for company in companies}

# Scatter 차트 표시
plt.figure(figsize=(10, 6))

for company in companies:
    plt.scatter(dates, values[company], label=company)

# NaN 값 위치에 초록색 X 마커 표시
for i, date in enumerate(dates):
    for company in companies:
        if np.isnan(values[company][i]):
            print(np.nanmin(list(values.values()))-0.1)
            plt.scatter(date, np.nanmin(list(values.values())) - 0.1, c='green', marker='x', s=100)

plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Scatter Chart for Stocks')
plt.legend()
plt.show()
