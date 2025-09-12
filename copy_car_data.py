#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将carinfo表中的所有数据复制到allcarinfo表中
"""
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DeviseProject.settings')

# 导入Django模块
import django
django.setup()

# 导入模型
from myApp.models import carInfo, AllCarInfo


def copy_car_data():
    """
    将carinfo表中的所有数据复制到allcarinfo表中
    """
    try:
        print("开始复制数据...")
        
        # 获取carinfo表中的所有数据
        car_info_list = carInfo.objects.all()
        total_count = car_info_list.count()
        print(f"从carinfo表获取了{total_count}条数据")
        
        if total_count == 0:
            print("carinfo表中没有数据，无需复制")
            return
        
        # 准备复制到allcarinfo表的数据列表
        all_car_info_list = []
        
        # 遍历carinfo数据，创建AllCarInfo对象
        for car in car_info_list:
            # 检查allcarinfo表中是否已存在相同的数据
            # 这里可以根据实际情况修改判断条件
            exists = AllCarInfo.objects.filter(
                brand=car.brand,
                carName=car.carName,
                carModel=car.carModel
            ).exists()
            
            if not exists:
                # 创建新的AllCarInfo对象
                all_car_info = AllCarInfo(
                    brand=car.brand,
                    carName=car.carName,
                    carImg=car.carImg,
                    saleVolume=car.saleVolume,
                    price=car.price,
                    manufacturer=car.manufacturer,
                    rank=car.rank,
                    carModel=car.carModel,
                    energyType=car.energyType,
                    marketTime=car.marketTime,
                    insure=car.insure
                )
                all_car_info_list.append(all_car_info)
        
        # 批量插入数据到allcarinfo表
        if all_car_info_list:
            AllCarInfo.objects.bulk_create(all_car_info_list)
            print(f"成功复制了{len(all_car_info_list)}条数据到allcarinfo表")
        else:
            print("所有数据都已存在于allcarinfo表中，无需复制")
        
        # 统计allcarinfo表中的数据总量
        all_car_count = AllCarInfo.objects.count()
        print(f"复制完成，allcarinfo表中现在共有{all_car_count}条数据")
        
    except Exception as e:
        print(f"复制数据时发生错误: {str(e)}")


if __name__ == "__main__":
    copy_car_data()