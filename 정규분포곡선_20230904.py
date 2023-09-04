import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 랜덤 데이터 생성 (평균 0, 표준편차 1)
data = np.random.normal(0, 1, 1000)

# Z-Score 계산 (여기서는 데이터가 이미 평균 0, 표준편차 1이므로 필요 없음)
z_scores = (data - np.mean(data)) / np.std(data)

print(z_scores)

# 히스토그램
plt.hist(z_scores, bins=20, density=True, alpha=0.6, color='g')

# 정규분포 곡선
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, 0, 1)
plt.plot(x, p, 'k', linewidth=2)

plt.title("Fit results: mean = %.2f,  std = %.2f" % (np.mean(data), np.std(data)))

plt.show()
