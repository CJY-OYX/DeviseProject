import time
import subprocess
import sys
import os
import csv
import logging
import traceback
from datetime import datetime

# 设置日志
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, 'auto_update_logs.txt')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='a'
)

# 全局变量
DJANGO_AVAILABLE = False
django = None
carInfo = None
AllCarInfo = None

def init_django():
    """初始化Django环境"""
    global DJANGO_AVAILABLE, django, carInfo, AllCarInfo
    try:
        import django as django_module
        django = django_module
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DeviseProject.settings")
        django.setup()
        from myApp.models import carInfo as carInfo_model, AllCarInfo as AllCarInfo_model
        carInfo = carInfo_model
        AllCarInfo = AllCarInfo_model
        DJANGO_AVAILABLE = True
        print(f"Django环境初始化成功")
        logging.info("Django环境初始化成功")
        return True
    except Exception as e:
        error_msg = f"Django环境初始化失败: {e}"
        print(error_msg)
        logging.error(error_msg)
        traceback_info = traceback.format_exc()
        logging.error(f"Django环境初始化异常详情: {traceback_info}")
        DJANGO_AVAILABLE = False
        return False

# 初始化Django环境
init_django()

def reset_django_connection():
    """重置Django数据库连接"""
    try:
        if DJANGO_AVAILABLE and django:
            from django.db import connection
            connection.close()
            logging.info("Django数据库连接已重置")
            return True
        return False
    except Exception as e:
        logging.error(f"重置Django数据库连接失败: {e}")
        return False

def get_latest_rank_data():
    """获取最新的排行榜数据，添加数据库连接管理和重试机制"""
    max_retries = 3  # 最大重试次数
    retry_count = 0
    success = False
    
    while retry_count < max_retries and not success:
        try:
            # 简易互斥锁，防止并发运行导致写入重复
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            spider_man_dir = os.path.dirname(os.path.abspath(__file__))
            lock_file_path = os.path.join(spider_man_dir, 'update.lock')
            if os.path.exists(lock_file_path):
                print(f"[{datetime.now()}] 检测到更新锁文件，已有更新进程运行，跳过本轮")
                logging.warning("检测到更新锁文件，已有更新进程运行，跳过本轮")
                return False
            # 写入锁文件
            with open(lock_file_path, 'w', encoding='utf-8') as lf:
                lf.write(f"pid={os.getpid()}, time={datetime.now()}\n")
            # 确保Django环境可用
            if not DJANGO_AVAILABLE:
                print("Django环境不可用，尝试重新初始化...")
                logging.warning("Django环境不可用，尝试重新初始化")
                if not init_django():
                    raise Exception("无法初始化Django环境")
            
            # 每次重试都重新初始化Django环境，确保数据库连接是新的
            print(f"[{datetime.now()}] 第{retry_count + 1}次尝试获取数据")
            logging.info(f"第{retry_count + 1}次尝试获取数据")
            
            # 重置数据库连接
            reset_django_connection()
            
            print(f"[{datetime.now()}] 项目根目录: {project_root}")
            print(f"[{datetime.now()}] SpiderMan目录: {spider_man_dir}")
            
            # 清空spiderPage.txt文件，确保每次都从第一页开始爬取
            page_file_path = os.path.join(spider_man_dir, 'spiderPage.txt')
            with open(page_file_path, 'w', encoding='utf-8') as f:
                f.write('')
            print(f"[{datetime.now()}] 已清空spiderPage.txt文件: {page_file_path}")
            
            # 清空temp.csv文件，确保数据是最新的
            temp_csv_path = os.path.join(spider_man_dir, 'temp.csv')
            with open(temp_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["brand", "carName", "carImg", "saleVolume", "price", "manufacturer", "rank", "carModel", "energyType",
                                "marketTime", "insure"])
            print(f"[{datetime.now()}] 已清空temp.csv文件: {temp_csv_path}")
            
            # 直接导入spiders模块
            sys.path.insert(0, project_root)
            from spiderMan.spiders import spider
            
            print(f"[{datetime.now()}] 初始化爬虫对象")
            
            # 创建爬虫对象
            spiderObj = spider()
            
            print(f"[{datetime.now()}] 开始爬取数据")
            
            # 开始爬取数据
            spiderObj.main()
            
            print(f"[{datetime.now()}] 爬取完成，开始保存数据到数据库")
            
            # 爬取完成后，将数据保存到数据库
            spiderObj.save_to_sql()
            
            print(f"[{datetime.now()}] 数据更新成功")
            logging.info("数据更新成功")
            success = True
            return True
            
        except django.db.utils.OperationalError as e:
            # 专门处理数据库连接错误
            retry_count += 1
            error_msg = str(e)
            print(f"[{datetime.now()}] 数据库操作错误 ({retry_count}/{max_retries}): {error_msg}")
            logging.error(f"数据库操作错误 ({retry_count}/{max_retries}): {error_msg}")
            traceback_info = traceback.format_exc()
            logging.error(f"数据库操作错误详情: {traceback_info}")
            
            if 'Server has gone away' in error_msg or 'Lost connection' in error_msg or '2006' in error_msg:
                wait_time = 5
                print(f"[{datetime.now()}] 数据库连接断开，将在{wait_time}秒后第{retry_count}次重试...")
                logging.warning(f"数据库连接断开，将在{wait_time}秒后重试 ({retry_count}/{max_retries})")
                time.sleep(wait_time)
                
                # 重新初始化Django数据库连接
                reset_django_connection()
            else:
                # 其他数据库错误，直接抛出
                raise
        except Exception as e:
            print(f"[{datetime.now()}] 执行爬虫脚本时出错: {str(e)}")
            logging.error(f"执行爬虫脚本时出错: {str(e)}")
            traceback_info = traceback.format_exc()
            logging.error(f"异常详情: {traceback_info}")
            # 非数据库连接错误，不再重试
            return False
        finally:
            # 清理锁文件
            try:
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)
            except Exception:
                pass
    
    error_msg = f"[{datetime.now()}] 已达到最大重试次数({max_retries})，数据更新失败"
    print(error_msg)
    logging.error(error_msg)
    return False

