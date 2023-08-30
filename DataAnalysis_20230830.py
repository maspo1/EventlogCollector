import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# 데이터 생성
# 데이터 생성 (10% 확률로 NaN 값을 가짐)
data = {'df1': [550, 590, 560, 520, 590, 600, 570, 540, 580, 610],
        'df2': [3, 4, 2.5, 5, 2, np.nan, 3.5, np.nan, 4.2, 3.9]}

df = pd.DataFrame(data)

# Min-Max 정규화
scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(df)
normalized_df = pd.DataFrame(normalized_data, columns=df.columns)

# 산점도 그리기
# 방법 2: 하나의 ax 를 가지는 하나의 figure 생성(ax의 색깔 지정 못함)
fig = Figure(figsize=(10,4))
ax = fig.add_subplot(111)


# 정규화 전 산점도
ax.scatter(df['df1'], df['df2'])
ax.set_title("Before Normalization")
ax.set_xlabel("df1")
ax.set_ylabel("df2")
#ax.legend()
plt.show()
