import json
import time
from.getPublicData import *

def getPieBrandData():
    cars = list(getAllCars())
    carsVolume = {}
    bestCarImg = {}
    maxVolumePerBrand = {}

    for i in cars:
        try:
            vol = int(i.saleVolume)
        except:
            vol = 0

        if carsVolume.get(i.brand, -1) == -1:
            carsVolume[str(i.brand)] = vol
        else:
            carsVolume[str(i.brand)] += vol
        
        # 记录每个品牌销量最高的车的图片
        if i.brand not in maxVolumePerBrand or vol > maxVolumePerBrand[i.brand]:
            maxVolumePerBrand[i.brand] = vol
            bestCarImg[i.brand] = i.carImg

    carsVolume = sorted(zip(carsVolume.values(), carsVolume.keys()), reverse=True)
    sortDict = {i[1]: i[0] for i in carsVolume}
    lastPieList = []
    for k, v in sortDict.items():
        lastPieList.append({
            'name': k,
            'value': v,
            'img': bestCarImg.get(k, '')
        })
    return lastPieList[:10]