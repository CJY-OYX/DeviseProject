# 车辆大屏可视化

> 基于 Django + Vue + ECharts/DataV 的汽车数据分析与展示平台，聚焦于汽车销量、品牌排行、车型分布、价格区间、能源结构等核心指标的可视化呈现，适用于汽车销售分析、市场运营看板和大屏展示场景。

## 项目简介

本项目是一套面向汽车行业的数据可视化解决方案，结合了前端大屏展示与后端数据处理能力。项目通过抓取、清洗和整理汽车相关数据，并利用可视化图表将数据转化为直观、易读的经营指标，帮助用户快速掌握品牌表现、车型趋势和市场结构。

该项目整体分为两部分：

- 前端：基于 Vue 2 + ECharts + DataV 构建的可视化大屏界面
- 后端：基于 Django 处理业务逻辑、接口返回和数据库交互
- 数据：利用 Python 爬虫方式采集汽车数据，并存入 MySQL

## 核心功能

- 汽车销量与销售排名展示
- 品牌占比和车型分布分析
- 价格区间与平均售价统计
- 能源类型（汽油 / 纯电动 / 混动）占比分析
- 热门车型和品牌排行榜
- 大屏式数据展示，适合会议、运营室、展厅等场景
- 支持数据动态更新和前端图表渲染

## 技术栈

- 前端：Vue.js、ECharts、DataV、SCSS
- 后端：Python、Django
- 数据库：MySQL
- 爬虫：Python + requests + lxml
- 服务器部署：Nginx + Gunicorn

## 项目结构

```text
DeviseProject/
├── big-screen-vue-datav-master/   # 前端大屏项目
├── myApp/                         # Django 应用
├── spiderMan/                     # 数据采集脚本
├── static/                        # 静态资源
├── templates/                     # 模板文件
├── manage.py                      # Django 管理入口
├── requirements.txt               # Python 依赖
├── README.md                      # 项目说明
└── ...
```

## 典型业务场景

- 汽车销售数据分析
- 品牌竞争力对比
- 新能源车型趋势看板
- 车企数据运营监控
- 数据大屏展示和汇报

## 快速开始

### 1. 环境准备

- Python 3.8+
- Node.js 14+
- MySQL 5.7+
- Nginx（生产部署）

### 2. 后端安装

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### 3. 前端安装

```bash
cd big-screen-vue-datav-master
npm install
npm run serve
```

### 4. 访问方式

- 前端：`http://localhost:8080`
- 后端接口：`http://localhost:8000`

## 部署说明

本项目原本包含较详细的云服务器部署步骤，包括：

- Ubuntu / CentOS 环境配置
- MySQL 数据库初始化
- Django + Gunicorn 部署
- Vue 前端构建与部署
- Nginx 反向代理和 HTTPS 配置
- SSL 证书和安全配置

如果你要在生产环境部署，可基于现有部署文档进一步补充实际服务器参数、域名、证书和环境变量配置。适合用于演示环境、测试环境或线上正式环境。

## 说明

这是一个适合学习和二次开发的汽车数据大屏项目，代码结构清晰，适合用来练习：

- Django 接口开发
- Vue 组件化开发
- ECharts 图表封装
- Python 爬虫与数据清洗
- 数据大屏设计与交互实现

如果你希望，我还可以继续帮你把这个 README 再优化成：

- 适合 GitHub 展示风格的版本
- 中文项目介绍 + 技术架构图版
- 企业风格/个人作品风格版本
- 含截图和功能模块说明的完整版

你也可以直接让我再生成一版“更正式、适合发到 GitHub 的 README”。
