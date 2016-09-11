import matplotlib.pyplot as plt
import data
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pylab

colours = ['#30a2da','#fc4f30','#e5ae38','#6d904f','#8b8b8b']
col = len(colours)

def scatter3d(data):
  nodes = []
  edges = []
  deviations = []

  for d in range(0,len(data)):
    nodes.append([data[d][i][0] for i in range(len(data[d]))])
    edges.append([data[d][i][1] for i in range(len(data[d]))])
    deviations.append([data[d][i][2] for i in range(len(data[d]))])

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  for d in range(0,len(data)):
    legend = "Plot " + str(d)
    ax.scatter(nodes[d], edges[d],deviations[d], c=colours[d%col], label=legend)

  ax.set_xlabel('Nodes')
  ax.set_ylabel('Edges')
  ax.set_zlabel('Strategy deviations')
  ax.legend()
  plt.show()

def scatter2d(data):
  nodes = []
  edges = []
  deviations = []

  for d in range(0,len(data)):
    nodes.append([data[d][i][0] for i in range(len(data[d]))])
    edges.append([np.sqrt(data[d][i][1])/2 for i in range(len(data[d]))])
    deviations.append([data[d][i][2] for i in range(len(data[d]))])

  fig = plt.figure()
  ax = fig.add_subplot(111)

  allnodes = []
  alldeviations = []

  for d in range(0,len(data)):
    allnodes.extend(nodes[d])
    alldeviations.extend(deviations[d])
    legend = "Plot " + str(d)
    ax.scatter(nodes[d],deviations[d], edges[d], c=colours[d%col], label=legend)

  plt.plot(allnodes, np.poly1d(np.polyfit(allnodes, alldeviations, 1))(allnodes))

  ax.set_xlabel('Nodes')
  ax.set_ylabel('Strategy deviations')
  ax.legend()
  plt.show()
