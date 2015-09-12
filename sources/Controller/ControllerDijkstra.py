#! /usr/bin/python
# -*- coding: utf-8 -*-

#csv
import csv
import io

#Model
from Model.Dijkstra import Dijkstra

#Controller
from Controller.StateCell import StateCellFactory

class ControllerDijkstra(object):
    """
    @brief  Dijkstraのコントローラ.
    """

    #初期マップの文字列定数.
    __INITIAL_MAP_STR__ = """W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W
W	S	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	W
W	R	W	R	W	W	W	R	W	W	W	R	W	R	W	W	W	W	W	W	W	W	W	R	R	R	R	R	R	W
W	R	W	R	W	R	R	R	R	R	W	R	W	R	R	R	R	R	R	R	R	W	R	W	R	R	R	R	R	W
W	R	W	R	W	R	R	R	R	R	W	R	R	W	R	R	R	R	R	R	R	W	R	R	W	R	R	R	R	W
W	R	W	R	W	R	R	R	R	R	W	R	R	R	W	R	R	R	R	R	R	W	R	R	R	W	R	R	R	W
W	R	W	R	W	R	R	R	R	R	W	R	R	R	R	W	R	R	R	R	R	W	R	R	R	R	W	R	R	W
W	R	W	R	W	R	R	R	R	R	W	R	R	R	R	R	W	R	R	R	R	W	R	R	R	R	R	W	R	W
W	R	W	R	W	R	R	R	R	R	W	R	R	R	R	W	R	W	R	R	R	W	R	R	R	R	R	R	R	W
W	R	W	R	W	R	R	R	R	R	W	R	R	R	W	R	R	R	W	R	R	W	W	W	W	W	W	W	R	W
W	R	W	R	W	R	R	R	R	R	W	R	R	W	R	R	R	R	R	W	R	R	R	W	R	W	R	R	R	W
W	R	W	R	W	R	R	R	R	R	W	R	W	R	R	R	R	R	R	R	W	W	R	W	R	W	R	R	R	W
W	R	W	R	W	R	R	R	R	R	W	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	W
W	R	W	R	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	R	W
W	R	W	R	R	W	R	W	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	W
W	R	W	R	W	R	R	W	R	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	R	R	W
W	R	W	R	W	R	R	W	R	W	R	R	R	W	R	R	R	W	R	R	R	W	R	R	R	W	R	R	R	W
W	R	W	R	W	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	R	R	W
W	R	W	R	W	R	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	W	R	W	W
W	R	W	R	W	R	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	R	R	W
W	R	W	R	W	R	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W
W	R	W	R	W	R	W	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	R	R	W
W	R	W	R	W	R	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	W	R	W	W
W	R	W	R	W	R	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	R	R	W
W	R	W	R	W	R	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W	R	W
W	R	W	R	W	R	R	W	R	W	R	W	R	R	R	W	R	R	R	W	R	R	R	W	R	R	R	R	R	W
W	R	W	R	R	R	R	W	R	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	R	R	W
W	R	R	R	R	R	R	R	R	W	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	R	W
W	R	W	W	W	W	W	R	R	R	R	R	R	W	R	R	W	W	W	R	R	R	R	W	W	W	W	W	G	W
W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W	W"""

    def __init__(self):
        """
        @brief  ControllerDijkstraの初期化.
        """
        self.dijkstra = Dijkstra()
        self.routeList = []

    def set_any_map(self, i_TableWidget):
        """
        @brief  ファイルからマップを設定.
        @note   map.tsvの書式
                タブ区切りのTSVとする.
                30x30のます目を想定している.それ以外では動作はどうなるかわからない.
                各ます目は以下のアルファベット1文字によって構成される.
                    W: 壁
                    R: 道
                    S: スタート
                    G: ゴール
                ex. 参考として次の変数を参照すること→self.__INITIAL_MAP_STR__
        """
        theFileHandler = open("map.tsv", "r")
        theMapStrList = self.csv_to_list(theFileHandler)
        theFileHandler.close()
        #マップを設定（実処理）.
        self.set_map_implement(i_TableWidget, theMapStrList)

    def set_initial_map(self, i_TableWidget):
        """
        @brief  初期マップを設定.
        """
        csv_string = self.__INITIAL_MAP_STR__
        csv_filehandler = io.StringIO(csv_string)
        theMapStrList = self.csv_to_list(csv_filehandler)
        csv_filehandler.close()
        #マップを設定（実処理）.
        self.set_map_implement(i_TableWidget, theMapStrList)

    def csv_to_list(self, i_csv_filehandler):
        """
        @brief  csvを2次元リストに変換する.
        """
        theReader = csv.reader(i_csv_filehandler, delimiter="\t")
        theMapStrList = []
        for theRow in theReader:
            theLine = []
            for theElement in theRow:
                theLine.append(theElement)
            theMapStrList.append(theLine)
        return theMapStrList
        
    def set_map_implement(self, i_TableWidget, i_MapStrList):
        """
        @brief  マップを設定（実処理）.
        """
        theFactory = StateCellFactory()
        theConvertDict = { "W":theFactory.WALL, "R":theFactory.ROAD, "S":theFactory.START, "G":theFactory.GOAL }
        for theRow in range(len(i_MapStrList)):
            for theCol in range(len(i_MapStrList[theRow])):
                theChar = i_MapStrList[theRow][theCol]
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
        @brief      ダイクストラクラスを生成.
        @note       T.B.A. 作りがひどい！！要リファクタ.
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
        """
        @brief  最短ルートを探索.
        """
        self.dijkstra.search_root()

        theNode = self.dijkstra.start
        while(theNode != self.dijkstra.goal):
            self.routeList.append(theNode)
            if(theNode != None): theNode = theNode.toGoal
            else: break
        self.routeList.append(self.dijkstra.goal) 

    def clear(self):
        """
        @brief  ダイクストラをクリア.
        """
        self.dijkstra.clear()
        self.routeList = []

        
    def print_debug_min_route(self):
        """
        @brief  デバッグ用に値を出力.
        """
        print("ControllerDijkstra: min route")
        for theIndex in range(len(self.routeList)):
            theNode = self.routeList[theIndex]
            if(None == theNode):
                print("ControllerDijkstra: do not reach goal.")
                return
            print( " {0}: {1}[{2} {3}]".format(theIndex, theNode, theNode.x, theNode.y) )
            theIndex += 1

