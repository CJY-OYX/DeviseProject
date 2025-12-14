import json
import time
from .getPublicData import *

def getPriceSortData():
    cars = list(getAllCars())
    priceSortList = {'0-5w':0, '5-10w':0, '10-20w':0, '20-30w':0, '30w以上':0}
    for i in cars:
        s = [json.loads(i.price)[0]][0]
        if s<5:
            priceSortList['0-5w'] += 1
        elif s>=5 and s<10:
            priceSortList['5-10w'] += 1
        elif s>=10 and s<20:
            priceSortList['10-20w'] += 1
        elif s>=20 and s<30:
            priceSortList['20-30w'] += 1
        else:
            priceSortList['30w以上'] += 1
    realData = []
    for k, v in priceSortList.items():
        realData.append({
            'name': k,
            'value': v
        })
    return realData

def getCenterRightData(energyType):
    # 根据能源类型过滤数据
    if energyType == 0:  # 全部
        cars = list(getAllCars())
    else:
        cars = list(getAllCars().filter(energyType=energyType))
    
    # 统计价格区间
    priceSortList = {'0-5w':0, '5-10w':0, '10-20w':0, '20-30w':0, '30w以上':0}
    for car in cars:
        price = json.loads(car.price)[0]  # 获取最低价
        if price < 5:
            priceSortList['0-5w'] += 1
        elif 5 <= price < 10:
            priceSortList['5-10w'] += 1
        elif 10 <= price < 20:
            priceSortList['10-20w'] += 1
        elif 20 <= price < 30:
            priceSortList['20-30w'] += 1
        else:
            priceSortList['30w以上'] += 1
    
    # 转换为前端需要的格式
    realData = []
    for name, value in priceSortList.items():
        realData.append({
            'name': name,
            'value': value
        })
    
    return realData
