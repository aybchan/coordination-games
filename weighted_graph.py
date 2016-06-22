#!/usr/local/bin/python
import random
import tabulate
import numpy as np
import plot
import data as dt

from tabulate import tabulate

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
def generate_graph(nodes, probability, num_strategies, weight):
  # initialise an empty graph object
  graph = Graph(set(),set(),[],[],num_strategies,weight)
  strategy_set = power_set(strategies(num_strategies))

  j = 1
  # for all nodes, starting from node 0
  for n in range(0, nodes):
    graph.nodes = graph.nodes.union({n})
    for m in range(j, nodes):
      if random.random() < probability:
        weight = random.choice(range(1,graph.max_weight))
        graph.edges = graph.edges.union({((n,m),weight)})

    j += 1
    graph.available.append(random.choice(strategy_set))
    graph.chosen.append(random.choice(graph.available[n]))

  #tabulate_graph(graph)
  return graph

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
  for e in range(0,len(graph_edges)):
    if graph_edges[e][0][0] > node:
      break
    if node in (graph_edges[e][0][1], graph_edges[e][0][0]):
      edges.append(graph_edges[e])
  return edges

# Get a list of nodes with edges to a given node in a graph
def connected_nodes(node, graph):
  connected_edges = node_edges(node, graph)
  connected_nodes = []

  for i in range(0,len(connected_edges)):
    if connected_edges[i][0][0] == node:
      connected_nodes.append((connected_edges[i][0][1],connected_edges[i][1]))
    else:
      connected_nodes.append((connected_edges[i][0][0],connected_edges[i][1]))

  return connected_nodes

# Get the payoff for a given node in a graph
def payoff(node, graph):
  payoff = 0
  connected_edges = node_edges(node, graph)
  chosen = graph.chosen

  for i in range(0, len(connected_edges)):
    if connected_edges[i][0][0] == node:
      if chosen[node] == chosen[connected_edges[i][0][1]]:
        payoff += connected_edges[i][1]
    else:
      if chosen[node] == chosen[connected_edges[i][0][0]]:
        payoff += connected_edges[i][1]

  return payoff

# Get social welfare
def social(graph):
  nodes = list(graph.nodes)
  welfare = 0

  for node in nodes:
    welfare += payoff(node, graph)

  return welfare

# Return the best response of a ndoe
def best_response(node, graph):
  best = graph.chosen[node]

  if len(graph.available[node]) < 2:
    print("Only one strategy available. No change.")
    return best

  linked_nodes = connected_nodes(node,graph)
  connected_strategies = [(graph.chosen[n[0]],n[1]) for n in linked_nodes]
  connected_strategies = [i for i in connected_strategies if i[0] in graph.available[node]]

  strategy_set = sorted(list(set([x[0] for x in connected_strategies])))

  agg_weights = []
  for s in strategy_set:
    weight = 0
    for c in connected_strategies:
      if c[0] == s:
        weight += c[1]
    agg_weights.append((weight,s))

  sorted(agg_weights, reverse=True)

  for w in agg_weights:
    if w[1] == graph.chosen[node]:
      print(w[1], "is already optimal. No change.")
      return graph.chosen[node]
    else:
      if w[0] > payoff(node,graph):
        print("Strategy changed from", graph.chosen[node], "to", w[1])
        return w[1]
      else:
        print(w[1], "is already optimal. No change.")
        return graph.chosen[node]

# Same as best_response() but without messages
def best_response_non_verbose(node, graph):
  best = graph.chosen[node]

  if len(graph.available[node]) < 2:
    return best

  linked_nodes = connected_nodes(node,graph)
  connected_strategies = [(graph.chosen[n[0]],n[1]) for n in linked_nodes]
  connected_strategies = [i for i in connected_strategies if i[0] in graph.available[node]]

  strategy_set = sorted(list(set([x[0] for x in connected_strategies])))

  agg_weights = []
  for s in strategy_set:
    weight = 0
    for c in connected_strategies:
      if c[0] == s:
        weight += c[1]
    agg_weights.append((weight,s))

  sorted(agg_weights, reverse=True)

  for w in agg_weights:
    if w[1] == graph.chosen[node]:
      return graph.chosen[node]
    else:
      if w[0] > payoff(node,graph):
        return w[1]
      else:
        return graph.chosen[node]

