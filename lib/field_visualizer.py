# _*_  coding: utf8 _*_

"""
field_visualizer: 用于日志数据的可视化展示
Copyright (C) 2018 YangZheng
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pandas as pd
import matplotlib.pyplot as plt

"""
注： 球场的Y坐标方向与2d中的Y坐标方向相反
"""


class FieldVisualizer(object):

    def __init__(self, data):
        """
        :param data: csv数据集
        """
        self.data = data
        self.left_team = self.data.iloc[1, :]['team_name']
        self.right_team = self.data.iloc[12, :]['team_name']
        self.left_data = self.data[self.data['team_name'] == self.left_team]
        self.right_data = self.data[self.data['team_name'] == self.right_team]

    def init(self):
        """
        使用matplotlib绘制球场
        :return: ax
        """
        # set size
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))

        # Sets up limits
        plt.xlim(-56.5, 56.5)
        plt.ylim(-38, 38)

        ax.set_xticks([-52.5, -36, -20, 0, 20, 36, 52.5])
        ax.set_yticks([34, 20, 7, 0, -7, -20, -34])

        # Draws field
        ax.plot([-52.5, -52.5], [-34, 34], color="k", linestyle="-", linewidth=1)
        ax.plot([52.5, 52.5], [-34, 34], color="k", linewidth=1)
        ax.plot([52.5, -52.5], [-34, -34], color="k", linewidth=1)
        ax.plot([52.5, -52.5], [34, 34], color="k", linewidth=1)
        ax.plot([0, 0], [34, -34], color="k", linewidth=0.5)

        # their penalty area
        ax.plot([36, 52.5], [-20, -20], color="k", linewidth=0.5)
        ax.plot([36, 52.5], [20, 20], color="k", linewidth=0.5)
        ax.plot([36, 36], [-20, 20], color="k", linewidth=0.5)
        # their goal
        ax.plot([52.5, 52.5], [7, -7], color='k', linewidth=1.0)
        ax.plot([54.5, 52.5], [7, 7], color='k', linewidth=1.0)
        ax.plot([54.5, 52.5], [-7, -7], color='k', linewidth=1.0)
        ax.plot([54.5, 54.5], [7, -7], color='k', linewidth=1.0)

        # our penalty area
        ax.plot([-36, -52.5], [-20, -20], color="k", linewidth=0.5)
        ax.plot([-36, -52.5], [20, 20], color="k", linewidth=0.5)
        ax.plot([-36, -36], [-20, 20], color="k", linewidth=0.5)
        # our goal
        ax.plot([-52.5, -52.5], [7, -7], color='k', linewidth=1.0)
        ax.plot([-54.5, -52.5], [7, 7], color='k', linewidth=1.0)
        ax.plot([-54.5, -52.5], [-7, -7], color='k', linewidth=1.0)
        ax.plot([-54.5, -54.5], [7, -7], color='k', linewidth=1.0)

        # Write teams' name
        # self.ax.text(-55, 4, left_team, color="k", rotation="vertical")
        # self.ax.text(53.5, 4, right_team, color="k", rotation="vertical")

        # set title
        plt.title(self.left_team + ' vs ' + self.right_team)
        return ax

    def showBallTrace(self):
        """
        显示整场比赛球的轨迹
        :return:
        """
        ax = self.init()

        ball_x = self.data['ball_x']
        ball_y = self.data['ball_y']
        ax.plot(ball_x, ball_y, color="r", linewidth=0.5, linestyle="-", alpha=1)
        plt.show()

    def showOurPlayerTrace(self, unum1=0, unum2=0):
        """
        显示左方球员整场比赛运动轨迹
        :param unum1:
        :param unum2:
        :return:
        """
        ax = self.init()

        player1_x = self.left_data[self.left_data['player_num'] == unum1]['player_x']
        player1_y = self.left_data[self.left_data['player_num'] == unum1]['player_y']
        ax.plot(player1_x, player1_y, color="r", linewidth=0.5, label='{}_{}'.format(self.left_team, str(unum1)))

        if unum2 != 0:
            player2_x = self.left_data[self.left_data['player_num'] == unum2]['player_x']
            player2_y = self.left_data[self.left_data['player_num'] == unum2]['player_y']
            ax.plot(player2_x, player2_y, color="b", linewidth=0.5, label='{}_{}'.format(self.left_team, str(unum2)))

        ax.legend(loc='upper left')
        plt.show()

    def showTheirPlayerTrace(self, unum1=0, unum2=0):
        """
        显示右方球员整场比赛运动轨迹
        :param unum1:
        :param unum2:
        :return:
        """
        ax = self.init()

        player1_x = self.right_data[self.right_data['player_num'] == unum1]['player_x']
        player1_y = self.right_data[self.right_data['player_num'] == unum1]['player_y']
        ax.plot(player1_x, player1_y, color='r', linewidth=0.5, label='{}_{}'.format(self.right_team, str(unum1)))

        if unum2 != 0:
            player2_x = self.right_data[self.right_data['player_num'] == unum2]['player_x']
            player2_y = self.right_data[self.right_data['player_num'] == unum2]['player_y']
            ax.plot(player2_x, player2_y, color='b', linewidth=0.5, label='{}_{}'.format(self.right_team, str(unum2)))

        ax.legend(loc='upper left')
        plt.show()

    def showKickLine(self):
        ax = self.init()
        left_kick = self.left_data[self.left_data['kick'].notnull()]
        right_kick = self.right_data[self.right_data['kick'].notnull()]

        ax.plot(left_kick['ball_x'], left_kick['ball_y'], marker='.', alpha=0.3, color='r', label=self.left_team)
        ax.plot(right_kick['ball_x'], right_kick['ball_y'], marker='.', alpha=0.3, color='b', label=self.right_team)

        ax.legend(loc='upper left')
        plt.show()


if __name__ == '__main__':
    data = pd.read_csv('../csv/20180504161434-MT2018_2-vs-YuShan2018_0.csv')

    # FieldVisualizer(data).init()
    # plt.show()

    FieldVisualizer(data).showBallTrace()
    FieldVisualizer(data).showOurPlayerTrace(11)
    FieldVisualizer(data).showOurPlayerTrace(9, 10)
    FieldVisualizer(data).showTheirPlayerTrace(9, 10)
    FieldVisualizer(data).showKickLine()
