import os
import csv
import pandas as pd
import platform


def pathByos(path):
    if platform.system() == 'Windows':
        return path.replace('/', '\\')
    return path

def read_txt(path):
    '''

    Args:
        path: 읽어들일 txt 경로

    Returns: 읽어들인 txt의 line으로 구성된 list

    '''
    path = pathByos(path)
    
    lines = []
    if os.path.exists(path):
        with open(path, 'r') as file:
            lines = file.readlines()
            
    return lines

def clear_file(path):
    path = pathByos(path)
    
    if platform.system() == 'Windows':
        os.system(f"del {path}")
    else:
        os.system(f"rm {path}")
        
def writecsv(list, path):
    '''

    Args:
        list: csv로 저장할 list
        path: csv 저장 위치

    Returns:

    '''
    if not os.path.exists(path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(list)
    else:
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list)

def writecsv_dict(dict, path, header = []):
    '''

    Args:
        dict: {이름:{저장할 dictionary}} 이중으로 된 dictionary를 저장
        path: csv 저장 위치
        header: header 지정 시 header 목록(정확하게 기재해야 함)

    Returns:

    '''
    if not os.path.exists(path):
        with open(path, 'w', newline='') as file:
            if header != []:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()
            else:
                writer = csv.writer(file)

            for element in dict:
                writer.writerow(dict[element])
    else:
        with open(path, 'a', newline='') as file:
            if header == []:
                writer = csv.writer(file)
            else:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()

            for element in dict:
                writer.writerow(dict[element])

def clearcsv(path):
    '''

    Args:
        path: 정보를 지울 csv 파일의 위치

    Returns:

    '''
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows([])

