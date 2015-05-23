#! /usr/bin/python
# -*- coding: utf-8 -*-

# 参考URL.
# ダイクストラ法による最短ルートの求めかた
# http://www.sousakuba.com/Programming/algo_root.html

import sys
import math

class Node(object):
	"""
	@brief	ノード クラス.
	"""

	def __init__(self, i_X, i_Y):
		"""
		@brief	ノードの初期化.
		"""
		self._x = i_X
		self._y = i_Y
		self._edgeList = []
		self._cost = -1
		self._toGoal = None
	
	def __del__(self):
		"""
		@brief	
		@note	self._edgeListを空にした方がよい？
		"""
		pass

	#座標X getter/setter.
	@property
	def x(self): return self._x
	@x.setter
	def x(self, i_X): self._x = i_X

	#座標Y getter/setter.
	@property
	def y(self): return self._y
	@y.setter
	def y(self, i_Y): self._y = i_Y

	#コスト getter/setter.
	@property
	def cost(self): return self._cost
	@cost.setter
	def cost(self, i_Cost): self._cost = i_Cost

	#ゴールへのNode getter/setter.
	@property
	def toGoal(self): return self._toGoal
	@toGoal.setter
	def toGoal(self, i_Node): self._toGoal = i_Node

	#接続されているNodeを取得. 
	#(EdgeクラスにNodeが保存されている為, Edgeクラスのリストを返す.)
	def get_edge_list(self): return self._edgeList

	def reset(self):
		"""
		@brief	計算結果をクリア.
		"""
		self._cost = -1
		self._toGoal = None

	def connect_node(self, i_Node, i_Cost):
		"""
		@brief	ノードを接続.
		"""
		#同一ノードでないか.
		if(i_Node == self): return False	#Nodeの接続に失敗
		#登録済みでないか.
		for theEdge in self._edgeList:
			if(i_Node == theEdge.node): return False #Nodeの接続に失敗.

		#Node接続.
		self._edgeList.append( Edge(i_Node, i_Cost) )

		return True	#Nodeの接続に成功.

	def set_among_node_cost(self, i_Node, i_Cost):
		"""
		@brief	Node間のコストを設定する.
		"""
		for theEdge in self._edgeList:
			if(i_Node == theEdge.node):
				#Nodeが見つかった場合.
				theEdge.cost = i_Cost
				#Node間のコスト設定に成功.
				return True	

		#Nodeが見つからなかった場合.
		#Node間のコスト設定に失敗.
		return False	


	def remove_connect(self, i_Node):
		"""
		@brief	特定ノードへの接続を削除.
		"""
		for theEdge in self._edgeList:
			theNode = theEdge.node
			if(i_Node == theEdge.node):
				self._edgeList.remove(theEdge)
				break
	
	def distance(self, i_Node):
		"""
		@brief	Nodeの距離を計算する.
		"""
		theLen = (self._x-i_Node._x)*(self._x-i_Node._x) + (self._y-i_Node._y)*(self._y-i_Node._y)
		return math.sqrt(theLen)


class Edge(object):
	"""
	@brief	エッジ クラス.
	"""

	def __init__(self, i_Node, i_Cost):
		"""
		@brief	エッジの初期化.
		"""
		self.node = i_Node
		self.cost = i_Cost


