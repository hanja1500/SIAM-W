import fileIO

'''
읽어들일 sqlmap 정보 목록의 파일 이름은
sqlmap_info.txt
로 해놓을 것
그 목록과 같은 위치에 이 파일이 있어야 하며 fileIO 모듈도 같은 directory에 저장해놓을 것
'''


# sqlmap_info.txt를 ---를 기준으로 크롤링
def SQLi_type(info):
    data = []
    read = False

    for line in info:
        line = line.strip()     # 줄 끝의 줄바꿈 문자 제거
        if read:
            data.append(line)
        if line == '---':
            if read:
                data.pop()      # 맨 마지막 --- 제거
            read = not read
    return data


# 크롤링한 데이터를 key-value로 parsing
def parsing_type(data):
    result = {}
    for line in data[1:]:
        if line[0:4] == 'Type':
            dict = {}
        if line == '':
            continue

        word = []
        distinction = 0
        for char in line:
            word.append(char)
            if not ''.join(word).isalpha():
                break
            distinction = distinction + 1
        dict[line[0:distinction]] = line[distinction+2:]

        if len(dict) >= 3:
            result[dict['Type']] = dict
    return result


# 크롤링 실행용 함수
def summary():
    """

    Returns: key 값이 ['Type', 'Title', 'Payload']인 dictionary 배열

    """
    try:
        data = SQLi_type(fileIO.read_txt('./sqlmap_info.txt'))
    except FileNotFoundError:
        base = ''
        return base

    result = parsing_type(data)

    return result


# crawling data 삭제
def clear_crawl():
    fileIO.clear_file('./sqlmap_info.txt')


''' csv 파일로 저장하고 싶을 경우의 코드
data_path = './crawling.csv'
fileIO.clearcsv(data_path)
fileIO.writecsv_dict(result, data_path, ['Type', 'Title', 'Payload'])
'''
