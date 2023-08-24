import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

# 실제 회귀직선의 계수와 절편
true_slope = 10
true_intercept = 0.115

# 데이터 생성
np.random.seed(42)
x = np.random.uniform(58, 60, size=(24*31,))
y = true_slope * x + true_intercept + np.random.normal(0, 5, size=(24*31,))  # 오차 추가

# 회귀 모델 학습
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 차원 수정
x_train = x_train.reshape(-1, 1)
x_test = x_test.reshape(-1, 1)

model = Sequential()
model.add(Dense(1, input_dim=1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=1000, verbose=1)

# 잔차 분석 및 표시 (Z-Score 차트)
y_pred = model.predict(x_test)
residuals = y_test - y_pred.flatten()

# Z-Score 계산
z_scores = (residuals - np.mean(residuals)) / np.std(residuals)

# Z-Score 차트 그리기
plt.figure(figsize=(8, 6))
plt.plot(z_scores, marker='o')
plt.axhline(y=0, color='red', linestyle='--')
plt.axhline(y=2, color='green', linestyle='--', label='Upper Threshold (2)')
plt.axhline(y=-2, color='green', linestyle='--', label='Lower Threshold (-2)')
plt.title('Z-Score Chart of Residuals')
plt.xlabel('Observations')
plt.ylabel('Z-Score')
plt.legend()
plt.show()
