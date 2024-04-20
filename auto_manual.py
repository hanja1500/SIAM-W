import os


# SQL Injection 취약점 유형에 따른 대응 방안 매핑
vulnerability_responses = {
    '': "Select SQLi",

    'vulnerabilities': "Select SQLi",

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

}


response_to_countermeasure = {

    '': "Select SQLi",

    'vulnerabilities': "Select SQLi",

    "UNION query": ["checking_input", "prepared_statement"],

    "error-based": ["checking_input", "error_message"],

    "time-based blind": ["server_security", "async"],

    "boolean-based blind": ["checking_input", "error_message", "server_security"],

    "Out-of-Band SQL Injection": ["prepared_statement", "DAL", "encrypting"],

    "stored procedure": ["checking_input", "least_previllege"]

}


vulnerability_countermeasures = {

    '': "Select SQLi",

    'vulnerabilities': "Select SQLi",

    "prepared_statement": 'String sql = "SELECT * FROM users WHERE name = ?";\n\n',

    "checking_input": "// 블랙 리스트 방식: 거부할 문자 및 키워드 정의\n\n"
                      "$blacklist = ['select', 'insert', 'update', 'shutdown', 'delete', 'drop',"
                      "'--', "'", '"', '=', ';', 'union', 'group by', 'if', 'column', 'end', 'instance'];\n\n"
                      "// 화이트 리스트 방식: 허용할 문자 패턴 정의 (예: 알파벳, 숫자, 공백)"
                      "$whitelist_pattern = '/^[a-zA-Z0-9\\s]+$/';\n\n"
                      "function validate_input($input_value) {\n"
                      "    global $blacklist, $whitelist_pattern;\n\n"
                      "    // 블랙 리스트 방식: 거부할 문자나 키워드가 입력값에 포함되어 있는지 확인\n"
                      "    foreach ($blacklist as $item) {\n"
                      "        if (stripos($input_value, $item) !== false) {\n"
                      "            return false;\n"
                      "        }\n"
                      "    }\n\n"
                      "    // 화이트 리스트 방식: 입력값이 허용된 패턴에 일치하는지 확인\n"
                      "    if (!preg_match($whitelist_pattern, $input_value)) {\n"
                      "        return false;\n"
                      "    }\n\n"
                      "    // 모든 검증 통과\n"
                      "    return true;\n"
                      "}\n\n"
                      "foreach ($input_values as $value) {\n"
                      "    if (validate_input($value)) {\n"
                      '        echo "Input "$value" is valid\\n";\n'
                      '    } else {\n'
                      '        echo "Input "$value" is invalid\\n";\n'
                      "    }\n"
                      "}\n\n",


    "error_message": "import sqlite3\n\n"
                     "def execute_sql_query(sql_query):\n"
                     "    try:\n"
                     "        # 데이터베이스 연결\n"
                     "        connection = sqlite3.connect('example.db')\n"
                     "        cursor = connection.cursor()\n\n"
                     "        # SQL 쿼리 실행\n"
                     "        cursor.execute(sql_query)\n\n"
                     "        # 결과 반환\n"
                     "        result = cursor.fetchall()\n\n"
                     "        # 연결 종료\n"
                     "        connection.close()\n\n"
                     "        return result\n\n"
                     "    except sqlite3.Error as e:\n"
                     "        # SQL 에러가 발생했을 때 최소화된 메시지 출력\n"
                     "        print('SQL 에러가 발생했습니다. 문의하신 작업을 수행할 수 없습니다.')\n\n"
                     "# 사용자로부터 입력 받은 SQL 쿼리\n"
                     "user_sql_query = input('실행할 SQL 쿼리를 입력하세요: ')\n\n"
                     "# SQL 쿼리 실행\n"
                     "execute_sql_query(user_sql_query)\n\n",


    "server_security": "import pyodbc\n\n"
                       "def connect_to_sql_server():\n"
                       "    try:\n"
                       "        # SQL Server 연결 설정\n"
                       "        conn = pyodbc.connect(\n"
                       "            'DRIVER={SQL Server};'\n"
                       "            'SERVER=<your_server_name>;'\n"
                       "            'DATABASE=<your_database_name>;'\n"
                       "            'UID=<your_username>;'\n"
                       "            'PWD=<your_password>;'\n"
                       "            'Encrypt=yes;'  # 연결 암호화 사용\n"
                       "            'TrustServerCertificate=no;'  # 서버 인증서 검증\n"
                       "            'Connection Timeout=30;'  # 연결 제한 시간 설정\n"
                       "        )\n\n"
                       "        # 연결 성공 메시지 출력\n"
                       "        print('SQL Server에 성공적으로 연결되었습니다.')\n\n"
                       "        # 연결 종료\n"
                       "        conn.close()\n\n"
                       "    except pyodbc.Error as e:\n"
                       "        # 에러 처리\n"
                       "        print('SQL Server 연결에 실패했습니다:', e)\n\n"
                       "# SQL Server에 연결\n"
                       "connect_to_sql_server()\n\n",


    "async": "console.log('start');\n"
             "setTimeout(() => {\n"
             "    console.log('continue...');\n"
             "}, 3000);\n"
             "console.log('print');\n\n",

    "DAL": "split the database to prevent from hacker that wants to see actual data.\n"
           "you can split the database into two, one for sorting and one for searching.\n\n",

    "encrypting": "Use OpenSSL to encrypt : https://www.openssl.org/\n\n",

    "least_privilege": "import pyodbc\n\n"
                       "def connect_to_sql_server():\n"
                       "    try:\n"
                       "        # SQL Server 연결 설정\n"
                       "        conn = pyodbc.connect(\n"
                       "            'DRIVER={SQL Server};'\n"
                       "            'SERVER=<your_server_name>;'\n"
                       "            'DATABASE=<your_database_name>;'\n"
                       "            'UID=restricted_user;'  # 최소권한\n"
                       "            'PWD=restricted_password>;'  # 최소권한\n"
                       "        )\n\n"
                       "        # 연결 성공 메시지 출력\n"
                       "        print('SQL Server에 성공적으로 연결되었습니다.')\n\n"
                       "        # 연결 종료\n"
                       "        conn.close()\n\n"
                       "    except pyodbc.Error as e:\n"
                       "        # 에러 처리\n"
                       "        print('SQL Server 연결에 실패했습니다:', e)\n\n"
                       "# SQL Server에 연결\n"
                       "connect_to_sql_server()\n\n",
}


# 명령어 입력 자동화
def call_SQLmap(url):
    command = f"python3 ./sqlmap/sqlmap.py -u {url} --batch > sqlmap_info.txt"
    os.system(command)