class Dijkstra(object):
	__DEBUG__ = False

	"""
	@brief	ダイクストラ法 クラス.
	"""

	def __init__(self):
		"""
		@brief	ダイクストラ法の初期化.
		"""
		self._start = None
		self._goal = None
		self._nodeList = []

	#スタートNodeのgetter/setter.
	@property
	def start(self): return self._start
	@start.setter
	def start(self, i_Node):
		self._start = i_Node
		if(self.__DEBUG__): print("Dijkstra.start:[%2d %2d]")%(self._start.x, self._start.y)

	#ゴールNodeのgetter/setter.
	@property
	def goal(self): return self._goal
	@goal.setter
	def goal(self, i_Node):
		self._goal = i_Node
		if(self.__DEBUG__): print("Dijkstra.goal:[%2d %2d]")%(self._goal.x, self._goal.y)

	@property
	def size(self):
		"""
		@brief	ノード数を取得.
		"""
		return len(self._nodeList)

	def get_node_form_point(self, i_X, i_Y):
		"""
		@brief	座標を指定してノードを取得.
		"""
		for theNode in self._nodeList:
			if( (i_X==theNode.x) and (i_Y==theNode.y) ): return theNode

		return None

	def get_node_from_index(self, i_Index):
		"""
		@brief	インデックスを指定してノードを取得.
		"""
		#インデックスの範囲チェック.
		if( (0>i_Index) or (len(self._nodeList)<=i_Index) ): return None
		return self._nodeList[i_Index]

	def get_index(self, i_Node):
		"""
		@brief	ノードがリストのの何番目か
		@note	0オリジン. Nodeが見つけれなかった場合-1.
		"""
		for theIndex in range(0, len(self._nodeList)):
			if(i_Node == self._nodeList[theIndex]): return theIndex

		return -1

	def add_node(self, i_Node):
		"""
		@brief	ノードを追加.
		"""
		self._nodeList.append(i_Node)

	def clear(self):
		"""
		@brief	全ノードを削除.
		"""
		self.start = None
		self.goal = None
		self._nodeList = []

	def remove_node(self, i_Node):
		"""
		@brief	指定ノードを削除.
		"""
		for theNode in self._nodeList:
			if(i_Node == theNode):
				self._nodeList.remove(i_Node)

	def remove_connect(self, i_Node1, i_Node2):
		"""
		@brief	指定ノード接続を削除.
		"""
		#i_Node1からi_Node2の接続を削除.
		i_Node1.remove_connect(i_Node2)
		#i_Node2からi_Node1の接続を削除.
		i_Node2.remove_connect(i_Node1)

	def connect_node(self, i_Node1, i_Node2):
		"""
		@brief	2点間のノードを接続.
		"""
		#コスト=距離計算.
		theCost = int(i_Node1.distance(i_Node2))

		#接続.
		i_Node1.connect_node(i_Node2, theCost)
		i_Node2.connect_node(i_Node1, theCost)

	def reset_node(self):
		"""
		@brief	各ノードをリセット.
		"""
		for theNode in self._nodeList:
			if(self.__DEBUG__): print("Clear[%2d %2d]")%(theNode.x, theNode.y)
			theNode.reset()
	
	def search_root(self):
		"""
		@brief	ルート検索開始.
		"""
		#全ノードの計算結果をリセット.
		self.reset_node()

		#スタート地点とゴール地点が設定されていなければ.
		if( (None==self.start) or (None==self.goal) ): return
		if(self.__DEBUG__): print("Dijkstra.search_root: start")


		#検索第一階層のノードリスト.
		theCurrentLevel = []
		#検索第二階層のノードリスト.
		theNextLevel = []

		#ゴールにコスト0をセットして計算済みとする.
		self.goal.cost = 0
		#検索第一階層のノードにゴールNodeを設定する.
		theCurrentLevel.append(self.goal)

		while( 0!=len(theCurrentLevel) ):
			for theNode in theCurrentLevel:
				for theEdge in theNode.get_edge_list():
					theCost = theNode.cost + theEdge.cost

					if( (theEdge.node.cost==-1) or (theCost<theEdge.node.cost) ):
						#未探索Node or 最短ルートを更新できる場合.

						#経路コストとゴールへ向かう為のNodeをセット.
						theEdge.node.cost = theCost
						theEdge.node.toGoal = theNode
						if(self.__DEBUG__): print(" Dijkstra.SetToGoal:[%2d %2d]")%(theEdge.node.toGoal.x, theEdge.node.toGoal.y)
					else:
						continue

					#次に探索する階層のリストに登録.
					theNextLevel.append(theEdge.node)

			#リストを入れ替えて次の階層を検索する.
			theSwapTemp = theCurrentLevel
			theCurrentLevel = theNextLevel
			theNextLevel = theSwapTemp
			theNextLevel = []

		#探索終了.
		if(self.__DEBUG__): print("Dijkstra.search_root: end")
		return



if __name__ == "__main__":
	########################################################
	# テスト関数とメイン関数.
	########################################################
	import unittest

	class TestCaseEdge(unittest.TestCase):
		"""
		@brief	Edgeクラス テストケース.
		"""
		def setUp(self):
			pass
		def tearDown(self):
			pass
		def test_create(self):
			theEdge = Edge(None, 0)
			self.assertEqual(None, theEdge.node)
			self.assertEqual(0, theEdge.cost)
	
	class TestCaseNode(unittest.TestCase):
		"""
		@brief	Nodeクラス テストケース.
		"""
		def setUp(self):
			pass
		def tearDown(self):
			pass
		def test_create(self):
			theNode = Node(0, 0)
			self.assertEqual(0, theNode.x)
			self.assertEqual(0, theNode.y)
			self.assertEqual([], theNode.get_edge_list())
			self.assertEqual(-1, theNode.cost)
			self.assertEqual(None, theNode.toGoal)
		def test_connect_node(self):
			theNode1 = Node(0, 0)
			theNode2 = Node(0, 1)
			theNode1.connect_node(theNode2, 1)
			theEdgeList = theNode1.get_edge_list()
			self.assertEqual(theNode2, theEdgeList[0].node)
			self.assertEqual(1, theEdgeList[0].cost)
		def test_set_among_node_cost(self):
			theNode1 = Node(0, 0)
			theNode2 = Node(0, 1)
			theNode1.connect_node(theNode2, 1)
			theNode1.set_among_node_cost(theNode2, 2)
			theEdgeList = theNode1.get_edge_list()
			self.assertEqual(2, theEdgeList[0].cost)
		def test_remove_connect(self):
			theNode1 = Node(0, 0)
			theNode2 = Node(0, 1)
			theNode1.connect_node(theNode2, 1)
			theNode1.remove_connect(theNode2)
			theEdgeList = theNode1.get_edge_list()
			self.assertEqual([], theEdgeList)
		def test_distance(self):
			theNode1 = Node(0, 0)
			theNode2 = Node(0, 1)
			theDistance = theNode1.distance(theNode2)
			self.assertEqual(1, theDistance)

	class TestCaseDijkstra(unittest.TestCase):
		"""
		@brief	Dijkstraクラス テストケース.
		"""
		def setUp(self):
			pass
		def tearDown(self):
			pass
	
	#ユニットテスト実行.
	unittest.main()
