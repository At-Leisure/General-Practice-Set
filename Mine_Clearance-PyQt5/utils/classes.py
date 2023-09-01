""" 类的集合 """

# official module
from functools import partial
# third-party module
import numpy as np
# local module
from func import create_mine_index
from deco import asEnum


class Ostream:
    """ ## Example
    >>> io = Ostream()
    >>> io << f'this emulates c++ cout.'"""

    def __lshift__(self, item):
        print(item)


IO = Ostream()


@asEnum()
class GameStatus:
    """ 游戏状态 """
    RUNNING = 0  # 运行中
    SUCCESSFUL = 1  # 成功
    FAILED = 2  # 失败


@asEnum()
class GridStatus:
    """ 网格状态 """
    UNKNOW = 0  # 未知状态
    BLANK = 1  # 确认空白
    ISMINE = 2  # 确认地雷


class MineClearanceGame:
    """ 扫雷游戏 """

    def __init__(self, n_row, n_mine) -> None:
        """ 初始化对象 """
        # """ 对象属性 """
        self.game_status_ = GameStatus.RUNNING  # 游戏初始状态默认为运行中
        self.row_num_ = n_row  # 行数&列数
        self.mine_num_ = n_mine  # 地雷数
        self.mine_set_ = set()  # 地雷位置集
        self.opened_num_ = 0  # 点开的空格数目
        self.grid_matrix_ = np.full([n_row, n_row], GridStatus.UNKNOW)  # 网格阵列
        self.nearby_matrix_ = np.zeros([n_row, n_row])  # 每个网格临近的地雷数

    def createNewGame(self):
        """ 创建新的游戏 """
        self.mine_set_ = create_mine_index(
            n_line=self.row_num_, n_mine=self.mine_num_)  # 新建地雷位置
        self.game_status_ = GameStatus.RUNNING  # 重置游戏状态
        self.nearby_matrix_ = np.zeros(
            [self.row_num_, self.row_num_], dtype=np.int8)  # 重置临近地雷数目
        self.opened_num_ = 0  # 点开的空格数目置零

        # """ 计算每个网格3x3区域内的地雷数 """
        print(self.mine_set_)
        for row_mine, col_mine in self.mine_set_:  # 遍历每个地雷的坐标
            print(row_mine, col_mine, '<<<')
            # 为该地雷的四周3x3的空格的临近地雷数目加一
            for row in range(row_mine-1, row_mine+2):
                for col in range(col_mine-1, col_mine+2):
                    print(row, col)
                    # 限制范围
                    if not 0 <= row <= self.row_num_-1:
                        continue
                    if not 0 <= col <= self.row_num_-1:
                        continue
                    # 跳过地雷
                    if row == row_mine and col == col_mine:
                        continue
                    self.nearby_matrix_[row, col] += 1

    def click(self, row, col) -> GameStatus:
        """ 检测点击事件 """
        print(row, col)
        if (row, col) in self.mine_set_:  # 点击到地雷
            self.game_status_ = GameStatus.FAILED  # 设置状态为-失败
        else:  # 点击空白
            self.opened_num_ += 1
            print(self.opened_num_)
            if self.opened_num_ == self.row_num_**2 - self.mine_num_:
                self.game_status_ = GameStatus.SUCCESSFUL
            else:
                self.game_status_ = GameStatus.RUNNING
        return self.game_status_

    def simulation(self):
        """ 仿真测试 """
        PX = 50  # 单个按钮的大小，像素单位px
        self.createNewGame()  # 新建游戏
        import tkinter as tk  # 临时加载tkinter库，只在函数调用时有效
        import tkinter.messagebox as mbox  # 加载提示框子模块

        # """ 创建交互窗口 """
        window = tk.Tk()  # 创建新窗口
        window.title('Simulation of MineClearanceGame class')  # 窗口标题
        window.geometry(f'{PX*self.row_num_}x{PX*self.row_num_}')  # 窗口大小

        buttons = []  # 按钮阵容器

        def btn_cmd(row, col):
            """ 新建按钮命令 """
            buttons[row][col].place_forget()  # 点击后按钮消失
            status = self.click(row, col)  # 触发点击事件
            if status == GameStatus.SUCCESSFUL:  # 成功
                mbox.showinfo(
                    title='Mine Clearance', message='Game Successed !')  # 弹出提示
                window.quit()  # 结束游戏，退出窗口
            elif status == GameStatus.FAILED:  # 失败
                mbox.showinfo(
                    title='Mine Clearance', message='Game Failed !')  # 弹出提示
                window.destroy()  # 结束游戏，销毁窗口
            else:  # 继续
                pass

        # """ 创建按钮阵列 """
        for row in range(self.row_num_):
            buttons.append([])
            for col in range(self.row_num_):
                btn = tk.Button(
                    window, command=partial(btn_cmd, row, col))
                if (row, col) in self.mine_set_:
                    btn['text'] = '@'
                else:
                    btn['text'] = str(self.nearby_matrix_[row, col] if self.nearby_matrix_[
                                      row, col] != 0 else '')
                btn.place(y=PX*row, x=PX*col, width=PX, height=PX)
                buttons[row].append(btn)
        window.mainloop()


if __name__ == '__main__':
    mc = MineClearanceGame(5, 3)
    mc.simulation()
