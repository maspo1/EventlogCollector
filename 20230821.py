import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense

# 예시 데이터 생성
X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# 모델 생성
model = Sequential()
model.add(Dense(units=1, input_dim=1))
model.compile(optimizer='sgd', loss='mean_squared_error')

# 모델 훈련
history = model.fit(X, y, epochs=1000, verbose=0)

# 훈련된 모델로 예측
predictions = model.predict(X)

# 예측 결과 그래프로 표현
plt.scatter(X, y, label='Raw Data')
plt.plot(X, predictions, color='red', label='Regression Line')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Regression Result')
plt.legend()
plt.show()
