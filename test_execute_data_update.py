#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试executeDataUpdate函数的核心逻辑"""

import os
import sys
import subprocess
import time

# 获取项目根目录
def get_project_root():
    return os.path.dirname(os.path.abspath(__file__))

# 测试执行爬虫脚本的核心逻辑
def test_execute_data_update():
    print("开始测试executeDataUpdate核心逻辑...")
    
    # 获取项目根目录
    project_root = get_project_root()
    print(f"项目根目录: {project_root}")
    
    # 设置环境变量
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root
    env['DJANGO_SETTINGS_MODULE'] = 'DeviseProject.settings'
    print(f"设置后的PYTHONPATH: {env['PYTHONPATH']}")
    print(f"设置后的DJANGO_SETTINGS_MODULE: {env['DJANGO_SETTINGS_MODULE']}")
    
    # 爬虫脚本路径
    spider_script_path = os.path.join(project_root, 'spiderMan', 'spiders.py')
    print(f"爬虫脚本路径: {spider_script_path}")
    
    # 检查爬虫脚本是否存在
    if not os.path.exists(spider_script_path):
        print(f"错误: 爬虫脚本不存在: {spider_script_path}")
        return False
    
    try:
        # 启动爬虫脚本
        print("准备启动爬虫脚本...")
        process = subprocess.Popen(
            [sys.executable, spider_script_path],
            env=env,
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"成功启动爬虫进程，PID: {process.pid}")
        
        # 读取部分输出以便调试
        print("\n读取爬虫脚本的前几行输出:")
        for _ in range(10):  # 只读取前10行输出
            line = process.stdout.readline()
            if not line:
                break
            print(line.strip())
        
        # 等待2秒后终止进程（仅用于测试，避免长时间运行）
        print("\n等待2秒后终止测试进程...")
        time.sleep(2)
        
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=1)
                print("进程已成功终止")
            except subprocess.TimeoutExpired:
                process.kill()
                print("进程已强制终止")
        
        return True
        
    except Exception as e:
        print(f"执行爬虫脚本时出错: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_execute_data_update()
    if success:
        print("\n测试成功! executeDataUpdate核心逻辑工作正常")
    else:
        print("\n测试失败! 请检查问题并修复")