import json
import time
import re
from.getPublicData import *

def getSquareData():
    cars = list(getAllCars())
    carsData = {}
    
    for i in cars:
        try:
            # Handle volume conversion
            vol_str = str(i.saleVolume).replace('万', '')
            vol = int(float(vol_str))
        except (ValueError, TypeError):
            vol = 0
            
        if i.carName not in carsData:
            carsData[i.carName] = {
                'volume': vol,
                'price': i.price
            }
        else:
            carsData[i.carName]['volume'] += vol
            
    # Sort by volume desc, take top 15
    sorted_cars = sorted(carsData.items(), key=lambda x: x[1]['volume'], reverse=True)[:15]
    
    brandList = []
    volumeList = []
    priceList = []
    
    for car_name, data in sorted_cars:
        brandList.append(car_name)
        volumeList.append(data['volume'])
        
        # Parse price
        try:
            price_str = str(data['price'])
            # Match float or int: \d+\.\d+ OR \d+
            matches = re.findall(r'\d+(?:\.\d+)?', price_str)
            if matches:
                # Take the first number found (usually the low price)
                priceList.append(float(matches[0]))
            else:
                priceList.append(0.0)
        except Exception:
            priceList.append(0.0)
            
    return brandList, volumeList, priceList
