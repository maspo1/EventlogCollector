import fitz  # PyMuPDF의 기능을 사용하기 위한 모듈
import re

# PDF 파일 경로
pdf_path = 'pdf.pdf'  # 본인의 PDF 파일 경로로 바꿔주세요

# PDF 파일 열기
pdf_document = fitz.open(pdf_path)

# 텍스트를 저장할 변수 초기화
pdf_text = ''

# 각 페이지의 텍스트 추출
a = []
pattern = r'(?<=\n)(\d+)(?=\n)'
pattern2 = r'dd\n(\w+)\n'
for page_num in range(pdf_document.page_count):
    page = pdf_document[page_num]
    pdf_text += page.get_text()
    a.append(pdf_text)
    b = re.findall(pattern, pdf_text)
    c = re.findall(pattern2,pdf_text)
    print(b)
    print(c)
# PDF 파일 닫기
pdf_document.close()
data=[]

#b = 숫자
#c = 기기명
new_list = []
for i in range(len(c)):
    b_elements = b[i * 2:i * 2 + 2]
    combined = [c[i]]
    # b의 원소를 추가, 중복 확인
    for elem in b_elements:
        if elem not in combined:
            combined.append(elem)
    new_list.append(combined)
print(new_list)