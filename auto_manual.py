import os
import sys
import pandas as pd
import fileIO
import crawling


# SQL Injection 취약점 유형에 따른 대응 방안 매핑
vulnerability_responses = {
    "boolean-based blind": "에러 메시지 노출을 최소화하여 공격자에게 정보를 노출하지 않도록 보호하세요. 보안 관련 로그를 잘 기록하여 시도된 공격을 모니터링하고 대응하세요.",

    "error-based": "에러 메시지 노출을 최소화하여 공격자에게 민감한 정보를 노출하지 않도록 주의하세요. 정적 쿼리 또는 ORM을 사용하여 쿼리를 작성하세요. 에러 기반 SQL Injection에 대비하여 입력값을 엄격하게 검증하고, 예외 처리를 강화하세요.",

    "time-based blind": "실행 시간이 긴 쿼리에 대한 응답 시간을 모니터링 외에도 CPU 및 메모리 사용량 모니터링을 통해 시간 지연 공격을 탐지하여 대응하세요. 대량의 데이터 처리를 요구하는 작업에서는 비동기 처리 및 캐싱을 활용하여 응답 시간을 최적화하세요.",

    "UNION query": "UNION based SQL Injection에 대비하여 입력값을 엄격하게 필터링하고, UNION 쿼리 시 결과 열의 수를 일치시키세요. Prepared Statement를 사용하거나 ORM를 적용하여 쿼리를 작성하세요.",

    "stacked queries": "쿼리 작성 시 적절한 매개변수화를 수행하여 공격을 방어하세요. DBMS 설정을 변경하고, 입력값을 엄격하게 검증하여 보호하세요.",

    "boolean-based blind (time-based)": "시간에 따라 조건문의 참/거짓 여부를 파악하여 정보를 유출하는 공격에 대비하여 실행 시간 모니터링 및 입력값 검증을 강화하세요. ORM 또는 Prepared Statement를 사용하여 쿼리를 작성하세요.",

    "union-based blind": "UNION 쿼리를 이용하여 정보를 추출하는 공격에 대비하여 UNION 쿼리 시 결과 열의 수를 일치시키세요. UNION 쿼리 대신 조인을 사용하여 데이터를 결합하여 공격 범위를 제한하는 것이 좋습니다. 데이터베이스 사용자의 권한을 최소화하여 UNION 공격으로부터 보호하세요.",

    "error-based (boolean-based blind)": "에러 메시지를 이용하여 정보를 유출하는 공격에 대비하여 에러 메시지 노출을 최소화하고, 입력값을 엄격하게 검증하세요. ORM 또는 Prepared Statement를 사용하여 쿼리를 작성하세요.",

    "inline query": "동적 쿼리를 생성하는 대신 ORM 또는 쿼리 빌더를 사용하여 정적 쿼리를 사용하여 쿼리의 안정성을 보장하세요. SQL Injection 대응을 위한 웹 애플리케이션 방화벽(WAF)을 구성하여 실시간으로 공격을 탐지 및 차단하세요.",

    "stored procedure": "프로시저를 호출할 때 필요한 최소한의 권한을 부여하여 보안을 강화하세요. 입력값의 유효성을 검사하고, 실행 결과를 신뢰할 수 있는지 확인하세요. 프로시저 내에서 사용자 입력값을 동적으로 생성하거나 실행하지 않도록 하여 보안을 강화하세요.",

    "Out-of-Band SQL Injection": "외부 연결을 필요로 하는 기능을 최소화하여 외부 네트워크에 대한 공격 범위를 줄이세요. 웹 응용 프로그램과 데이터베이스 사이의 통신을 암호화하여 중간자 공격으로부터 보호하세요."
}

# 각 값의 끝에 따옴표 추가 및 쉼표로 각 요소 구분, 문구 검증 완료


# 명령어 입력 자동화
def call_SQLmap(url):
    command = f"python3 ./sqlmap/sqlmap.py -u {url} --batch > sqlmap_info.txt"
    os.system(command)

