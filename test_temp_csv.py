import os
import csv

# 打印文件路径信息
current_dir = os.getcwd()
print(f"当前工作目录: {current_dir}")

# 检查并打印temp.csv的可能路径
temp_csv_path1 = os.path.join(os.getcwd(), 'temp.csv')
temp_csv_path2 = os.path.join(os.getcwd(), 'spiderMan', 'temp.csv')

print(f"路径1: {temp_csv_path1}, 是否存在: {os.path.exists(temp_csv_path1)}")
print(f"路径2: {temp_csv_path2}, 是否存在: {os.path.exists(temp_csv_path2)}")

# 尝试读取文件行数
if os.path.exists(temp_csv_path2):
    with open(temp_csv_path2, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"文件行数: {len(lines)}")
        print(f"前5行内容:\n{''.join(lines[:5])}")

print("\n开始清空文件...")

# 清空文件
with open(temp_csv_path2, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["brand", "carName", "carImg", "saleVolume", "price", "manufacturer", "rank", "carModel", "energyType",
                    "marketTime", "insure"])

print("文件已清空")

# 验证文件是否被清空
with open(temp_csv_path2, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"清空后的文件行数: {len(lines)}")
    print(f"清空后的内容:\n{''.join(lines)}")