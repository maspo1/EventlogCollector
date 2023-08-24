import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers

# 날짜 범위 생성 (1시간 간격)
date_range = pd.date_range(start='2023-07-01', end='2023-08-01', freq='H')

# 데이터 생성
data1 = np.random.uniform(60, 61, len(date_range))
data2_high_corr_1 = data1 + np.random.uniform(-0.05, 0.05, len(date_range))
data2_high_corr_2 = data1 + np.random.uniform(-0.1, 0.1, len(date_range))
data2_low_corr_1 = np.random.uniform(650, 680, len(date_range))
data2_low_corr_2 = np.random.uniform(650, 680, len(date_range))

# 데이터프레임 생성
df_high_corr_1 = pd.DataFrame({'Date': date_range, 'Data1': data1, 'Data2': data2_high_corr_1})
df_high_corr_2 = pd.DataFrame({'Date': date_range, 'Data1': data1, 'Data2': data2_high_corr_2})
df_low_corr_1 = pd.DataFrame({'Date': date_range, 'Data1': data1, 'Data2': data2_low_corr_1})
df_low_corr_2 = pd.DataFrame({'Date': date_range, 'Data1': data1, 'Data2': data2_low_corr_2})

# 데이터 전처리
X_high_corr_1 = df_high_corr_1['Data1'].values.reshape(-1, 1)
y_high_corr_1 = df_high_corr_1['Data2'].values

X_high_corr_2 = df_high_corr_2['Data1'].values.reshape(-1, 1)
y_high_corr_2 = df_high_corr_2['Data2'].values

X_low_corr_1 = df_low_corr_1['Data1'].values.reshape(-1, 1)
y_low_corr_1 = df_low_corr_1['Data2'].values

X_low_corr_2 = df_low_corr_2['Data1'].values.reshape(-1, 1)
y_low_corr_2 = df_low_corr_2['Data2'].values

# 모델 생성
model_high_corr_1 = keras.Sequential([
    layers.Input(shape=(1,)),
    layers.Dense(1, use_bias=False, kernel_initializer=keras.initializers.Constant(value=1.0))
])

model_high_corr_2 = keras.Sequential([
    layers.Input(shape=(1,)),
    layers.Dense(1, use_bias=False, kernel_initializer=keras.initializers.Constant(value=0.6))
])

model_low_corr_1 = keras.Sequential([
    layers.Input(shape=(1,)),
    layers.Dense(1, use_bias=False, kernel_initializer=keras.initializers.Constant(value=0.3))
])

model_low_corr_2 = keras.Sequential([
    layers.Input(shape=(1,)),
    layers.Dense(1, use_bias=False, kernel_initializer=keras.initializers.Constant(value=0.1))
])

model_high_corr_1.compile(optimizer='adam', loss='mean_squared_error')
model_high_corr_2.compile(optimizer='adam', loss='mean_squared_error')
model_low_corr_1.compile(optimizer='adam', loss='mean_squared_error')
model_low_corr_2.compile(optimizer='adam', loss='mean_squared_error')

# 모델 훈련
model_high_corr_1.fit(X_high_corr_1, y_high_corr_1, epochs=50, batch_size=32, verbose=1)
model_high_corr_2.fit(X_high_corr_2, y_high_corr_2, epochs=50, batch_size=32, verbose=1)
model_low_corr_1.fit(X_low_corr_1, y_low_corr_1, epochs=50, batch_size=32, verbose=1)
model_low_corr_2.fit(X_low_corr_2, y_low_corr_2, epochs=50, batch_size=32, verbose=1)

# 모델 예측
y_pred_high_corr_1 = model_high_corr_1.predict(X_high_corr_1)
y_pred_high_corr_2 = model_high_corr_2.predict(X_high_corr_2)
y_pred_low_corr_1 = model_low_corr_1.predict(X_low_corr_1)
y_pred_low_corr_2 = model_low_corr_2.predict(X_low_corr_2)

