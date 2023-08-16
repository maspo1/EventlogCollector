import numpy as np
import pandas as pd
import concurrent.futures
import time

# 가상의 데이터 생성 (2800개 태그, 각 태그에 60개의 데이터)
np.random.seed(0)
n = 60
num_tags = 2800
data = np.random.rand(n, num_tags)
df = pd.DataFrame(data)
counter = 0

# 상관계수 계산 함수
def calculate_correlation(tag1, tag2):
    correlation_coefficient = df[tag1].corr(df[tag2])
    return (tag1, tag2, correlation_coefficient)

# 멀티스레드로 상관계수 분석
start_time = time.time()

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    for i in range(num_tags):
        for j in range(i + 1, num_tags):
            tag1 = df.columns[i]
            tag2 = df.columns[j]
            future = executor.submit(calculate_correla tion, tag1, tag2)
            results.append(future)
            counter += 1

# 결과 출력
completed, _ = concurrent.futures.wait(results)
for future in completed:
    tag1, tag2, correlation_coefficient = future.res  ult()
    if abs(correlation_coefficient) > 0.5:
        '''
        -> 상관계수가 0.5 이상인 설비에 대해서 P-검정을 실시하여 해당 값이 우연에 의한 것인지
           통계적으로 유의미한 값인지 판별하여 최종적인 상관계수를 구한다.
           P-Value가 0.05보다 낮다면 귀무가설을 기각하고 유의미하다고 판단한다.
        
        -> 해당검정을 통과한 후 데이터를 저장하고(메모리 상), 임의의 시간대에 분석을 수행하여 태그간 계수변화를 추적한다.
           단, 임의의 시간대는 다른날의 같은 시간대를 사용한다.
           해당 계수변화추적에는 F-검정을 사용한다.
           
        -> F-검정 후 matpoli를 이용하여 그래프를 출력한다.
        '''
        print(f"상관계수 {tag1}-{tag2}: {round(correlation_coefficient,3)}")

end_time = time.time()
execution_time = end_time - start_time

print(f"총 분석 : {counter} 개")
print(f"실행 시간: {execution_time}초")
