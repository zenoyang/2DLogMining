# -*- coding: utf-8 -*-

"""
world_model: analyze RoboCup Soccer Simulator rcg and rcl files
modify by YangZheng
Date: 2017-11-28
Version: v1.1.1
Reference: https://github.com/Seiya-Yamamoto/python_scripts
Thanks to Seiya Yamamoto(Copyright)
"""


import math
import re


class World:
    def __init__(self, file_path):
        # error process
        # argvs = sys.argv
        # print(argvs[1])
        # argc = len(argvs)
        # if argc != 2:
        #     print("file open error")
        #     sys.exit()

        # file_path = "20140709193255-HELIOS2014_3-vs-WrightEagle_0.rcg"

        self.rcg = []
        self.rcg.append("(show 0 ((b) 0.000 0.000")

        self.rcl_l = [[None for j in range(12)]
                      for i in range(self.fullstateTime() + 1)]
        self.rcl_r = [[None for j in range(12)]
                      for i in range(self.fullstateTime() + 1)]

        self.playmode = []

        # file_name = argvs[1].split(".")[0]
        self.file_name = file_path.split("/")[-1].split(".")[0]  # 20140709193255-HELIOS2014_3-vs-WrightEagle_0

        self.left_team_name = re.split(
            "_[0-9]+", re.split("^[0-9]+-", self.file_name.split("-vs-")[0])[1])[0]  # ^[0-9]+-  yz modify
        self.right_team_name = re.split(
            "_[0-9]+", self.file_name.split("-vs-")[1])[0]

        self.left_team_score = int(self.file_name.split(
            "-vs-")[0].split(self.left_team_name + "_")[1])

        self.right_team_score = int(self.file_name.split(
            "-vs-")[1].split(self.right_team_name + "_")[1])


        # initialize game mode
        self.game_mode = Type(self.left_team_score, self.right_team_score)

        # initialize game time
        self.game_time = GameTime(0, 6000)

        # initialize last kicker side
        self.last_kicker_side = "left"

        rcgfile = file_path[0:-3] + "rcg"
        rclfile = file_path[0:-3] + "rcl"  # ../log/20140709193255-HELIOS2014_3-vs-WrightEagle_0.rcl
        # file open & close
        with open(rcgfile, 'r') as rcg:
            # rcg file
            for line in rcg:
                if("show" in line and int(self.rcg[-1].split(" ")[1]) < int(line.split(" ")[1])):
                    self.rcg.append(line)
                    self.game_time.game_time += 1
                    if(int(self.rcg[-1].split(" ")[1]) == 2999):
                        self.rcg.append("(show 3000 ((b) 0.000 0.000")
                        self.game_time.game_time += 1

                elif("playmode" in line):
                    mode = line.split(" ")[2].split(")")[0]
                    cycle = int(line.split(" ")[1])
                    self.playmode.append([cycle, mode])

            self.game_time.t_over = self.time().cycle()

            # error handling
            if(self.ball() is None):
                self.game_time.t_over -= 1

            # reset cycle count
            self.time().resetTime()

        # rcl file
        """
        解析球员发送的动作请求     YangZheng 2018-05-06
        """
        with open(rclfile, 'r') as rcl:
            for line in rcl:
                if(int(line.split(',')[0]) >= 1):
                    rcl_cycle = int(line.split(',')[0])

                    action = {'kick': None, 'dash': None, 'turn': None, 'turn_neck': None, 'change_view': None,
                              'tackle': None, 'attentionto': None, 'say': None, 'pointto': None}

                    if(self.left_team_name in line and not "Coach" in line):
                        rcl_unum = int(line.split(self.left_team_name)[1].split(": ")[0].split("_")[1])

                        if rcl_cycle == 6000:
                            self.rcl_l[rcl_cycle][rcl_unum] = PlayerObject(_unum=rcl_unum, action=action)
                            continue

                        # rcl_action = line.split(self.left_team_name)[1].split(": (")[1].split(" ")[0].split(")")[0]
                        rcl_action = line.split(self.left_team_name)[1].split(": ")[1]

                        if 'kick' in rcl_action:
                            action['kick'] = [rcl_action.split('kick')[1].split(' ')[1],
                                              rcl_action.split('kick')[1].split(' ')[2].split(')')[0]]
                        if 'dash' in rcl_action:
                            action['dash'] = float(rcl_action.split('dash')[1].split(' ')[1].split(')')[0])
                        if 'turn_neck' in rcl_action:
                            action['turn_neck'] = float(rcl_action.split('turn_neck')[1].split(' ')[1].split(')')[0])
                        if 'pointto' in rcl_action:
                            action['pointto'] = rcl_action.split('pointto')[1].split(' ')[1].split(')')[0]
                        if 'say' in rcl_action:
                            action['say'] = rcl_action.split('say')[1].split(' ')[1].split(')')[0].split('"')[1]
                        if 'turn' in rcl_action:
                            action['turn'] = float(rcl_action.split('turn')[1].split(' ')[1].split(')')[0])
                        if 'tackle' in rcl_action:
                            action['tackle'] = ' '.join(rcl_action.split('tackle')[1].split(' ')[1:]).split(')')[0]
                        if 'change_view' in rcl_action:
                            action['change_view'] = rcl_action.split('change_view')[1].split(' ')[1].split(')')[0]
                        if 'attentionto' in rcl_action:
                            action['attentionto'] = " ".join(rcl_action.split('attentionto')[1].split(' ')[1:]).split(')')[0]
                        self.rcl_l[rcl_cycle][rcl_unum] = PlayerObject(_unum=rcl_unum, action=action)

                    elif(self.right_team_name in line and not "Coach" in line):
                        rcl_unum = int(line.split(self.right_team_name)[1].split(": ")[0].split("_")[1])

                        if rcl_cycle == 6000:
                            self.rcl_r[rcl_cycle][rcl_unum] = PlayerObject(_unum=rcl_unum, action=action)
                            continue

                        # rcl_action = line.split(self.right_team_name)[1].split(": (")[1].split(" ")[0].split(")")[0]
                        rcl_action = line.split(self.right_team_name)[1].split(": ")[1]

                        if 'kick' in rcl_action:
                            action['kick'] = [rcl_action.split('kick')[1].split(' ')[1],
                                              rcl_action.split('kick')[1].split(' ')[2].split(')')[0]]
                        if 'dash' in rcl_action:
                            action['dash'] = float(rcl_action.split('dash')[1].split(' ')[1].split(')')[0])
                        if 'turn_neck' in rcl_action:
                            action['turn_neck'] = float(rcl_action.split('turn_neck')[1].split(' ')[1].split(')')[0])
                        if 'pointto' in rcl_action:
                            action['pointto'] = rcl_action.split('pointto')[1].split(' ')[1].split(')')[0]
                        if 'say' in rcl_action:
                            action['say'] = rcl_action.split('say')[1].split(' ')[1].split(')')[0].split('"')[1]
                        if 'turn' in rcl_action:
                            action['turn'] = float(rcl_action.split('turn')[1].split(' ')[1].split(')')[0])
                        if 'tackle' in rcl_action:
                            action['tackle'] = ' '.join(rcl_action.split('tackle')[1].split(' ')[1:]).split(')')[0]
                        if 'change_view' in rcl_action:
                            action['change_view'] = rcl_action.split('change_view')[1].split(' ')[1].split(')')[0]
                        if 'attentionto' in rcl_action:
                            action['attentionto'] = " ".join(rcl_action.split('attentionto')[1].split(' ')[1:]).split(')')[0]
                        self.rcl_r[rcl_cycle][rcl_unum] = PlayerObject(_unum=rcl_unum, action=action)

    # end constructor

    """
    @brief get teammate action
    @param unum : player unum
    @return player action or NULL
    """

    def __ourAction(self, unum, cycle = 0):

        if (cycle == 0):
            cycle = self.time().cycle()

        if(self.rcl_l[cycle][unum] is None):
            return None
        return self.rcl_l[cycle][unum].action()

    """
    @brief get opponent action
    @param unum : player unum
    @return player action or NULL
    """

    def __theirAction(self, unum, cycle = 0):

        if(cycle == 0):
            cycle = self.time().cycle()

        if(self.rcl_r[cycle][unum] is None):
            return None
        return self.rcl_r[cycle][unum].action()

    """
    @brief get opponent teamname
    @return const reference to the team name string
    """

    def opponentTeamName(self):
        return self.right_team_name

    """
    @brief get our teamname
    @return const reference to the team name string
    """

    def teamName(self):
        return self.left_team_name

    # test
    def setTeamName(self, teamName):
        self.left_team_name = teamName

    """
    @brief get ball info
    @return const reference to the BallObject
    """

    def ball(self, cycle = 0):

        if(cycle == 0):
            cycle = self.time().cycle()

        if(len(self.rcg) <= cycle):
            return None
        ball_x = float(self.rcg[cycle].split("((b) ")[1].split(" ")[0])
        ball_y = float(self.rcg[cycle].split("((b) ")[1].split(" ")[1])

        """
        添加球的速度信息    YangZheng 2018-05-05
        """
        ball_vx = float(self.rcg[cycle].split("((b) ")[1].split(" ")[2])
        ball_vy = float(self.rcg[cycle].split("((b) ")[1].split(" ")[3][0:-1])

        return BallObject(ball_x, ball_y, ball_vx, ball_vy, 0.5)

    """
    @brief get last updated time (== current game time)
    @return const reference to the game time object
    """

    def time(self):
        return self.game_time

    """
    @brief get last time updated by fullstate
    @return const reference to the game time object
    """

    def fullstateTime(self):
        return 6000

    """
    @brief get current playmode info
    @return const reference to the GameMode object
    """

    def gameMode(self):
        # update game_mode
        self.game_mode._UpdatePlayMode(self.time().cycle(), self.playmode)
        return self.game_mode

    """
    @brief get the distance from input point to the nearest opponent
    @param with_goalie include goalie if true
    @return distance to the matched opponent. if not found, a big value is returned.
    """

    def ourDefenseLineX(self):
        teammate = []
        teammate.append(PlayerObject(0.0, 0.0, 0))
        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        defense_line = 65535.0

        if(self.rcg[self.time().cycle()] is None):
            return defense_line

        for i in range(1, 12):
            teammate.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        for i in range(2, 12):
            if(defense_line > teammate[i].pos().x):
                defense_line = teammate[i].pos().x

        return defense_line

    def ourOffenseLineX(self):
        teammate = []
        teammate.append(PlayerObject(0.0, 0.0, 0))
        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        offense_line = -65535.0
        for i in range(1, 12):
            teammate.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        for i in range(2, 12):
            if(offense_line < teammate[i].pos().x):
                offense_line = teammate[i].pos().x

        return offense_line

    def theirDefenseLineX(self):
        opponent = []
        opponent.append(PlayerObject(0.0, 0.0, 0))
        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        defense_line = -65535.0
        for i in range(1, 12):
            opponent.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        for i in range(2, 12):
            if(defense_line < opponent[i].pos().x):
                defense_line = opponent[i].pos().x

        return defense_line

    def theirOffenseLineX(self):
        opponent = []
        opponent.append(PlayerObject(0.0, 0.0, 0))
        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        offense_line = 65535.0
        for i in range(1, 12):
            opponent.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        for i in range(2, 12):
            if(offense_line > opponent[i].pos().x):
                offense_line = opponent[i].pos().x

        return offense_line

    def existKickableOpponent(self):
        dist_OppToBall = self.getDistOpponentNearestToBall(True)
        dist_MateToBall = self.getDistTeammateNearestToBall(True)
        if(dist_MateToBall > dist_OppToBall and dist_OppToBall < 1.5):
            return True
        else:
            return False

    def existKickableTeammate(self):
        dist_OppToBall = self.getDistOpponentNearestToBall(True)
        dist_MateToBall = self.getDistTeammateNearestToBall(True)
        if(dist_MateToBall < dist_OppToBall and dist_MateToBall < 1.5):
            return True
        else:
            return False

    def lastKickerSide(self):
        if(self.existKickableOpponent()):
            self.last_kicker_side = "right"
        elif(self.existKickableTeammate()):
            self.last_kicker_side = "left"
        return self.last_kicker_side

    def getDistOpponentNearestTo(self, with_goalie, point):
        opponent = []
        opponent.append(PlayerObject(0.0, 0.0, 0))
        d = 65535.0
        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        for i in range(1, 12):
            opponent.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        minimum = 1 if(with_goalie) else 2
        for i in range(minimum, 12):
            if(d > point.dist(opponent[i])):
                d = point.dist(opponent[i])

        return d

    """
    @brief get the distance to opponent nearest to ball wtth accuracy count
    @param with_goalie include goalie if true
    @return distance to the matched opponent. if not found, a big value is returned.
    """

    def getDistOpponentNearestToBall(self, with_goalie=False):
        return self.getDistOpponentNearestTo(with_goalie, self.ball().pos())

    """
    @brief get the distance from opponent nearest to self wtth accuracy count
    @param with_goalie include goalie if true
    @return distance to the matched opponent. if not found, a big value is returned.
    """

    def getDistOpponentNearestToSelf(self, with_goalie=False):
        pass

    """
    @brief get the distance from input point to the nearest teammate
    @param with_goalie include goalie if true
    @return distance to the matched teammate. if not found, a big value is returned.
    """

    def getDistTeammateNearestTo(self, with_goalie, point):
        teammate = []
        teammate.append(PlayerObject(0.0, 0.0, 0))
        d = 65535.0
        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        for i in range(1, 12):
            teammate.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        minimum = 1 if(with_goalie) else 2
        for i in range(minimum, 12):
            if(d > point.dist(teammate[i])):
                d = point.dist(teammate[i])

        return d

    """
    @brief get the distance to teammate nearest to ball wtth accuracy count
    @param with_goalie include goalie if true
    @return distance to the matched teammate. if not found, a big value is returned.
    """

    def getDistTeammateNearestToBall(self, with_goalie):
        return self.getDistTeammateNearestTo(with_goalie, self.ball().pos())

    """
    @brief get the distance from teammate nearest to self wtth accuracy count
    @param with_goalie include goalie if true
    @return distance to the matched teammate. if not found, a big value is returned.
    """

    def getDistTeammateNearestToSelf(self, with_goalie):
        pass

    """
      @brief get opponent pointer nearest to the specified player
      @param with_goalie : bool
      @param point variable pointer to store the distance
      from retuned player to point
      @return pointer to player object
    """

    def getOpponentNearestTo(self, with_goalie, point):
        opponent = []
        opponent.append(PlayerObject(0.0, 0.0, 0))
        d = 65535.0
        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        for i in range(1, 12):
            opponent.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)
                                               [i].split(" ")[3]),
                                         i, ball_pos=self.ball().pos(), action=self.__theirAction(i)))

        minimum = 1 if(with_goalie) else 2
        for i in range(minimum, 12):
            if(d > point.dist(opponent[i].pos())):
                d = point.dist(opponent[i].pos())
                nearest_opponent = opponent[i]

        return nearest_opponent

    def getOpponentNearestToBall(self, with_goalie=False):
        return self.getOpponentNearestTo(with_goalie, self.ball().pos())

    def getOpponentNearestToSelf(self, with_goalie=False):
        pass

    def getTeammateNearestTo(self, with_goalie, point):
        teammate = []
        teammate.append(PlayerObject(0.0, 0.0, 0))
        d = 65535.0
        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        for i in range(1, 12):
            teammate.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)
                                               [i].split(" ")[3]),
                                         i, ball_pos=self.ball().pos(), action=self.__ourAction(i)))

        minimum = 1 if(with_goalie) else 2
        for i in range(minimum, 12):
            if(d > point.dist(teammate[i].pos())):
                d = point.dist(teammate[i].pos())
                nearest_teammate = teammate[i]

        return nearest_teammate

    def getTeammateNearestToBall(self, with_goalie=False):
        return self.getTeammateNearestTo(with_goalie, self.ball().pos())

    def getOpponentNearestToSelf(self, with_goalie=False):
        pass

    def ourPlayer(self, unum, cycle = 0):

        if(cycle == 0):
            cycle = self.time().cycle()

        if(unum < 1 or unum > 11):
            return None

        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[cycle]

        return PlayerObject(float(re.split(pattern, match)[unum].split(" ")[2]),
                            float(re.split(pattern, match)[unum].split(" ")[3]),
                            float(re.split(pattern, match)[unum].split(" ")[4]),
                            float(re.split(pattern, match)[unum].split(" ")[5]),
                            unum, self.ball(cycle).pos(), self.__ourAction(unum, cycle))

    def theirPlayer(self, unum, cycle = 0):

        if(cycle == 0):
            cycle = self.time().cycle()

        if(unum < 1 or unum > 11):
            return None

        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[cycle]
        return PlayerObject(float(re.split(pattern, match)[unum].split(" ")[2]),
                            float(re.split(pattern, match)[unum].split(" ")[3]),
                            float(re.split(pattern, match)[unum].split(" ")[4]),
                            float(re.split(pattern, match)[unum].split(" ")[5]),
                            unum, self.ball(cycle).pos(), self.__theirAction(unum, cycle))


