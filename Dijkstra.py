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

	def __init__(self):
		"""
		@brief	ノードの初期化.
		"""
		self._x = 0				#ノードX座標.
		self._y = 0				#ノードY座標.
		self._edgeList = []		#接続されているノード.接続にはEdgeクラスを使用する.
		self._cost = -1			#現ノードからゴールまでのコスト.
		self._toGoal = None		#ゴールまで至る次のノード.

	def __str__(self):
		theStr = "Node"
		if(self.__DEBUG__):
			theStr = theStr + "\n"
			theStr = "%s\t (x y)=(%d %d)"%(self.x, self.y)
			theStr = "%s\t edge=%s"%(self._edgeList)
			theStr = "%s\t cost=%d"%(self.cost)
			theStr = "%s\t toGoal=%s"%(self._toGoal)
		return theStr

	def __repr__(self):
		# Return a string representation.
		return "<Node>"

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
		@brief	Node間の距離を計算する.
		"""
		theLen = (self.x-i_Node.x)*(self.x-i_Node.x) + (self.y-i_Node.y)*(self.y-i_Node.y)
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
	def numNode(self):
		"""
		@brief	ノード数を取得.
		"""
		return len(self._nodeList)

	def get_node_from_point(self, i_X, i_Y):
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
			theCurrentLevel = theNextLevel
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
			theNode = Node()
			self.assertEqual(0, theNode.x)
			self.assertEqual(0, theNode.y)
			self.assertEqual([], theNode.get_edge_list())
			self.assertEqual(-1, theNode.cost)
			self.assertEqual(None, theNode.toGoal)
		def test_reset(self):
			"""
			@brief	Node.reset()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_connect_node(self):
			"""
			@brief	Node.connect_node()のテストケース.
			@note	2つのノードが接続できていればOK.
			@note	2つのノードのコストが1であればOK. （初期値は1）
			"""
			#前処理. Nodeクラスを2個生成し, 接続する.
			theNode1 = Node()
			theNode1.x = 0
			theNode1.y = 0
			theNode2 = Node()
			theNode2.x = 0
			theNode2.y = 0
			theNode1.connect_node(theNode2, 1)
			#2個のNodeが接続されていることを確認.
			theEdgeList = theNode1.get_edge_list()
			self.assertEqual(theNode2, theEdgeList[0].node)
			#2個のNode間のコストが1であることを確認.
			self.assertEqual(1, theEdgeList[0].cost)
		def test_set_among_node_cost(self):
			"""
			@brief	Node.set_among_node_cost()のテストケース.
			@note	2つのNode間のコストが変更できていればOK.
			"""
			#前処理. Nodeクラスを2個生成し, 接続する.
			theNode1 = Node()
			theNode1.x = 0
			theNode1.y = 0
			theNode2 = Node()
			theNode2.x = 0
			theNode2.y = 1
			theNode1.connect_node(theNode2, 1)
			#接続されているNode間のコストを変更.
			theNode1.set_among_node_cost(theNode2, 2)
			#Node間のコストが変更されていることを確認.
			theEdgeList = theNode1.get_edge_list()
			self.assertEqual(2, theEdgeList[0].cost)
		def test_remove_connect(self):
			"""
			@brief	Node.remove_connect()のテストケース.
			@note	接続したノードが削除できていればOK.
			"""
			#前処理. Nodeクラスを2個生成し, 接続する.
			theNode1 = Node()
			theNode1.x = 0
			theNode1.y = 0
			theNode2 = Node()
			theNode2.x = 0
			theNode2.y = 1
			theNode1.connect_node(theNode2, 1)
			#Nodeの接続を削除.
			theNode1.remove_connect(theNode2)
			#Nodeの接続が削除されている事を確認.
			theEdgeList = theNode1.get_edge_list()
			self.assertEqual([], theEdgeList)
		def test_distance(self):
			"""
			@brief	Node.distance()のテストケース.
			@note	ノード間の距離が計算できていればOK.
			"""
			#前処理. Nodeクラスを2個生成.
			theNode1 = Node()
			theNode1.x = 0
			theNode1.y = 0
			theNode2 = Node()
			theNode2.x = 0
			theNode2.y = 1
			#2つのNode間の距離を計算.
			theDistance = theNode1.distance(theNode2)
			#2つのNode間の距離を確認. ※(0,0)と(0,1)の距離.
			self.assertEqual(1, theDistance)

	class TestCaseDijkstra(unittest.TestCase):
		"""
		@brief	Dijkstraクラス テストケース.
		"""
		def setUp(self):
			pass
		def tearDown(self):
			pass
		def test_create(self):
			"""
			@brief	Dijkstraの生成 テストケース.
			@note	Dijkstra.startがNoneならばOK.
			@note	Dijkstra.goalがNoneならばOK.
			@note	Dijkstra.sizeが0ならばOK. （登録されているノードが0）.
			"""
			#前処理. Dijkstraクラスを生成.
			theDijkstra = Dijkstra()
			#Dijkstra.startがNoneであることを確認.
			self.assertEqual(None, theDijkstra.start)
			#Dijkstra.goalがNoneであることを確認.
			self.assertEqual(None, theDijkstra.goal)
			#Dijkstra.sizeが0であることを確認.　（Nodeが登録されていない事を確認）.
			self.assertEqual(0, theDijkstra.numNode)
		def test_add_node(self):
			"""
			@brief	Dijkstra.add_node()のテストケース.
			@note	ダイクストラにノードを1つ追加し, 追加されているノード数が1であればOK.
			"""
			#前処理.
			theDijkstra = Dijkstra()
			theNode = Node()
			#ダイクストラにノードを追加.
			theDijkstra.add_node(theNode)
			#ダイクストラに追加されているノードが1である事を確認.
			self.assertEqual(1, theDijkstra.numNode)
		def test_node_from_point(self):
			"""
			@brief	Dijkstra.get_node_from_point()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_node_from_index(self):
			"""
			@brief	Dijkstra.get_node_from_index()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_get_index(self):
			"""
			@brief	Dijkstra.get_index()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_celar(self):
			"""
			@brief	Dijkstra.clear()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_remove_node(self):
			"""
			@brief	Dijkstra.remove_node()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_remove_connect(self):
			"""
			@brief	Dijkstra.remove_connect()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_connect_node(self):
			"""
			@brief	Dijkstra.connect_node()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_reset_node(self):
			"""
			@brief	Dijkstra.reset_node()のテストケース.
			@note	TBA.未着手.
			"""
			pass
		def test_search_root(self):
			"""
			@brief	Dijkstra.search_root()のテストケース.
			@note	TBA.未着手.
			"""
			pass


	
	#ユニットテスト実行.
	unittest.main()
