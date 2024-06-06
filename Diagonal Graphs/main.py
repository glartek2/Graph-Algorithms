from collections import deque, defaultdict


class Node:
  def __init__(self, idx):
    self.idx = idx
    self.out = set()              # zbiór sąsiadów

  def connect_to(self, v):
    self.out.add(v)



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






def checkLexBFS(G, vs):
  n = len(G)
  pi = [None] * n
  for i, v in enumerate(vs):
    pi[v] = i

  for i in range(n-1):
    for j in range(i+1, n-1):
      Ni = G[vs[i]].out
      Nj = G[vs[j]].out

      verts = [pi[v] for v in Nj - Ni if pi[v] < i]
      if verts:
        viable = [pi[v] for v in Ni - Nj]
        if not viable or min(verts) <= min(viable):
          return False
  return True

def min_vertex_cover_size(graph, lex_order):
  independent_set = set()

  for v in reversed(lex_order):
    neighbors = {u for u in graph[v].out}
    if not neighbors.intersection(independent_set):
      independent_set.add(v)

  return len(graph) - len(independent_set)


def chromatic_number(graph, lex_order):
  color = defaultdict(int)

  for v in lex_order:
    neighbors = {color[u] for u in graph[v].out}
    c = 1
    while c in neighbors:
      c += 1
    color[v] = c

  max_color = max(color.values())
  return max_color



def find_max_clique(graph, order):
  def get_neighbors_before(v, order):
    neighbors_before = set()
    for u in order:
      if u == v:
        break
      if u in graph[v].out:
        neighbors_before.add(u)
    return neighbors_before


  max_len = 0

  for v in order:
    neighbors_before_v = get_neighbors_before(v, order)
    max_len = max(max_len, len(neighbors_before_v)+1)

  return max_len


def is_perfect_elimination_ordering(graph, order):
  def get_neighbors_before(v, order):
    neighbors_before = set()
    for u in order:
      if u == v:
        break
      if u in graph[v].out:
        neighbors_before.add(u)
    return neighbors_before


  for v in order:
    neighbors_before_v = get_neighbors_before(v, order)
    parent_v = max(neighbors_before_v, key=order.index, default=None)

    if parent_v is not None:
      neighbors_before_parent = get_neighbors_before(parent_v, order)
      neighbors_before_v.discard(parent_v)

      if not neighbors_before_v.issubset(neighbors_before_parent):
        return False

  return True





def lexBFSHope(graph, start_vertex):
  def update_sets(sets, v):
    new_sets = []
    for s in sets:
      neighbors = graph[v].out & s
      rest = s - neighbors
      if neighbors:
        if rest:
          new_sets.append(rest)
        new_sets.append(neighbors)
      else:
        new_sets.append(s)
    return new_sets

  vertices = set(node.idx for node in graph)
  vertices.remove(start_vertex)
  sets_list = [vertices, {start_vertex}]
  lex_order = []

  while sets_list:
    current_set = sets_list.pop()
    current_vertex = current_set.pop()
    lex_order.append(current_vertex)

    if current_set:
      sets_list.append(current_set)

    sets_list = update_sets(sets_list, current_vertex)

  return lex_order




"""
G = [Node(i) for i in range(8)]
G[0].connect_to(5)
G[1].connect_to(7)
G[2].connect_to(7)
G[2].connect_to(5)
G[3].connect_to(7)
G[3].connect_to(6)
G[4].connect_to(7)
G[4].connect_to(6)
G[5].connect_to(0)
G[5].connect_to(2)
G[5].connect_to(6)
G[5].connect_to(7)
G[6].connect_to(3)
G[6].connect_to(4)
G[6].connect_to(5)
G[6].connect_to(7)
G[7].connect_to(1)
G[7].connect_to(2)
G[7].connect_to(3)
G[7].connect_to(4)
G[7].connect_to(5)
G[7].connect_to(6)
"""





(V, L) = loadWeightedGraph("Zad_4/path")

G = [Node(i) for i in range(V+1)]

G2 = [None] + [Node(i) for i in range(V+1)]

for (u, v, _) in L:
  G[u-1].connect_to(v-1)
  G[v-1].connect_to(u-1)

  G2[u].connect_to(v)
  G2[v].connect_to(u)






hope = lexBFSHope(G, 0)

# LexBFS kolejność
#print(hope)

# Sprawdzenie czy LexBFS działa
#print(checkLexBFS(G, hope))

# Zad 1
#print(is_perfect_elimination_ordering(G, hope))

# Zad 2
#print(find_max_clique(G, hope))

# Zad 3
#print(chromatic_number(G, hope))

# Zad 4
print(min_vertex_cover_size(G, hope))