import scipy.stats as stats
import numpy as np
import pandas as pd


np.random.seed(0)
n = 10
num_tags = 1000
data = np.random.rand(n, num_tags)
df = pd.DataFrame(data)
counter = 0

# 두 변수의 데이터를 준비합니다. (예시 데이터)
x = [1, 2, 3, 4, 5]
y = [5, 4, 2, 2, 1]

# 피어슨 상관계수와 p-value를 계산합니다.
#correlation_coefficient, p_value = stats.pearsonr(x, y)

#print("피어슨 상관계수:", correlation_coefficient)
#print("p-value:", p_value)


for i in range(num_tags):
    for j in range(i+1, num_tags):
        correlation_coefficient, p_value = stats.pearsonr(df[i], df[j])
        if abs(correlation_coefficient) > 0.5 and abs(correlation_coefficient) < 1 and p_value <= 0.05:
            print(f'Corr:{round(correlation_coefficient, 3)} P-Value:{round(p_value, 3)}')