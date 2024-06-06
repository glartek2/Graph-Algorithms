import copy
from collections import deque


class Node:
  def __init__(self):
    self.edges = {}    # słownik  mapujący wierzchołki do których są krawędzie na ich wagi

  def addEdge( self, to, weight):
    self.edges[to] = self.edges.get(to,0) + weight  # dodaj krawędź do zadanego wierzchołka
                                                    # o zadanej wadze; a jeśli taka krawędź
                                                    # istnieje, to dodaj do niej wagę

  def delEdge( self, to ):
    del self.edges[to]                              # usuń krawędź do zadanego wierzchołka

def merge_vertices(self, vertex1, vertex2):
  for destination, weight in self[vertex2].edges.items():
    self[vertex1].addEdge(destination, weight)
    self[vertex2].addEdge(destination, -weight)

  del self[vertex2]



def loadDirectedWeightedGraph( name ):
  """Load a directed graph in the DIMACS ascii format (with weights) from
     the file "name" and return it as a list of sets
     Returns (V,L)
     V -- number of vertices (1, ..., V)
     L -- list of edges in the format (x,y,w): edge between x and y with weight w"""

  V = 0
  L = []

  f = open( name, "r" )
  lines = f.readlines()
  for l in lines:
    s = l.split()
    if(len(s) < 1): continue
    if( s[0] == "c" ):
      continue
    elif( s[0] == "p" ):
      V = int(s[2])
    elif( s[0] == "e" ):
      (a,b,c) = (int(s[1]), int(s[2]), int(s[3]))
      L.append((a,b,c))

  f.close()
  return (V,L)

def readSolution(name):
    """Read the expected solution from the first line of the graph file"""
    with open(name, 'r') as f:
        line = f.readline()
        return line.split()[-1]




def DFSVisited(j, Gf, visitedD, parent):
  visitedD[j] = True
  for v in range(len(Gf[j])):
    if not visitedD[v] and Gf[j][v] > 0:
      parent[v] = j
      DFSVisited(v, Gf, visitedD, parent)


def DFS(Gf, s, t, parent):
  n = len(Gf)
  visitedD = [False] * n
  for i in range(s, n):
    if not visitedD[i] and Gf[s][i] > 0:
      parent[i] = s
      DFSVisited(i, Gf, visitedD, parent)
  return visitedD[t]

def fordFulkerson(G, s, t):
  n = len(G)
  parent1 = [-1] * n
  parent2 = [-1] * n

  Gf1 = copy.deepcopy(G)
  Gf2 = copy.deepcopy(G)
  max_flow = 0


  while DFS(Gf2, s, t, parent2):
    path_flow = float("Inf")
    t2 = t
    while (t2 != s):
      path_flow = min(path_flow, Gf2[parent2[t2]][t2])
      t2 = parent2[t2]

    max_flow += path_flow

    v = t
    while (v != s):
      u = parent2[v]
      Gf2[u][v] -= path_flow
      Gf2[v][u] += path_flow
      v = parent2[v]


  return max_flow


def MinimumCutPhase(G):
  a = 0
  S = {a}

  while len(S) < len(G):
    v = max(set(range(len(G))) - S, key=lambda x: sum(G[x].edges[w] for w in G[x].edges if w in S))
    S.add(v)

  t, s = list(S)[-1], list(S)[-2]

  potential_result = sum(G[s].edges[w] for w in G[s].edges)

  merge_vertices(G, s, t)

  return potential_result


def MinimumCut(G):
  res = float('inf')
  while len(G) > 1:
    res = min(res, MinimumCutPhase(G))
  return res




V, L = loadDirectedWeightedGraph("grid5x5")


G = [ Node() for i in range(V) ]

for (x,y,c) in L:
  G[x-1].addEdge(y,c)
  G[y-1].addEdge(x,c)


# Print the updated graph
#for vertex, node in graph.items():
 #   print(f"{vertex}: {node.edges}")

#G = [[0 for _ in range(V)] for __ in range(V)]

#for i in range(len(L)):
 #G[L[i][0] - 1].append((L[i][1] - 1, L[i][2]))

#for i in range(len(L)):
 # G[L[i][0]-1][L[i][1]-1] = L[i][2]
 # G[L[i][1]-1][L[i][0]-1] = L[i][2]

#ans = float('inf')

#for i in range(1, len(G)-1):
 #   Gr = copy.deepcopy(G)
  #  ans = min(ans, fordFulkerson(Gr, 0, i))

#print(ans)
print(MinimumCut(G))

