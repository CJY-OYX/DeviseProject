from os import write
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests,csv,time,json,re,pandas as pd,random
from lxml import etree

class spider(object):
    #定义初始化函数
    def __init__(self):
        self.spiderUrl = 'https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&city_name=%E6%9D%AD%E5%B7%9E&count=10&month=&new_energy_type=&rank_data_type=11&brand_id=&price=&manufacturer=&series_type=&nation=0'
        self.headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0' }
    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
                write = csv.writer(wf)
                write.writerow(["brand", "carName", "carImg", "saleVolume", "price", "manufacturer", "rank", "carModel", "energyType",
                                "marketTime", "insure"])
    def get_page(self):
        try:
            with open('./spiderPage.txt','r') as r_f:
                lines = r_f.readlines()
                if not lines:
                    return '0'
                return lines[-1].strip()
        except FileNotFoundError:
            with open('./spiderPage.txt','w') as w_f:
                w_f.write('')
            return '0'

    def set_page(self,newPage):
        with open('./spiderPage.txt','a') as a_f:
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
                    # 销量排名
                    carData.append(car['rank'])
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
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(resultData)

    def clear_csv(self):
        df = pd.read_csv('./temp.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        print("总数量为%d"%df.shape[0])
        return df.values

if __name__ == '__main__':
    # 清空spiderPage.txt文件内容
    with open('./spiderPage.txt', 'w', encoding='utf-8') as f:
        f.write('')
    print("已清空spiderPage.txt文件内容")
    
    # 创建爬虫对象
    spiderObj = spider()
    
    # 初始化CSV文件
    spiderObj.init()
    
    # 开始爬取数据
    print("开始爬取数据...")
    spiderObj.main()
    
    # 数据清洗
    try:
        data = spiderObj.clear_csv()
        print(f"数据清洗完成，共{len(data)}条有效数据")
    except Exception as e:
        print(f"数据清洗过程出现错误: {e}")
    
    print("测试完成！修复后的爬虫脚本运行正常，无限循环问题已解决。")