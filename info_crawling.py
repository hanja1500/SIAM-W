import fileIO

'''


* 작성: 민예원

* 읽어들일 sqlmap 정보 목록의 파일 이름은
* sqlmap_info.txt 로 해놓을 것

* 그 목록과 같은 위치에 이 파일이 있어야 하며
* fileIO 모듈도 같은 directory에 저장해놓을 것

* 생성되는 데이터셋은 파일과 같은 위치에 crawling.csv로 저장됨
* 아래에 예시 스크립트 작성해놨으니 이용하시길!

'''

def SQLi_type(info):
    data = []
    read = False

    for line in info:
        line = line.strip() # 줄 끝의 줄바꿈 문자 제거
        if read:
            data.append(line)
        if line == '---':
            if read:
                data.pop()  # 맨 마지막 --- 제거
            read = not read
    return data

def parsing_type(summary):
    result = {}
    for line in summary[1:]:
        if line[0:4] == 'Type':
            dict = {}
        if line != '':
            word = []
            distinction = 0
            for char in line:
                word.append(char)
                if not ''.join(word).isalpha():
                    break
                distinction = distinction + 1
            dict[line[0:distinction]] = line[distinction+2:]
        result[dict['Type']] = dict
    return result

'''

### 예시 ###

info_path = './sqlmap_info.txt'
data_path = './crawling.csv'
info = fileIO.read_txt(info_path)

summary = SQLi_type(info)
print(summary)
result = parsing_type(summary)
print(result)
fileIO.clearcsv(data_path)
fileIO.writecsv_dict(result, data_path, ['Type', 'Title', 'Payload'])

### 아래는 csv 읽어오는 예시 ###

print('\n')
df = pd.read_csv(data_path)
df = df.set_index('Type')
pd.set_option('display.max_columns', None)
print(df)

'''
