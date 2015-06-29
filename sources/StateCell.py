#! /usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *

from View.widget import Ui_Widget

from Model.Dijkstra import Dijkstra
from Model.Dijkstra import Node
from Model.Dijkstra import Edge


class Hook(object):
    """
    @brief  フック クラス.
    """
    def __init__(self):
        pass
    def notify(self, i_Node):
        pass

class StateCellFactory(object):
    """
    @brief  セルの状態クラスを生成する クラス.
    """
    __DEBUG__ = False

    WALL = 0
    ROAD = 1
    START = 2
    GOAL = 3

    def __init__(self):
        pass

    def create(self, i_State):
        """
        @brief  セルの状態クラスを生成する.
        @params i_State 生成する状態.
        @return StateCellオブジェクト.
        """
        theStateDict = {
                self.WALL:Wall, 
                self.ROAD:Road,
                self.START:Start,
                self.GOAL:Goal
                }
        if(self.__DEBUG__): print( "create:{0}".format(theStateDict[i_State]()) )
        return theStateDict[i_State]()

class StateCell(Node):
    """
    @brief  セルの状態 クラス.
    @note   抽象クラス. インスタンス化はしないこと.
    """
    def __init__(self):
        Node.__init__(self)
    def fore_color(self):
        """
        @brief  前景色を取得.
        @params なし.
        @return 前景色. QtColor.
        """
        pass
    def back_color(self):
        """
        @brief  背景色を取得.
        @params なし.
        @return 背景色. QtColor.
        """
        pass
    def text(self):
        """
        @brief  表示文字列を取得.
        @params なし.
        @return 表示文字列.
        """
        pass
    def image(self):
        """
        @brief  表示アイコンを取得.
        @params なし.
        @return アイコン.
        """
        pass

class Wall(StateCell):
    """
    @brief    壁 クラス.
    """
    def __init__(self):
        StateCell.__init__(self)
    def __str__(self):
        return "Wall"
    def __repr__(self):
        return "<Wall>"
    def fore_color(self):
        """
        @brief  前景色を取得.
        @params なし.
        @return 前景色. QtColor.
        """
        return (Qt.black)
    def back_color(self):
        """
        @brief  背景色を取得.
        @params なし.
        @return 背景色. QtColor.
        """
        return (Qt.gray)
    def text(self):
        """
        @brief  表示文字列を取得.
        @params なし.
        @return 表示文字列.
        """
        return "W"
    def image(self):
        """
        @brief  表示アイコンを取得.
        @params なし.
        @return アイコン.
        """
        pass

class Road(StateCell):
    """
    @brief    道 クラス.
    """
    def __init__(self):
        StateCell.__init__(self)
    def __str__(self):
        return "Road"
    def __repr__(self):
        return "<Road>"
    def fore_color(self):
        """
        @brief  前景色を取得.
        @params なし.
        @return 前景色. QtColor.
        """
        return (Qt.gray)
    def back_color(self):
        """
        @brief  背景色を取得.
        @params なし.
        @return 背景色. QtColor.
        """
        return (Qt.white)
    def text(self):
        """
        @brief  表示文字列を取得.
        @params なし.
        @return 表示文字列.
        """
        return "R"
    def image(self):
        """
        @brief  表示アイコンを取得.
        @params なし.
        @return アイコン.
        """
        pass

class Start(Road):
    """
    @brief    スタート地点 クラス.
    """
    def __init__(self):
        StateCell.__init__(self)
    def __str__(self):
        return "Start"
    def __repr__(self):
        return "<Start>"
    def fore_color(self):
        """
        @brief  前景色を取得.
        @params なし.
        @return 前景色. QtColor.
        """
        return (Qt.lightGray)
    def back_color(self):
        """
        @brief  背景色を取得.
        @params なし.
        @return 背景色. QtColor.
        """
        return (Qt.blue)
    def text(self):
        """
        @brief  表示文字列を取得.
        @params なし.
        @return 表示文字列.
        """
        return "S"
    def image(self):
        """
        @brief  表示アイコンを取得.
        @params なし.
        @return アイコン.
        """
        pass

class Goal(Road):
    """
    @brief    ゴール地点 クラス.
    """
    def __init__(self):
        StateCell.__init__(self)
    def __str__(self):
        return "Goal"
    def __repr__(self):
        return "<Goal>"
    def fore_color(self):
        """
        @brief  前景色を取得.
        @params なし.
        @return 前景色. QtColor.
        """
        return (Qt.lightGray)
    def back_color(self):
        """
        @brief  背景色を取得.
        @params なし.
        @return 背景色. QtColor.
        """
        return (Qt.red)
    def text(self):
        """
        @brief  表示文字列を取得.
        @params なし.
        @return 表示文字列.
        """
        return "G"
    def image(self):
        """
        @brief  表示アイコンを取得.
        @params なし.
        @return アイコン.
        """
        pass

