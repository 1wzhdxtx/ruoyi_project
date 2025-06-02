# import pandas as pd
# from sqlalchemy import create_engine
#
# # 数据库连接信息
# engine = create_engine("mysql+pymysql://root:1wzhdxtx@localhost:3306/test?charset=utf8mb4")
#
# # 读取游戏记录表
# df = pd.read_sql("SELECT * FROM client_record", engine)
#
# # 显示前几行数据
# print(df.head())
import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1wzhdxtx',
    database='test',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 执行更新语句
cursor.execute("UPDATE client_record SET status = '使用' WHERE status = '启用'")
cursor.execute("UPDATE client_record SET status = '未使用' WHERE status = '未启用'")

# 提交更改
conn.commit()

# 关闭连接
cursor.close()
conn.close()



