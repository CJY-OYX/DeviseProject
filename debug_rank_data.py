# -*- coding: utf-8 -*-
"""
调试脚本：检查API返回的原始rank数据格式
"""
import requests
import json

# 设置API请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# API请求URL
url = 'https://****.com/gateway/m/salesRank'

# 请求参数
params = {
    'page': 1,
    'pageSize': 10,
    'dateType': 'month',
    'date': '2025-09',
    'salesType': 'retail'
}

print("开始调试rank字段数据格式...")

# 发送请求
try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # 检查请求是否成功
    
    # 尝试解析JSON
    data = response.json()
    print("成功获取API数据")
    
    # 检查数据结构
    if 'data' in data and 'data' in data['data']:
        cars = data['data']['data']
        print(f"获取到{len(cars)}条车辆数据")
        
        # 检查每条数据的rank字段
        for i, car in enumerate(cars):
            if 'rank' in car:
                rank = car['rank']
                print(f"车辆[{i+1}] - rank值: {rank}, 类型: {type(rank).__name__}")
                
                # 尝试应用我们的修复逻辑并显示结果
                # 逻辑1：直接转换为字符串
                rank_str1 = str(rank)
                print(f"  转换为字符串: {rank_str1}, 类型: {type(rank_str1).__name__}")
                
                # 逻辑2：移除小数点
                if '.' in rank_str1:
                    rank_str2 = rank_str1.split('.')[0]
                else:
                    rank_str2 = rank_str1
                print(f"  移除小数点: {rank_str2}, 类型: {type(rank_str2).__name__}")
                
                # 逻辑3：转换为整数再转回字符串
                try:
                    rank_int = int(rank_str2)
                    rank_str3 = str(rank_int)
                    print(f"  转换为整数再转回字符串: {rank_str3}, 类型: {type(rank_str3).__name__}")
                except ValueError:
                    print(f"  无法转换为整数")
    else:
        print("数据结构不符合预期")
        print(f"响应数据结构: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
except requests.exceptions.RequestException as e:
    print(f"请求错误: {e}")
    
except json.JSONDecodeError:
    print("无法解析JSON响应")
    print(f"原始响应内容: {response.text}")