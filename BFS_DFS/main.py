import copy
from collections import deque


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



def BFS(G, s, t, parent):
  n = len(G)
  visited = [False] * n
  Q = deque()
  Q.append(s)
  visited[s] = True

  while bool(Q):
    u = Q.popleft()
    for i in range(n):
      if not visited[i] and G[u][i] > 0:
        Q.append(i)
        visited[i] = True
        parent[i] = u
        if i == t:
          return True

  return False

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

def fordFulkerson(G, s, t, stype):
  n = len(G)
  parent1 = [-1] * n
  parent2 = [-1] * n

  Gf1 = copy.deepcopy(G)
  Gf2 = copy.deepcopy(G)
  max_flow = 0

  if stype == 0:
    while BFS(Gf1, s, t, parent1):
      path_flow = float("Inf")
      t2 = t
      while (t2 != s):
        path_flow = min(path_flow, Gf1[parent1[t2]][t2])
        t2 = parent1[t2]

      max_flow += path_flow

      v = t
      while (v != s):
        u = parent1[v]
        Gf1[u][v] -= path_flow
        Gf1[v][u] += path_flow
        v = parent1[v]

  elif stype == 1:
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




V, L = loadDirectedWeightedGraph("grid100x100")
G = [[0 for _ in range(V)] for __ in range(V)]

#for i in range(len(L)):
 #G[L[i][0] - 1].append((L[i][1] - 1, L[i][2]))

for i in range(len(L)):
  G[L[i][0]-1][L[i][1]-1] = L[i][2]

print(fordFulkerson(G, 0, V-1, 0))
print(fordFulkerson(G, 0, V-1, 1))


