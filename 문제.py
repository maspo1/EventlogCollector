'''
세트가격: 단품가격 + 1500원
라지세트의 가격은 일반세트의 가격 +500원
세트의 기본 구성은 감자튀김과 콜라 기준
세트의 사이드 변경시 감자튀김 대비 선택한 사이드 제품의 차액 적용
세트의 음료변경시 콜라 가격 대비 선택한 음료 제품의 차액 적용
재료추가: 버거 재료 추가는 양상추 추가 무료 & 버거 치즈 추가 1장당 +500원 &양파 1번당 +500원
음료 기본값은 m사이즈이고 L로 변경시 +500원
메뉴입력, 버튼입력은 모두 숫자로 받는다(input함수)

'''

burger = {"빅맥":4600, "맥스파이시상하이치킨버거":4600, "트리플리치포테이토머쉬룸버거":6900, "트리플리치포테이토버거":6500,
          "트리플치즈버거":5600, "1955버거":5700, "더블팔레오피쉬버거":5000, "팔레오피쉬버거":5000}
happy_snack = {"츄러스":1500, "카페라떼":2200, "자두칠러":2000, "케이준비프스낵랩":1500, "불고기버거":1900,
               "에그불고기버거":2500, "팔레오피쉬버거":2500}
side = {"감자튀김":1500, "츄러스&선데이콤보":3000, "츄러스&맥카페":3200, "케이준비프스낵랩":1500, "상하이치킨스낵랩":2200,
        "맥너겟10p":4500, "맥너겟4p":1800, "맥스파이시치킨텐더":4900, "맥너겟6p":3000, "맥스파이시치킨텐더2p":2500,
        "골든모짜렐라치즈4p":4000, "골든모짜렐라치즈2p":2200}
set_side = {"감자튀김":0, "골든모짜렐라치즈2p":500, "감자튀김&골든모짜렐라치즈2p":800}
coffee = {"츄러스&맥카페-콤보":3200, "바닐라라떼":3200, "카페라떼":2200, "아메리카노":1700, "에스프레소":1500, "카푸치노":2200,
          "드립커피":1000, "아이스바닐라라떼":3200, "아이스아메리카노":2200, "아이스카페라떼":2700, "아이스드립커피":1000,
          "디카페인아메리카노":1800}
dessert = {"츄러스":1500, "츄러스&선데이콤보":3000, "베리스트로베리맥플러리":2500, "스트로베리콘":1200, "오레오맥플러리":2500,
           "딸기오레오맥플러리":2500, "초코오레오맥플러리":2500, "초코콘":700, "아이스크림콘":700, "초코선데이아이스크림":1500,
           "딸기선데이아이스크림":1500, "애플파이":1400}
drink = {"딸기칠러":2000, "자두칠러":2000, "초코쉐이크":2500, "딸기쉐이크":2500, "바닐라쉐이크":2500, "코카콜라제로":1400,
         "코카콜라":1400, "스프라이트":1400, "환타":1400, "우유":1500, "생수":1200}
set_drink = {"코카콜라M":0, "스프라이트M":0, "환타M":0, "코카콜라제로M":0, "딸리칠러M":1300, "자두칠러M":1300, "아이스드립커피":0,
             "아이스아메리카노M":0, "아이스카페라떼M":0, "아이스바닐라라떼M":0, "드립커피M":0, "아메리카노M":0}
happy_meal = {"불고기버거":3900, "맥너겟":3900, "치즈버거":3900, "햄버거":3900}
mcmorning = {"에그 맥머핀":3000, "베이컨 에그 맥머핀":3400, "베이컨 토마토 에그 머핀":3700}
mcmorning_combo = {"에그 맥머핀 콤보":3500, "베이컨 에그 맥머핀 콤보":3700, "소세지 에그 맥머핀 콤보":4200}

통합 ={}
통합['burger']=burger
통합['happy_snack']=happy_snack
통합['side']=side
통합['coffee']=coffee
통합['dessert']=dessert
통합['drink']=drink
통합['happy_meal']=happy_meal
통합['set_side']=set_side
통합['set_drink']=set_drink
통합['mcmorning']=mcmorning
통합['mcmorning_combo']=mcmorning_combo
menuCategory = list(통합.keys())
menuDetail = list(통합.values())

#프로그램 흐름
# 메뉴추가 -> 장바구니 추가 -> 장바구니 수정-> 최종

