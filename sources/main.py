#! /usr/bin/python
# -*- coding: utf-8 -*-

#Widgetの変換方法.
#%python /Library/Python/2.7/site-packages/PyQt4/uic/pyuic.py ./View/GUI/widget.ui -o ./View/widget.py

import sys
import PyQt4.QtGui as QtGui

#Controller
from Controller.ControllerWidget import ViewWidget

def main():
    """
    @brief  メイン.
    """
    app = QtGui.QApplication(sys.argv)

    panel = ViewWidget()

    main_window = QtGui.QMainWindow()
    main_window.setWindowTitle("Dijkstra")
    main_window.setCentralWidget(panel)
    main_window.show()

    app.exec_()

if __name__ == '__main__':
    main()

