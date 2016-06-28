import sys
import hypergraph

def main():
  a = []
  for i in sys.argv[1:]:
    a.append(int(i))
  hypergraph.gen_dataset(a[0],a[1],a[2],a[3],a[4])

if __name__ == "__main__":
  main()

