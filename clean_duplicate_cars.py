import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DeviseProject.settings')
django.setup()

from django.db import connection, transaction

def clean_duplicate_records():
    print("=== 清理allcarinfo表中的重复记录 ===")
    print("注意：此操作将删除重复记录，保留每组中最早创建的记录！")
    
    # 在事务中执行删除操作
    with transaction.atomic():
        # 1. 创建临时表，存储每组重复记录中要保留的最小ID
        with connection.cursor() as cursor:
            print("创建临时表存储要保留的记录ID...")
            
            # 首先删除可能存在的临时表
            cursor.execute("DROP TABLE IF EXISTS temp_keep_ids")
            
            # 创建临时表
            cursor.execute("""
                CREATE TABLE temp_keep_ids AS
                SELECT MIN(id) as keep_id
                FROM allcarinfo
                GROUP BY brand, carName, carModel
            """)
            
            # 2. 统计将要删除的记录数
            cursor.execute("""
                SELECT COUNT(*) 
                FROM allcarinfo 
                WHERE id NOT IN (SELECT keep_id FROM temp_keep_ids)
            """)
            records_to_delete = cursor.fetchone()[0]
            
            print(f"将删除 {records_to_delete} 条重复记录")
            
            # 3. 执行删除操作
            if records_to_delete > 0:
                print("开始删除重复记录...")
                cursor.execute("""
                    DELETE FROM allcarinfo 
                    WHERE id NOT IN (SELECT keep_id FROM temp_keep_ids)
                """)
                deleted_count = cursor.rowcount
                print(f"成功删除 {deleted_count} 条重复记录")
            else:
                print("没有找到需要删除的重复记录")
            
            # 4. 清理临时表
            cursor.execute("DROP TABLE IF EXISTS temp_keep_ids")
            
            # 5. 验证清理结果
            cursor.execute("""
                SELECT COUNT(*)
                FROM (
                    SELECT brand, carName, carModel, COUNT(*) as count
                    FROM allcarinfo
                    GROUP BY brand, carName, carModel
                    HAVING COUNT(*) > 1
                ) as duplicates
            """)
            remaining_duplicates = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM allcarinfo")
            final_count = cursor.fetchone()[0]
            
            print(f"\n清理完成后:")
            print(f"- 剩余记录总数: {final_count}")
            print(f"- 剩余重复组数: {remaining_duplicates}")
            
            if remaining_duplicates == 0:
                print("✓ 清理成功！所有重复记录已移除")
            else:
                print("! 仍有重复记录存在，请检查")

if __name__ == "__main__":
    # 检查命令行参数
    auto_confirm = len(sys.argv) > 1 and sys.argv[1] == '--auto-confirm'
    
    if auto_confirm:
        print("通过命令行参数自动确认清理操作")
        clean_duplicate_records()
    else:
        confirm = input("确定要清理allcarinfo表中的重复记录吗？(y/n): ")
        if confirm.lower() == 'y':
            clean_duplicate_records()
        else:
            print("操作已取消")