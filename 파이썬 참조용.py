import random
import datetime as dt
class Bank:
    count = 0
    print("---고객 리스트----")
    print("이름\t생년월일\t비밀번호\t은행\t계좌번호\t잔액")

    def __str__(self):
        return f"{self.Name} {self.Bank_name} {self.Bank_name} {self.Pw} {self.Bank_num} {self.Money}"
    def __init__(self, Name, Bank_name, Birthday, Pw, Money):
        self.Name = Name
        self.Bank_name = Bank_name
        self.Birthday = Birthday
        self.Pw = Pw
        self.Money = Money
        self.Bank_num = self.Number()

    def Number(self):
        bank_num = ""
        for i in range(10):
            bank_num += str(random.randrange(10))
        return int(bank_num)

    def SendMoney(self):
        print("송금")
        password = int(input("비밀번호 입력 : "))
        if password == num1.Pw:
            account = int(input("송금할 계좌번호 입력 : "))
            for i in Numbers:
                print(i.Bank_num)
                print(type(i.Bank_num))
                if account == i.Bank_num:
                    remit = int(input("송금할 금액 입력: "))
                    if remit > num1.Money:
                        print("잔액 부족")
                    else:
                        num1.Money -= remit
                        i.Money += remit
                        print("송금완료")
                        print(f"{num1.Money}, {i.Money}")
                else:
                    print("일치하는 계좌번호가 없습니다..")
        else:
            print("비밀번호가 일치하지 않습니다. 다시 확인해주세요.")


num1 = Bank("유재석", "농협", 920316, 7545, 2000000)
num2 = Bank("박명수", "농협", 900228, 7512, 500000)
Numbers = [num1, num2]
Id = num1

while True:
    for i , num in enumerate(Numbers):
        print(i+1, str(num))
    choice = input("\n1. 송금 2. 출금 3. 입금 4. 종료\n")
    if choice == "1":
        Id.SendMoney()