#1. 요소가 3개인 리스트 3개사용
#2. 합이 15가 되는 조합을 찾음
#3. 리스트들 끼리도 15가 되는 조합을 찾음

#15가 되는 중복되지 않는 쌍을 모두 구하기


loop = [1,2,3,4,5,6,7,8,9]
concat = []

# 3개의 숫자로 15를 만드는 쌍을 모두 구하기

for i in range(len(loop)):
    for j in range(len(loop)):
        for k in range(len(loop)):
            if loop[i] + loop[j] + loop[k] == 15 and len(set([loop[i],loop[j],loop[k]])) == 3:
                a = [loop[i],loop[j],loop[k]]
                concat.append(a)

comp = []

for i in range(len(concat)):
    for j in range(len(concat)):
        for k in range(len(concat)):
            if concat[i][0] + concat[j][0] + concat[k][0] == 15 and \
                    concat[i][1] + concat[j][1] + concat[k][1] == 15 and \
                    concat[i][2] + concat[j][2] + concat[k][2] == 15 and \
                    concat[i][2] + concat[j][1] + concat[k][0] == 15 and \
                    concat[i][0] + concat[j][1] + concat[k][2] == 15:
                    for l in range(3):
                        comp.append(concat[i][l])
                        comp.append(concat[j][l])
                        comp.append(concat[k][l])
                    if len(set(comp)) == 9:
                        comp = []
                        print(f"마방진이 가능한 조합은{concat[i]}입니다...{concat[j]} {concat[k]}")


