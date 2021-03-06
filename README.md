Coordination games on graphs
===================

This is a Python command line program for generating experimental data for [coordination games][1] on graphs. We are interested in how many strategy deviations it takes to reach Nash equilibria in such games.

----------

How it works
-------------

[Hypergraphs][2] of a specified size (number of nodes) are randomly generated with edges between any two nodes added with a random probability.

Hypergraphs are graphs with hyperedges. A hyperedge can have have more than two nodes as members as opposed to conventional graphs where an edge is always a relation between two nodes.

Each node (i.e. a 'player' or 'agent') then selects a non-empty set of available strategies from a power set of a specified number of strategies (i.e for a 2-strategy game, each player randomly chooses from {{a}, {b}, {a,b}}). Each player picks one strategy from this set of available strategies.

We then iterate through each player and change its strategy if it can improve its payoff (defined as the aggregate weight of all hyperedges with strategies in common) until we reach an overall strategy picking for all players that is a Nash equilibrium (i.e. no player can profitably deviate with all other players' strategies staying the same).

----------

Generating data for games on hypergraphs
-------------

1. Install dependencies

  ```
  make
  ```

2. Do some experiments

  ```
  python hypergraph 20 10 100 5 1000000
  ```

  Arguments:

      1. Graph size (number of nodes)
      2. Upper bound on number of nodes each hyperedge contains
      3. Number of graphs to be generated
      4. Number of strategies available
      5. Maximum edge weight

  This command will generate 100 random graphs size 20, with each hyperedge having at most 10 members, with edge-weights ranging from -1,000,000 to 1,000,000 (excluding 0), playing 5-strategy games.

  A .json file with the generated data will be created in the data directory. The data for each game is saved as a tuple:

  >(nodes, edges, number of deviations until Nash eq.)
  
  For running experiments with graphs of different sizes, i.e. for graphs of 10 nodes up to graphs 200 nodes, 20 times each, we can do:
  ```
  for i in `seq 10 200`; do python hypergraph $i 10 20 10 1000000; done
  ```

3. Visualise the data with matplotlib

  To plot a 2D scatter plot do:

  ```
  python hypergraph plot
  ```

  (The size of each point is proportional to the number of edges of the generated graph.)

  To visualise the data on a 3D scatter plot:

  ```
  python hypergraph plot3d
  ```


----------

### Further information
https://en.wikipedia.org/wiki/Coordination_game
https://en.wikipedia.org/wiki/Hypergraph

[1]: https://en.wikipedia.org/wiki/Coordination_game
[2]: https://en.wikipedia.org/wiki/Hypergraph