def main():
    """主函数，持续监听并更新数据"""
    print("开始监听懂车帝排行榜变化...")
    logging.info("汽车排行榜数据自动更新程序启动")
    
    # 设置更新间隔（秒）
    update_interval = 300  # 每5分钟更新一次
    
    while True:
        try:
            # 获取当前时间
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{current_time}] 开始更新汽车排行榜数据...")
            logging.info(f"[{current_time}] 开始更新汽车排行榜数据")
            
            # 每5分钟检查一次排行榜变化
            success = get_latest_rank_data()
            
            if success:
                print(f"[{datetime.now()}] 已完成一次数据更新")
                logging.info(f"[{datetime.now()}] 已完成一次数据更新")
            else:
                print(f"[{datetime.now()}] 数据更新失败，将在下次循环重试")
                logging.warning(f"[{datetime.now()}] 数据更新失败，将在下次循环重试")
            
            print(f"\n[{current_time}] 更新完成，等待下次更新...")
            logging.info(f"[{current_time}] 更新完成，等待下次更新")
            
            # 等待5分钟（300秒）后再次检查
            time.sleep(update_interval)
            
        except KeyboardInterrupt:
            print("\n程序被用户中断，正在退出...")
            logging.info("程序被用户中断，正在退出")
            break
        except Exception as e:
            print(f"[{datetime.now()}] 监听过程中出现错误: {str(e)}")
            logging.error(f"监听过程中出现错误: {str(e)}")
            traceback_info = traceback.format_exc()
            logging.error(f"异常详情: {traceback_info}")
            # 出现错误后等待一段时间再重试
            print(f"等待{update_interval // 2}秒后继续...")
            time.sleep(update_interval // 2)

def test_run():
    """测试运行模式，只执行一次数据更新就退出"""
    print("开始测试运行模式...")
    logging.info("测试运行模式启动")
    
    try:
        # 初始化Django环境
        if not init_django():
            print("无法初始化Django环境，测试失败")
            return False
        
        # 执行一次数据更新
        success = get_latest_rank_data()
        
        if success:
            print("测试运行成功完成！")
            logging.info("测试运行成功完成")
            return True
        else:
            print("测试运行失败")
            logging.error("测试运行失败")
            return False
    except Exception as e:
        print(f"测试运行过程中发生错误: {e}")
        logging.error(f"测试运行过程中发生错误: {e}")
        traceback_info = traceback.format_exc()
        logging.error(f"异常详情: {traceback_info}")
        return False

if __name__ == "__main__":
    # 检查是否为测试运行模式
    if len(sys.argv) > 1 and sys.argv[1] == '--test-run':
        test_run()
    else:
        main()