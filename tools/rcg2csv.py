# _*_ coding: utf-8 _*_

"""
rcg2csv: Convert RoboCup Soccer Simulator rcg and rcl files to CSV.
Copyright (C) 2018 YangZheng
Data: 2018-05-04
Version： v1.0.0
Bugs or Suggestions please mail to cookie.yz@qq.com
"""

import sys
sys.path.append("../lib")
from world_model import World
import csv


"""
TODO: 
    通过配置文件的形式，选择需要生成的字段
    添加体力信息等
"""


class Rcg2csv(object):
    def __init__(self, wm):
        self.wm = wm
        self.our_name = self.wm.teamName()
        self.opp_name = self.wm.opponentTeamName()
        self.rowlist = self.getRowList()

    def getRowList(self):
        rowlist = []

        while self.wm.time().kick_off() <= self.wm.time().cycle() and self.wm.time().cycle() <= 2:
            # player_num = '{}_{}'
            """add our player row"""
            for unum in range(1, 12):
                kick = self.wm.ourPlayer(unum, wm.time().cycle()).kick()
                row = {
                    'cycle': self.wm.time().cycle(),
                    # 'player_num': player_num.format(self.our_name, unum),
                    'player_num': unum,
                    'ball_x': self.wm.ball(self.wm.time().cycle()).x,
                    'ball_y': self.wm.ball(self.wm.time().cycle()).y,
                    'ball_vx': self.wm.ball(self.wm.time().cycle()).vx,
                    'ball_vy': self.wm.ball(self.wm.time().cycle()).vy,
                    'player_x': self.wm.ourPlayer(unum).x,
                    'player_y': self.wm.ourPlayer(unum).y,
                    'player_vx': self.wm.ourPlayer(unum, wm.time().cycle()).vx,
                    'player_vy': self.wm.ourPlayer(unum, wm.time().cycle()).vy,
                    'kick': ','.join(kick) if kick is not None else None,
                    'dash': self.wm.ourPlayer(unum, wm.time().cycle()).dash(),
                    'turn': self.wm.ourPlayer(unum, wm.time().cycle()).turn(),
                    'turn_neck': self.wm.ourPlayer(unum, wm.time().cycle()).turn_neck(),
                    'tackle': self.wm.ourPlayer(unum, wm.time().cycle()).tackle(),
                    'change_view': self.wm.ourPlayer(unum, wm.time().cycle()).change_view(),
                    'attentionto': self.wm.ourPlayer(unum, wm.time().cycle()).attentionto(),
                    'pointto': self.wm.ourPlayer(unum, wm.time().cycle()).pointto(),
                    'say': self.wm.ourPlayer(unum, wm.time().cycle()).say(),
                    'team_name': self.our_name
                }
                rowlist.append(row)

            """add their player row"""
            for unum in range(1, 12):
                kick = self.wm.theirPlayer(unum, wm.time().cycle()).kick()
                row = {
                    'cycle': self.wm.time().cycle(),
                    # 'player_num': player_num.format(self.opp_name, unum),
                    'player_num': unum,
                    'ball_x': self.wm.ball(self.wm.time().cycle()).x,
                    'ball_y': self.wm.ball(self.wm.time().cycle()).y,
                    'ball_vx': self.wm.ball(self.wm.time().cycle()).vx,
                    'ball_vy': self.wm.ball(self.wm.time().cycle()).vy,
                    'player_x': self.wm.theirPlayer(unum).x,
                    'player_y': self.wm.theirPlayer(unum).y,
                    'player_vx': self.wm.theirPlayer(unum, wm.time().cycle()).vx,
                    'player_vy': self.wm.theirPlayer(unum, wm.time().cycle()).vy,
                    'kick': ','.join(kick) if kick is not None else None,
                    'dash': self.wm.theirPlayer(unum, wm.time().cycle()).dash(),
                    'turn': self.wm.theirPlayer(unum, wm.time().cycle()).turn(),
                    'turn_neck': self.wm.theirPlayer(unum, wm.time().cycle()).turn_neck(),
                    'tackle': self.wm.theirPlayer(unum, wm.time().cycle()).tackle(),
                    'change_view': self.wm.theirPlayer(unum, wm.time().cycle()).change_view(),
                    'attentionto': self.wm.theirPlayer(unum, wm.time().cycle()).attentionto(),
                    'pointto': self.wm.theirPlayer(unum, wm.time().cycle()).pointto(),
                    'say': self.wm.theirPlayer(unum, wm.time().cycle()).say(),
                    'team_name': self.opp_name
                }
                rowlist.append(row)

            self.wm.gameMode().UpdatePlayMode()
            self.wm.time().addTime()

        return rowlist

    def execute(self):
        f = open('../csv/{}.csv1'.format(self.wm.file_name), 'a')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(
            ['cycle', 'team_name', 'player_num', 'ball_x', 'ball_y', 'ball_vx', 'ball_vy', 'player_x', 'player_y', 'player_vx',
             'player_vy', 'kick', 'dash', 'turn', 'turn_neck', 'tackle', 'change_view', 'attentionto', 'pointto', 'say'])

        for i in self.rowlist:
            writer.writerow(
                [i['cycle'], i['team_name'], i['player_num'], i['ball_x'], i['ball_y'], i['ball_vx'], i['ball_vy'],
                 i['player_x'],i['player_y'], i['player_vx'], i['player_vy'], i['kick'], i['dash'], i['turn'],
                 i['turn_neck'], i['tackle'], i['change_view'], i['attentionto'], i['pointto'], i['say']])

        f.close()


if __name__ == '__main__':
    rcg_path = "../log/20180504161434-MT2018_2-vs-YuShan2018_0.rcg"
    wm = World(rcg_path)
    Rcg2csv(wm).execute()
