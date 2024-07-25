import pandas as pd
from io import StringIO
from re import sub

"""
## 사용 방법
1.  ECM TR interface 명세에 있는 inBlock 에서
    [BlOCK 명] ~ [비고] 컬럼에 해당하는 영역을 복사하여
    input_string 변수에 넣는다

2.  파이썬 파일 실행
    $ python interfaceGenerator_mrsapi_request.py
"""

# 입력 문자열 데이터
input_data_str = """
InBlock1		[Single]			InBlock1
InBlock1	PROS_CLS_CODE	string	1	1	처리 구분 코드
InBlock1	RCNO	string	13	13	실명확인번호
InBlock1	ACNO	string	8	8	계좌번호
InBlock1	ACNT_PWD	string	68	68	계좌 비밀번호
InBlock1	BRNC_PWD	string	68	68	지점 비밀번호
InBlock1	RCNO_PIP	string	68	68	실명확인번호PIP
"""

# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])

# 문자열 데이터를 DataFrame으로 파싱하는 함수
def parse_input_data(input_data_str):
    # 데이터의 각 컬럼에 대한 이름 정의
    columns = ['Block', 'Field Name', 'Data Type', 'Length1', 'Length2', 'Description', 'Remarks']
    
    # StringIO를 사용하여 문자열 데이터를 파일처럼 취급하고, pandas의 read_csv 함수로 읽어들임
    # 수정된 부분: skiprows 제거, delimiter로 공백을 사용
    df = pd.read_csv(StringIO(input_data_str), delimiter='\t', names=columns, engine='python', skipinitialspace=True)

    # 'Remarks' 컬럼에서 NaN 값을 빈 문자열로 대체
    df.fillna('', inplace=True)
    
    return df

# 입력 문자열 데이터를 DataFrame으로 변환
input_df = parse_input_data(input_data_str)

def create_output_excel(input_df, file_path='output_excel.xlsx'):
    # 고정된 행 데이터
    fixed_rows = [
        ['Method', 'POST'],
        ['URL', '/individualProInvestExp'],
        ['Character Set', 'UTF-8'],
        ['Headers', 'Name', 'Type', 'Description'],
        ['', 'Content-type', 'String', 'application/json'],
        ['', 'Accept', 'String', 'application/json'],
        ['Query Parameter', 'Name', 'Type', 'Null-able', 'Description', '비고']
    ]
    
    # 입력 데이터를 기반으로 Query Parameter 행 추가
    for index, row in input_df.iterrows():
        if row['Data Type'] == '[Single]' or row['Data Type'] == '[Array]':
            continue
            
        field_name = camel_case(row['Field Name'].lower())  # 필드 이름 소문자로 변환
        nullable = 'N' if row['Remarks'] == 'X' else 'Y'  # Nullable 값 조정
        fixed_rows.append(['', field_name, row['Data Type'], nullable, row['Description'], row['Remarks']])

    # 추가할 행들: 사용자 ID, 지점 코드
    extra_rows = [
        ['', 'userId', 'String', 'N', '사번 (모집인 로그인 id)', ''],
        ['', 'brCode', 'String', 'N', '지점 코드', '']
    ]
    
    # DataFrame으로 변환
    output_df = pd.DataFrame(fixed_rows + extra_rows)
    
    # 엑셀 파일로 저장
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        output_df.to_excel(writer, index=False, header=False)

    return file_path

# 엑셀 파일 생성 및 파일 경로 반환
output_excel_path = create_output_excel(input_df)
output_excel_path