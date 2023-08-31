import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# 예제 데이터
a = np.array([500, 530, np.nan, 550, 570, np.nan, 590, 515])
b = np.array([2, 3, 4, 5, 6, 7, 8, 9])

# 결측값 위치 찾기
nan_indices = np.isnan(a)

# 결측값 제거
a_not_nan = a[~nan_indices]
b_not_nan = b[~nan_indices]

# 데이터 정규화
scaler = MinMaxScaler()
a_not_nan_scaled = scaler.fit_transform(a_not_nan.reshape(-1, 1)).flatten()
b_not_nan_scaled = scaler.fit_transform(b_not_nan.reshape(-1, 1)).flatten()

# 결측값 위치에 대한 정규화된 y 값
b_nan_scaled = scaler.transform(b[nan_indices].reshape(-1, 1)).flatten()

# 산점도 그리기 (정규화된 데이터)
plt.scatter(a_not_nan_scaled, b_not_nan_scaled, marker='o')

# 결측값 위치에 'x' 마커 표시
plt.scatter(np.full(b_nan_scaled.shape, 1), b_nan_scaled, marker='x', c='red')

plt.xlabel('Normalized x')
plt.ylabel('Normalized y')
plt.title('Scatter Plot with Missing Values')
plt.grid(True)
plt.show()
