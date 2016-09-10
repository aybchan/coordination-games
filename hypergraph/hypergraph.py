#!/usr/local/bin/python
import random
#import tabulate
import numpy as np
#import plot
import data as dt
import time

#from tabulate import tabulate
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
  strategy_set = power_set(strategies(num_strategies))

  j = 1
  # for all nodes, starting from node 0
  for n in range(0, nodes):
    graph.nodes = graph.nodes.union({n})
    num = random.randint(1,maxedges)
    for m in range(0, num):
      hyperedge = generate_hyperedge(nodes,n)
      w = random.choice(range(-weight,weight))
      graph.edges = graph.edges.union({(tuple(hyperedge),w)})
    graph.available.append(random.choice(strategy_set))
    graph.chosen.append(random.choice(graph.available[n]))

  return graph

# Generate a hyperedge
def generate_hyperedge(nodes,x):
    # determine degree of hyperedge
    degree_flag = True
    degree = 1
    while degree_flag and degree < nodes:
      degree_flag = random.choice([True, False])
      degree += 1

    # randomly add nodes to hyperedge of size degree
    hyperedge = [x]

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

# Generate a power set from the set of strategies, minus the empty set
def power_set(strategy_set):
  power_set=[[]]
  for elem in strategy_set:
    for sub_set in power_set:
      power_set=power_set+[list(sub_set)+[elem]]
  power_set.remove([])
  return power_set

# Print a graph
def tabulate_graph(graph):
  table = [[n, graph.available[n], graph.chosen[n], payoff(n, graph), node_edges(n, graph)] for n in graph.nodes]
  headers = ["Node","Strategies", "Strategy", "Payoff", "Edges"]
  return print("Nodes:", len(graph.nodes), "\tEdges:", len(graph.edges), "\tSocial welfare:", social(graph),"\n",tabulate(table, headers), "\n\n")

# Get a list of edges connected to a given node
def node_edges(node, graph):
  edges = []
  graph_edges = sorted(list(graph.edges))
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
  speculate = [0 for i in range(graph.num_strategies)]
  edges = node_edges(node,graph)
  for edge in range(len(edges)):
    common_strategy = set()
    for n in edges[edge][0]:
      if (not n == node) and graph.chosen[n] in graph.available[node]:
        common_strategy = common_strategy.union({graph.chosen[n]})
    if len(common_strategy) == 1:
      speculate[tuple(common_strategy)[0]] += edges[edge][1]

  strategy = graph.chosen[node]
  max = payoff(node,graph)

  for i in range(len(speculate)):
    if max < speculate[i]:
      strategy = i
      max = speculate[i]

  return strategy

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

  print("[nodes:", len(graph.nodes),"| edges:",len(graph.edges),"| strategies:",graph.num_strategies,"]","\tNash equilibrium found after", cnt, "iterations! (","{0:.2f}".format(end-start),"seconds)")
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
  print("Avg. iterations num", sumcount/num_datapoints)
  dt.save(data[i])
