import pandas as pd
from re import sub

"""
## 사용 방법
1.  ECM TR interface 명세에 있는 outBlock 에서
    [BlOCK 명] ~ [비고] 컬럼에 해당하는 영역을 복사하여
    input_string 변수에 넣는다

2.  파이썬 파일 실행
    $ python interfaceGenerator_mrsapi_response.py
"""

# 입력 문자열 데이터
input_data = """
OutBlock1		[Array]	30		OutBlock1
OutBlock1	ELFN_ID	string	20	20	전자금융 ID
OutBlock1	ID_REG_DATE	string	8	8	ID 등록 일자
OutBlock1	ELFN_PWD_MSTK_TMNU	numstring	4	3	전자금융 비밀번호 오류 횟수
OutBlock1	CSNO	string	10	10	고객번호
OutBlock1	PROS_CSNU	numstring	8	7	처리건수
OutBlock1	CUST_FULL_NAME	string	100	100	고객 풀 명
OutBlock1	ATMT_ISNC_YN	string	1	1	자동발급여부
OutBlock2		[Array]	30		OutBlock2
OutBlock2	ELFN_ID	string	20	20	전자금융 ID
"""


# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])

# 입력 데이터 (예시로 주어진 문자열 데이터를 처리하기 위한 파싱 함수)
def parse_input_data(input_data):
    lines = input_data.strip().split("\n")
    parsed_data = {}
    current_block = ""
    for line in lines:
        # 블록 이름을 식별합니다.
        if "OutBlock" in line and ("[Single]" in line or "[Array]" in line):
            current_block = line.split("\t")[0]
            parsed_data[current_block] = []
        elif current_block and line:
            # 각 라인에서 필드 정보를 추출합니다.
            parts = line.split("\t")
            if len(parts) >= 6:  # 유효한 필드 라인인지 확인합니다.
                field_info = {
                    'block': parts[0],
                    'name': parts[1],
                    'type': parts[2],
                    'description': parts[5]
                }
                parsed_data[current_block].append(field_info)
    return parsed_data

# 데이터 변환
def transform_data(parsed_data):
    transformed_data = {}
    for block_name, fields in parsed_data.items():
        transformed_data[block_name] = []
        for field in fields:
            field_entry = {
                "Name": camel_case(field['name']),
                "Type": "String",  # 이 예시에서는 모든 타입을 String으로 가정
                "Null-able": "No",
                "Description": field['description'],
                "Length": ""  # 실제 구현에서는 필요에 따라 길이 값을 채울 수 있음
            }
            # 특정 필드는 Nullable이 "Yes"로 설정
            if block_name in ["OutBlock1", "OutBlock2", "OutBlock3", "OutBlock4", "OutBlock5"] and field['name'] in ["data", "outBlock", "nextKeyData"]:
                field_entry["Null-able"] = "Yes"

            transformed_data[block_name].append(field_entry)
    return transformed_data

# 엑셀 파일 작성
def write_excel(transformed_data, filename="output.xlsx"):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 고정된 데이터 세트를 한 번만 상단에 작성합니다.
        fixed_data = {
            "Name": ["status", "message", "data"],
            "Type": ["Integer", "String", "Json Object"],
            "Null-able": ["No", "No", "Yes"],
            "Description": ["결과 코드", "결과 메시지", "결과 데이터(status가 200일 경우 필수)"],
            "Length": ["", "", ""]
        }
        fixed_df = pd.DataFrame(fixed_data)
        fixed_df.to_excel(writer, index=False, sheet_name="Data")  # 여기서 헤더를 추가합니다.
        startrow = len(fixed_df.index) + 1  # 고정된 데이터와 다음 섹션 사이에 공백 행 추가

        for block_name, data in transformed_data.items():
            # 각 blockName에 해당하는 설명 데이터를 추가합니다.
            # 여기서는 열 이름 대신 값만 추가합니다 (header=False, index=False).
            block_intro = [
                [block_name, "JSON Array", "Yes", "결과 데이터(status가 200일 경우 필수)", ""]
            ]
            pd.DataFrame(block_intro).to_excel(writer, index=False, header=False, startrow=startrow, sheet_name="Data")
            startrow += 1  # block_intro 다음 행부터 데이터 추가를 시작합니다.

            # 실제 블록 데이터를 추가합니다 (헤더는 생략합니다, header=False).
            df = pd.DataFrame(data)
            df.to_excel(writer, index=False, header=False, startrow=startrow, sheet_name="Data")
            startrow += len(df.index) + 1  # 데이터 세트 사이에 공백 행 추가

# 실행
parsed_data = parse_input_data(input_data)
# print(parsed_data)

transformed_data = transform_data(parsed_data)
print(transformed_data)

write_excel(transformed_data)