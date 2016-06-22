import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

colours = ['r','g','b','y','m','c']

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
    ax.scatter(nodes[d], edges[d],iterations[d], c=colours[d%6], label=legend)

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
    edges.append([data[d][i][1] for i in range(len(data[d]))])
    iterations.append([data[d][i][2] for i in range(len(data[d]))])

  fig = plt.figure()
  ax = fig.add_subplot(111)

  for d in range(0,len(data)):
    legend = "Plot " + str(d)
    plt.plot(nodes[d], np.poly1d(np.polyfit(nodes[d], iterations[d], 1))(nodes[d]))
    ax.scatter(nodes[d],iterations[d], edges[d], c=colours[d%6], label=legend)

  ax.set_xlabel('nodes')
  ax.set_ylabel('iterations')
  ax.legend()
  plt.ion()
  plt.show()
