import os
import sys
import pandas as pd
import fileIO
import info_crawling

# URL 입력 확인


while True:
    try:
        x = sys.argv[1]
        break
    except IndexError:
        print("Usage : python auto_manual.py [victim URL]")
        sys.exit(-1)


# 취약점 매뉴얼 출력 함

def print_vulnerability_response(info_path):
    

# SQL Injection 취약점 유형에 따른 대응 방안 매핑
    

    vulnerability_responses = {
        "boolean-based blind": "사용자 입력값을 필터링하고, Prepared Statement 또는 ORM을 사용하여 쿼리를 작성하세요.",
        "error-based": "에러 메시지가 노출되지 않도록 설정하고, 에러 기반 SQL Injection에 대비하는 방어책을 구현하세요.",
        "time-based blind": "실행 시간이 긴 쿼리에 대한 응답 시간 모니터링 및 사용자 입력값을 검증하여 대응하세요.",
        "UNION query": "UNION based SQL Injection에 대비하여 입력값을 검증하고, UNION 쿼리 시 결과 열의 수를 맞추세요."

# 추가적인 취약점 유형에 따른 대응 방안을 여기에 추가 가능
        
    }

# SQLmap 정보 파일 읽기
    
    with open(info_path, 'r') as file:
        info_lines = file.readlines()

# 취약점 유형 추출
    
    vulnerabilities = []
    for line in info_lines:
        if line.startswith("    Type:"):
            vulnerabilities.append(line.split(":")[1].strip())

# 취약점 유형에 따른 대응 방안 출력
    
    for vulnerability in vulnerabilities:
        if vulnerability in vulnerability_responses:
            print()
            print(f"취약점 유형 : '{vulnerability}'")
            print(f"대표적 공격 페이로드 : %s" % df["Payload"][vulnerability])
            print(vulnerability_responses[vulnerability])





# 명령어 입력 자동화


command = "python3 sqlmap.py -u "+sys.argv[1]+" --batch > sqlmap_info.txt"

os.system(command)


# 예시 파일 경로


info_path = './sqlmap_info.txt'

data_path = './crawling.csv'


# raw data 정렬


info = fileIO.read_txt(info_path)
summary = info_crawling.SQLi_type(info)
result = info_crawling.parsing_type(summary)

fileIO.clearcsv(data_path)
fileIO.writecsv_dict(result, data_path, ['Type', 'Title', 'Payload'])



# crawling한 정보 입력


df = pd.read_csv(data_path)

df = df.set_index('Type')

pd.set_option('display.max_columns', None)


    
# 함수 호출


print_vulnerability_response(info_path)



# crawling data 삭제


os.system("del sqlmap_info.txt crawling.csv")



