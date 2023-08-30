import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Dense
from scipy import stats
from sklearn.model_selection import train_test_split
EPOCH = 5000

tag1 = 'DCD1AIG01ACTI01'
tag2 = 'DCD1AIG01CURR01'

def loadCsvData(tagName):
    df = pd.read_csv(f"./hourData/{tagName}_HAN.csv")
    return df.iloc[:,1]

# 데이터 생성
np.random.seed(42)
#X = [10,20,30,40,50,60,77,80,91]
#y = [100,200,300,400,500,600,700,800,900]
X = loadCsvData(tag1)
y = loadCsvData(tag2)

X = np.array(X)
y = np.array(y)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 정의
model = Sequential()
model.add(Dense(1, input_dim=1))

# 컴파일
model.compile(loss='mean_squared_error', optimizer='Adam')

# 학습
model.fit(X, y, epochs=EPOCH, batch_size=32, verbose=1)

# 예측값 생성
y_pred = model.predict(X).flatten()

# 잔차 계산
residuals = y - y_pred

# 잔차의 표준 오차 계산
stderr = np.std(residuals)

# 95% 신뢰 구간 계산
confidence_interval = stderr * stats.t.ppf((1 + 0.95) / 2, len(y) - 1)

# x2와 y2 데이터
X2 = X  # x2는 x와 값이 완벽하게 같다고 가정
y2 = pd.read_csv(f'./hourData/{tag2}_HAN_zzinppa.csv').iloc[:,1]

X2 = np.array(X2)
y2 = np.array(y2)

# 이상치 판단 기준 설정 (예: 3 * 표준편차)
threshold = 3 * np.std(residuals)

# 이상치 탐지
residuals2 = y2 - y_pred
outliers = np.where(np.abs(residuals2) > threshold)[0]

#잔차의 연속적인 증가구간 찾기
# x와 y를 x에 따라 정렬
sorted_pairs = sorted(zip(X2, y2))
x_sorted, y_sorted = zip(*sorted_pairs)

# 동일한 y값을 가진 연속적인 x 구간 찾기
same_y_intervals = []
start_x = x_sorted[0]
current_y = y_sorted[0]

for i in range(1, len(y_sorted)):
    if y_sorted[i] != current_y:
        if start_x != x_sorted[i-1]:
            same_y_intervals.append((start_x, x_sorted[i-1], current_y))
        start_x = x_sorted[i]
        current_y = y_sorted[i]

# 마지막 구간 체크
if start_x != x_sorted[-1]:
    same_y_intervals.append((start_x, x_sorted[-1], current_y))

# 결과 출력
print("Intervals where y-values are constant while x is increasing:")
for interval in same_y_intervals:
    print(f"From x = {interval[0]} to x = {interval[1]} (y = {interval[2]})")

model.fit(X2, y2)

# 산점도 그리기
plt.figure(figsize=(12, 6))

#정상차트표시
plt.subplot(2, 1, 1)
plt.scatter(X, y, c='orange', s=65, label="Original Data", alpha=0.3)
plt.plot(X, model.predict(X), color='blue', linewidth=1, label="Regression Line")
plt.xlabel(f"{tag1}")
plt.ylabel(f"{tag2}")
# 신뢰구간 그리기
plt.fill_between(X.flatten(), (y_pred - confidence_interval), (y_pred + confidence_interval), color='gray', alpha=0.5)
plt.title("Original Data")
plt.legend()

#오류차트표시
plt.subplot(2, 1, 2)
plt.scatter(X2, y2, c='orange', s=65, label="Error Data", alpha=0.3)
plt.plot(X, model.predict(X), color='blue', linewidth=1, label="Regression Line")
plt.scatter(X2[outliers], y2[outliers], color='red', label="Outliers", marker='x', zorder=5)
plt.xlabel(f"{tag1}")
plt.ylabel(f"{tag2}")
# 신뢰구간 그리기
plt.fill_between(X.flatten(), (y_pred - confidence_interval), (y_pred + confidence_interval), color='gray', alpha=0.5)
x_position = 63 # 예시입니다. 실제로는 원하는 위치를 지정해주세요.
y_position = 616  # 예시입니다. 실제로는 원하는 위치를 지정해주세요.
plt.annotate('95% Confidence Interval', xy=(x_position, y_position), xytext=(x_position+20, y_position + 20),
             arrowprops=dict(facecolor='black', arrowstyle='->'),
             fontsize=12)
plt.title("Predict Data")

# 그래프 그리기
plt.scatter(x_sorted, y_sorted)
plt.title('Scatter Plot with Constant y Intervals')

# 동일한 y값을 가진 구간 표시
for interval in same_y_intervals:
    plt.hlines(interval[2], interval[0], interval[1], colors='r', linestyles='dashed')
plt.legend()



plt.tight_layout()
plt.show()
