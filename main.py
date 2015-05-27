#! /usr/bin/python
# -*- coding: utf-8 -*-

#Widgetの変換方法.
#%python /Library/Python/2.7/site-packages/PyQt4/uic/pyuic.py ./GUI/widget.ui -o widget.py

import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

from View.widget import Ui_Widget

from Model.Dijkstra import Dijkstra
from Model.Dijkstra import Node
from Model.Dijkstra import Edge

class ViewCell(QtGui.QTableWidgetItem):
	pass

class Wall(ViewCell, Node):
	"""
	@brief	壁 クラス.
	"""
	pass
class Road(ViewCell, Node):
	"""
	@brief	道 クラス.
	"""
	pass
class Start(Road):
	"""
	@brief	スタート地点 クラス.
	"""
	pass
class Goal(Road):
	"""
	@brief	ゴール地点 クラス.
	"""
	pass

class ViewWidget(QtGui.QMainWindow, Ui_Widget):
	INTERVAL = 200
	SIZE = 30

	def __init__(self, *args, **kw):
		QtGui.QMainWindow.__init__(self, *args, **kw)
		self.setupUi(self)

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
		self.onceButton.clicked.connect(self.once_action)

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
				theItem = Road()
				self.tableWidget.setItem(theRow, theCol, theItem)

	def do_loop(self):
		pass
		
	def start_action(self):
		"""
		@brief	スタートボタン 押下.
		"""
		#選択不可に設定.
		self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
		#ダクストラを設定.

		#更新用タイマースタート.
		self._timer.start()

	def stop_action(self):
		"""
		@brief	ストップボタン 押下.
		"""
		#表示用セルを選択可に設定.
		self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		#更新用タイマーストップ.
		self._timer.stop()

	def once_action(self):
		"""
		@brief	ワンスボタン 押下.
		"""
		#表示用セルを選択可に設定.
		self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		#更新用タイマーストップ.
		self._timer.stop()


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

