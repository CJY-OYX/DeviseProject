#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试修复后的auto_update.py功能"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from spiderMan.auto_update import get_latest_rank_data

def test_fix():
    print(f"[{datetime.now()}] 开始测试修复后的auto_update功能")
    
    # 直接调用修复后的get_latest_rank_data函数
    success = get_latest_rank_data()
    
    if success:
        print(f"[{datetime.now()}] 测试成功! 数据更新功能已修复")
        print("carInfo数据表应该已成功更新为最新数据")
    else:
        print(f"[{datetime.now()}] 测试失败! 请检查错误信息")
    
    return success

if __name__ == '__main__':
    test_fix()