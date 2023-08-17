orderData = {
    'burger':{
        '빅맥':4600,
        '1955버거':5500
    },
    'coffee':{
        '아메리카노':1800
    }
}
print("***주문하신 목록입니다...")
count = 0
for i in orderData.items():
    for elm in i[1].items():
        count+=1
        print(f"{count}. {elm[0]} : {elm[1]}")
insertItem = int(input("삭제할 주문목록 번호를 입력하세요 : "))

count = 0
found_item = None
for category, items in orderData.items():
    for item, price in items.items():
        count += 1
        if count == insertItem:
            found_item = (category, item)
            break
    if found_item:
        break

if found_item:
    #첫번째 변수에 튜플의 첫째요소, 두번째 변수에 튜플의 둘째 요소를 담음
    #category와 item은 둘다 key임
    category, item = found_item
    del orderData[category][item]
    if orderData[category] == {}:
        del orderData[category]
    print(f"{item}이(가) 삭제되었습니다.")
else:
    print("유효하지 않은 주문목록 번호입니다.")

print(orderData)


#번호를 입력하면 번호에 해당하는 elm의 상위요소를 찾아 키값으로 활용함



#insertItem에 해당하는 키 값을 먼저 구해야함
#a = list(orderData['burger'].keys())[insertItem-1]
#del orderData['burger'][a]

#ount = 0
#for i in orderData.items():
#    for elm in i[1].items():
#        count+=1
#        print(f"{count}. {elm[0]} : {elm[1]}")
#print(list(list(orderData.items())))
#print(list(list(orderData.items())[0][1].items())[0][0]+"을 삭제합니다.")