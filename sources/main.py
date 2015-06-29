#! /usr/bin/python
# -*- coding: utf-8 -*-

#Widgetの変換方法.
#%python /Library/Python/2.7/site-packages/PyQt4/uic/pyuic.py ./View/GUI/widget.ui -o ./View/widget.py

import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

from View.widget import Ui_Widget

from StateCell import StateCellFactory
from StateCell import StateCell

from Model.Dijkstra import Dijkstra
from Model.Dijkstra import Node
from Model.Dijkstra import Edge

class ViewCell(QtGui.QTableWidgetItem):
    __DEBUG__ = False

    def __init__(self):
        QtGui.QTableWidgetItem.__init__(self)
        self.state = None
        self.state_factory = StateCellFactory()
        self.change_state(StateCellFactory.ROAD)

    def change_state(self, i_State):
        self.state = self.state_factory.create(i_State)
        self.draw()

    def draw(self):
        theBackColor = self.state.back_color()
        theForeColor = self.state.fore_color()
        theText = self.state.text()
        theImage = self.state.image()

        #前景色を設定.
        theColor = QtGui.QColor(theForeColor)
        theBrush = QtGui.QBrush()
        theBrush.setColor(theColor)
        self.setForeground(theBrush)

        #背景色を設定.
        self.setBackgroundColor(theBackColor)

        #表示テキストを設定.
        self.setText(theText)
        
        if(self.__DEBUG__): print("ViewCell.draw.BackColor:{0}".format(theBackColor))
        if(self.__DEBUG__): print("ViewCell.draw.ForeColor:{0}".format(theForeColor))
        if(self.__DEBUG__): print("ViewCell.draw.text:{0}".format(theText))
        if(self.__DEBUG__): print("ViewCell.draw.Image:{0}".format(theImage))

class ViewWidget(QtGui.QMainWindow, Ui_Widget):
    __DEBUG__ = False
    SIZE = 30
    INTERVAL = 30

    def __init__(self, *args, **kw):
        QtGui.QMainWindow.__init__(self, *args, **kw)
        self.setupUi(self)

        #Dijkstra設定を生成.
        self.controller_dijikstra = ControllerDijkstra()

        self.set_Geometry_size(self.SIZE, self.SIZE)

        #ダブクリックで編集しないようにする.
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        #self.setFixedSize(370, 400)

        #タイマーの設定.
        self._interval = self.INTERVAL
        self._timer = QtCore.QTimer(parent=self)
        self._timer.setInterval(self._interval)
        #タイマーと動作を繋げる.
        self._timer.timeout.connect(self.do_loop)

        #ボタンと動作を繋げる.
        self.startButton.clicked.connect(self.start_action)
        self.stopButton.clicked.connect(self.stop_action)
        self.openButton.clicked.connect(self.open_action)
        self.resetButton.clicked.connect(self.reset_action)

        #マップを開く.
        self.open_action()

        #初期はストップボタンを押下したのと同等状態とする.
        self.stop_action()

   
    def set_Geometry_size(self, i_Row, i_Col):
        self.tableWidget.setRowCount(i_Row)
        self.tableWidget.setColumnCount(i_Col)

        Hsize = self.tableWidget.horizontalHeader().defaultSectionSize()
        Vsize = self.tableWidget.verticalHeader().defaultSectionSize()
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, (i_Row+2)*Vsize, (i_Col+2)*Hsize))

        for theRow in range(i_Row):
            for theCol in range(i_Col):
                theItem = ViewCell()
                self.tableWidget.setItem(theRow, theCol, theItem)


    def do_loop(self):
        if(0==len(self.controller_dijikstra.routeList)):
            self.stop_action()
            return

        theNode = self.controller_dijikstra.routeList.pop(0)
        if(None == theNode):
            self.stop_action()
            return

        if("Start" == theNode.__str__()): return
        if("Goal" == theNode.__str__()): return
            
        theX = theNode.x
        theY = theNode.y
        theItem = self.tableWidget.item(theY, theX)
        theItem.setSelected(True)
       
    def start_action(self):
        """
        @brief    スタートボタン 押下.
        """
        #選択不可に設定.
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)

        #ダクストラを設定.
        self.controller_dijikstra.make_dijkstra(30, 30, self.tableWidget)

        #ルート探索.
        self.controller_dijikstra.search_root()

        #デバッグ用に最短ルートを出力.
        if(self.__DEBUG__): self.controller_dijikstra.print_debug_min_route()

        #更新用タイマースタート.
        self._timer.start()


    def stop_action(self):
        """
        @brief    ストップボタン 押下.
        """
        ##表示用セルを選択可に設定.
        #self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        #選択不可に設定.
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        #更新用タイマーストップ.
        self._timer.stop()

    def open_action(self):
        """
        @brief    オープンボタン 押下.
        """
        ##表示用セルを選択可に設定.
        #self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        #選択不可に設定.
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        #更新用タイマーストップ.
        self._timer.stop()

        #マップを読み込み.
        self.controller_dijikstra.set_map(self.tableWidget)

    def reset_action(self):
        """
        """
        #選択不可に設定.
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        #更新用タイマーストップ.
        self._timer.stop()

        #ダイクストラをクリア.
        self.controller_dijikstra.clear()

        for theRow in range(self.SIZE):
            for theCol in range(self.SIZE):
                theItem = ViewCell()
                self.tableWidget.setItem(theRow, theCol, theItem)
                theItem.setSelected(False)

