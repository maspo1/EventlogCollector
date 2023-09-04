import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import pandas as pd
from sklearn.metrics import r2_score
from keras import backend as K
from scipy import stats

TAG = 'DCD1AIG01ACTI01'
STDNUM = 4

def r_squared(y_true, y_pred):
    SS_res = K.sum(K.square(y_true - y_pred))
    SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
    return (1 - SS_res/(SS_tot + K.epsilon()))

# 샘플 데이터 생성
np.random.seed(0)
x = np.linspace(0, 10, 500)
y = 2*x**3 - 3*x**2 + x + np.random.normal(0, 10, 500)  # 삼차함수 + 노이즈
df = pd.read_csv(f'./hourData/{TAG}_HAN.csv')
x = pd.to_datetime(df.iloc[:,0]).astype('int64') / 10**9
y = df.iloc[:,1]

# 데이터 정규화
# x = (x - np.min(x)) / (np.max(x) - np.min(x))
# y = (y - np.min(y)) / (np.max(y) - np.min(y))

y = (y-0) / (50-0)
# x = pd.Series(x)
# 훈련/테스트 데이터 분리


# 시퀀스로 변환
def to_sequences(data, seq_length):
    d = []
    for i in range(len(data) - seq_length):
        d.append(data[i:i+seq_length])
    return np.array(d)

seq_length = 10

# 시계열 데이터를 시퀀스로 변환
x_seq = [x[i:i + seq_length] for i in range(len(x) - seq_length)]
y_seq = [y[i + seq_length] for i in range(len(y) - seq_length)]

x_seq = np.array(x_seq)
y_seq = np.array(y_seq)

# Reshape to 3D tensor 차원변환

#x_seq = x_seq.reshape((x_seq.shape[0], seq_length, 1))
#y_seq = y_seq.reshape((y_seq.shape[0], seq_length, 1))
x_train, x_test, y_train, y_test = train_test_split(x_seq, y_seq, test_size=0.2, random_state=0)
# x_train_reshaped = x_train_seq.reshape((x_train_seq.shape[0], seq_length, 1))
# x_test_reshaped = x_test_seq.reshape((x_test_seq.shape[0], seq_length, 1))

# 모델 구성
model = Sequential([
    LSTM(256, input_shape=(seq_length, 1), return_sequences=True),
    LSTM(256),
    Dense(1)
    # Dense(256, activation='relu', input_shape=(1,)),
    # Dense(256, activation='relu'),
    # Dense(256, activation='relu'),
    # Dense(1)
])

# 모델 컴파일
model.compile(optimizer='adam', loss='mse', metrics=[r_squared])

# 모델 훈련
model.fit(x_train, y_train, epochs=500, batch_size=32, verbose=1)

# 예측
y_pred = model.predict(x_test)
r2 = r2_score(y_test, y_pred)
print(y_test.shape)
print(y_pred.shape)
residuals = y_test - y_pred.squeeze()
# 표준편차표시
stderr = np.std(residuals)
print(stderr)
# 신뢰구간 표시 (리니어)
confidence_interval = stderr * stats.t.ppf((1 + 0.95) / 2, len(y_test) - 1)
# 신뢰구간 표시
y_pred_upper = y_pred.squeeze() + 1.96 * stderr
y_pred_lower = y_pred.squeeze() + 1.96 * stderr
# 이동 표준편차 계산
rolling_std = pd.Series(residuals).rolling(window=60).std()
# 이상치 판단 기준 설정 (예: 3 * 표준편차)
threshold = STDNUM * np.std(residuals)
# 이상치 탐지
outliers = np.where(np.abs(residuals) > threshold)[0]
#outliers = np.where(np.abs(residuals) > rolling_std * 3)[0]
# 검증데이터 산점도 그리기
plt.subplot(3,1,1)
plt.scatter(x_test, y_test, label='True')
plt.scatter(x_test, y_pred.squeeze(), label=r'$R^2 : {:.2f}$'.format(r2))
plt.scatter(np.array(x_test)[outliers], np.array(y_test)[outliers], color='red', label=r"$Outliers : {:}.$".format(len(outliers)), marker='x', zorder=5)
plt.fill_between(x_test, y_pred_lower, y_pred_upper, color='gray', alpha=0.5)
plt.title(f"{TAG}_TEST Data for Neural Network Trained")
plt.legend()

# 훈련데이터 산점도
# 재정의부분
y_pred = model.predict(x_train)
residuals = y_train - y_pred.squeeze()
stderr = np.std(residuals)
threshold = STDNUM * np.std(residuals)
outliers = np.where(np.abs(residuals) > threshold)[0]
y_pred_upper = y_pred.squeeze() + 1.96 * stderr
y_pred_lower = y_pred.squeeze() + 1.96 * stderr
r2 = r2_score(y_train, y_pred)

# Z-점수 계산
mean_residual = np.mean(residuals)
std_residual = np.std(residuals)
z_scores = np.abs((residuals - mean_residual) / std_residual)

# 이상치 인덱스 찾기
outliers = np.where(z_scores > 2)[0]

#재정의끝
plt.subplot(3,1,2)
plt.scatter(x_train, y_train, label='True')
plt.scatter(x_train, y_pred.squeeze(), label=r'$R^2 : {:.2f}$'.format(r2))
plt.scatter(np.array(x_train)[outliers], np.array(y_train)[outliers], color='red', label=r"$Outliers : {:}.$".format(len(outliers)), marker='x', zorder=5)
plt.fill_between(x_train, y_pred_lower, y_pred_upper, color='gray', alpha=0.5)
plt.title(f"{TAG}_ORG Data Neural Network Trained")
plt.legend()

plt.subplot(3,1,3)
plt.scatter(x_train, z_scores, c='b')
plt.axhline(y=2, color='r', linestyle='--', label='Z=2')
plt.axhline(y=-2, color='r', linestyle='--', label='Z=-2')
plt.title('Z-scores of Residuals')

plt.show()



