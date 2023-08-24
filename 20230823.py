import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import seaborn as sns
from scipy import stats  # Import scipy's stats module

# 실제 회귀직선의 계수와 절편
true_slope = 10
true_intercept = 0.115

# 데이터 생성
np.random.seed(42)
x = np.random.uniform(58, 60, size=(24*31,))
y = true_slope * x + true_intercept + np.random.normal(0, 5, size=(24*31,))  # 오차 추가

# 2행 3열의 subplot 생성
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# 회귀 모델 학습
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 차원 수정
x_train = x_train.reshape(-1, 1)
x_test = x_test.reshape(-1, 1)


optimizer = Adam(lr=0.001)
#model.add(Dense(10, activation='relu', input_dim=1))  # 더 깊은 신경망 구조 적용
#model.compile(loss='mean_squared_error', optimizer=optimizer)
model = Sequential()
model.add(Dense(1, input_dim=1))
model.compile(loss='mean_squared_error', optimizer=optimizer)
model.fit(x_train, y_train, epochs=8000, verbose=1, validation_data=(x_test, y_test))

# 원본 산점도와 회귀모델 표시
axs[0, 0].scatter(x, y)
axs[0, 0].plot(x, model.predict(x), color='red', label='Regression Line')
axs[0, 0].set_title('Original Scatter Plot and Regression Line')
axs[0, 0].legend()

# 잔차 분석 및 표시
y_pred = model.predict(x_test).flatten()
residuals = y_test - y_pred
# sns.residplot(x=x_test, y=residuals, ax=axs[1, 0])
# axs[1, 0].set_title('Residuals Plot')
# Z-Score 계산
z_scores = (residuals - np.mean(residuals)) / np.std(residuals)

# Z-Score 차트 그리기
axs[1, 0].plot(z_scores, marker='o')
axs[1, 0].axhline(y=0, color='red', linestyle='--')
axs[1, 0].axhline(y=2, color='green', linestyle='--', label='Upper Threshold (2)')
axs[1, 0].axhline(y=-2, color='green', linestyle='--', label='Lower Threshold (-2)')
axs[1, 0].set_title('Z-Score Chart of Residuals')
#axs[1, 0].xlabel('Observations')
#axs[1, 0].ylabel('Z-Score')
axs[1, 0].legend()

r2 = r2_score(y_test, y_pred)

# 유의미한 회귀 모델인 경우
if r2 >= 0.5:
    # 랜덤한 데이터 생성
    np.random.seed(42)
    x_new = np.random.uniform(58, 60, size=(24 * 31,))
    #y_new = np.random.uniform(580, 600, size=(24 * 31,)) + np.random.normal(0, 10, size=(24 * 31,))
    y_new = true_slope * x + true_intercept + np.random.normal(0, 5, size=(24 * 31,))  # 오차 추가
    x_new = x_new.reshape(-1, 1)  # 차원 수정

    # 훈련된 회귀직선 표시
    regression_line = model.predict(x_new)
    axs[0, 1].scatter(x_new, y_new, c='blue', label='Data')
    axs[0, 1].plot(x_new, model.predict(x_new.reshape(-1, 1)), color='orange', label='Regression Line')
    axs[0, 1].set_title('Regression Line')

    # 유의미한 신뢰대 벗어나는 데이터 표시
    confidence_interval = residuals.std() * 1.96
    outliers = np.where(np.abs(residuals) > confidence_interval)[0]
    axs[0, 1].scatter(x_test[outliers], y_test[outliers], c='red', marker='x', label='Outliers')
    axs[0, 1].legend()

    # 신뢰대 표시
    axs[0, 1].fill_between(x_new.flatten(), regression_line.flatten() - confidence_interval,
                           regression_line.flatten() + confidence_interval, color='gray', alpha=0.3,
                           label='Confidence Interval')
    axs[0, 1].legend()

# 모델의 MSE와 MAE 계산
mse = np.mean((y_test - y_pred.flatten())**2)
mae = np.mean(np.abs(y_test - y_pred.flatten()))

# 오차 검증 정보 표시
axs[1, 1].axis('off')
axs[1, 1].text(0, 0.3, f'R-squared: {r2:.4f}', fontsize=8)
axs[1, 1].text(0, 0.25, f'Standard Error: {np.std(residuals):.4f}', fontsize=8)
axs[1, 1].text(0, 0.2, f'Coefficients1: {model.layers[0].get_weights()[0][0][0]:.4f}', fontsize=8)
# MSE와 MAE 표시
axs[1, 1].text(0, 0.15, f'MSE: {mse:.4f}', fontsize=8)
axs[1, 1].text(0, 0.1, f'MAE: {mae:.4f}', fontsize=8)






plt.tight_layout()
plt.show()
