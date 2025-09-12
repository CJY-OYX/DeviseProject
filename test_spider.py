import os
import subprocess
import time
import sys

# 测试executeDataUpdate函数中的爬虫启动代码
def test_spider_execution():
    try:
        # 获取项目根目录
        project_root = os.path.dirname(os.path.abspath(__file__))
        print(f"项目根目录: {project_root}")
        
        # 构建爬虫脚本的绝对路径
        spider_script_path = os.path.join(project_root, 'spiderMan', 'spiders.py')
        print(f"爬虫脚本路径: {spider_script_path}")
        print(f"爬虫脚本是否存在: {os.path.exists(spider_script_path)}")
        
        # 设置环境变量
        env = os.environ.copy()
        env['PYTHONPATH'] = project_root + (os.pathsep + env.get('PYTHONPATH', '')) if env.get('PYTHONPATH') else project_root
        print(f"设置后的PYTHONPATH: {env['PYTHONPATH']}")
        
        # 创建一个测试版本的爬虫脚本，只打印信息不实际爬取
        test_spider_content = '''
import os
import sys
import time
print("测试脚本执行成功")
print("当前工作目录: %s" % os.getcwd())
print("PYTHONPATH: %s" % os.environ.get('PYTHONPATH'))
print("sys.path: %s" % sys.path)
# 等待几秒后退出
for i in range(5, 0, -1):
    print(f"测试脚本将在{i}秒后退出")
    time.sleep(1)
'''
        
        test_spider_path = os.path.join(project_root, 'spiderMan', 'test_spider.py')
        with open(test_spider_path, 'w', encoding='utf-8') as f:
            f.write(test_spider_content)
        
        print("\n创建了测试爬虫脚本，尝试使用修复后的方式执行...")
        
        # 启动测试爬虫脚本（非阻塞方式）
        process = subprocess.Popen(
            ['python', test_spider_path],
            shell=True,
            cwd=project_root,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"子进程ID: {process.pid}")
        
        # 等待子进程完成
        print("等待测试脚本执行...")
        stdout, stderr = process.communicate(timeout=10)
        
        print(f"\n测试脚本执行结果:")
        print(f"返回码: {process.returncode}")
        print(f"标准输出:\n{stdout}")
        print(f"错误输出:\n{stderr}")
        
        # 清理测试脚本
        if os.path.exists(test_spider_path):
            os.remove(test_spider_path)
            print(f"已删除测试脚本: {test_spider_path}")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("开始测试爬虫执行环境...")
    test_spider_execution()
    print("测试完成")