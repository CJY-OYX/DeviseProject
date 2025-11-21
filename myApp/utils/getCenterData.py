import json
import time
from.getPublicData import *

def getBaseData():
    cars = list(getAllCars())
    sumCar = len(cars)
    if sumCar == 0:
        return 0, 0, '', '', '', 0.0
    highVolume = getattr(cars[0], 'saleVolume', 0)
    topCar = getattr(cars[0], 'carName', '')
    # 车型
    carModels = {}
    maxModel = 0
    mostModel = ''
    for i in cars:
        if carModels.get(i.carModel, -1) == -1:
            carModels[str(i.carModel)] = 1
        else:
            carModels[str(i.carModel)] += 1
    carModels = sorted(carModels.items(), key=lambda x: x[1], reverse=True)
    mostModel = carModels[0][0]
    # 品牌
    carBrands = {}
    maxBrand = 0
    mostBrand = ''
    for i in cars:
        if carBrands.get(i.brand, -1) == -1:
            carBrands[str(i.brand)] = 1
        else:
            carBrands[str(i.brand)] += 1
    for k, v in carBrands.items():
        if v > maxBrand:
            maxBrand = v
            mostBrand = k
    # 均价
    carPrices = {}
    aveagePrice = 0
    sumPrice = 0
    valid_pairs = 0
    for i in cars:
        try:
            price_list = json.loads(i.price)
            if isinstance(price_list, list) and len(price_list) >= 2:
                x = float(price_list[0]) + float(price_list[1])
                sumPrice += x
                valid_pairs += 1
        except Exception:
            pass
    if valid_pairs > 0:
        aveagePrice = sumPrice / (valid_pairs * 2)
    averagePrice = round(aveagePrice, 2)
    return sumCar, highVolume, topCar, mostModel, mostBrand, averagePrice

def getRollData():
    cars = list(getAllCars())
    # 品牌
    carBrands = {}
    for i in cars:
        if carBrands.get(i.brand, -1) == -1:
            carBrands[str(i.brand)] = 1
        else:
            carBrands[str(i.brand)] += 1
    brandlist = [(value, key) for key, value in carBrands.items()]
    brandlist = sorted(brandlist, reverse=True)[:10]
    sortDict = {i[1]:i[0] for i in brandlist}
    lastSortList = []
    for k, v in sortDict.items():
        lastSortList.append({
            'name':k,
            'value':v
        })
    return lastSortList

def getTypeRate():
    cars = list(getAllCars())
    # 使用实际的车辆总数，而不是硬编码的636
    sumCar = len(cars)
    if sumCar == 0:
        return 0.0, 0.0, 0.0
    
    # 能源类型
    carTypes = {}
    for i in cars:
        if carTypes.get(i.energyType, -1) == -1:
            carTypes[str(i.energyType)] = 1
        else:
            carTypes[str(i.energyType)] += 1
    
    # 使用实际总数计算比例，并处理可能的键缺失情况
    oil_count = carTypes.get('汽油', 0)
    electric_count = carTypes.get('纯电动', 0)
    
    oilRate = round(oil_count / sumCar * 100, 2)
    electricRare = round(electric_count / sumCar * 100, 2)
    # 混合类型包括所有既不是汽油也不是纯电动的车型
    mixRate = round(((sumCar - oil_count - electric_count) / sumCar * 100), 2)
    
    return oilRate, electricRare, mixRate