#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查carInfo表中rank字段的数据格式"""

import os
import sys
from datetime import datetime

# 设置Django环境
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DeviseProject.settings")

import django
django.setup()

from myApp.models import carInfo

def check_rank_format():
    print(f"[{datetime.now()}] 开始检查carInfo表中rank字段的数据格式")
    
    # 查询前10条数据检查格式
    first_10_cars = carInfo.objects.all()[:10]
    print("前10条数据的rank值:")
    for car in first_10_cars:
        print(f"ID: {car.id}, 车名: {car.carName}, rank: {car.rank}, 类型: {type(car.rank).__name__}")
    
    # 检查是否有带小数点的rank值
    problematic_ranks = []
    all_cars = carInfo.objects.all()[:1000]  # 限制检查前1000条数据以提高性能
    
    for car in all_cars:
        # 检查rank是否为字符串且包含小数点
        if isinstance(car.rank, str) and '.' in car.rank:
            problematic_ranks.append((car.id, car.carName, car.rank))
    
    if problematic_ranks:
        print(f"\n发现{len(problematic_ranks)}条带小数点的rank值:")
        for id, carName, rank in problematic_ranks[:20]:  # 只显示前20条
            print(f"ID: {id}, 车名: {carName}, rank: {rank}")
        if len(problematic_ranks) > 20:
            print(f"... 还有{len(problematic_ranks) - 20}条未显示")
    else:
        print("\n未发现带小数点的rank值")
    
    # 检查排名较大的数据，因为问题可能在后面
    high_rank_cars = carInfo.objects.order_by('-rank')[:50]  # 获取rank值较大的50条数据
    print("\nrank值较大的前10条数据:")
    for car in high_rank_cars[:10]:
        print(f"ID: {car.id}, 车名: {car.carName}, rank: {car.rank}")
    
    return problematic_ranks

if __name__ == '__main__':
    check_rank_format()