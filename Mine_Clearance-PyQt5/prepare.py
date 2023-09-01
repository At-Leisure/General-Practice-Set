# encoding:utf-8
# anthor:ZYF
# date:2023/06


# official module

# third-party module

# local module
import utils


# enum page
@utils.asEnum()
class Page:
    """ 界面序号 """
    START = 0
    GAME = 1
    ADJUST = 2
    DEV = 3


# enum cursor
@utils.asEnum()
class Cursor:
    """ 光标状态 """
    NORMAL = 0
    MARK_MINE = 1
    MARK_GRID = 2


# game status
@utils.asEnum()
class GameStatus:
    DEFEATED = 0  # 失败了
    VICTORY = 1  # 胜利了


@utils.asEnum()
class ExecStatus:
    GAMING = 0  # 游戏中
    PREPARE = 1  # 准备中
