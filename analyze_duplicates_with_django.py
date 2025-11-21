import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DeviseProject.settings')
django.setup()

from myApp.models import AllCarInfo

def analyze_duplicates():
    print("=== 分析allcarinfo表中的重复记录 ===")
    
    # 1. 查询总记录数
    total_count = AllCarInfo.objects.count()
    print(f"总记录数: {total_count}")
    
    # 2. 使用Django ORM查询重复记录
    # 由于Django ORM不直接支持复杂的GROUP BY HAVING查询，我们使用原始SQL
    from django.db import connection
    
    print("\n重复记录分析（基于品牌+车名+车型）:")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT brand, carName, carModel, COUNT(*) as duplicate_count
            FROM allcarinfo
            GROUP BY brand, carName, carModel
            HAVING COUNT(*) > 1
            ORDER BY duplicate_count DESC
        """)
        duplicate_records = cursor.fetchall()
    
    if duplicate_records:
        print(f"找到 {len(duplicate_records)} 组重复记录:")
        for record in duplicate_records[:10]:  # 只显示前10组
            print(f"品牌: {record[0]}, 车名: {record[1]}, 车型: {record[2]}, 重复次数: {record[3]}")
        
        if len(duplicate_records) > 10:
            print(f"... 还有 {len(duplicate_records) - 10} 组重复记录未显示")
    else:
        print("没有找到重复记录")
    
    # 3. 计算预计可去重的记录数
    total_duplicates = sum(record[3] - 1 for record in duplicate_records)
    print(f"\n预计可清理的重复记录数: {total_duplicates}")
    print(f"清理后预计剩余记录数: {total_count - total_duplicates}")
    
    # 4. 显示一些重复记录的详细信息作为示例
    if duplicate_records:
        brand, carName, carModel, _ = duplicate_records[0]
        print(f"\n第一组重复记录详情（品牌: {brand}, 车名: {carName}, 车型: {carModel}）:")
        
        duplicates = AllCarInfo.objects.filter(
            brand=brand, 
            carName=carName, 
            carModel=carModel
        ).order_by('creteTime')
        
        for car in duplicates:
            print(f"ID: {car.id}, 价格: {car.price}, 创建时间: {car.creteTime}")

if __name__ == "__main__":
    analyze_duplicates()