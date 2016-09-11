import sys
import hypergraph
import data
import plot

def main():
  a = []

  if sys.argv[1] == "plot":
    plot.scatter2d(data.read())
  elif sys.argv[1] == "plot3d":
    plot.scatter3d(data.read())
  else:
    for i in sys.argv[1:]:
      a.append(int(i))
    hypergraph.gen_dataset(a[0],a[1],a[2],a[3],a[4])

if __name__ == "__main__":
  main()

