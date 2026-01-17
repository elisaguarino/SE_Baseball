from itertools import combinations

import networkx as nx

from database.dao import DAO
from model.squadre import Squadre

class Model:
    def __init__(self):
        self.anni=[]
        self.squadre=[]
        self.squadre_map={}
        self.nodi = []
        self.G=nx.Graph()
        self.K=3

    def get_anni(self):
       self.anni=DAO.get_anni()
       return self.anni


    def get_squadre(self,anno):
       self.squadre=DAO.get_squadre(anno)
       return self.squadre

    def load_map(self,anno):
        self.squadre_map=DAO.get_squadre_diz(anno)
        return self.squadre_map


    def costruisci_grafo(self,anno):
        self.squadre_map=self.load_map(anno)
        self.nodi=[]
        self.G.clear()
        for squadra in self.squadre:
            self.nodi.append(squadra.id)

        self.G.add_nodes_from(self.nodi)
        lista_nodi=self.G.nodes()
        print(lista_nodi)
        archi=list(combinations(lista_nodi, 2))
        for u,v in archi:
           h1=u
           tot1=self.squadre_map[h1].salaryTot
           h2=v
           tot2=self.squadre_map[h2].salaryTot
           peso=tot1+tot2
           self.G.add_edge(h1,h2,weight=peso)
        print(self.G)

    def squadre_adiacenti(self,squadra):
        neighbors=list(self.G.neighbors(squadra))
        vicini=[]
        for v in neighbors:
            peso=self.squadre_map[v].salaryTot
            vicini.append((v,peso))
        vicini=sorted(vicini, key=lambda x: x[1], reverse=True)
        return vicini

    def get_node(self):
        return self.G.nodes()


    def get_cammino(self,squadra):
        print("inizio...")
        self.best_percorso=[]
        self.best_peso=float("inf")
        partial=[squadra]
        self.ricorsione(partial,0,float("inf"))

        print(self.best_percorso)
        return self.best_percorso

    def ricorsione(self, path, weight, last_edge_weight):
        last = path[-1]
        if len(path) > 20 or not self.squadre_adiacenti(path[-1]):
            if weight > self.best_peso:
                self.best_weight = weight
                self.best_percorso = path.copy()
            return

        vicini = self.squadre_adiacenti(last)
        neighbors = []
        counter = 0
        for node, edge_w in vicini:
            if node in path:
                continue
            if edge_w <= last_edge_weight:
                neighbors.append((node, edge_w))
                counter += 1
                if counter == self.K:
                    break

        for node, edge_w in neighbors:
            path.append(node)
            self.ricorsione(path, weight + edge_w, edge_w)
            path.pop()



    def calcola_peso(self,squadre):
        tot=0
        for s in squadre:
            tot+=self.squadre_map[s].salaryTot
        return tot



