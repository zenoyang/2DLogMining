# _*_  coding: utf8 _*_

"""
count_tackle: 统计Tackle
Copyright (C) 2018 YangZheng
"""

import sys
reload(sys)
sys.path.append("../lib")
sys.setdefaultencoding('utf8')
import pandas as pd
# import matplotlib.pyplot as plt
from field_analyzer import FieldAnalyzer

"""
TODO：
将统计结果追加到CSV文件中，用柱状图展示数据
"""


class CountTackle(object):
    def __init__(self, data):
        self.left_team = data.iloc[1, :]['team_name']
        self.right_team = data.iloc[12, :]['team_name']
        self.left_data = data[data['team_name'] == self.left_team]
        self.right_data = data[data['team_name'] == self.right_team]
        self.tackle_data = data[data['tackle'].notnull()]
        self.fa = FieldAnalyzer(data)

    def countOurTackle(self):
        self.__countTackle(self.left_team)

    def countTheirTackle(self):
        self.__countTackle(self.right_team)

    def count(self):
        self.countOurTackle()
        self.countTheirTackle()

    def __countTackle(self, team_name):
        tackle = self.tackle_data[self.tackle_data['team_name'] == team_name]
        tackle_cycle = tackle['cycle']

        get_shell, out_side, pass_t, fail, shoot = 0, 0, 0, 0, 0
        o_s_c, t_c, g_s_c, p_t_c, f_c, s_c = [], [], [], [], [], []

        for i in tackle_cycle:
            cycle = i + 1  # 执行铲球的周期
            t_c.append(cycle)
            if self.fa.lastKickerSide(cycle)[1] != self.fa.nextKickerSide(cycle)[1] \
                    and self.fa.lastKickerSide(cycle)[1] != team_name:
                get_shell += 1
                g_s_c.append(cycle)
            elif self.fa.isBallOutside(self.fa.nextKickerSide(cycle)[0] - 1):
                out_side += 1
                o_s_c.append(cycle)
            elif self.fa.lastKickerSide(cycle)[1] == self.fa.nextKickerSide(cycle)[1] \
                    and self.fa.lastKickerSide(cycle)[1] == team_name:
                pass_t += 1
                p_t_c.append(cycle)
            elif self.fa.lastKickerSide(cycle)[1] == self.fa.nextKickerSide(cycle)[1] \
                    and self.fa.ballPos(self.fa.nextKickerSide(cycle)[0] - 1)[0] == 0.0 \
                    and self.fa.ballPos(self.fa.nextKickerSide(cycle)[0] - 1)[1] == 0.0:
                shoot += 1
                s_c.append(cycle)
            else:
                fail += 1
                f_c.append(cycle)

        print('-' * 40 + team_name + '铲球统计' + '-' * 40)
        print('总共铲球{}次: {}'.format(tackle_cycle.count(), t_c))
        print('铲球获取球权{}次： {}'.format(get_shell, g_s_c))
        print('铲出界{}次： {}'.format(out_side, o_s_c))
        print('铲传{}次： {}'.format(pass_t, p_t_c))
        print('铲射成功{}次： {}'.format(shoot, s_c))
        print('无效铲球{}次： {}\n'.format(fail, f_c))


if __name__ == '__main__':
    data = pd.read_csv('../csv/20180504161434-MT2018_2-vs-YuShan2018_0.csv')
    # CountTackle(data).countOurTackle()
    # CountTackle(data).countTheirTackle()
    CountTackle(data).count()
"""
----------------------------------------MT2018铲球统计----------------------------------------
总共铲球18次: [515, 583, 682, 1535, 1714, 1801, 2117, 2802, 2866, 3152, 3184, 3336, 3711, 3884, 4116, 5018, 5372, 5670]
铲球获取球权4次： [682, 2117, 2802, 3884]
铲出界7次： [515, 583, 1535, 1714, 1801, 3336, 5670]
铲传2次： [2866, 5372]
铲射成功1次： [5018]
无效铲球4次： [3152, 3184, 3711, 4116]

----------------------------------------YuShan2018铲球统计----------------------------------------
总共铲球23次: [93, 369, 965, 1094, 1426, 2006, 2111, 2292, 2488, 2491, 2703, 2745, 3530, 3865, 4652, 4791, 4800, 4956, 5312, 5371, 5488, 5777, 5962]
铲球获取球权7次： [1426, 2111, 2745, 3530, 4652, 5488, 5962]
铲出界4次： [369, 965, 2292, 4800]
铲传1次： [3865]
铲射成功0次： []
无效铲球11次： [93, 1094, 2006, 2488, 2491, 2703, 4791, 4956, 5312, 5371, 5777]
"""