import networkx as nx
from networkx.algorithms.planarity import check_planarity
from networkx.algorithms.flow import maximum_flow
from networkx.algorithms.components import strongly_connected_components

def loadWeightedGraph( name ):
  """Load a graph in the DIMACS ascii format (with weights) from
     the file "name" and return it as a list of sets
     Returns (V,L)
     V -- number of vertices (1, ..., V)
     L -- list of edges in the format (x,y,w): edge between x and y with weight w (x<y)"""

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
      (x,y,c) = (min(a,b), max(a,b), c)
      L.append((x,y,c))

  f.close()
  return (V,L)


def loadCNFFormula( name ):
  """Load a CNF formula in the DIMACS ascii format from
     the file "name" and return it as a list of clauses
     Returns (V,F)
     V -- highest variable number
     F -- list of clauses"""

  V = 0
  L = []

  f = open( name, "r" )
  lines = f.readlines()
  for l in lines:
    s = l.split()
    if(len(s) < 1): continue
    if( s[0] == "c" ):
      print(s)
      continue
    elif( s[0] == "p" ):
      V = int(s[2])
    else:
      clause = [int(v) for v in s[:-1]]
      L.append(clause)

  f.close()
  return (V,L)




V, L = loadWeightedGraph("flow/simple")

G = nx.Graph()
for i in range(V):
  G.add_node(i+1)
G.add_weighted_edges_from(L)

for i in range(len(L)):
  G[L[i][0]][L[i][1]]['capacity'] = L[i][2]


print(check_planarity(G))
print(maximum_flow(G, 1, V))


V2, L2 = loadCNFFormula("CNF/simple_sat")

G2 = nx.DiGraph()

for i in range(V2):
  G2.add_node(i+1)
  G2.add_node(-i-1)

for i in range(len(L2)):
  a, b = L2[i]
  G2.add_edge(-a, b)
  G2.add_edge(-b, a)

SCC = strongly_connected_components(G2)

n = 0
for _ in SCC:
  n += 1

# wypisz zawartość składowych
t = 0
temp = [[] for _ in range(n)]

for S in SCC:
  print("Silnie spojna składowa", t, "zawiera wierzcholki")
  for v in S:
    temp[t].append(v)
    print("  ",v)
  t += 1


print(temp)


flag = True
for S in SCC:
  for v in S:
    if v in S and -v in S:
      flag = False

print(flag)


H = nx.DiGraph()

H.add_nodes_from(SCC)

for S in SCC:
  print(S)

