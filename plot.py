import matplotlib.pyplot as plt
import data
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

colours = ['#30a2da','#fc4f30','#e5ae38','#6d904f','#8b8b8b']
col = len(colours)

def scatter3d(data):
  nodes = []
  edges = []
  iterations = []

  for d in range(0,len(data)):
    nodes.append([data[d][i][0] for i in range(len(data[d]))])
    edges.append([data[d][i][1] for i in range(len(data[d]))])
    iterations.append([data[d][i][2] for i in range(len(data[d]))])

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  for d in range(0,len(data)):
    legend = "Plot " + str(d)
    ax.scatter(nodes[d], edges[d],iterations[d], c=colours[d%col], label=legend)

  ax.set_xlabel('nodes')
  ax.set_ylabel('edges')
  ax.set_zlabel('iterations')
  ax.legend()
  plt.ion()
  plt.show()

def scatter2d(data):
  nodes = []
  edges = []
  iterations = []

  for d in range(0,len(data)):
    nodes.append([data[d][i][0] for i in range(len(data[d]))])
    edges.append([np.sqrt(data[d][i][1])/2 for i in range(len(data[d]))])
    iterations.append([data[d][i][2] for i in range(len(data[d]))])

  fig = plt.figure()
  ax = fig.add_subplot(111)

  allnodes = []
  alliterations = []

  for d in range(0,len(data)):
    allnodes.extend(nodes[d])
    alliterations.extend(iterations[d])
    legend = "Plot " + str(d)
    ax.scatter(nodes[d],iterations[d], edges[d], c=colours[d%col], label=legend)

  plt.plot(allnodes, np.poly1d(np.polyfit(allnodes, alliterations, 1))(allnodes))

  ax.set_xlabel('nodes')
  ax.set_ylabel('iterations')
  ax.legend()
  plt.ion()
  plt.show()

