# # # Columns: [id, player_id, player_name, script_name, game_start, game_end, score, qr_code]

# # import pandas as pd
# # from sqlalchemy import create_engine
# #
# # engine = create_engine("mysql+pymysql://root:1wzhdxtx@localhost:3306/test?charset=utf8mb4")
# #
# # # 新增 client_record 数据
# # client_data = pd.DataFrame([
# #     ('QR003', '小红书', '2024-06-02'),
# #     ('QR004', '抖音', '2024-06-03'),
# #     ('QR005', '微博', '2024-06-03'),
# #     ('QR006', '公众号', '2024-06-04'),
# #     ('QR007', '抖音', '2024-06-04'),
# #     ('QR008', '小红书', '2024-06-05'),
# # ], columns=['qr_code', 'channel_name', 'create_time'])
# #
# # client_data.to_sql('client_record', con=engine, if_exists='append', index=False)
# #
# # # 新增 game_record 数据
# # game_data = pd.DataFrame([
# #     ('剧本杀-迷雾森林', '2024-06-02 15:30:00'),
# #     ('剧本杀-时间牢笼', '2024-06-03 19:00:00'),
# #     ('剧本杀-深海迷踪', '2024-06-04 14:00:00'),
# #     ('剧本杀-迷雾森林', '2024-06-04 20:00:00'),
# #     ('剧本杀-时间牢笼', '2024-06-05 18:30:00'),
# #     ('剧本杀-深海迷踪', '2024-06-06 16:00:00'),
# # ], columns=['script_name', 'game_start'])
# #
# # game_data.to_sql('game_record', con=engine, if_exists='append', index=False)
# import pandas as pd
# import random
# from datetime import datetime, timedelta
# from sqlalchemy import create_engine
#
# # 配置数据库连接
# engine = create_engine("mysql+pymysql://root:1wzhdxtx@localhost:3306/test?charset=utf8mb4")
#
# # 模拟渠道和剧本名
# channels = ['公众号', '小红书', '抖音', '微博']
# scripts = ['剧本杀-迷雾森林', '剧本杀-时间牢笼', '剧本杀-深海迷踪', '剧本杀-极寒追凶']
#
# # 当前日期作为基准
# start_date = datetime.strptime("2024-06-01", "%Y-%m-%d")
#
# # ---------- 模拟 100 条 client_record ----------
# client_data = []
# for i in range(10000):
#     qr_code = f'QR{1000 + i}'
#     channel = random.choice(channels)
#     days_offset = random.randint(0, 10)  # 模拟 10 天之内的注册
#     reg_date = start_date + timedelta(days=days_offset)
#     client_data.append((qr_code, channel, reg_date.strftime("%Y-%m-%d")))
#
# client_df = pd.DataFrame(client_data, columns=['qr_code', 'channel_name', 'create_time'])
# client_df.to_sql('client_record', con=engine, if_exists='append', index=False)
# print("✅ 成功写入 100 条 client_record 数据")
#
# # ---------- 模拟 100 条 game_record ----------
# game_data = []
# # for i in range(10000):
# #     script = random.choice(scripts)
# #     days_offset = random.randint(0, 10)
# #     hours = random.randint(10, 22)
# #     minutes = random.choice([0, 15, 30, 45])
# #     game_datetime = start_date + timedelta(days=days_offset, hours=hours, minutes=minutes)
# #     game_data.append((script, game_datetime.strftime("%Y-%m-%d %H:%M:%S")))
# #
# # game_df = pd.DataFrame(game_data, columns=['script_name', 'game_start'])
# # game_df.to_sql('game_record', con=engine, if_exists='append', index=False)
# # print("✅ 成功写入 100 条 game_record 数据")
import random
import pymysql
from faker import Faker

# 初始化
fake = Faker('zh_CN')
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1wzhdxtx',
    database='test',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 可选剧本和渠道
scripts = ['剧本杀-迷雾森林', '剧本杀-时间牢笼', '剧本杀-幻影追凶', '剧本杀-遗失真相']
channels = ['公众号', '抖音', '小红书', '线下推广']
statuses = ['使用', '未使用']

# 插入模拟数据
for i in range(10000):
    qr_code = f"QR{1000 + i}"
    script_name = random.choice(scripts)
    channel_name = random.choice(channels)
    status = random.choice(statuses)
    image_url = f"http://example.com/images/{qr_code}.png"
    remark = fake.sentence(nb_words=6)
    operation = "无"

    sql = """
        INSERT INTO client_record 
        (qr_code, script_name, channel_name, status, image_url, remark, operation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (qr_code, script_name, channel_name, status, image_url, remark, operation))

# 提交并关闭
conn.commit()
cursor.close()
conn.close()

print("✅ 成功插入 100 条模拟数据。")
import random
from datetime import datetime, timedelta
import pymysql
from faker import Faker

# 初始化
fake = Faker('zh_CN')
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1wzhdxtx',
    database='test',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 假定存在的二维码编号（应与 client_record 中的相同）
qr_codes = [f"QR{1000 + i}" for i in range(10000)]

# 剧本列表
scripts = ['剧本杀-迷雾森林', '剧本杀-时间牢笼', '剧本杀-幻影追凶', '剧本杀-遗失真相']

# 插入 100 条模拟数据
for i in range(100):
    player_id = 1000 + i
    player_name = fake.name()
    script_name = random.choice(scripts)

    # 随机生成时间（过去一个月内）
    start_time = fake.date_time_between(start_date='-30d', end_date='now')
    end_time = start_time + timedelta(hours=random.randint(1, 3))

    score = random.randint(50, 100)
    qr_code = random.choice(qr_codes)

    sql = """
        INSERT INTO game_record 
        (player_id, player_name, script_name, game_start, game_end, score, qr_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (player_id, player_name, script_name, start_time, end_time, score, qr_code))

# 提交并关闭
conn.commit()
cursor.close()
conn.close()

print("✅ 成功插入 100 条游戏记录模拟数据。")

