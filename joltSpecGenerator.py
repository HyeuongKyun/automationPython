import json
import re


"""
## 사용 방법
1.  ECM TR interface 명세에 있는 outBlock 에서
    [BlOCK 명] ~ [이름] 컬럼에 해당하는 영역을
    input_string 변수에 넣는다

2.  파이썬 파일 실행
    $ python joltSpecGenerator.py
"""

def snake_to_camel(word):
    """Snake case를 Camel case로 변환"""
    first, *rest = word.lower().split('_')
    return ''.join([first.lower()] + [word.capitalize() for word in rest])

def generate_jolt_spec(input_string):
    lines = input_string.strip().split('\n')
    spec = [{
        "operation": "shift",
        "spec": {
            "status": "&0",
            "message": "&0",
            "data": {}
        }
    }]
    data_spec = spec[0]["spec"]["data"]

    for line in lines:
        if '[Single]' in line or '[Array]' in line:
            block_name = line.split()[0]
            if block_name.startswith("Next"):
                data_spec["next_key_data"] = {}
            else:
                data_spec[block_name] = {"*": {}}
            
        else:
            parts = line.split('\t')
            if len(parts) > 1:
                original_field_name = parts[1].lower()
                camel_case_field_name = snake_to_camel(original_field_name)
                if block_name.startswith("Next"):
                    path = f"data.nextKeyData.{camel_case_field_name}"
                    data_spec["next_key_data"][original_field_name] = path
                else:
                    path = f"data.{block_name}[&1].{camel_case_field_name}"
                    data_spec[block_name]["*"][original_field_name] = path
    
    spec[0]["spec"]["data"]["message"] = {
        "msg_code": "data.message.msgCode",
        "sub_msg": "data.message.subMsg",
        "msg_prepared": "data.message.msgPrepared",
        "err_msg_show_method": "data.message.errMsgShowMethod",
        "err_msg_attr_set": "data.message.errMsgAttrSet",
        "is_app_err": "data.message.isAppErr",
        "main_msg": "data.message.mainMsg"
    }

    return spec

input_string = """
OutBlock1		[Single]	1		OutBlock1
OutBlock1	kyc_invt_incl_grad_code	string	2	2	KYC투자성향등급코드
OutBlock1	ques_scor	numstring	8.3	6.3	설문점수
OutBlock1	kyc_vald_prd_mtrt_date	string	8	8	KYC유효기간만기일자
OutBlock1	kyc_invt_rcmd_cls_code	string	1	1	KYC투자권유구분코드
OutBlock1	kyc_spcl_invr_yn	string	1	1	KYC전문투자자여부
OutBlock1	kyc_dvpd_epmd_code	string	2	2	KYC파생상품유의코드
OutBlock1	entt_ivic_grcd	string	2	2	일임투자성향등급코드
OutBlock1	trust_ivic_grcd	string	2	2	신탁투자성향등급코드
OutBlock1	trust_prod_grcd	string	2	2	신탁상품등급코드
OutBlock1	wrap_prod_grad	string	2	2	WRAP상품등급
OutBlock1	trust_acit_yn	string	1	1	신탁계정여부
OutBlock1	wa_hldn_yn	string	1	1	랩어카운트보유여부
OutBlock1	entt_kyc_mtrt_date	string	8	8	일임KYC만기일자
OutBlock1	trust_kyc_mtrt_date	string	8	8	신탁KYC만기일자
OutBlock1	unfit_ntic_csnu	numstring	5	4	부적합고지건수
OutBlock2		[Array]	100		OutBlock2
OutBlock2	acno	string	8	8	계좌번호
OutBlock2	asno	string	2	2	계좌일련번호
OutBlock2	ui_acnt_prnm	string	60	60	UI계좌상품명
OutBlock2	kyc_prod_grad_code	string	2	2	KYC상품등급코드
OutBlock2	unfit_yn	string	1	1	부적합여부
OutBlock2	anxt_aprt_yn	string	1	1	부적정여부
"""

jolt_spec = generate_jolt_spec(input_string)

# Jolt Spec을 JSON 파일로 저장
with open('joltSpec.json', 'w') as json_file:
    json.dump(jolt_spec, json_file, indent=4)

print(" 'joltSpec.json' 파일 생성 완료")
