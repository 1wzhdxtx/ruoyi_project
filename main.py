import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from datetime import datetime


class DataAnalysis:
    def __init__(self):
        # 数据库连接
        self.engine = create_engine("mysql+pymysql://root:1wzhdxtx@localhost:3306/test?charset=utf8mb4")

        # 加载 client_record 数据
        self.client_df = pd.read_sql("SELECT * FROM client_record", self.engine)
        self.client_df.dropna(subset=['qr_code', 'channel_name','status'], inplace=True)
        self.client_df.drop_duplicates(subset=['qr_code'], inplace=True)

        # 加载 game_record 数据
        self.game_df = pd.read_sql("SELECT * FROM game_record", self.engine)
        self.game_df.dropna(subset=['script_name', 'game_start'], inplace=True)

        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    # 对未统计注册时间的数据虚拟时间
    def add_virtual_create_time(self):

        if 'create_time' not in self.client_df.columns or self.client_df['create_time'].isnull().all():
            # 模拟注册时间
            start_time = pd.Timestamp("2024-06-01")
            self.client_df = self.client_df.sort_values(by='qr_code').reset_index(drop=True)
            self.client_df['create_time'] = [start_time + pd.Timedelta(days=i) for i in range(len(self.client_df))]

        self.client_df['create_time'] = pd.to_datetime(self.client_df['create_time'])

    # 统计各渠道用户的折线图
    def plot_channel_registration_trend(self, freq='D'):

        self.add_virtual_create_time()
        df = self.client_df.copy()
        df_cleared = df[df['status'] != '未使用']
        df['date'] = df['create_time'].dt.to_period(freq).dt.to_timestamp()
        grouped = df.groupby(['date', 'channel_name']).size().unstack(fill_value=0)

        grouped.plot(figsize=(10, 6), marker='o')
        plt.title("各渠道随时间新增客户趋势")
        plt.xlabel("时间")
        plt.ylabel("新增客户数量")
        plt.grid(True)
        plt.legend(title="渠道")
        plt.tight_layout()
        plt.show()

    def plot_script_play_trend(self, freq='D'):
        """按时间统计各剧本游玩次数趋势（折线图）"""
        df = self.game_df.copy()
        df['game_start'] = pd.to_datetime(df['game_start'])
        df['date'] = df['game_start'].dt.to_period(freq).dt.to_timestamp()
        grouped = df.groupby(['date', 'script_name']).size().unstack(fill_value=0)

        grouped.plot(figsize=(10, 6), marker='o')
        plt.title("各剧本随时间游玩数量趋势")
        plt.xlabel("时间")
        plt.ylabel("游玩次数")
        plt.grid(True)
        plt.legend(title="剧本")
        plt.tight_layout()
        plt.show()

    def pie_script_play_trend(self):
        df = self.game_df.copy()

        # 按剧本统计次数
        grouped = df.groupby('script_name').size()

        # 绘制饼图
        plt.pie(grouped.values, labels=grouped.index, autopct='%1.1f%%', startangle=140)
        plt.title("各剧本游玩占比")
        plt.axis('equal')  # 保证饼图为圆形
        plt.tight_layout()
        plt.show()

    def plot_script_play_by_hour(self):
        """统计一天中每个小时的游玩次数（所有日期合并统计）"""
        df = self.game_df.copy()
        df['game_start'] = pd.to_datetime(df['game_start'])
        df['hour'] = df['game_start'].dt.hour  # 取小时，范围 0-23

        # 按小时和剧本名称分组计数
        grouped = df.groupby(['hour', 'script_name']).size().unstack(fill_value=0)

        grouped.plot(kind='line', marker='o', figsize=(12, 6))
        plt.title("各剧本一天24小时游玩次数统计")
        plt.xlabel("小时（0-23）")
        plt.ylabel("游玩次数")
        plt.xticks(range(24))
        plt.grid(True)
        plt.legend(title="剧本")
        plt.tight_layout()
        plt.show()


# ✅ 调用方式
if __name__ == '__main__':
    da = DataAnalysis()
    da.plot_channel_registration_trend()  # 默认按天
    da.plot_script_play_trend()
    da.pie_script_play_trend()
    da.plot_script_play_by_hour()
