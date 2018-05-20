# _*_  coding: utf-8 _*_

"""
FieldAnalyzer: 用于2d比赛数据的分析
Copyright (C) 2018 YangZheng
"""

import pandas as pd
import math


class FieldAnalyzer(object):
    def __init__(self, data):
        """
        :param data: csv数据集
        """
        self.data = data
        self.left_team = data.iloc[1, :]['team_name']
        self.right_team = data.iloc[12, :]['team_name']
        self.left_data = data[data['team_name'] == self.left_team]
        self.right_data = data[data['team_name'] == self.right_team]
        self.kick_data = data[data['kick'].notnull()]

    def ballPos(self, cycle):
        """
        :param cycle:
        :return: 返回该周期球的x、y坐标
        """
        return self.data[self.data['cycle'] == cycle].iloc[0, 3:5]

    def playerPos(self, cycle, team_name, unum):
        d1 = self.data[self.data['cycle'] == cycle]
        d2 = d1[d1['team_name'] == team_name]
        pos = float(d2[d2['player_num'] == unum]['player_x']),\
              float(d2[d2['player_num'] == unum]['player_y'])
        return pos

    def isBallOutside(self, cycle):
        """
        判断该周期球是否出界
        :param cycle:
        :return:
        """
        ball_x = self.ballPos(cycle)[0]
        ball_y = self.ballPos(cycle)[1]

        if ball_x >= 52.5 or ball_x <= -52.5 or ball_y >= 34.0 or ball_y <= -34.0:
            return True
        elif math.fabs(ball_x) == 51.5 and math.fabs(ball_y) == 33:
            return True
        elif math.fabs(ball_x) == 47.0 and math.fabs(ball_y) == 9.0:    # TODO: 待确认
            return True
        else:
            return False

    def ourDefenseLineX(self, cycle):
        cycle_data = self.left_data[self.left_data['cycle'] == cycle].iloc[1:, :]
        return cycle_data['player_x'].min()

    def ourOffenseLineX(self, cycle):
        cycle_data = self.left_data[self.left_data['cycle'] == cycle].iloc[1:, :]
        return cycle_data['player_x'].max()

    def theirDefenseLineX(self, cycle):
        cycle_data = self.right_data[self.right_data['cycle'] == cycle].iloc[1:, :]
        return cycle_data['player_x'].max()

    def theirOffenseLineX(self, cycle):
        cycle_data = self.right_data[self.right_data['cycle'] == cycle].iloc[1:, :]
        return cycle_data['player_x'].min()

    def existKickableOpponent(self, cycle):
        dist_OppToBall = self.getDistOpponentNearestToBall(cycle, True)
        dist_MateToBall = self.getDistTeammateNearestToBall(cycle, True)
        if(dist_MateToBall > dist_OppToBall and dist_OppToBall < 1.5):
            return True
        else:
            return False

    def existKickableTeammate(self, cycle):
        dist_OppToBall = self.getDistOpponentNearestToBall(cycle, True)
        dist_MateToBall = self.getDistTeammateNearestToBall(cycle, True)
        if(dist_MateToBall < dist_OppToBall and dist_MateToBall < 1.5):
            return True
        else:
            return False

    def getDistTeammateNearestToBall(self, cycle, with_goalie=True):
        cycle_data = self.left_data[self.left_data['cycle'] == cycle]
        ball = [cycle_data['ball_x'], cycle_data['ball_y']]
        return self.getDistNearestTo(cycle_data, with_goalie, ball)

    def getDistOpponentNearestToBall(self, cycle, with_goalie=False):
        cycle_data = self.right_data[self.right_data['cycle'] == cycle]
        ball = [cycle_data['ball_x'], cycle_data['ball_y']]
        return self.getDistNearestTo(cycle_data, with_goalie, ball)

    def getDistNearestTo(self, data, with_goalie, point):
        """
        :param cycle_data: 指定周期的数据
        :param with_goalie: 是否包含守门员
        :param point: 指定的点，点的x和y坐标组成的数组
        :return: 最近的距离
        """
        cycle_data = data if with_goalie else data.iloc[1:, :]
        d2 = (point[0] - cycle_data['player_x']) ** 2 + (point[1] - cycle_data['player_y']) ** 2
        d = d2.apply(lambda x: math.sqrt(x))
        return d.min()

    def lastKickerSide(self, cycle):
        """
        :param cycle:
        :return: 返回该周期前踢球的周期和球队名
        """
        """
        TODO:
            怎么过滤掉无效kick的数据？
        """
        # kick_data = self.data[self.data['kick'].notnull() | self.data['tackle'].notnull()]
        try:
            last_kick = self.kick_data[self.kick_data['cycle'] < cycle].iloc[-1, :]
        except:
            return 0, 'None', 1
        return last_kick['cycle'] + 1, last_kick['team_name'], last_kick['player_num']

    def nextKickerSide(self, cycle):
        """
        :param cycle:
        :return: 返回该周期后踢球的周期和球队名
        """
        """
        TODO:
            怎么过滤掉无效kick的数据？
        """
        # kick_data = self.data[self.data['kick'].notnull() | self.data['tackle'].notnull()]
        try:
            next_kick = self.kick_data[self.kick_data['cycle'] > cycle].iloc[0, :]
        except:
            return 6000, 'None', 1
        return next_kick['cycle'] + 1, next_kick['team_name'], next_kick['player_num']


if __name__ == '__main__':
    data = pd.read_csv('../csv/20180504161434-MT2018_2-vs-YuShan2018_0.csv')
    field_analyzer = FieldAnalyzer(data)

