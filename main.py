import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from datetime import datetime


class DataAnalysis:
    def __init__(self):
        # 数据库连接
        self.engine = create_engine("mysql+pymysql://root:1wzhdxtx@localhost:3306/test?charset=utf8mb4")

        # 加载客户管理数据
        self.client_df = pd.read_sql("SELECT * FROM client_record", self.engine)
        self.client_df.dropna(subset=['qr_code', 'channel_name','status'], inplace=True)
        self.client_df.drop_duplicates(subset=['qr_code'], inplace=True)

        # 加载游玩管理数据
        self.game_df = pd.read_sql("SELECT * FROM game_record", self.engine)
        self.game_df.dropna(subset=['script_name', 'game_start'], inplace=True)

        # 加载游戏通关时长数据
        self.stagetime_df = pd.read_sql("SELECT * FROM stagetime_record", self.engine)


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
        # 除去未使用的二维码
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

    # 按时间统计各剧本游玩次数
    def plot_script_play_trend(self, freq='D'):

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
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    # 统计一天中各时间段的玩家
    def plot_script_play_by_hour(self):

        df = self.game_df.copy()
        df['game_start'] = pd.to_datetime(df['game_start'])
        df['hour'] = df['game_start'].dt.hour

        # 按小时和剧本名称分组计数
        grouped = df.groupby(['hour', 'script_name']).size().unstack(fill_value=0)

        grouped.plot(kind='line', marker='o', figsize=(12, 6))
        plt.title("各剧本一天24小时游玩次数统计")
        plt.xlabel("小时（从0到23）")
        plt.ylabel("游玩次数")
        plt.xticks(range(24))
        plt.grid(True)
        plt.legend(title="剧本")
        plt.tight_layout()
        plt.show()



if __name__ == '__main__':
    da = DataAnalysis()
    da.plot_channel_registration_trend()
    da.plot_script_play_trend()
    da.pie_script_play_trend()
    da.plot_script_play_by_hour()

