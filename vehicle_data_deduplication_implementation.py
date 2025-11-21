import os
import sys
import django
from django.db import connection

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DeviseProject.settings')
django.setup()

from myApp.models import carInfo, AllCarInfo

def add_unique_index():
    """为allcarinfo表添加唯一索引，防止重复数据"""
    print("=== 添加唯一索引到allcarinfo表 ===")
    
    with connection.cursor() as cursor:
        try:
            # 检查是否已存在索引
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND tbl_name='allcarinfo' AND name='unique_car_identifier'
            """)
            if cursor.fetchone():
                print("唯一索引 'unique_car_identifier' 已存在，跳过创建")
            else:
                # 添加唯一索引
                cursor.execute("""
                    CREATE UNIQUE INDEX unique_car_identifier 
                    ON allcarinfo(brand, carName, carModel)
                """)
                print("成功在 allcarinfo 表的 brand, carName, carModel 字段上创建唯一索引")
                print("注意：此索引将防止相同品牌、车名和车型的重复记录被插入")
        except Exception as e:
            print(f"添加索引时出错: {e}")
            print("这可能是因为表中仍然存在重复记录，请先确保表中没有重复数据")

def process_vehicle_data(vehicle_data):
    """处理单条车辆数据，实现去重逻辑
    
    Args:
        vehicle_data: 包含车辆信息的字典
    
    Returns:
        tuple: (是否成功, 消息)
    """
    try:
        # 1. 首先将数据写入carinfo表（存储最新数据）
        new_car = carInfo(
            brand=vehicle_data['brand'],
            carName=vehicle_data['carName'],
            carModel=vehicle_data['carModel'],
            carImg=vehicle_data.get('carImg', ''),
            saleVolume=vehicle_data.get('saleVolume', ''),
            price=vehicle_data.get('price', ''),
            manufacturer=vehicle_data.get('manufacturer', ''),
            # rank字段可以设为空或默认值，因为用户说不需要
            rank='',
            energyType=vehicle_data.get('energyType', ''),
            marketTime=vehicle_data.get('marketTime', ''),
            insure=vehicle_data.get('insure', '')
        )
        new_car.save()
        
        # 2. 检查是否已存在于allcarinfo表中
        existing_car = AllCarInfo.objects.filter(
            brand=vehicle_data['brand'],
            carName=vehicle_data['carName'],
            carModel=vehicle_data['carModel']
        ).first()
        
        if existing_car:
            # 车辆已存在，不需要重复添加到allcarinfo表
            return True, f"车辆 '{vehicle_data['brand']} {vehicle_data['carName']}' 已存在于allcarinfo表中，跳过添加"
        else:
            # 车辆不存在，添加到allcarinfo表
            new_all_car = AllCarInfo(
                brand=vehicle_data['brand'],
                carName=vehicle_data['carName'],
                carModel=vehicle_data['carModel'],
                carImg=vehicle_data.get('carImg', ''),
                saleVolume=vehicle_data.get('saleVolume', ''),
                price=vehicle_data.get('price', ''),
                manufacturer=vehicle_data.get('manufacturer', ''),
                rank='',  # 同样设为空，因为不需要
                energyType=vehicle_data.get('energyType', ''),
                marketTime=vehicle_data.get('marketTime', ''),
                insure=vehicle_data.get('insure', '')
            )
            new_all_car.save()
            return True, f"成功将车辆 '{vehicle_data['brand']} {vehicle_data['carName']}' 添加到allcarinfo表"
            
    except Exception as e:
        # 处理可能的唯一索引冲突或其他错误
        if 'UNIQUE constraint failed' in str(e):
            return False, f"重复数据错误: 车辆 '{vehicle_data['brand']} {vehicle_data['carName']}' 已存在于allcarinfo表中"
        return False, f"处理车辆数据时出错: {e}"

def batch_process_vehicles(vehicles_list):
    """批量处理车辆数据列表
    
    Args:
        vehicles_list: 车辆数据字典列表
    """
    print(f"\n=== 开始批量处理 {len(vehicles_list)} 条车辆数据 ===")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, vehicle in enumerate(vehicles_list, 1):
        success, message = process_vehicle_data(vehicle)
        print(f"[{i}/{len(vehicles_list)}] {message}")
        
        if success:
            if "跳过" in message:
                skip_count += 1
            else:
                success_count += 1
        else:
            error_count += 1
    
    print(f"\n批量处理完成:")
    print(f"- 成功添加到allcarinfo表: {success_count}")
    print(f"- 因重复跳过: {skip_count}")
    print(f"- 处理失败: {error_count}")

def demo_usage():
    """演示去重逻辑的使用方法"""
    print("=== 车辆数据去重逻辑演示 ===")
    print("此脚本演示了如何从懂车帝爬取数据并避免重复写入allcarinfo表")
    print("\n数据处理流程:")
    print("1. 爬虫数据 → carinfo表(始终写入，保存最新数据)")
    print("2. 通过 brand+carName+carModel 检查allcarinfo表中是否已存在")
    print("3. 如果不存在，才写入allcarinfo表")
    print("\n注意: allcarinfo表仅存储唯一的车辆信息，carinfo表可存储最新的爬取数据")
    
    # 示例数据
    sample_vehicles = [
        {
            'brand': '示例品牌',
            'carName': '示例车型A',
            'carModel': '紧凑型车',
            'carImg': 'http://example.com/car1.jpg',
            'saleVolume': '1000',
            'price': '[10.98, 15.98]',
            'manufacturer': '示例厂商',
            'energyType': '汽油',
            'marketTime': '2024-01',
            'insure': '3年或10万公里'
        },
        {
            'brand': '示例品牌',
            'carName': '示例车型B',
            'carModel': '中型SUV',
            'carImg': 'http://example.com/car2.jpg',
            'saleVolume': '800',
            'price': '[18.98, 25.98]',
            'manufacturer': '示例厂商',
            'energyType': '混动',
            'marketTime': '2024-03',
            'insure': '4年或12万公里'
        },
        # 重复数据测试
        {
            'brand': '示例品牌',
            'carName': '示例车型A',  # 与第一条重复的品牌+车名+车型
            'carModel': '紧凑型车',
            'carImg': 'http://example.com/car1_updated.jpg',
            'saleVolume': '1200',  # 更新的销量
            'price': '[10.98, 16.98]',  # 更新的价格
            'manufacturer': '示例厂商',
            'energyType': '汽油',
            'marketTime': '2024-01',
            'insure': '3年或10万公里'
        }
    ]
    
    # 询问是否执行演示
    # 注意：实际使用时，这里应该是从爬虫获取的真实数据
    if len(sys.argv) > 1 and sys.argv[1] == '--run-demo':
        # 添加唯一索引
        add_unique_index()
        
        # 执行批量处理演示
        batch_process_vehicles(sample_vehicles)
        
        print("\n=== 爬虫整合建议 ===")
        print("在实际爬虫代码中，建议这样整合去重逻辑:")
        print("""
        # 爬虫代码示例
        def crawl_and_save():
            # 1. 从懂车帝爬取数据
            vehicles_data = crawl_dongchedi()
            
            # 2. 批量处理数据
            batch_process_vehicles(vehicles_data)
        """)
    else:
        print("\n要运行演示，请使用命令: python vehicle_data_deduplication_implementation.py --run-demo")

if __name__ == "__main__":
    demo_usage()