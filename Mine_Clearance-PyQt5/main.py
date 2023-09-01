# encoding:utf-8
# anthor:ZYF
# date:2023/06


# official module
import sys
import enum
from functools import partial
import time

# third-party module
from PyQt5 import QtWidgets, uic, QtGui

# local module
import utils
import styles
from prepare import *

# Imitate c++ cout
IO = utils.Ostream()

# main window
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('./ui/MC.ui', self)

        """ 图形属性 """
        #页面控制器
        self.Page_Controler_ = self.ui.PageControler
        self.Page_Controler_: QtWidgets.QStackedWidget
        # 显示页面状态
        self.Page_Status_ = self.ui.PageStatus
        self.Page_Status_: QtWidgets.QLabel
        # 显示游戏状态
        self.Game_Status_ = self.ui.GameStatus
        self.Game_Status_: QtWidgets.QLabel
        # 返回开始界面
        self.Goto_Start_ = self.ui.GotoStart
        self.Goto_Start_: QtWidgets.QPushButton
        # 网格阵列容器
        self.Grid_Frame_ = self.ui.GridFrame
        self.Grid_Frame_:QtWidgets.QFrame

        """ 初始属性 """
        self.mine_number_ = 5  # 地雷的数量
        self.line_number_ = 5  # 行高的格数
        self.open_number_ = 0  # 被点开的按键数量
        self.mark_number_ = 0  # 被标记的地雷数量
        self.grid_matrix_ = [[]]  # 按键阵列-QPushButton
        self.mine_set_ = [[]]  # 地雷阵列-QPushButton
        self.IS_DEV_ = 1  # 是否处于开发者模式
        self.cursor_status_ = Cursor.NORMAL
        self.game_status_ = GameStatus.PREPARE

        """ 初始设置 """
        self.goto_StartPage_event()

    def goto_StartPage_event(self):
        """ go to start page """
        self.Goto_Start_.setEnabled(False)
        self.Game_Status_.setText('Prepareing')
        self.Page_Status_.setText('start page')
        self.Page_Controler_.setCurrentIndex(Page.START)

    def goto_GamePage_event(self):
        """ 创建网格 """
        # 创建地雷位置
        self.mine_set_ = utils.create_mine_index(
            n_line=self.line_number_, n_mine=self.mine_number_)
        if self.IS_DEV_:
            print(f'{self.mine_number_}/{self.line_number_**2}',
                  self.mine_set_)

        # 创建网格按钮
        self.grid_matrix_ = []  # 创建新的容器
        for row in range(self.line_number_):
            self.grid_matrix_.append([])
            for col in range(self.line_number_):
                # 创建按钮
                self.grid_matrix_[row].append(
                    QtWidgets.QPushButton(' ', self.ui.GridFrame))
                this_button = self.grid_matrix_[row][col]
                this_button: QtWidgets.QPushButton
                # 绑定事件
                this_button.clicked.connect(partial(self.click_scan, row, col))
                # 显示地雷
                if self.IS_DEV_ and ((row, col) in self.mine_set_):
                    this_button.setText(f'@{row}.{col}')
                # 添加到布局
                this_button.setProperty('is_grid', True)
                this_button.move(row*60, col*60)

        # 清零点开的按键数量
        self.open_number_ = 0

        """ go to game page """
        self.Goto_Start_.setEnabled(True)
        self.Game_Status_.setText(
            f'GAMING    opened:{self.open_number_:2d}    marked:{self.mark_number_:2d}')
        self.Page_Status_.setText('game page')
        self.Page_Controler_.setCurrentIndex(Page.GAME)

    def click_scan(self, row, col):
        """ 处理网格按键点击事件 """
        if self.IS_DEV_:
            print(f'{row}.{col} was clicked', end='')
            print(', this is a mine' if (row, col) in self.mine_set_ else '')
        
        # normal cursor
        if self.cursor_status_ == Cursor.NORMAL:
            # 点击到地雷
            if (row, col) in self.mine_set_:
                ...
            # 点击到空白
            else:
                self.open_number_ += 1
                self.grid_matrix_[row][col].setVisible(False)
                self.Game_Status_.setText(
                    f'GAMING    opened:{self.open_number_:2d}    marked:{self.mark_number_:2d}')
                
                 # 检测是否获胜
                if self.open_number_ == self.line_number_**2-self.mine_number_:
                    IO << "Win"
        
        # mark mine
        elif self.cursor_status_ == Cursor.MARK_MINE:
            #加载图案
            mine_pixmap = QtGui.QPixmap('./icon/flash.png').scaled(20,20)
            mine_icon = QtGui.QIcon(mine_pixmap)
            #标记地雷
            self.grid_matrix_[row][col].setIcon(mine_icon)

        # mark grid
        elif self.cursor_status_ == Cursor.MARK_GRID:
            ...

    def goto_AdjustPage_event(self):
        """ go to adjust page """
        self.Goto_Start_.setEnabled(True)
        self.Page_Status_.setText('adjust page')
        self.Page_Controler_.setCurrentIndex(Page.ADJUST)

    def goto_DevPage_event(self):
        """ go to developer page """
        self.Goto_Start_.setEnabled(True)
        self.Page_Status_.setText('dev page')
        self.Page_Controler_.setCurrentIndex(Page.DEV)

    def goto_MarkMineButton_event(self):
        """ 修改Frame中的鼠标图案 """
        #加载图案文件
        cursor_pixmap = QtGui.QPixmap('./icon/flash.png').scaled(28,28)
        #加载为光标图案
        cursor_img = QtGui.QCursor(cursor_pixmap)
        #设置光标图案
        self.Grid_Frame_.setCursor(cursor_img)
        # 更新光标状态
        self.cursor_status_ = Cursor.MARK_MINE


    def goto_MarkGridButton_event(self):
        """  """

    def goto_RestartButton_event(self):
        """  """



# main threading
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Mine Clearance - zyf')
    window.setWindowIcon(QtGui.QIcon('./icon/flash.png'))
    # window.setStyleSheet(styles.read_qss('./styles/style0.qss','utf8'))
    window.show()
    sys.exit(app.exec_())
