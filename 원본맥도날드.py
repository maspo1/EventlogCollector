import datetime

now = datetime.datetime.now()
# 맥모닝 시간대에는 맥모닝,맥모닝콤보,해피스낵,음료,추천메뉴만 노출되며(burger출력x), 추천메뉴내부구성은 맥모닝 및 음료메뉴, 해피스낵으로 구성
# 그 외 시간에는 하단메뉴 전부노출
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
#2중 while로 작성을했었어야 장바구니에 저장할수있었으려나
while True:
    print("맥도날드키오스크프로젝트")
    eat = int(input("1.포장? 2.매장?: "))
    if eat == 1:
        print("포장을 선택하셨군요")
        print("추천메뉴: 1.버거 2.해피스낵 3.사이드 4.커피 5.디저트 6.음료 7.해피밀이 있습니다.") #
        meal = int(input("위 메뉴중 하나를 선택해 주세요.: "))

        if meal == 1:
            if 4 < now.hour < 10 and now.minute < 30:
                print(f"현재시간은 {now.hour}시{now.minute}분이므로 맥모닝 시간대입니다.")
                print(f"맥모닝 시간대의 메뉴는", *mcmorning, "(와)과 ", *mcmorning_combo, "(이)가 있습니다.")
                m_morning = int(input("맥모닝 메뉴는 무엇을 선택하시겠습니까? 1)맥모닝 2)맥모닝콤보: "))
                if m_morning == 1:
                    print("맥모닝 메뉴를 선택하셨습니다.")
                    print("맥모닝 메뉴에는", *mcmorning,"이(가) 있습니다.")
                    macMorning = int(input("위의 메뉴중 드시고 싶으신 맥모닝 메뉴를 선택하세요.: "))
                    a = list(mcmorning.items())
                    for i in range(len(a)):
                        if a == a[i][0]:
                            print(a[i][0])
                        elif a != a[i][0]:
                            print("a[i][0]이 아니다.")
                        else:
                            print("????")
                elif m_morning == 2:
                    print("맥모닝콤보 메뉴를 선택하셨습니다.")
                    print("맥모닝콤보 메뉴에는", *mcmorning_combo,"이(가) 있습니다.")
                    macMorning2 = int(input("위의 메뉴중 드시고 싶으신 맥모닝 콤보를 선택하세요.: "))
                    a = list(mcmorning.items())
                    for i in range(len(a)):
                        if a == a[i][0]:
                            print(a[i][0])
                        elif a != a[i][0]:
                            print("a[i][0]가 아니다")
                        else:
                            print("??????????")
            else:
                print(f"현재시간은 {now.hour}시{now.minute}분이므로 맥모닝 시간대가 아닙니다.")
                print(f"맥모닝 시간대가 아닌 메뉴는", *burger,"(이)가 있습니다.")
            set_menu = int(input("버거는 1.단품메뉴인가요? 2.세트메뉴인가요?:"))
            if set_menu == 1:
                print("단품메뉴를 선택하셨습니다.")
                print("버거 메뉴에는", *burger,"(이)가 있습니다.")
                mcburger = int(input("위의 메뉴중 드시고 싶으신 메뉴를 입력하세요.: "))
                a = list(burger.keys())
                #print(a) #(키, 밸류)형식의 튜플
                for i in range(len(a)):
                    if
                        print(a[mcburger-1][0], "입니다")
                    else:
                        print("오답")
                print("단품버거 재료추가/변경란 입니다.")
                print("버거에 ①양상추 추가는 무료, 버거에 ②치즈추가는 1장당 500원 추가, ③양파 1번당 500원이 추가됩니다.")
                print("①양상추추가, ②치즈추가, ③양파추가 (모든재료 중복추가가능)")
                addFood = int(input("양상추 추가는 1번, 치즈 추가는 2번, 양파 추가는 3번을 눌러주세요: "))
                if addFood == 1:
                    addCabbage = int(input("양상추는 몇번이나 추가할까요?: "))
                    print(f"양상추 {addCabbage}번 추가하며 가격추가는 없습니다.")
                elif addFood == 2:
                    addCheese = int(input("치즈는 몇장이나 추가할까요?: "))
                    print(f"치즈 {addCheese}장 추가하며, 추가가격은 {addCheese * 500}원 입니다.")
                elif addFood == 3:
                    addOnion = int(input("양파는 몇번이나 추가할까요?: "))
                    print(f"양파 {addOnion}번 추가하며, 추가가격은 {addOnion * 500}원 입니다.")
                else:
                    print("잘못입력하셨습니다.")

            elif set_menu == 2:
                print("세트메뉴를 선택하셨습니다.")
                size = int(input("세트메뉴 사이즈는 1.일반인가요 2.라지인가요?"))
                if size == 1:
                    print("일반사이즈를 선택하셨습니다. 세트메뉴 버거먼저 선택해주세요.")
                    print("세트메뉴 버거선택에는", *burger,"(이)가 있습니다.")
                    mcburger2 = int(input("위의 메뉴중 드시고 싶으신 메뉴를 입력하세요.: "))
                    a = list(burger.items())
                    for i in range(len(a)):
                        if a == a[i][0]:
                            print(a[i][0])
                        elif a != a[i][0]:
                            print("x")
                        else:
                            print("??????")
                    print("세트메뉴 사이드메뉴 선택란입니다.")
                    print("세트메뉴 사이드메뉴에는", *set_side,"(이)가 있습니다")
                    print("세트메뉴사이드 기본선택은 '감자튀김'이며, 사이드메뉴 변경시 차액이 추가될 수 있습니다.")
                    mcSetside = int(input("세트메뉴 사이드메뉴를 선택해주세요.: "))
                    if mcSetside == 1:
                        print("감자튀김")
                    elif mcSetside == 2:
                        print("골든모짜렐라치즈2p")
                    elif mcSetside == 3:
                        print("감자튀김&골든모짜렐라치즈2p")
                    else:
                        print("잘못입력.")
                    print("세트메뉴 음료 선택란입니다.")
                    print("세트메뉴 음료에는", *set_drink,"(이)가 있습니다.")
                    print("세트음료 기본선택은 '콜라M'이며, 음료 변경 및 음료 사이즈변경시 차액이 추가될 수 있습니다.")
                    mcSetdrink = int(input("세트메뉴 음료를 선택해 주세요.: "))
                    if mcSetdrink == 1:
                        print("콜라M")
                    elif mcSetdrink == 2:
                        print("스프라이트M")
                    elif mcSetdrink == 3:
                        print("환타M") #for문 돌릴것.
                    print("세트메뉴 버거 재료추가/변경란입니다.")
                    print("버거에 ①양상추추가는 무료, 버거에 ②치즈추가는 1장당 500원 추가, ③양파 1번당 500원이 추가됩니다.")
                    print("①양상추추가, ②치즈추가, ③양파추가 (모든메뉴 중복추가가능)")
                    addFood = int(input("양상추 추가는 1번, 치즈 추가는 2번, 양파 추가는 3번을 눌러주세요: "))
                    if addFood == 1:
                        print("양상추추가는 무료입니다.")
                    elif addFood == 2:
                        print("치즈추가합니다.")
                    elif addFood == 3:
                        print("양파추가합니다.")
                    else:
                        print("잘못입력하셨습니다.")
                elif size == 2: #라지사이트 선택시 일반세트가격의 +500
                    print("라지사이즈를 선택하셨습니다. 세트메뉴 버거먼저 선택해주세요.")
                    print("세트메뉴 버거에는", *burger,"(이)가 있습니다.")
                    mcburger2 = int(input("위의 메뉴중 드시고 싶으신 메뉴를 입력하세요.: "))
                    a = list(burger.items())
                    for i in range(len(a)):
                        if a == a[i][0]:
                            print(a[i][0])
                        elif a != a[i][0]:
                            print("a[i][0]이 아니다.")
                        else:
                            print("?????????")
                    print("세트메뉴 사이드메뉴 선택란입니다.")
                    print("세트메뉴 사이드 메뉴에는", *set_side,"(이)가 있습니다.")
                    print("세트메뉴 기본선택은 '감자튀김'이며, 사이즈 메뉴 변경시 차액이 추가될 수 있습니다.")
                    mcSetside = int(input("세트메뉴 사이즈메뉴를 선택해주세요: "))
                    if mcSetside == 1:
                        print("감자튀김")
                    elif mcSetside == 2:
                        print("골든모짜렐라치즈2p")
                    elif mcSetside == 3:
                        print("감자튀김&골든모짜렐라치즈2p")
                    else:
                        print("잘못입력.")
                    print("세트메뉴 음료 선택란입니다.")
                    print("세트메뉴 음료에는", *set_drink,"(이)가 있습니다.")
                    print("세트음료 기본선택은 '콜라M'이며, 음료 변경 및 음료 사이즈변경시 차액이 추가될 수 있습니다.")
                    mcSetdrink = int(input("세트메뉴 음료를 선택해 주세요.: "))
                    if mcSetdrink == 1:
                        print("콜라M")
                    elif mcSetdrink == 2:
                        print("스프라이트M")
                    elif mcSetdrink == 3:
                        print("환타M") #for문돌릴것.
                    print("세트메뉴 버거 재료추가/변경란입니다.")
                    print("버거에 ①양상추 추가는 무료, 버거에 ②치즈추가는 1장당 500원 추가, ③양파 1번당 500원이 추가됩니다.")
                else:
                    print("잘못된 입력입니다 다시 입력해주세요.")

        elif meal == 2:
            print("해피스낵을 선택하셨군요 메뉴보여드릴게요.")
            print("해피스낵 메뉴에는", *happy_snack,"(이)가 있습니다.")
            mcsnack = input("위의 메뉴중 드시고 싶으신 메뉴를 입력하세요.: ")
            a = list(happy_snack.items())
            for i in range(len(a)):
                if a == a[i][0]:
                    print(a[i][0])
                elif a != a[i][0]:
                    print("a[i][0]가 아니다")
                else:
                    print("???????????")

        elif meal == 3:
            print("사이드메뉴를 선택하셨군요. 메뉴보여드릴게요.")
            print("사이드메뉴에는", *side,"(이)가 있습니다.")
            mcside = input("위의 메뉴중 드시고 싶으신 사이드메뉴를 선택하세요.: ")
            a = list(side.items())
            for i in range(len(a)):
                if a == a[i][0]:
                    print(a[i][0])
                elif a != a[i][0]:
                    print("a[i][0]가 아니다")
                else:
                    print("???????????")

        elif meal == 4:
            print("커피를 선택하셨군요. 메뉴보여드릴게요.")
            print("커피메뉴에는", *coffee,"(이)가 있습니다.")
            coffe_size = int(input("커피 사이즈는 1.일반인가요 2.라지인가요?: "))#커피 라지는 +500
            if coffe_size == 1:
                print("커피 일반사이즈 선택하셨습니다")
                print("1")
                mcCoffee = int(input("위의 메뉴중 드시고 싶으신 커피메뉴를 선택하세요.: "))
                a = list(coffee.items())
                for i in range(len(a)):
                    if a == a[i][0]:
                        print(a[i][0])
                    elif a != a[i][0]:
                        print("a[i][0]가 아니다")
                    else:
                        print("???????????")
            elif coffe_size == 2:
                print("커피 라지사이즈 선택하셨습니다")
                print("2")
                mcCoffee = int(input("위의 메뉴중 드시고 싶으신 커피메뉴를 선택하세요.: "))
                a = list(coffee.items())
                for i in range(len(a)):
                    if a == a[i][0]:
                        print(a[i][0])
                    elif a != a[i][0]:
                        print("a[i][0]가 아니다")
                    else:
                        print("???????????")
            else:
                print("잘못된 입력입니다. 다시입력해주세요.")

        elif meal == 5:
            print("디저트메뉴를 선택하셨군요. 메뉴보여드릴게요.")
            print("디저트메뉴에는", *dessert,"(이)가 있습니다.")
            mcdessert = int(input("위의 메뉴중 드시고 싶으신 디저트메뉴를 선택하세요.: "))
            a = list(dessert.items())
            for i in range(len(a)):
                if a == a[i][0]:
                    print(a[i][0])
                elif a != [i][0]:
                    print("a[i][0]가 아니다")
                else:
                    print("???????")

        elif meal == 6:
            print("음료를 선택하셨군요. 메뉴보여드릴게요.")
            print("음료메뉴에는", *drink,"(이)가 있습니다.")
            drink_size = int(input("음료 사이즈는 일반인가요 라지인가요?: "))
            if drink_size == 1:
                print("음료 일반입니다.")
                mcdrink = int(input("위의 메뉴중 드시고 싶으신 음료를 선택하세요.:"))
                a = list(drink.items())
                for i in range(len(a)):
                    if a == a[i][0]:
                        print(a[i][0])
                    elif a != [i][0]:
                        print("a[i][0]가 아니다")
                    else:
                        print("???????")
            elif drink_size == 2:
                print("음료 라지입니다.")
                mcdrink2 = int(input("위의 메뉴중 드시고 싶으신 음료를 선택하세요.: "))
                a = list(drink.items())
                for i in range(len(a)):
                    if a == a[i][0]:
                        print(a[i][0])
                    elif a != [i][0]:
                        print("a[i][0]가 아니다")
                    else:
                        print("???????")
            else:
                print("잘못된 입력입니다. 다시입력해주세요")

        elif meal == 7:
            print("해피밀을 선택하셨군요. 메뉴보여드릴게요.")
            print("해피밀메뉴에는", *happy_meal,"(이)가 있습니다.")
            mcmeal = int(input("위의 메뉴중 드시고 싶으신 해피밀을 선택하세요.: "))
            a = list(happy_meal.items())
            for i in range(len(a)):
                if a == a[i][0]:
                    print(a[i][0])
                elif a != a[i][0]:
                    print("a[i][0]가 아니다")
                else:
                    print("???????")
        else:
            print("잘못입력하셨습니다.")
        print("이용해주셔서 감사합니다.")
    elif eat == '매장':
        print("매장식사를 선택하셨군요")
    else:
        print("잘못된 입력입니다. 다시 입력하세요.")