#전역변수 및 함수정의
orderData = {}
summation = 0
def burgerSelect(burgerList):
    print("버거 메뉴에는", *burgerList[0], "가 있습니다.")
    addBurger = int(input("선택할 버거 입력 : "))
    tempSummation = list(burgerList[0].values())[addBurger - 1]
    print("단품버거 재료추가/변경란 입니다.")
    print("버거에 ①양상추 추가는 무료, 버거에 ②치즈추가는 1장당 500원 추가, ③양파 1번당 500원이 추가됩니다.")
    print("①양상추추가, ②치즈추가, ③양파추가 (모든재료 중복추가가능)")
    addCabbage = int(input("양상추는 몇번이나 추가할까요?: "))
    addCheese = int(input("치즈는 몇번이나 추가할까요?: "))
    addOnion = int(input("양파는 몇번이나 추가할까요?: "))
    print(f"양상추 {addCabbage}번, 치즈 {addCheese}장, 양파{addOnion}번, 재료추가 가격은 +{(addOnion + addCheese) * 500}원 입니다.")
    tempSummation += (addCheese + addOnion) * 500
    print(f"총 가격은 {tempSummation}원 입니다.")
    return tempSummation
def showMainMenu():
    print("포장을 선택하셨습니다.")
    print("추천메뉴: 1.버거, 2.해피스낵, 3.사이드, 4.커피, 5.디저트, 6.음료, 7.해피밀이 있습니다.")
    meal = int(input("위 번호 중 하나를 입력하세요 : "))
    return meal

def insertMenu(shopList):
    print("수정을 선택하셨습니다.")
    for i in range(len(shopList)):
        print(f"{shopList}")
#어떤 메뉴에도 적용되는 함수
def universialSelect(dict,dictIndex):
    tempSummation = {}
    print(f"{list(dict.keys())[dictIndex]}을(를) 선택하셨군요 메뉴 보여드릴게요.")
    for i in range(len(list(dict.values())[dictIndex].keys())):
        print(f"({i+1}) {list(list(dict.values())[dictIndex].keys())[i]} : {list(list(dict.values())[dictIndex].values())[i]}원")
    while True:
        addItem = int(input(f"위의 메뉴 중 드시고 싶으신 메뉴를 입력하세요 : "))
        stopFunction = int(input(f"선택한 메뉴는 ★{list(list(dict.values())[dictIndex].keys())[addItem - 1]}★ 입니다. 장바구니에 추가하시려면 0을 눌러주세요. 취소는 다른 번호입니다."))
        #print("최고 상위 메인 메뉴로 돌아가기 만들어야함!!!!!!!!!!!")
        #print("버거 계산용 배열따로 만들고 수정기능 만들어야함")
        if stopFunction ==0:
            break
    a = {}
    result = {}
    b = list(dict.keys())[dictIndex]
    v = list(list(dict.values())[dictIndex].keys())[addItem - 1]
    x = list(list(dict.values())[dictIndex].values())[addItem - 1]
    a[v]=x
    result[b]=a
    return result


#코드시작
print("#################################################")
print("")
print("맥도날드 키오스크 프로그램 v1.0")
print("")
print("#################################################")
eatSelect = int(input("포장=> 1 입력, 매장=> 2 입력, 종료=> 0 입력 : "))

if eatSelect ==1:
    d = 0
    while eatSelect !=0:
        meal = showMainMenu()
        chosenMenu = universialSelect(통합,meal-1)
        if list(chosenMenu.keys())[0] not in orderData:
            orderData[list(chosenMenu.keys())[0]] = list(chosenMenu.values())[0]
        else:
            orderData[list(chosenMenu.keys())[0]].update(list(chosenMenu.values())[0])
        print(orderData,"현재까지 장바구니에 추가된 목록입니다.....**")
        eatSelect = int(input("==>다른 메뉴가 있으면 선택 해주세요 포장=>1입력, 매장=>2입력, 종료=>0 : "))

        for category, items in orderData.items():
            for item, price in items.items():
                print(price)

    print(f"장바구니의 총 합계는 {summation}원 입니다.")
    #insertMenu(orderData)
    #for i in shopList:
    #    summation +=i
    #print(f"총 가격은 {summation}원 입니다.")
else:
    pass

'''
    #같은 키가 존재할 때
    if list(dict.keys())[dictIndex] in shopList:
        #print("같은키가 존재합니다.")
        #shopList[list(dict.keys())[dictIndex]].append
    #같은 키가 존재하지 않을
    else:
        #shopList[list(dict.keys())[dictIndex]]=[list(list(dict.values())[dictIndex].items())[addItem-1]]
        #print(type(shopList))
        #print(shopList)

'''


