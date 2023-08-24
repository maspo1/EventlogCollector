import pandas as pd

# CSV 파일을 읽어 DataFrame 생성 (컬럼 이름이 없는 경우 header=None을 지정)
df = pd.read_csv('./ex.csv', header=None)

# 0열과 2열을 그룹화하여 횟수를 계산
grouped = df.groupby([0, 1]).size().reset_index(name='count')

# combined_counts가 30 이상인 조합을 필터링
filtered_groups = grouped[grouped['count'] >= 30]
print(filtered_groups)
print("카운트가 31이상이면 안됨")

# 필터링된 조합의 유니크한 행 추출
unique_filtered_groups = filtered_groups.drop_duplicates(subset=[0, 1])

# 유니크한 조합과 조건을 만족하는 데이터 추출
filtered_df = df[
    (df[0].isin(unique_filtered_groups[0])) &
    (df[1].isin(unique_filtered_groups[1]))
]

print(filtered_df)

# 새로운 DataFrame을 CSV 파일로 저장
filtered_df.to_csv('filtered_rows_file.csv', index=False)
