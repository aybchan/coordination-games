import random
import numpy as np
import data as dt
import time
import copy

from tabulate import tabulate
from collections import OrderedDict

data = []

# Graph object
class Graph:
  def __init__(self, nodes, edges, chosen, available, num_strategies, max_weight):
    self.nodes = nodes
    self.edges = edges
    self.chosen = chosen
    self.available = available
    self.num_strategies = num_strategies
    self.max_weight = max_weight

# Generate random graph
def generate_graph(nodes, maxedges, num_strategies, weight):
  # initialise an empty graph object
  graph = Graph(set(),set(),[],[],num_strategies,weight)

  j = 1
  # for all nodes, starting from node 0
  for n in range(0, nodes):
    graph.nodes = graph.nodes.union({n})
    num = random.randint(1,maxedges)
    for m in range(0, num):
      hyperedge = generate_hyperedge(nodes,n)
      w = random.choice(range(-weight,weight))
      graph.edges = graph.edges.union({(tuple(hyperedge),w)})
    graph.available.append(available_strategies(num_strategies))
    graph.chosen.append(random.choice(graph.available[n]))

  return graph

# Generate a list of available strategies
def available_strategies(max_strategies):
    available = []
    flag = True
    all_strategies = [i for i in range(max_strategies)]

    while flag and all_strategies:
      choice = random.choice(all_strategies)
      available.append(choice)
      all_strategies.remove(choice)
      flag = random.choice([True, False])

    return available

# Generate a hyperedge
def generate_hyperedge(nodes,node):
    # determine degree of hyperedge
    degree_flag = True
    degree = 1
    while degree_flag and degree < nodes:
      degree_flag = random.choice([True, False])
      degree += 1

    # randomly add nodes to hyperedge of size degree
    hyperedge = [node]

    i = 1
    while i < degree:
      n = random.randint(0,nodes-1)
      if n not in hyperedge:
        hyperedge.append(n)
        i += 1

    return sorted(hyperedge)

# Initialise set of all strategies
def strategies(num_strategies):
  strategies = set()
  for n in range(0, num_strategies):
    strategies = strategies.union({n})
  return strategies

# Print a graph
def tabulate_graph(graph):
  table = [[n, graph.available[n], graph.chosen[n], payoff(n, graph), node_edges(n, graph)] for n in graph.nodes]
  headers = ["Node","Strategies", "Strategy", "Payoff", "Edges"]
  return print("Nodes:", len(graph.nodes), "\tEdges:", len(graph.edges), "\tSocial welfare:", social(graph),"\n",tabulate(table, headers), "\n\n")

# Get a list of edges connected to a given node
def node_edges(node, graph):
  edges = []
  graph_edges = list(graph.edges)
  for edge in range(0,len(graph_edges)):
    if node in graph_edges[edge][0]:
      edges.append(graph_edges[edge])
  return edges


# Get the payoff for a given node in a graph
def payoff(node, graph):
  payoff = 0
  hyperedges = node_edges(node,graph)

  for e in range(0,len(hyperedges)):
    for n in range(0,len(hyperedges[e][0])):
      if not graph.chosen[hyperedges[e][0][n]] == graph.chosen[node]:
          break
      if n + 1 == len(hyperedges[e][0]):
        payoff += hyperedges[e][1]
  return payoff

# Get social welfare
def social(graph):
  nodes = list(graph.nodes)
  welfare = 0

  for node in nodes:
    welfare += payoff(node, graph)

  return welfare

# Return the best response of a node
def best_response(node, graph):
  if len(graph.available[node]) < 2:
    return graph.chosen[node]

  best_payoff = payoff(node, graph)
  best_strategy = graph.chosen[node]

  for strategy in graph.available[node]:
    if not strategy == best_strategy:
      speculate = speculate_payoff(node,strategy,graph)
      if speculate > best_payoff:
        best_payoff = speculate
        best_strategy = strategy
  return best_strategy

def speculate_payoff(node, strategy, graph):
  spec_graph = copy.copy(graph)
  spec_graph.chosen[node] = strategy
  spec_payoff = payoff(node, spec_graph)
  return spec_payoff

# Update strategy choice of a node
def update_strategy(node, new_strategy, graph):
  if not new_strategy in graph.available[node]:
    return
  else:
    graph.chosen[node] = new_strategy

# Iterate best_response() function until there are len(nodes) of iterations
# without a strategy change (i.e. Nash equilibrium)
def nash(node, graph):
  strategy_set = graph.chosen[:]
  nash_count = 0
  count = node
  cnt = 0
  start = time.time()

  while nash_count < len(graph.nodes):
    current_node = count % len(graph.nodes)
    count += 1
    update_strategy(current_node, best_response(current_node,graph), graph)
    if graph.chosen == strategy_set:
      nash_count += 1
    else:
      nash_count = 0
      cnt += 1
      strategy_set = graph.chosen[:]
    end = time.time()

  print("[nodes: {0} | edges: {1} | strategies: {2}]\tNash eq. after {3} deviations! ({4:.2f} secs)".format(len(graph.nodes), len(graph.edges), graph.num_strategies, cnt, end-start))

  return(len(graph.nodes), len(graph.edges), graph.num_strategies, cnt)

# generate a set of data for graphs with size over a given range
def gen_dataset(size,maxedges,num_datapoints,num_strategies,weight):
  sumcount = 0
  i = len(data)
  data.append([])
#  for size in range(start_size,end_size):
  for point in range(0,num_datapoints):
    test = nash(0,generate_graph(size,maxedges,num_strategies,weight))
    data[i].append((size,test[1],test[3]))
    sumcount += test[3]
  print("Avg. deviations:", sumcount/num_datapoints)
  dt.save(data[i])

