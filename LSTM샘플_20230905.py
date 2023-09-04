import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.dates as mdates

# CSV 파일에서 데이터 읽어오기
df = pd.read_csv('./hourData/DCD1AIG01ACTI01_HAN.csv', parse_dates=['datetime_column'])
df.sort_values('datetime_column', inplace=True)

# 시계열 데이터와 레이블 분리
x = df['datetime_column'].values.astype('int')
y = df['target'].values

# y를 정규화
scaler = MinMaxScaler(feature_range=(0, 1))
y = scaler.fit_transform(y.reshape(-1, 1))

# 시퀀스 길이 설정
seq_length = 10

# 시계열 데이터를 시퀀스로 변환
x_seq = [x[i:i + seq_length] for i in range(len(x) - seq_length)]
y_seq = [y[i + seq_length] for i in range(len(y) - seq_length)]

x_seq = np.array(x_seq)
y_seq = np.array(y_seq)

# 데이터를 3차원으로 변환
x_seq = np.reshape(x_seq, (x_seq.shape[0], x_seq.shape[1], 1))

# 훈련/테스트 데이터 분리
x_train, x_test, y_train, y_test = train_test_split(x_seq, y_seq, test_size=0.2, random_state=0)

# LSTM 모델 생성
# model = Sequential([
#     LSTM(128, input_shape=(seq_length,1)),
#     LSTM(128),
#     Dense(1)
# ])
model = Sequential()
model.add(LSTM(256, activation='relu', input_shape=(seq_length, 1), return_sequences=True))
model.add(LSTM(256, activation='relu', return_sequences=True))
model.add(LSTM(256))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 훈련
model.fit(x_train, y_train, epochs=500, batch_size=32)

# 훈련 데이터와 테스트 데이터에 대한 예측 수행
train_preds = model.predict(x_train)
test_preds = model.predict(x_test)

# 정규화 해제
train_preds_original = scaler.inverse_transform(train_preds)
y_train_original = scaler.inverse_transform(y_train)
test_preds_original = scaler.inverse_transform(test_preds)
y_test_original = scaler.inverse_transform(y_test)

# 결과를 시각화
plt.figure(figsize=(15, 6))

# 훈련 데이터의 원본과 예측 값을 표시
plt.subplot(1, 2, 1)
plt.scatter(x_train[:, seq_length-1, 0], y_train_original, label='True Train')
plt.scatter(x_train[:, seq_length-1, 0], train_preds_original, label='Predicted Train', alpha=0.6)
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Train Data')
plt.legend()

# 테스트 데이터의 원본과 예측 값을 표시
plt.subplot(1, 2, 2)
plt.scatter(x_test[:, seq_length-1, 0], y_test_original, label='True Test')
plt.scatter(x_test[:, seq_length-1, 0], test_preds_original, label='Predicted Test', alpha=0.6)
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Test Data')
plt.legend()

plt.tight_layout()
plt.show()