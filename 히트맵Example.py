import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# CSV 파일 읽기
df1 = pd.read_csv("./hourData/DCD1AIG01CURR01_HAN.csv", parse_dates=[0])  # 타임스탬프를 datetime 형태로 파싱
df2 = pd.read_csv("./hourData/DCD1AIG01ACTI01_HAN.csv", parse_dates=[0])

# 날짜로 데이터 묶기
df1['date'] = df1['timestamp'].dt.date
df2['date'] = df2['timestamp'].dt.date

unique_dates = df1['date'].unique()

correlation_list = []

for date in unique_dates:
    subset1 = df1[df1['date'] == date]['value']
    subset2 = df2[df2['date'] == date]['value']

    if len(subset1) == len(subset2):
        correlation = subset1.corr(subset2)
        correlation_list.append((date, correlation))

# 상관계수 DataFrame 생성
correlation_df = pd.DataFrame(correlation_list, columns=['Date', 'Correlation'])

# 상관계수 히트맵
plt.figure(figsize=(20, 5))
sns.heatmap(correlation_df.set_index('Date').T, annot=True, cmap='coolwarm', cbar=True)
plt.title("Daily Correlation Heatmap")
plt.show()
