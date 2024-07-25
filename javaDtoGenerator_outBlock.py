"""
## 사용 방법
1.  ECM TR interface 명세에 있는 outBlock 에 대해
    [BlOCK 명] ~ [이름] 컬럼에 해당하는 영역을 복사하여
    input_string 변수에 넣는다

2.  파이썬 파일 실행
    $ python javaDtoGenerator_outBlock.py

3.  생성될 파일 이름을 입력
"""

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def generate_java_dto(prefix):
    input_text = """
OutBlock2	acno	string	8	8	계좌번호
OutBlock2	asno	string	2	2	계좌일련번호
OutBlock2	ui_acnt_prnm	string	60	60	UI계좌상품명
OutBlock2	kyc_prod_grad_code	string	2	2	KYC상품등급코드
OutBlock2	unfit_yn	string	1	1	부적합여부
OutBlock2	anxt_aprt_yn	string	1	1	부적정여부
    """

    lines = input_text.strip().split("\n")
    block_number = ""
    fields = []

    for line in lines:
        parts = line.split()
        if len(parts) > 1 and parts[0].startswith("OutBlock"):
            if not block_number:
                block_number = parts[0].replace("OutBlock", "")
            field_name = to_camel_case(parts[1].lower())  # Convert snake_case to camelCase
            description = " ".join(parts[5:])
            fields.append((field_name, description))
    a = '{'
    class_name = f"{prefix}OutBlock{block_number}"
    annotations = """@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)"""
    java_code = f"import com.fasterxml.jackson.annotation.JsonInclude;\nimport lombok.AllArgsConstructor;\nimport lombok.Data;\nimport lombok.NoArgsConstructor;\n\n{annotations}\npublic class {class_name} {a}\n"

    for field_name, description in fields:
        # Determine the field type based on the input
        field_type = "String"
        java_code += f"    private {field_type} {field_name}; // {description}\n"

    java_code += "}"

    return java_code

prefix = input()  # 여기에 클래스 이름 앞에 붙일 접두사를 입력하세요.

res = generate_java_dto(prefix)

print(res)