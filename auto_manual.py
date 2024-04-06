import os


# SQL Injection 취약점 유형에 따른 대응 방안 매핑
vulnerability_responses = {
    "UNION query": "UNION based SQL Injection에 대비하여 입력값을 엄격하게 필터링하고, UNION 쿼리 시 결과 열의 수를 일치시키세요.\n"
                   "Prepared Statement를 사용하거나 ORM를 적용하여 쿼리를 작성하세요.",

    "error-based": "에러 메시지 노출을 최소화하여 공격자에게 민감한 정보를 노출하지 않도록 주의하세요.\n"
                   "정적 쿼리 또는 ORM을 사용하여 쿼리를 작성하세요.\n"
                   "에러 기반 SQL Injection에 대비하여 입력값을 엄격하게 검증하고, 예외 처리를 강화하세요.",

    "time-based blind": "실행 시간이 긴 쿼리에 대한 응답 시간을 모니터링 외에도 CPU 및 메모리 사용량 모니터링을 통해 시간 지연 공격을 탐지하여 대응하세요.\n"
                        "대량의 데이터 처리를 요구하는 작업에서는 비동기 처리 및 캐싱을 활용하여 응답 시간을 최적화하세요.",

    "boolean-based blind": "에러 메시지 노출을 최소화하여 공격자에게 정보를 노출하지 않도록 보호하세요.\n"
                           "보안 관련 로그를 잘 기록하여 시도된 공격을 모니터링하고 대응하세요.",

    "Out-of-Band SQL Injection": "외부 연결을 필요로 하는 기능을 최소화하여 외부 네트워크에 대한 공격 범위를 줄이세요.\n"
                                 "웹 응용 프로그램과 데이터베이스 사이의 통신을 암호화하여 중간자 공격으로부터 보호하세요.",

    "stored procedure": "프로시저를 호출할 때 필요한 최소한의 권한을 부여하여 보안을 강화하세요.\n"
                        "입력값의 유효성을 검사하고, 실행 결과를 신뢰할 수 있는지 확인하세요.\n"
                        "프로시저 내에서 사용자 입력값을 동적으로 생성하거나 실행하지 않도록 하여 보안을 강화하세요."

    
    #추가할 것 있음 여기다 추가하세요~~~
}



# 명령어 입력 자동화
def call_SQLmap(url):
    command = f"python3 ./sqlmap/sqlmap.py -u {url} --batch > sqlmap_info.txt"
    os.system(command)