"""
 @class Vector2D
 @brief 2d vector class

 @param float x
 @param float y
"""


class Vector2D:
    """
    添加速度信息 vx, vy   YangZheng 2018-05-05
    """
    def __init__(self, x, y, vx=0.0, vy=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def pos(self):
        return Vector2D(self.x, self.y)

    def abs(self):
        return Vector2D(abs(self.x), abs(self.y))

    def absX(self):
        return abs(self.x)

    def absY(self):
        return abs(self.y)

    def dist(self, point):
        d = math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
        return d


"""
  @class Circle2D
  @brief 2d circle class

  @param Vector2d center
  @param float radius
"""


class Circle2D:

    def __init__(self, center_pos, radius):
        self.center_pos = center_pos
        self.radius = radius

    def center(self):
        return self.center_pos

    def contains(self, pos):
        if(self.center_pos.dist(pos) <= self.radius):
            return True
        else:
            return False

"""
  @class Line2D
  @brief 2d straight line class
  @param Vector2D pos1
  @param Vector2D pos2

  @Line Fomula: aX + bY + c = 0
"""


class Line2D:

    def __init__(self, p1, p2):
        self.a = -(p2.y - p1.y)
        self.b = p2.x - p1.x
        self.c = -self.a * p1.x - self.b * p1.y

    def dist(self, p):
        return math.fabs((self.a * p.x + self.b * p.y + self.c) / math.sqrt(self.a * self.a + self.b * self.b))

    """
      @brief get the intersection point with 'line'
      @param line considered line
      @return intersection point. if it does not exist,
      the invalidated value vector is returned.
    """

    def intersection(self, line):

        if(self.a * line.b == line.a * self.b):
            return Vector2D(-100.0, -100.0)

        intersection_x = (self.b * line.c - line.b * self.c) / \
            (self.a * line.b - line.a * self.b)
        intersection_y = (line.a * self.c - self.a * line.c) / \
            (self.a * line.b - line.a * self.b)

        if(intersection_x > 52.5000 or intersection_x < -52.5000
           or intersection_y > 34.000 or intersection_y < -34.000):
            return Vector2D(-100.0, -100.0)

        return Vector2D(intersection_x, intersection_y)

    """
      @brief check if the slope of this line is same to the slope of 'line'
      @param line considered line
      @retval true almost same
      @retval false not same
    """

    def isParallel(self, line):
        if(math.fabs(self.a * line.b - line.a * self.b) <= 0.051):
            return True
        else:
            return False

    def getA(self):
        return self.a

    def getB(self):
        return self.b

    def getC(self):
        return self.c

"""
  @class Rect2D
  @brief 2D rectangle regin class.

  The model and naming rules are depend on soccer simulator environment
          -34.0
            |
            |
-52.5 ------+------- 52.5
            |
            |
          34.0
"""


class Rect2D:

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def top(self):
        return self.top_left.y

    def bottom(self):
        return self.bottom_right.y

    def left(self):
        return self.top_left.x

    def right(self):
        return self.bottom_right.x

    def center(self):
        return Vector2D((self.left() + self.right()) * 0.5, (self.top() + self.bottom()) * 0.5)

    def contains(self, point):
        if(self.left() <= point.x and point.x <= self.right()
           and self.top() <= point.y and point.y <= self.bottom()):
            return True
        else:
            return False


class BallObject(Vector2D):
    """
    添加球的速度信息    YangZheng 2018-05-05
    """
    def __init__(self, x, y, vx=0.0, vy=0.0, ball_size=0.5):
        Vector2D.__init__(self, x, y, vx, vy)
        self.ball_size = ball_size

    def size(self):
        return self.ball_size


class GameTime:

    def __init__(self, game_time, t_over):
        self.game_time = game_time
        self.t_over = t_over

    def resetTime(self):
        self.game_time = 1

    def kick_off(self):
        return 1

    def time_over(self):
        return self.t_over

    def addTime(self):
        self.game_time += 1

        if(self.game_time == 3000):
            self.game_time = 3001

    def cycle(self):
        return self.game_time

    def setCycleTo(self, c):
        # if(1 <= c and c <= self.time_over):
        if (1 <= c and c <= 6000):
            self.game_time = c


"""
@brief get current playmode type
@return client side playmode type Id
"""
# playmode(
#   kick_off
#   play_on
#   kick_in
#   offside
#   free_kick
#   foul_charge
#   goal
#   time_over
# )


class Type:

    def __init__(self, score_l, score_r):
        self.mode = "kick_off"
        self.score_l = score_l
        self.score_r = score_r

    '''
    corner_kick_l
    play_on
    goal_kick_r
    '''
    def type(self):
        return self.mode

    def scoreLeft(self):
        return self.score_l

    def scoreRight(self):
        return self.score_r

    def _UpdatePlayMode(self, cycle, line):
        for i in line:
            if(i[0] <= cycle):
                self.mode = i[1]
            elif(i[0] > cycle):
                break

    def UpdatePlayMode(self):
        pass

    def __CheckPlayMode(self):
        return self.mode

    def __ChangePlayModeToFoul(self):
        self.mode = "foul_charge"

    def __ChangePlayModeToOffSide(self):
        self.mode = "offside"

    def __ChangePlayModeToPlayOn(self):
        self.mode = "play_on"

"""
@class PlayerObject
@brief observed player object class
"""


class PlayerObject(Vector2D):
    """
    添加球员的速度信息   YangZheng 2018-05-05
    """
    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, _unum=0, ball_pos=Vector2D(0.0, 0.0), action="unknown"):
        Vector2D.__init__(self, x, y, vx, vy)
        self._unum = _unum
        self._ball_pos = ball_pos
        self._action = action

        """
        添加动作信息  YangZheng 2018-05-06
        """
        self._kick = self._dash = self._turn = self._attentionto = self._change_view = self._pointto = \
            self._turn_neck = self._say = self._tackle = None

        if action is not None:  # when cycle is 6000 happen
            self._kick = action['kick']
            self._dash = action['dash']
            self._turn = action['turn']
            self._attentionto = action['attentionto']
            self._change_view = action['change_view']
            self._pointto = action['pointto']
            self._turn_neck = action['turn_neck']
            self._say = action['say']
            self._tackle = action['tackle']

    def isKickable(self):
        if(self.pos().dist(self._ball_pos) < 1.5):
            return True
        else:
            return False

    def unum(self):
        return self._unum

    def distFromBall(self):
        return self.pos().dist(self._ball_pos)

    def action(self):
        return self._action

    def kick(self):
        return self._kick

    def dash(self):
        return self._dash

    def turn(self):
        return self._turn

    def attentionto(self):
        return self._attentionto

    def change_view(self):
        return self._change_view

    def pointto(self):
        return self._pointto

    def turn_neck(self):
        return self._turn_neck

    def say(self):
        return self._say

    def tackle(self):
        return self._tackle


if __name__ == '__main__':
    rcg_path = "../log/20180504161434-MT2018_2-vs-YuShan2018_0.rcg"
    wm = World(rcg_path)

    while wm.time().kick_off() <= wm.time().cycle() and wm.time().cycle() <= wm.time().time_over():
        pass
        wm.gameMode().UpdatePlayMode()
        wm.time().addTime()

