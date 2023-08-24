import fitz  # PyMuPDF의 기능을 사용하기 위한 모듈

# PDF 파일 경로
pdf_path = '숙박_7월영수증.pdf'  # 본인의 PDF 파일 경로로 바꿔주세요

# PDF 파일 열기
pdf_document = fitz.open(pdf_path)

# 텍스트를 저장할 변수 초기화
pdf_text = ''

# 각 페이지의 텍스트 추출

for page_num in range(pdf_document.page_count):
    page = pdf_document[page_num]
    pdf_text += page.get_text()

# PDF 파일 닫기
pdf_document.close()

# 추출된 텍스트 출력
print(pdf_text)
