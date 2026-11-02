# 车辆大屏可视化项目部署说明

## 1. 项目概览

本项目是一个基于 Django + Vue + ECharts/DataV 的汽车数据大屏展示系统，主要用于展示：

- 汽车销量与品牌排行
- 车型分布与能源结构
- 价格区间与平均售价
- 热门品牌和车型概览
- 大屏可视化展示效果

项目整体架构包括：

- 前端：Vue.js + ECharts + DataV
- 后端：Python + Django
- 数据库：MySQL
- 数据采集：Python 爬虫
- 部署：Nginx + Gunicorn

---

## 2. 运行环境要求

### 2.1 服务器环境

建议使用以下环境：

- Ubuntu 20.04 / 22.04 LTS
- 或 CentOS 7 / 8
- CPU：至少 2 核
- 内存：至少 4 GB
- 磁盘：至少 50 GB SSD
- 带宽：至少 5 Mbps

### 2.2 本地开发环境

- Node.js 14+
- npm / yarn
- Python 3.8+
- Git
- MySQL 5.7+
- SSH 客户端

---

## 3. 服务器初始化

### 3.1 连接服务器

```bash
ssh root@你的服务器IP
```

### 3.2 更新系统包

Ubuntu / Debian：

```bash
sudo apt update && sudo apt upgrade -y
```

CentOS：

```bash
sudo yum update -y
```

### 3.3 安装基础软件

Ubuntu / Debian：

```bash
sudo apt install -y curl wget git vim nginx mysql-server python3-pip nodejs npm
```

CentOS：

```bash
sudo yum install -y curl wget git vim nginx mysql-server python3-pip nodejs npm
```

### 3.4 启动 MySQL

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 3.5 初始化数据库

```bash
sudo mysql -u root -p
```

在 MySQL 中执行：

```sql
CREATE DATABASE carData CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'cardata_user'@'localhost' IDENTIFIED BY '你的强密码';
GRANT ALL PRIVILEGES ON carData.* TO 'cardata_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 4. 项目拉取与目录准备

### 4.1 拉取代码

```bash
mkdir -p /var/www
cd /var/www
git clone https://github.com/你的用户名/DeviseProject.git
cd DeviseProject
```

### 4.2 查看项目结构

```bash
ls -la
```

常见目录说明：

```text
DeviseProject/
├── big-screen-vue-datav-master/   # 前端项目
├── myApp/                         # Django 应用
├── spiderMan/                     # 爬虫脚本
��── manage.py                      # Django 管理入口
├── requirements.txt               # Python 依赖
├── static/                        # 静态文件
├── templates/                     # 模板目录
├── README.md                      # 项目说明
└── ...
```

---

## 5. 后端部署（Django）

### 5.1 创建 Python 虚拟环境

```bash
cd /var/www/DeviseProject
python3 -m venv venv
source venv/bin/activate
```

### 5.2 安装 Python 依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

如果项目中有 Django 等依赖未安装，确保安装完整。

### 5.3 配置 Django 项目

打开项目的 settings 文件，确认以下配置：

```python
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'carData',
        'USER': 'cardata_user',
        'PASSWORD': '你的强密码',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

ALLOWED_HOSTS = ['你的服务器IP', 'localhost', '127.0.0.1']
```

如果项目中使用了 PyMySQL，需要在 Django 项目的 `__init__.py` 中加入：

```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 5.4 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5.5 收集静态文件

```bash
python manage.py collectstatic --noinput
```

---

## 6. 前端部署（Vue）

### 6.1 进入前端目录

```bash
cd /var/www/DeviseProject/big-screen-vue-datav-master
```

### 6.2 安装依赖并打包

```bash
npm install
npm run build
```

构建完成后，通常会生成 `dist/` 目录。

### 6.3 复制静态资源到 Nginx 目录

```bash
sudo mkdir -p /var/www/vueapp
sudo cp -r dist/* /var/www/vueapp/
sudo chown -R www-data:www-data /var/www/vueapp
```