# 잔차 계산
residuals_high_corr_1 = y_high_corr_1 - y_pred_high_corr_1.flatten()
residuals_high_corr_2 = y_high_corr_2 - y_pred_high_corr_2.flatten()
residuals_low_corr_1 = y_low_corr_1 - y_pred_low_corr_1.flatten()
residuals_low_corr_2 = y_low_corr_2 - y_pred_low_corr_2.flatten()

# Z-score 계산
z_scores_high_corr_1 = zscore(residuals_high_corr_1)
z_scores_high_corr_2 = zscore(residuals_high_corr_2)
z_scores_low_corr_1 = zscore(residuals_low_corr_1)
z_scores_low_corr_2 = zscore(residuals_low_corr_2)
z_score_threshold = 2

plt.figure(figsize=(18, 12))

# 상관계수가 1에 가까운 데이터의 산점도와 회귀분석 (1번째 데이터)
plt.subplot(2, 3, 1)
plt.scatter(X_high_corr_1, y_high_corr_1, label='Data1 vs Data2 (Correlation ~ 1)', alpha=0.5)
plt.plot(X_high_corr_1, y_pred_high_corr_1, color='red', label='Model Prediction')
plt.xlabel('Data1')
plt.ylabel('Data2')
plt.legend()

# 상관계수가 1에 가까운 데이터의 잔차와 Z-score (1번째 데이터)
plt.subplot(2, 3, 4)
plt.plot(date_range, residuals_high_corr_1 / np.max(np.abs(residuals_high_corr_1)),
         label='Residuals (Correlation ~ 1)')
plt.axhline(y=z_score_threshold, color='red', linestyle='--', label='Z-Score Threshold')
plt.axhline(y=-z_score_threshold, color='red', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Residuals / Z-Score')
plt.legend()

# 상관계수가 1에 가까운 데이터의 산점도와 회귀분석 (2번째 데이터)
plt.subplot(2, 3, 2)
plt.scatter(X_high_corr_2, y_high_corr_2, label='Data1 vs Data2 (Correlation ~ 0.6)', alpha=0.5)
plt.plot(X_high_corr_2, y_pred_high_corr_2, color='red', label='Model Prediction')
plt.xlabel('Data1')
plt.ylabel('Data2')
plt.legend()

# 상관계수가 1에 가까운 데이터의 잔차와 Z-score (2번째 데이터)
plt.subplot(2, 3, 5)
plt.plot(date_range, residuals_high_corr_2 / np.max(np.abs(residuals_high_corr_2)),
         label='Residuals (Correlation ~ 0.6)')
plt.axhline(y=z_score_threshold, color='red', linestyle='--', label='Z-Score Threshold')
plt.axhline(y=-z_score_threshold, color='red', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Residuals / Z-Score')
plt.legend()

# 상관계수가 0.1에 가까운 데이터의 산점도와 회귀분석 (1번째 데이터)
plt.subplot(2, 3, 3)
plt.scatter(X_low_corr_1, y_low_corr_1, label='Data1 vs Data2 (Correlation ~ 0.1)', alpha=0.5)
plt.plot(X_low_corr_1, y_pred_low_corr_1, color='red', label='Model Prediction')
plt.xlabel('Data1')
plt.ylabel('Data2')
plt.legend()

# 상관계수가 0.1에 가까운 데이터의 잔차와 Z-score (1번째 데이터)
plt.subplot(2, 3, 6)
plt.plot(date_range, residuals_low_corr_1 / np.max(np.abs(residuals_low_corr_1)),
         label='Residuals (Correlation ~ 0.1)')
plt.axhline(y=z_score_threshold, color='red', linestyle='--', label='Z-Score Threshold')
plt.axhline(y=-z_score_threshold, color='red', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Residuals / Z-Score')
plt.legend()

plt.tight_layout()
plt.show()
