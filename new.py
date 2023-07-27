import networkx as nx

import pandas as pd
import numpy as np
import networkx as nx
import operator
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from mysql import read_url

DATA_SQL = """
    SELECT * FROM COHERENCE;
"""
COLUMNS_SQL = """
    SELECT COLUMN_NAME FROM (
	SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE 1=1 AND TABLE_NAME="COHERENCE") C
    ;
"""

RESULT = read_url(DATA_SQL)
COLUMNS = read_url(COLUMNS_SQL)
COLUMNS = [col[0] for col in COLUMNS]
dataset = pd.DataFrame(RESULT, columns=COLUMNS)
print(dataset.head(10))

#----- 중심성 구하기
"""
중심성은 Graph에 edge를 추가하여 구한다.
연결, 매개, 근접, 위세, 페이지랭크 다섯가지가 있다.
"""

G_centrality = nx.Graph()
for i in range(len(dataset[dataset['freq']>=10])):
    G_centrality.add_edge(dataset['word1'][i], dataset['word2'][i], weight=dataset['freq'][i])

dgr = nx.degree_centrality(G_centrality)#연결중심성
btw = nx.betweenness_centrality(G_centrality)#매개
cls = nx.closeness_centrality(G_centrality)#근접
egv = nx.eigenvector_centrality(G_centrality)#위세
pgr = nx.pagerank(G_centrality) #페이지랭크
print("연결중심성", dgr)
print("매개중심성", btw)
print("근접중심성", cls)
print("위세중심성", egv)
print("페이지랭크", pgr)

sorted_dgr = sorted(dgr.items(), key=lambda item: item[1], reverse=True)
sorted_btw = sorted(btw.items(), key=lambda item: item[1], reverse=True)
sorted_cls = sorted(cls.items(), key=lambda item: item[1], reverse=True)
sorted_egv = sorted(egv.items(), key=lambda item: item[1], reverse=True)
sorted_pgr = sorted(pgr.items(), key=lambda item: item[1], reverse=True)
print("정렬 연결중심성", sorted_dgr)
print("정렬 매개중심성", sorted_btw)
print("정렬 근접중심성", sorted_cls)
print("정렬 위세중심성", sorted_egv)
print("정렬 페이지랭크", sorted_pgr)


#----- 중심성 수치를 가지고 그래프 그리기
G = nx.Graph() #그릴 그래프
for i in range(len(sorted_dgr)):
    #노드추가: 노드크기는 연결중심성 크기로
    G.add_node(sorted_pgr[i][0], size=sorted_dgr[i][1])
for ind in range((len(np.where(dataset['freq'] >=10)[0]))):
    #엣지추가: 노드와 노드에 맞게 weight는 freq로
    G.add_weighted_edges_from([(dataset['word1'][ind], dataset['word2'][ind], int(dataset['freq'][ind]))])

font_fname = 'C:/Windows/Fonts/HMFMMUEX.TTC'
fontprop = fm.FontProperties(fname=font_fname, size=18).get_name()

# 노드 크기 조정
sizes = [G.nodes[node]['size'] *500 for node in G]

nx.draw(G, node_size=sizes, with_labels=True, font_family=fontprop)
plt.show()

