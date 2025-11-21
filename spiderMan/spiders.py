from os import write
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests,csv,time,json,re,pandas as pd,random,hashlib
from lxml import etree
import django

# 尝试设置Django环境，如果失败则跳过数据库操作
try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DeviseProject.settings")
    django.setup()
    from myApp.models import carInfo, AllCarInfo
    DJANGO_AVAILABLE = True
except Exception as e:
    print(f"Django环境初始化失败: {e}")
    print("将以测试模式运行，不连接数据库")
    DJANGO_AVAILABLE = False

class spider(object):
    #定义初始化函数
    def __init__(self):
        self.spiderUrl = 'https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&city_name=%E6%9D%AD%E5%B7%9E&count=10&month=&new_energy_type=&rank_data_type=11&brand_id=&price=&manufacturer=&series_type=&nation=0'
        self.headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0' }
    def init(self):
        # 使用绝对路径指向spiderMan目录下的temp.csv
        current_dir = os.path.dirname(os.path.abspath(__file__))
        temp_csv_path = os.path.join(current_dir, 'temp.csv')
        
        if not os.path.exists(temp_csv_path):
            with open(temp_csv_path, 'a', newline='', encoding='utf-8') as wf:
                write = csv.writer(wf)
                write.writerow(["brand", "carName", "carImg", "saleVolume", "price", "manufacturer", "rank", "carModel", "energyType",
                                "marketTime", "insure"])
    def get_page(self):
        # 使用绝对路径指向spiderPage.txt
        current_dir = os.path.dirname(os.path.abspath(__file__))
        page_file_path = os.path.join(current_dir, 'spiderPage.txt')
        
        try:
            with open(page_file_path, 'r') as r_f:
                lines = r_f.readlines()
                if not lines:
                    return '0'
                return lines[-1].strip()
        except FileNotFoundError:
            with open(page_file_path, 'w') as w_f:
                w_f.write('')
            return '0'

    def set_page(self,newPage):
        # 使用绝对路径指向spiderPage.txt
        current_dir = os.path.dirname(os.path.abspath(__file__))
        page_file_path = os.path.join(current_dir, 'spiderPage.txt')
        
        with open(page_file_path, 'a') as a_f:
            a_f.write('\n'+str(newPage))

    def main(self):
        max_retries = 3
        retry_count = 0
        
        while True:
            count = self.get_page()
            params = {
                'offset':int(count)
            }
            print(f"数据从{int(count)+1}开始爬取")
            headers = self.headers
            
            try:
                pageJson = requests.get(self.spiderUrl, headers=headers, params=params).json()
                
                # 检查响应结构
                if 'data' not in pageJson or 'list' not in pageJson['data']:
                    print("响应数据结构异常，停止爬取")
                    return
                
                pageJson = pageJson['data']['list']

                if not pageJson:
                    print("没有更多数据可爬取，停止爬取")
                    return
                
                for index, car in enumerate(pageJson):
                    carData = []
                    print(f"正在爬取第{index + 1}数据")
                    # 品牌名
                    carData.append(car['brand_name'])
                    # 车名
                    carData.append(car['series_name'])
                    # 图片链接
                    carData.append(car['image'])
                    # 销量
                    carData.append(car['count'])
                    # 价格
                    price = []
                    price.append(car['min_price'])
                    price.append(car['max_price'])
                    carData.append(price)
                    # 厂商
                    carData.append(car['sub_brand_name'])
                    # 销量排名 - 强制转换为整数后再转为字符串，确保没有小数点
                    try:
                        # 直接处理原始rank值
                        rank_str = str(car['rank'])
                        # 移除可能的小数点和小数部分
                        if '.' in rank_str:
                            rank_str = rank_str.split('.')[0]
                        # 转换为整数后再转为字符串
                        rank_value = int(rank_str)
                        carData.append(str(rank_value))
                    except (ValueError, TypeError):
                        # 如果转换失败，记录错误并使用默认值
                        print(f"警告: 无法将rank值 '{car['rank']}' 转换为整数")
                        carData.append("0")  # 使用默认值0
                    # 第二个页面
                    carNumber = car['series_id']

                    infoHTML = requests.get("https://www.dongchedi.com/auto/params-carIds-x-%s" % carNumber, headers=headers)
                    infoHTMLpath = etree.HTML(infoHTML.text)
                    
                    # 车型 - 添加异常处理
                    try:
                        carModel = infoHTMLpath.xpath("//div[@data-row-anchor='jb']/div[2]/div/text()")[0]
                    except (IndexError, AttributeError):
                        carModel = "未知"
                    carData.append(carModel)
                    
                    # 能源类型 - 添加异常处理
                    try:
                        energyType = infoHTMLpath.xpath("//div[@data-row-anchor='fuel_form']/div[2]/div/text()")[0]
                    except (IndexError, AttributeError):
                        energyType = "未知"
                    carData.append(energyType)
                    
                    # 上市时间 - 添加异常处理
                    try:
                        marketTime = infoHTMLpath.xpath("//div[@data-row-anchor='market_time']/div[2]/div/text()")[0]
                    except (IndexError, AttributeError):
                        marketTime = "未知"
                    carData.append(marketTime)
                    
                    # 保修期限 - 添加异常处理
                    try:
                        insure = infoHTMLpath.xpath("//div[@data-row-anchor='period']/div[2]/div/text()")[0]
                    except (IndexError, AttributeError):
                        insure = "未知"
                    carData.append(insure)
                    
                    self.save_to_csv(carData)
                
                # 重置重试计数
                retry_count = 0
                
            except requests.exceptions.RequestException as e:
                print(f"网络请求错误: {e}")
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"达到最大重试次数({max_retries})，停止爬取")
                    return
                time.sleep(2)  # 重试前等待
                continue
                
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                return
                
            except Exception as e:
                print(f"爬取过程中出现错误: {e}")
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"达到最大重试次数({max_retries})，停止爬取")
                    return
                time.sleep(2)  # 重试前等待
                continue

            self.set_page(int(count) + 10)
            
            # 添加随机延时，避免被反爬虫
            sleep_time = random.uniform(1, 3)
            time.sleep(sleep_time)

    def save_to_csv(self, resultData):
        # 使用绝对路径指向spiderMan目录下的temp.csv
        current_dir = os.path.dirname(os.path.abspath(__file__))
        temp_csv_path = os.path.join(current_dir, 'temp.csv')
        
        with open(temp_csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(resultData)

    def clear_csv(self):
        # 使用绝对路径指向spiderMan目录下的temp.csv
        current_dir = os.path.dirname(os.path.abspath(__file__))
        temp_csv_path = os.path.join(current_dir, 'temp.csv')
        
        df = pd.read_csv(temp_csv_path)
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        print("总数量为%d"%df.shape[0])
        return df.values

    def save_to_sql(self):
        """保存数据到数据库，添加事务处理和分批插入"""
        if not DJANGO_AVAILABLE:
            print("Django不可用，跳过数据库保存")
            return
            
        try:
            # 导入Django事务和连接
            from django.db import transaction, connection
            
            # 确保使用新的数据库连接
            print("确保数据库连接有效...")
            connection.close()  # 关闭可能过期的连接
            
            data = self.clear_csv()
            print(f"准备处理{len(data)}条数据")

            # 覆盖阈值控制：抓取数据量过少时跳过快照覆盖
            MIN_ROWS = 100
            if len(data) < MIN_ROWS:
                print(f"本次抓取数据量({len(data)})低于阈值({MIN_ROWS})，跳过carInfo覆盖，保留上一次快照")
                return

            # 变更检测：基于(rank, carName, saleVolume)签名比对，数据未变更则跳过覆盖
            def normalize_rank(rv):
                try:
                    s = str(rv)
                    if '.' in s:
                        s = s.split('.')[0]
                    return str(int(s))
                except Exception:
                    return '0'

            def build_signature_rows_from_temp(temp_rows):
                rows = []
                for car in temp_rows:
                    rank_n = normalize_rank(car[6])
                    name_n = str(car[1])
                    sale_n = str(car[3])
                    rows.append((rank_n, name_n, sale_n))
                rows.sort(key=lambda x: int(x[0]))
                return rows

            def build_signature_rows_from_db():
                rows = []
                for rec in carInfo.objects.values('rank', 'carName', 'saleVolume'):
                    rank_n = normalize_rank(rec.get('rank'))
                    name_n = str(rec.get('carName', ''))
                    sale_n = str(rec.get('saleVolume', ''))
                    rows.append((rank_n, name_n, sale_n))
                rows.sort(key=lambda x: int(x[0]))
                return rows

            new_rows = build_signature_rows_from_temp(data)
            old_rows = build_signature_rows_from_db()
            new_sig = hashlib.sha256(json.dumps(new_rows, ensure_ascii=False).encode('utf-8')).hexdigest()
            old_sig = hashlib.sha256(json.dumps(old_rows, ensure_ascii=False).encode('utf-8')).hexdigest()

            if new_sig == old_sig:
                print("检测到排行榜数据未发生变化，跳过carInfo覆盖")
                return

            # 批量创建对象列表
            car_info_objects = []
            # 根据之前的去重策略，AllCarInfo表不再使用批量追加，而是检查后插入
            
            # 先处理数据，准备对象列表
            for i, car in enumerate(data):
                # 检查并修复rank字段格式
                rank_value = car[6]
                print(f"处理第{i+1}条数据 - 原始rank值: {rank_value}, 类型: {type(rank_value).__name__}")
                
                # 确保rank是纯整数字符串
                try:
                    # 如果是浮点数格式的字符串，转换为整数
                    if isinstance(rank_value, str) and '.' in rank_value:
                        rank_value = rank_value.split('.')[0]
                    # 如果是浮点数，转换为整数
                    elif isinstance(rank_value, float):
                        rank_value = str(int(rank_value))
                    # 转换为字符串
                    rank_value = str(rank_value)
                    # 确保是数字字符串
                    int(rank_value)  # 验证可以转换为整数
                    print(f"处理后rank值: {rank_value}, 类型: {type(rank_value).__name__}")
                except (ValueError, TypeError):
                    print(f"警告: rank值 '{rank_value}' 无效，使用默认值'0'")
                    rank_value = "0"
                
                # 创建carInfo表对象
                car_info_objects.append(
                    carInfo(
                        brand = car[0],
                        carName=car[1],
                        carImg=car[2],
                        saleVolume=car[3],
                        price=car[4],
                        manufacturer=car[5],
                        rank=rank_value,
                        carModel=car[7],
                        energyType=car[8],
                        marketTime=car[9],
                        insure=car[10]
                    )
                )
            
            # 使用事务处理carInfo表的清空和插入操作
            print("开始数据库事务操作...")
            with transaction.atomic():
                print("清空carInfo表数据...")
                # 使用DELETE语句直接清空，避免加载所有对象到内存
                carInfo.objects.all().delete()
                
                # 分批插入数据，每批50条，避免内存占用过大
                batch_size = 50
                for i in range(0, len(car_info_objects), batch_size):
                    batch_end = min(i + batch_size, len(car_info_objects))
                    batch = car_info_objects[i:batch_end]
                    carInfo.objects.bulk_create(batch)
                    print(f"已插入carInfo表第{i//batch_size + 1}批数据，共{len(batch)}条")
                
                print(f"已成功覆盖carInfo表，共插入{len(car_info_objects)}条数据")
            
            # 处理AllCarInfo表（使用去重逻辑）
            print("开始处理AllCarInfo表（去重逻辑）...")
            all_car_added_count = 0
            
            # 遍历数据，对每辆车应用去重逻辑
            for car in data:
                brand = car[0]
                car_name = car[1]
                car_model = car[7]
                
                # 检查是否已存在
                existing_car = AllCarInfo.objects.filter(
                    brand=brand,
                    carName=car_name,
                    carModel=car_model
                ).first()
                
                if not existing_car:
                    # 创建AllCarInfo表对象（使用同样的rank处理逻辑）
                    rank_value = car[6]
                    try:
                        if isinstance(rank_value, str) and '.' in rank_value:
                            rank_value = rank_value.split('.')[0]
                        elif isinstance(rank_value, float):
                            rank_value = str(int(rank_value))
                        rank_value = str(rank_value)
                        int(rank_value)
                    except (ValueError, TypeError):
                        rank_value = "0"
                    
                    new_all_car = AllCarInfo(
                        brand = car[0],
                        carName=car[1],
                        carImg=car[2],
                        saleVolume=car[3],
                        price=car[4],
                        manufacturer=car[5],
                        rank=rank_value,
                        carModel=car[7],
                        energyType=car[8],
                        marketTime=car[9],
                        insure=car[10]
                    )
                    new_all_car.save()
                    all_car_added_count += 1
            
            print(f"AllCarInfo表去重处理完成，新增{all_car_added_count}条数据")
            
            # 在数据保存到数据库后，主动清空temp.csv文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            temp_csv_path = os.path.join(current_dir, 'temp.csv')
            
            with open(temp_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["brand", "carName", "carImg", "saleVolume", "price", "manufacturer", "rank", "carModel", "energyType",
                                "marketTime", "insure"])
            print(f"数据保存完成后，已主动清空temp.csv文件: {temp_csv_path}")
            
        except django.db.utils.OperationalError as e:
            print(f"数据库操作错误: {e}")
            if 'Server has gone away' in str(e) or 'Lost connection' in str(e):
                print("数据库连接断开，请检查数据库服务是否正常运行")
            raise
        except Exception as e:
            print(f"保存数据到数据库时出错: {e}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == '__main__':
    try:
        # 清空spiderPage.txt文件内容 - 使用绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        page_file_path = os.path.join(current_dir, 'spiderPage.txt')
        
        with open(page_file_path, 'w', encoding='utf-8') as f:
            f.write('')
        print(f"已清空spiderPage.txt文件内容: {page_file_path}")
        
        # 清空temp.csv文件内容 - 使用绝对路径
        temp_csv_path = os.path.join(current_dir, 'temp.csv')
        
        with open(temp_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["brand", "carName", "carImg", "saleVolume", "price", "manufacturer", "rank", "carModel", "energyType",
                            "marketTime", "insure"])
        print(f"已清空temp.csv文件内容: {temp_csv_path}")
        
        # 创建爬虫对象
        spiderObj = spider()
        
        # 初始化CSV文件
        spiderObj.init()
        
        # 开始爬取数据
        print("开始爬取数据...")
        spiderObj.main()
        
        # 爬取完成后，将数据保存到数据库
        spiderObj.save_to_sql()
        print("数据保存操作已完成！")
    except Exception as e:
        print(f"执行过程中出错: {e}")
        import traceback
        traceback.print_exc()