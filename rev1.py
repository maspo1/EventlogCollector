import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress, zscore
import random

# 날짜 범위 생성
date_range = pd.date_range(start='2023-07-01', end='2023-07-31', freq='H')

# 기준 데이터 생성
data1 = np.random.uniform(60, 61, len(date_range))

# 상관계수 목표치
correlation_target = 0.9

# 두 번째 데이터 생성
data2 = correlation_target * data1 + np.random.uniform(-0.2, 0.2, len(date_range))

# 데이터프레임 생성
df = pd.DataFrame({'Date': date_range, 'Data1': data1, 'Data2': data2})

# 상관계수 계산
correlation = df['Data1'].corr(df['Data2'])
print(correlation)
if correlation >= 0.7:
    print("두 데이터의 상관계수는 0.9 이상입니다.")
else:
    print("두 데이터의 상관계수가 0.9 이상이 아닙니다.")

# 회귀분석
slope, intercept, r_value, p_value, std_err = linregress(df['Data1'], df['Data2'])
regression_line = slope * df['Data1'] + intercept

# 잔차 계산
residuals = df['Data2'] - regression_line

# Z-score 계산
z_scores = zscore(residuals)
z_score_threshold = 2

# 그래프 그리기
plt.figure(figsize=(12, 8))

# 산점도
plt.subplot(3, 2, 1)
plt.scatter(df['Date'], df['Data1'], label='Data1', alpha=0.5)
plt.scatter(df['Date'], df['Data2'], label='Data2', alpha=0.5)
plt.xlabel('Date')
plt.ylabel('Data')
plt.legend()

# 회귀분석
plt.subplot(3, 2, 3)
plt.scatter(df['Data1'], df['Data2'], label='Scatter Plot', alpha=0.5)
plt.plot(df['Data1'], regression_line, color='red', label='Regression Line')
plt.xlabel('Data1')
plt.ylabel('Data2')
plt.legend()


# 잔차와 Z-score
plt.subplot(3, 2, 5)
plt.plot(df['Date'], residuals, label='Residuals')
plt.axhline(y=z_score_threshold, color='red', linestyle='--', label='Z-Score Threshold')
plt.axhline(y=-z_score_threshold, color='red', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Residuals / Z-Score')
plt.legend()

# 산점도
plt.subplot(3, 2, 2)
plt.scatter(df['Date'], df['Data1'], label='Data1', alpha=0.5)
plt.scatter(df['Date'], df['Data2'], label='Data2', alpha=0.5)
plt.xlabel('Date')
plt.ylabel('Data')
plt.legend()

# 회귀분석
plt.subplot(3, 2, 4)
plt.scatter(df['Data1'], df['Data2'], label='Scatter Plot', alpha=0.5)
plt.plot(df['Data1'], regression_line, color='red', label='Regression Line')
plt.xlabel('Data1')
plt.ylabel('Data2')
plt.legend()


# 잔차와 Z-score
plt.subplot(3, 2, 6)
plt.plot(df['Date'], residuals, label='Residuals')
plt.axhline(y=z_score_threshold, color='red', linestyle='--', label='Z-Score Threshold')
plt.axhline(y=-z_score_threshold, color='red', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Residuals / Z-Score')
plt.legend()

plt.tight_layout()
plt.show()