---

## 7. Gunicorn 部署

### 7.1 安装 Gunicorn

```bash
source /var/www/DeviseProject/venv/bin/activate
pip install gunicorn
```

### 7.2 测试是否能启动

```bash
cd /var/www/DeviseProject
gunicorn --bind 0.0.0.0:8000 project_name.wsgi:application
```

注意：将 `project_name` 替换成你的 Django 项目名。

### 7.3 创建 systemd 服务

```bash
sudo vim /etc/systemd/system/gunicorn.service
```

内容示例如下：

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/DeviseProject
ExecStart=/var/www/DeviseProject/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/DeviseProject/project_name.sock project_name.wsgi:application

[Install]
WantedBy=multi-user.target
```

请将：

- `project_name` 替换为你的实际 Django 项目名称
- 工作目录和 sock 路径按实际情况调整

### 7.4 启动 Gunicorn

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

---

## 8. Nginx 配置

### 8.1 创建站点配置

```bash
sudo vim /etc/nginx/sites-available/your_domain.conf
```

示例配置：

```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your_domain.com www.your_domain.com;

    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    root /var/www/vueapp;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://unix:/var/www/DeviseProject/project_name.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 8.2 启用站点

```bash
sudo ln -s /etc/nginx/sites-available/your_domain.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 9. SSL 证书配置（可选）

### 9.1 安装 Certbot

Ubuntu / Debian：

```bash
sudo apt install certbot python3-certbot-nginx -y
```

CentOS：

```bash
sudo yum install certbot python3-certbot-nginx -y
```

### 9.2 申请证书

```bash
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

### 9.3 测试自动续期

```bash
sudo certbot renew --dry-run
```

---

## 10. 启动所有服务

```bash
sudo systemctl start mysql
sudo systemctl start gunicorn
sudo systemctl start nginx
sudo systemctl enable mysql gunicorn nginx
```

---

## 11. 验证部署结果

### 11.1 前端访问

```text
https://your_domain.com
```

### 11.2 API 访问

```text
https://your_domain.com/api/center
```

### 11.3 查看服务状态

```bash
sudo systemctl status nginx gunicorn mysql
```

### 11.4 查看日志

```bash
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/error.log
```

---

## 12. 常见问题排查

### 12.1 端口占用

```bash
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443
sudo kill -9 PID
```

### 12.2 Nginx 配置错误

```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

### 12.3 Django 启动失败

```bash
cd /var/www/DeviseProject
source venv/bin/activate
python manage.py check
```

### 12.4 MySQL 连接失败

检查以下内容：

- MySQL 是否启动
- 数据库名、用户名、密码是否正确
- Django settings 中的 HOST / PORT / charset 是否配置正确

### 12.5 静态资源无法加载

```bash
sudo chown -R www-data:www-data /var/www/vueapp
sudo chmod -R 755 /var/www/vueapp
```

---

## 13. 部署完成检查清单

- [ ] 服务器环境准备完成
- [ ] MySQL 数据库已创建
- [ ] Django 依赖已安装
- [ ] 数据库迁移成功
- [ ] Vue 前端已构建并部署
- [ ] Gunicorn 已启动并正常运行
- [ ] Nginx 已配置站点并开启 HTTPS
- [ ] 域名访问正常
- [ ] API 接口返回正常
- [ ] 日志可查看，服务状态正常

---

## 14. 说明

本说明文档用于指导本项目在 Linux 服务器上的部署与运行，适用于：

- 本地开发测试
- 线上演示环境
- 生产部署环境

在真实部署中，仍需根据服务器环境、域名、证书和网络条件进行适当调整。

如果后续需要进行二次开发或功能扩展，建议优先维护以下几个关键点：

- Django settings 中的数据库与主机配置
- 前端接口地址统一管理
- Nginx 站点配置的反向代理规则
- Gunicorn 进程管理与日志监控

---

此文档可作为本项目的部署说明书，适合直接放置在仓库根目录作为 README 使用。
