[Dijkstra法で最短ルートを求める](https://github.com/kantoku009/Dijkstra)
====
#はじめに
ダイクストラ法で最短距離を求めるPythonプログラムを作成した.  
以下図のように任意のマップにて最短ルートを求めることができる.  
![最短ルート1](./image/ShortestRoute/Dijkstra1.gif)
![最短ルート2](./image/ShortestRoute/Dijkstra2.gif)

GitHubのリポジトリと全ソースコードのダウンロードは以下URLから行える.  

- [GitHub リポジトリ](https://github.com/kantoku009/Dijkstra)
- [全ソースコード ダウンロード](https://github.com/kantoku009/Dijkstra/archive/master.zip)

----

#使用方法
使用方法を記す.  

	ターミナルから以下を実行.
		%python main.py

各ボタンの動作は以下を参照.

 - Start:最短ルート探索をスタート
		Stop:最短ルート探索を停止
		Map:マップをファイルから読み込む(./sources/map.tsvを読み込む)
		Rest:マップをリセット

[map.tsv](./sources/map.tsv)について記す.

	タブ区切りのTSVとする.
	30x30のます目を想定している.それ以外では動作はどうなるかわからない.
	各ます目は以下のアルファベット1文字によって構成される.
		W: 壁
		R: 道
		S: スタート
		G: ゴール

----

#UML
クラス図とシーケンス図を作成した.  
以下からダウンロード可能.  

- [UML](./UML/UML.asta)

UMLの作成には無償のUMLモデリングツール[astah community](http://astah.change-vision.com/ja/)を使用している.  

----

#参考情報
##ダイクストラ法
ダイクストラ法は以下のWeb Pageを参考にした.  

- [ダイクストラ法による最短ルートの求めかた](http://www.sousakuba.com/Programming/algo_root.html)


