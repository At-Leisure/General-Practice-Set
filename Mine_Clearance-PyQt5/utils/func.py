""" 函数集合 """

# official module
import random as rdm

# third-party module
# local module

def create_mine_index(*, n_line: int, n_mine: int) -> set[tuple[int, int]]:
    """ 创建地雷的位置 
    ## Param
    `n_line` - 行高的数量\n
    `n_mine` - 地雷的数量
    ## Return
    地雷位置集合{(row,colume)}
    ## Example
    >>> create_mine_index(n_line=3, n_mine=2)
    {(3, 2), (0, 3)}"""
    result = set()  # 使用集合，避免位置重复
    assert n_mine <= n_line**2, '地雷数量超过总格数量，无法继续进行'
    while len(result) < n_mine:
        row = rdm.randint(0, n_line-1)
        col = rdm.randint(0, n_line-1)
        result.add((row, col))
    return result