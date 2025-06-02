# 写的代码来模拟数据产生
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

print("成功插入 10000 条模拟数据。")
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
for i in range(10000):
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

print(" 成功插入 10000 条游戏记录模拟数据。")

# 我自己建的模拟数据库的列名
# mysql> DESCRIBE client_record;
# +--------------+--------------+------+-----+---------+----------------+
# | Field        | Type         | Null | Key | Default | Extra          |
# +--------------+--------------+------+-----+---------+----------------+
# | id           | int          | NO   | PRI | NULL    | auto_increment |
# | qr_code      | varchar(100) | NO   |     | NULL    |                |
# | script_name  | varchar(100) | YES  |     | NULL    |                |
# | channel_name | varchar(100) | YES  |     | NULL    |                |
# | status       | varchar(20)  | YES  |     | 启用    |                |
# | image_url    | varchar(255) | YES  |     | NULL    |                |
# | remark       | text         | YES  |     | NULL    |                |
# | operation    | varchar(50)  | YES  |     | NULL    |                |
# | create_time  | datetime     | YES  |     | NULL    |                |
# +--------------+-------------
# +-------------+--------------+------+-----+---------+----------------+
# | Field       | Type         | Null | Key | Default | Extra          |
# +-------------+--------------+------+-----+---------+----------------+
# | id          | int          | NO   | PRI | NULL    | auto_increment |
# | player_id   | int          | YES  |     | NULL    |                |
# | player_name | varchar(50)  | YES  |     | NULL    |                |
# | script_name | varchar(100) | YES  |     | NULL    |                |
# | game_start  | datetime     | YES  |     | NULL    |                |
# | game_end    | datetime     | YES  |     | NULL    |                |
# | score       | int          | YES  |     | NULL    |                |
# | qr_code     | varchar(100) | YES  |     | NULL    |                |
# +-------------+--------------+------+-----+---------+----------------+
# 8 rows in set (0.00 sec)
