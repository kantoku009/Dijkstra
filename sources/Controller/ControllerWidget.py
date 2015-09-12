#! /usr/bin/python
# -*- coding: utf-8 -*-

#PyQt
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

#View
from View.widget import Ui_Widget

#Controller
from Controller.StateCell import StateCellFactory
from Controller.ControllerDijkstra import ControllerDijkstra

class ViewCell(QtGui.QTableWidgetItem):
    __DEBUG__ = False

    def __init__(self):
        """
        @brief  ViewCellの初期化.
        """
        QtGui.QTableWidgetItem.__init__(self)
        self.state = None
        self.state_factory = StateCellFactory()
        self.change_state(StateCellFactory.ROAD)

    def change_state(self, i_State):
        """
        @brief  ステートを変更.
        """
        self.state = self.state_factory.create(i_State)
        self.draw()

    def draw(self):
        """
        @brief  セルをステートに合わせて描画.
        """
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
        """
        @brief  ViewWidgetの初期化.
        """
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

        #マップをリセット.
        self.reset_action()

        #初期はストップボタンを押下したのと同等状態とする.
        self.stop_action()

   
    def set_Geometry_size(self, i_Row, i_Col):
        """
        @brief  TableWidgetの設定.
        """
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
        """
        @brief  タイマーカウント 動作
        """
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
        self.controller_dijikstra.make_dijkstra(self.SIZE, self.SIZE, self.tableWidget)

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
        self.reset_action()
        #テキストファイルからマップを読み込み.
        self.controller_dijikstra.set_any_map(self.tableWidget)
        self.open_action_implement()

    def open_action_implement(self):
        ##表示用セルを選択可に設定.
        #self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        #選択不可に設定.
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        #更新用タイマーストップ.
        self._timer.stop()
   
    def reset_action(self):
        """
        @brief  リセットボタン 押下.
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

        #初期マップを読み込み.
        self.controller_dijikstra.set_initial_map(self.tableWidget)
        self.open_action_implement()


