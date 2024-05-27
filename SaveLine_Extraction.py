"""
SaveLine_Extraction.py

1. 입력값 검증 강화
2. 프리페이드 스테이트
3. 에러 메세지 정보

4. 서버 보안 강화
5. 비동기 처리 / 캐싱
6. 최소 권한 부여
7. 탐색용 DB 분리
8. 데이터 암호화
"""
import os
import pandas as pd
import platform

# 필요한 조건을 포함하는 라인 추출
relevant_lines = []
change_lines = []


# def


def process_file(file_path):
    global relevant_lines

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return []

    for i, line in enumerate(lines):
        # PHP 파일인 경우에만 처리
        if os.path.splitext(file_path)[1] == ".php":
            if '$' in line or any(func in line for func in ['mysqli_query', 'mysqli_fetch_array', 'mysqli_fetch_assoc',
                                                            'mysqli_fetch_row', 'mysqli_fetch_object',
                                                            'mysqli_real_escape_string', 'PDO::query', 'PDO::prepare',
                                                            'PDOStatement::execute', 'PDOStatement::fetch',
                                                            '<script>alert']):
                relevant_lines.append((i, line.strip()))
        else:
            break

    checking()
    minimize_error_message()
    #popup()
    save_csv()


# 입력값 검증 강화 및 Prepared statment 작성
def checking():
    global relevant_lines
    global change_lines

    check = 0
    for i, line in enumerate(relevant_lines):
        if "[a-zA-Z0-9]" not in line:
            continue
        else:
            check = 1
            break

    if check == 0:
        for (ii, iline) in enumerate(relevant_lines):
            lower = iline[1].lower()
            if "id" in lower:
                if "pw" in lower:
                    change_lines.insert(ii,
                                        (iline[0],
                                         "$statement = $connect->prepare('SELECT * FROM member WHERE ID = :id AND PW = :pw');\n"
                                         "$statement->bindValue(':id', $username, PDO::PARAM_STR);\n"
                                         "$statement->bindValue(':pw', $userpass, PDO::PARAM_STR);\n"
                                         "$statement->execute();\n"))
                else:
                    continue
            else:
                continue

        for (ti, tline) in enumerate(relevant_lines):
            lower = tline[1].lower()
            if "select" in lower:
                temp = change_lines.pop()
                change_lines.insert(ti, (tline[0], "$match = '/^[a-zA-z0-9]+$/';\n\n"
                                                   "if(!preg_match($match, $<variable>)){\n"
                                                   "echo '<script>alert('use only alphabet and numbers')</script>';\n"
                                                   "exit;}\n\n" + temp[1]))
            else:
                continue


# 에러메세지 최소화
def minimize_error_message():
    global relevant_lines
    global change_lines

    check = 1
    for i, line in enumerate(relevant_lines):
        lower = line[1].lower()
        if "alert" in lower:
            if "id" in lower:
                check = 0
                break
            if "name" in lower:
                check = 0
                break
            elif "pw" in lower:
                check = 0
                break
            elif "password" in lower:
                check = 0
                break
            else:
                continue
        else:
            continue

    if check == 0:
        for (ii, iline) in enumerate(relevant_lines):
            lower = iline[1].lower()
            if "alert" in lower:
                if "id" in lower:
                    if "pw" not in lower:
                        if "and" in lower:
                            continue
                        elif "or" in lower:
                            continue
                        else:
                            change_lines.insert(ii,
                                                (iline[0],
                                                 "echo '&lt;script>alert('Invalid ID or Password!')</script>';"))
                    else:
                        continue
                elif "name" in lower:
                    if "pw" not in lower:
                        if "and" in lower:
                            continue
                        elif "or" in lower:
                            continue
                        else:
                            change_lines.insert(ii,
                                                (iline[0],
                                                 "echo '&lt;script>alert('Invalid ID or Password!')</script>';"))
                    else:
                        continue
                elif "pw" in lower:
                    if "id" not in lower:
                        if "and" in lower:
                            continue
                        elif "or" in lower:
                            continue
                        else:
                            change_lines.insert(ii,
                                                (iline[0],
                                                 "echo '&lt;script>alert('Invalid ID or Password!')</script>';"))
                    else:
                        continue
                elif "password" in lower:
                    if "id" not in lower:
                        if "and" in lower:
                            continue
                        elif "or" in lower:
                            continue
                        else:
                            change_lines.insert(ii,
                                                (iline[0],
                                                 "echo '&lt;script>alert('Invalid ID or Password!')</script>';"))
                    else:
                        continue
                else:
                    continue


# 기타 출력
def popup():
    popup()


def save_csv():
    global change_lines

    df = pd.DataFrame(change_lines, columns=['Line Number', 'Content'])
    if platform.system() == 'Windows':
        df.to_csv("output.csv", index=False)
    else:
        df.to_csv("./output.csv", index=False)


"""

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
"""