# Update strategy choice of a node
def update_strategy(node, new_strategy, graph):
  if not new_strategy in graph.available[node]:
    return
  else:
    graph.chosen[node] = new_strategy

# Iterate best_reponse() function over all nodes
def cycle_nodes(node, graph):
  count = 0
  for n in range(node, len(graph.nodes) + node):
    print("Iteration", count + 1)
    current_node = n % len(graph.nodes)
    update_strategy(current_node, best_response(current_node,graph), graph)
    print( "\tNodes:", len(graph.nodes), "\tEdges:", len(graph.edges), "\tSocial welfare:", social(graph),"\n", "\n")
    count += 1

# Iterate best_response() function until there are len(nodes) of iterations
# without a strategy change (i.e. Nash equilibrium)
def cycle_nash(node,graph):
  strategy_set = graph.chosen[:]
  nash_count = 0
  count = 0

  while nash_count < len(graph.nodes):
    count += 1
    print("Iteration", count, "(",nash_count + 1,"iterations since last strategy change)")
    current_node = count % len(graph.nodes)
    update_strategy(current_node, best_response(current_node,graph), graph)
    print( "\tNodes:", len(graph.nodes), "\tEdges:", len(graph.edges), "\tSocial welfare:", social(graph),"\n", "\n")
    tabulate_graph(graph)
    if graph.chosen == strategy_set:
      nash_count += 1
    else:
      nash_count = 0
      strategy_set = graph.chosen[:]
  print("\nNash equilibrium found after", count, "iterations!")


# Iterate best_response() function until there are len(nodes) of iterations
# without a strategy change (i.e. Nash equilibrium), non-verbose
def cycle_nash_test(node, graph):
  strategy_set = graph.chosen[:]
  nash_count = 0
  count = 0
  p = 1

  while nash_count < len(graph.nodes):
    count += 1
    current_node = count % len(graph.nodes)
    update_strategy(current_node, best_response_non_verbose(current_node,graph), graph)
    if graph.chosen == strategy_set:
      nash_count += 1
    else:
      nash_count = 0
      strategy_set = graph.chosen[:]
  p += 1
  print("[nodes:", len(graph.nodes),"| edges:",len(graph.edges),"| strategies:",graph.num_strategies,"]","\tNash equilibrium found after", count, "iterations!")
  return(len(graph.nodes), len(graph.edges), graph.num_strategies, count)

# generate a set of data for graphs with size over a given range
def gen_dataset(start_size,end_size,num_datapoints,num_strategies,weight):
  i = len(data)
  data.append([])
  for size in range(start_size,end_size):
    for point in range(0,num_datapoints):
      test = cycle_nash_test(0,generate_graph(size,random.random(),num_strategies, weight))
      data[i].append((size,test[1],test[3]))

# Generate test data for graphs of given node-size,
# random edges, and given strategy set size

def averages():
  data_list = []
  sorted(data)

  for i in range(0,len(data)):
    size = data[i][0]
    if data[i][0] == size:
      data_list.append([])
      for j in range(i,len(data) - i):
        data_list[len(data_list - 1)].append(data[i])


  headers = ["Nodes","Avg. edges", "Avg. iterations", "Avg. payoff"]
  tabulate(table, headers)

# Generate a 3D scatter plot of the generated data
def scatter_plot():
  plot.scatter(data)

# write data array to json file
def save():
  dt.save(data)

#example_graph = Graph({0,1,2,3},{(0,1),(1,2),(2,3),(0,3)},[0,1,0,1],[[0,1],[0,1],[0,1],[0,1]],2,1000)
#example_random_graph = generate_graph(100,random.random(),10)
#example_nash_cycle = cycle_nash(0, example_random_graph)

# generate 2000 datapoints for games with 3 strategies and draw plot
def example_experiment():
  # generate 20 datapoints each for random graphs of size 1 to 100 nodes with 10-strategy games and max edge weight of 1,000,000
  gen_dataset(1,100,20,10,1000000)
  scatter_plot()
