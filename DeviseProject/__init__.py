import pymysql
# 使用 PyMySQL 作为 MySQLdb
pymysql.install_as_MySQLdb()

# 兼容 Django 4.2 对 mysqlclient 版本检查：
# Django 会检查 MySQLdb.__version__ 是否 >= 1.4.3
# 这里将 PyMySQL 的别名模块版本号提升以通过检查
try:
    import MySQLdb  # 此时实际为 PyMySQL 的别名
    # 设置版本信息以满足 Django 检查
    MySQLdb.__version__ = "1.4.6"
    MySQLdb.version_info = (1, 4, 6, "final", 0)
except Exception:
    # 如果别名未生效，保持静默，后续启动时会报错提示
    pass