class ControllerDijkstra(object):
    def __init__(self):
        self.dijkstra = Dijkstra()
        self.routeList = []

    def set_map(self, i_TableWidget):
        theFactory = StateCellFactory()
        theMapStrList = [
            ["W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W"],
            ["W",     "S",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "W",     "W",     "R",     "W",     "W",     "W",     "R",     "W",     "R",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W",     "W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "W",     "R",     "W",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "W",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "W",     "R",     "W",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "W",     "R",     "R",     "W",     "R",     "W",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "R",     "R",     "R",     "R",     "W",     "R",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "R",     "R",     "W"],
            ["W",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "R",     "W"],
            ["W",     "R",     "W",     "W",     "W",     "W",     "W",     "R",     "R",     "R",     "R",     "R",     "R",     "W",     "R",     "R",     "W",     "W",     "W",     "R",     "R",     "R",     "R",     "W",     "W",     "W",     "W",     "W",     "G",     "W"],
            ["W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W",     "W"],
        ]
#        theMapStrList = [
#                ["W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W"],
#                ["W",        "G",        "W",        "W",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "R",        "R",        "R",        "R",        "R",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W"],
#                ["W",        "W",        "W",        "R",        "W",        "W",        "R",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "W",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "S",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "R",        "W",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W",        "R",        "W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "W",        "R",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "R",        "R",        "W"],
#                ["W",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "R",        "W"],
#                ["W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W",        "W"],
#        ]
        theConvertDict = { "W":theFactory.WALL, "R":theFactory.ROAD, "S":theFactory.START, "G":theFactory.GOAL }
        for theRow in range(len(theMapStrList)):
            for theCol in range(len(theMapStrList[theRow])):
                theChar = theMapStrList[theRow][theCol]
                theState = theConvertDict[theChar]
                theItem = i_TableWidget.item(theRow, theCol)
                theItem.change_state(theState)
                #NodeのX座標とY座標を設定.
                theItem.state.x = theCol
                theItem.state.y = theRow
                #ダイクストラへスタート地点ととゴール地点を設定.
                if("S"==theChar): self.dijkstra.start = theItem.state
                if("G"==theChar): self.dijkstra.goal = theItem.state

    def get_neighbor_list(self, i_Row, i_Col, i_TableWidget):
        """
        @brief    隣接Nodeを取得.
        """
        theNeighborList = []

        theRowRelativeList = [-1,  0,  1,  0]    #縦方向 相対位置. ("上右下左"の順で並んでいる）.
        theColRelativeList = [ 0,  1,  0, -1]    #横方向 相対位置. ("上右下左"の順で並んでいる）.

        for theIndex in range(0, 4):
            theNeighborRow = i_Row + theRowRelativeList[theIndex]        #隣接Node 縦方向 Index.
            theNeighborCol = i_Col + theColRelativeList[theIndex]        #隣接Node 横方向 Index.
            theNeighbor = i_TableWidget.item(theNeighborRow, theNeighborCol).state    #隣接Nodeを取得.
            theNeighborList.append(theNeighbor)
        return theNeighborList

    def make_dijkstra(self, i_RowMax, i_ColMax, i_TableWidget):
        """
        @brief    ダイクストラクラスを生成.
        """
        for theRow in range(0, i_RowMax):
            for theCol in range(0, i_ColMax):
                theNode = i_TableWidget.item(theRow, theCol).state

                #Wallならば,ダイクストラにNodeを追加しない.
                if( "Wall" == theNode.__str__() ): continue
                #ダイクストラにNodeを追加.
                self.dijkstra.add_node(theNode)

                #隣接Nodeを取得.
                theNeighborList = self.get_neighbor_list(theRow, theCol, i_TableWidget)

                for theNeighbor in theNeighborList:
                    #Wallならば,リンクは作成しない.
                    if( "Wall" == theNeighbor.__str__() ): continue
                    #Node間をリンクさせる.
                    self.dijkstra.connect_node(theNode, theNeighbor)

    def search_root(self):
        self.dijkstra.search_root()

        theNode = self.dijkstra.start
        while(theNode != self.dijkstra.goal):
            self.routeList.append(theNode)
            if(theNode != None): theNode = theNode.toGoal
            else: break
        self.routeList.append(self.dijkstra.goal) 

    def clear(self):
        self.dijkstra.clear()
        self.routeList = []

        
    def print_debug_min_route(self):
        print("ControllerDijkstra: min route")
        for theIndex in range(len(self.routeList)):
            theNode = self.routeList[theIndex]
            if(None == theNode):
                print("ControllerDijkstra: do not reach goal.")
                return
            print( " {0}: {1}[{2} {3}]".format(theIndex, theNode, theNode.x, theNode.y) )
            theIndex += 1


def main():
    app = QtGui.QApplication(sys.argv)

    panel = ViewWidget()

    main_window = QtGui.QMainWindow()
    main_window.setWindowTitle("Dijkstra")
    main_window.setCentralWidget(panel)
    main_window.show()

    app.exec_()

if __name__ == '__main__':
    main()

