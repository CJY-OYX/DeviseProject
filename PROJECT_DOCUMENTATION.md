# 汽车数据爬取与去重系统 - 项目文档

## 项目概述

本项目是一个汽车数据爬取、存储、去重和展示的完整系统，主要功能包括：

- 从懂车帝网站爬取汽车排行榜数据
- 数据存储到MySQL数据库
- 数据去重处理
- 数据可视化展示（Vue大屏展示）
- 自动定时更新机制

## 项目结构

```
DeviseProject/
├── DeviseProject/           # Django项目配置目录
│   ├── settings.py          # 项目配置（包含数据库连接等）
│   ├── urls.py              # URL路由配置
│   └── wsgi.py/asgi.py      # Web服务器网关接口
├── myApp/                   # Django主应用
│   ├── models.py            # 数据模型定义
│   ├── views.py             # API视图
│   ├── utils/               # 数据处理工具函数
│   └── migrations/          # 数据库迁移文件
├── spiderMan/               # 爬虫模块
│   ├── spiders.py           # 爬虫核心代码
│   ├── auto_update.py       # 自动更新程序
│   └── auto_update_logs.txt # 自动更新日志
├── big-screen-vue-datav-master/ # Vue前端大屏展示
├── 数据分析与去重脚本/
│   ├── analyze_duplicate_cars.py        # 重复数据分析
│   ├── clean_duplicate_cars.py          # 重复数据清理
│   ├── vehicle_data_deduplication_strategy.md     # 去重策略文档
│   └── vehicle_data_deduplication_implementation.py # 去重逻辑实现
└── manage.py                # Django管理脚本
```

## 核心模块说明

### 1. 数据模型

**主要数据表：**
- `carInfo` - 存储最新的汽车排行榜数据（定期更新覆盖）
- `AllCarInfo` - 存储所有汽车数据的历史记录（去重后添加）

### 2. 爬虫模块 (`spiderMan`)

- **spiders.py**: 包含`CarSpider`类，负责从懂车帝爬取数据并保存到CSV和数据库
- **auto_update.py**: 自动定时更新程序，每5分钟执行一次爬取和数据更新

### 3. 数据去重系统

- 基于`brand` + `carName` + `carModel`组合作为唯一标识
- 已清理`AllCarInfo`表中的重复数据（清理了99932条重复记录）
- 实现了新数据写入时的自动去重检查

### 4. 前端展示

- 使用Vue和DataV构建的数据可视化大屏
- 展示汽车销售数据、排行趋势等信息

## 最近修复和优化（2025-11-21）

### 解决的主要问题

1. **数据库连接断开问题**
   - 修复了"Server has gone away"错误
   - 优化了数据库连接管理和超时设置
   - 实现了智能重试机制

2. **数据去重实现**
   - 清理了AllCarInfo表中的大量重复数据
   - 实现了写入时的去重检查逻辑

### 具体代码改进

#### 1. 数据库配置优化 (`DeviseProject/settings.py`)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'carData',
        'USER': 'admin',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'CONN_MAX_AGE': 0,  # 不使用连接池
        'OPTIONS': {
            'connect_timeout': 10,  # 连接超时10秒
            'read_timeout': 30,     # 读取超时30秒
            'write_timeout': 30,    # 写入超时30秒
            'charset': 'utf8mb4',
            'sql_mode': 'STRICT_TRANS_TABLES',
        }
    }
}
```

#### 2. 爬虫保存逻辑改进 (`spiderMan/spiders.py`)

- 添加了事务处理 (`transaction.atomic()`)
- 实现了分批插入数据（每批50条）
- 集成了去重逻辑，避免重复写入AllCarInfo表
- 增强了错误捕获和日志记录

#### 3. 自动更新程序优化 (`spiderMan/auto_update.py`)

- 重构了代码结构，添加了全局变量管理
- 实现了Django环境动态初始化
- 添加了数据库连接重置机制
- 实现了智能重试逻辑（最多3次重试）
- 添加了测试运行模式（`--test-run`参数）
- 完善了日志记录系统

## 当前运行状态

### 正在运行的服务

1. **Django开发服务器** - 提供API接口
   - 运行命令: `python manage.py runserver`
   - 运行目录: `e:\DeviseProject`

2. **Vue开发服务器** - 前端大屏展示
   - 运行命令: `npm run serve`
   - 运行目录: `e:\DeviseProject\big-screen-vue-datav-master`
   - 访问地址: http://localhost:8080

### 待启动服务

- **自动更新服务**: 需要手动启动以实现数据定时更新
  - 启动命令: `python auto_update.py`
  - 测试命令: `python auto_update.py --test-run`
  - 运行目录: `e:\DeviseProject\spiderMan`

## 开发注意事项

1. **数据库配置**
   - MySQL数据库必须运行在localhost:3306
   - 用户名: admin，密码: 123456，数据库名: carData

2. **爬虫相关**
   - 爬虫可能需要处理网络代理问题（根据日志显示有代理连接错误）
   - 爬取频率设置为每5分钟一次，避免对目标网站造成过大压力

3. **日志文件**
   - 自动更新日志: `spiderMan/auto_update_logs.txt`
   - 注意定期清理日志文件以避免过大

4. **错误处理**
   - 系统现在有较完善的错误处理和重试机制
   - 如果遇到连接问题，系统会自动重试最多3次

## 下一步开发建议

1. 实现更完善的监控告警机制
2. 优化数据库查询性能，添加必要的索引
3. 考虑使用更稳定的定时任务框架（如Celery）替代简单的while循环
4. 完善前端展示功能，添加更多数据分析图表
5. 实现数据备份和恢复机制

## 联系方式

如有问题，请联系项目负责人。