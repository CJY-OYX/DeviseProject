import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== 分析allcarinfo表中的重复记录 ===")

# 1. 查询总记录数
cursor.execute("SELECT COUNT(*) FROM allcarinfo")
total_count = cursor.fetchone()[0]
print(f"总记录数: {total_count}")

# 2. 查询基于品牌、车名、车型的重复记录
print("\n重复记录分析（基于品牌+车名+车型）:")
cursor.execute("""
    SELECT brand, carName, carModel, COUNT(*) as duplicate_count
    FROM allcarinfo
    GROUP BY brand, carName, carModel
    HAVING COUNT(*) > 1
    ORDER BY duplicate_count DESC
""")
duplicate_records = cursor.fetchall()

if duplicate_records:
    print(f"找到 {len(duplicate_records)} 组重复记录:")
    for record in duplicate_records[:10]:  # 只显示前10组
        print(f"品牌: {record[0]}, 车名: {record[1]}, 车型: {record[2]}, 重复次数: {record[3]}")
    
    if len(duplicate_records) > 10:
        print(f"... 还有 {len(duplicate_records) - 10} 组重复记录未显示")
else:
    print("没有找到重复记录")

# 3. 计算预计可去重的记录数
total_duplicates = sum(record[3] - 1 for record in duplicate_records)
print(f"\n预计可清理的重复记录数: {total_duplicates}")
print(f"清理后预计剩余记录数: {total_count - total_duplicates}")

# 4. 显示一些重复记录的详细信息作为示例
if duplicate_records:
    brand, carName, carModel, _ = duplicate_records[0]
    print(f"\n第一组重复记录详情（品牌: {brand}, 车名: {carName}, 车型: {carModel}）:")
    cursor.execute("""
        SELECT id, brand, carName, carModel, price, creteTime
        FROM allcarinfo
        WHERE brand = ? AND carName = ? AND carModel = ?
        ORDER BY creteTime
    """, (brand, carName, carModel))
    
    details = cursor.fetchall()
    for detail in details:
        print(f"ID: {detail[0]}, 价格: {detail[4]}, 创建时间: {detail[5]}")

# 关闭数据库连接
conn.close()