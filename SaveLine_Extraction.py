import asyncio
import re
import pymysql
import pandas as pd

# 입력값 강화: 정규 표현식을 사용하여 입력값을 검증하고, 쿼리문을 변수로 받을 때 ?를 사용하여 Prepared Statement의 일부로 사용
def validate_input(user_input):
    if not re.match(r'^[a-zA-Z0-9]+$', user_input):
        print("유효하지 않은 입력입니다.")
        return False
    return True

# 에러메세지 최소화: 일반적이고 유용한 메시지로 변경
def database_connect():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='password', database='test')
        return conn
    except Exception as e:
        print("데이터베이스 연결 오류가 발생했습니다.")
        return None

# 프리페어드: 입력값 강화의 일부로 정규 표현식을 사용하여 입력값을 검증하고, Prepared Statement를 사용하여 쿼리를 작성
def execute_query(conn, username):
    if validate_input(username):
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                print(result)
        except Exception as e:
            print("쿼리 실행 중 오류가 발생했습니다.")

# 비동기 처리: async 키워드를 사용하여 비동기 함수를 정의
async def delay_response():
    print("비동기 처리 시작")
    await asyncio.sleep(5)  # 5초간 대기
    print("비동기 처리 완료")

# 파일 입력 받은 후 라인별로 구분하여 필요한 조건이 있는 라인 추출
def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return []

    # 필요한 조건을 포함하는 라인 추출
    relevant_lines = []
    for i, line in enumerate(lines):
        # PHP 파일인 경우에만 처리
        if file_path.endswith('.php'):
            if '$' in line and any(func in line for func in ['mysqli_query', 'mysqli_fetch_array', 'mysqli_fetch_assoc', 'mysqli_fetch_row', 'mysqli_fetch_object', 'mysqli_real_escape_string', 'PDO::query', 'PDO::prepare', 'PDOStatement::execute', 'PDOStatement::fetch']):  
                relevant_lines.append((i, line.strip()))
        else:
            print("PHP 파일이 아닙니다.")
            break
    
    return relevant_lines

# 결과를 데이터프레임으로 저장하여 CSV 파일로 출력
def save_to_csv(data, output_file):
    df = pd.DataFrame(data, columns=['Line Number', 'Content'])
    df.to_csv(output_file, index=False)

# 메인 함수
def main(file_path):
    # 파일 입력 받기
    # file_path = input("파일 경로를 입력하세요: ")

    # 파일 처리 후 필요한 조건을 만족하는 라인 추출
    relevant_lines = process_file(file_path)

    if not relevant_lines:
        print("추출된 라인이 없습니다.")
        return

    # CSV 파일로 저장
    output_file = 'output.csv'
    save_to_csv(relevant_lines, output_file)
    print(f"추출된 데이터를 {output_file}로 저장했습니다.")

    # 사용자 입력 받기
    username = input("사용자 이름을 입력하세요: ")

    # 에러메세지 최소화: 데이터베이스 연결
    conn = database_connect()
    if conn:
        # 프리페어드: 쿼리 실행
        execute_query(conn, username)

        # 비동기처리: 비동기 함수 실행
        asyncio.run(delay_response())  # 비동기 함수 실행

if __name__ == "__main__":
    main()
