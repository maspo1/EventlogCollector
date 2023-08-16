import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

# 가상의 데이터 생성
X = np.random.rand(100, 1)
y = 2 * X + np.random.normal(0, 0.1, size=(100, 1))

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 모델 생성 및 훈련
model = Sequential()
model.add(Dense(1, input_dim=1))
model.compile(loss='mse', optimizer='adam')
model.fit(X_train, y_train, epochs=10000, verbose=1)

# 예측값 계산
y_pred = model.predict(X_test)

# 그래프로 예측값과 실제값 표시
plt.scatter(X_test, y_test, label='Actual')
plt.scatter(X_test, y_pred, label='Predicted')
plt.legend()
plt.show()
