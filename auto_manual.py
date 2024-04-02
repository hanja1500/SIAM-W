import os
import sys
import pandas as pd
import fileIO
import crawling


# SQL Injection 취약점 유형에 따른 대응 방안 매핑
vulnerability_responses = {
    "boolean-based blind": "사용자 입력값을 필터링하고, Prepared Statement 또는 ORM을 사용하여 쿼리를 작성하세요.",
    "error-based": "에러 메시지가 노출되지 않도록 설정하고, 에러 기반 SQL Injection에 대비하는 방어책을 구현하세요.",
    "time-based blind": "실행 시간이 긴 쿼리에 대한 응답 시간 모니터링 및 사용자 입력값을 검증하여 대응하세요.",
    "UNION query": "UNION based SQL Injection에 대비하여 입력값을 검증하고, UNION 쿼리 시 결과 열의 수를 맞추세요."
# 추가적인 취약점 유형에 따른 대응 방안을 여기에 추가 가능
}

info_path = './sqlmap_info.txt'

# 명령어 입력 자동화
def call_SQLmap(url):
    command = f"python3 sqlmap.py -u {url} --batch > sqlmap_info.txt"
    os.system(command)
    
# crawling data 삭제
def clear_crawl():
    os.system("del sqlmap_info.txt")
    





