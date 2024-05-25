'''
1. 입력값 검증 강화
2. 프리페이드 스테이트
3. 에러 메세지 정보

4. 서버 보안 강화
5. 비동기 처리 / 캐싱
6. 최소 권한 부여
7. 탐색용 DB 분리
8. 데이터 암호화
'''
import os
import pandas as pd

# 필요한 조건을 포함하는 라인 추출
relevant_lines = []

# def

def process_file(file_path):
    global relevant_lines
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("not found")
        return []

    for i, line in enumerate(lines):
        # PHP 파일인 경우에만 처리
        if os.path.splitext(file_path)[1] == ".php":
            if '$' in line or any(func in line for func in ['mysqli_query', 'mysqli_fetch_array', 'mysqli_fetch_assoc',
                                                            'mysqli_fetch_row', 'mysqli_fetch_object',
                                                            'mysqli_real_escape_string', 'PDO::query',
                                                            'PDO::prepare', 'PDOStatement::execute',
                                                            'PDOStatement::fetch']):
                relevant_lines.append((i, line.strip()))
        else:
            print("not php")
            break

def checking(file_path):
    global relevant_lines

    check = setting = 0
    for i, line in enumerate(relevant_lines):
        if "[a-zA-Z0-9]" not in line:
            continue
        else:
            check = 1
            break

    if check == 0:
        for (ii, iline) in enumerate(relevant_lines):
            print(iline)
            if "SELECT" in iline[1]:
                relevant_lines.insert(ii, (iline[0], "$match = '/^[a-zA-z0-9]+$/'"))
                relevant_lines.insert(ii+1, (iline[0]+1, "if(!preg_match($match, $<variable>)){"))
                relevant_lines.insert(ii+2, (iline[0]+2, 'echo "<script>alert("use only alphabet and numbers")</script>"; exit;}'))
                break
            else:
                continue
        for (ii, iline) in enumerate(relevant_lines):
            print(iline)
            if "use only alphabet and numbers" in iline[1]:
                setting = 1
                continue

            if setting == 1:
                relevant_lines[ii] = (iline[0]+3, iline[1])
            else:
                continue

    print(relevant_lines)
    df = pd.DataFrame(relevant_lines, columns=['Line Number', 'Content'])
    df.to_csv("./output.csv", index=False)

process_file("./test.php")
checking("./test.php")