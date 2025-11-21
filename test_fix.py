import os
import sys
from datetime import datetime

# 确保可以导入项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print(f"[{datetime.now()}] 开始测试爬虫数据写入数据库修复")
    
    try:
        # 导入并调用auto_update模块的get_latest_rank_data函数
        from spiderMan.auto_update import get_latest_rank_data
        
        print(f"[{datetime.now()}] 导入auto_update模块成功")
        print(f"[{datetime.now()}] 开始执行数据更新...")
        
        # 执行数据更新
        success = get_latest_rank_data()
        
        if success:
            print(f"[{datetime.now()}] 测试成功！数据更新功能已修复")
            print(f"[{datetime.now()}] 爬取的数据应该已经成功写入数据库")
        else:
            print(f"[{datetime.now()}] 测试失败！数据更新未成功")
            sys.exit(1)
            
    except Exception as e:
        print(f"[{datetime.now()}] 测试过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()