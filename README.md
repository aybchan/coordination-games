Coordination games on graphs
===================

This is a Python command line program for generating experimental data for [coordination games][1] on graphs. We are interested in how many iterations of strategy updates for players in these games it takes to reach Nash equilibria.

----------

How it works
-------------

Undirected graphs of a specified size (number of nodes) are randomly generated with edges between any two nodes added with a random probability.

Each node (player) then selects a non-empty set of strategies from a power set of a specified number of strategies (i.e for a 2-strategy game, each player randomly chooses an element from {{a}, {b}, {a,b}}). Each player picks one strategy from its set of strategies.

We then iterate through each node and update its strategy if it can improve its payoff (defined as the number of connected nodes picking same strategy) until we reach a strategy picking for all players that is a Nash equilibrium (no player can profitably deviate).

We consider graphs with unweighted edges, weighted edges, and [hypergraphs][2] (i.e. able to have more than two nodes in an 'edge').

----------

Generating data for games on hypergraphs
-------------

1. Run the setup script to install dependency packages

```
python3.5 setup.py install
```


2. Run the program with some arguments

```
python3.5 ./ 10 20 5 10 1000000
```
Arguments:

		1. Starting graph size
		2. End graph size
		3. Number of graphs generated for each graph size
		4. Number of strategies available
		5. Maximum edge weight

This command will generate data for 5 random graphs each of graphs of size 10 to 19 with maximum edge-weight of 1,000,000, playing 10-strategy games.

A .json file with the generated data will be created in the data directory. The data for each game is saved as a tuple:

>(nodes, edges, iterations to reach Nash eq.)

3. Plot the data

Run plot.py in the Python interpreter:

```
python3.5 -i plot.py
```

To plot the generated data on a 3d scatter plot, call the function to read the data files in the 'data' directory, and pass it through to the 3d plot function:

```
>>>scatter3d(data.read())
```

To plot the generated data on a 2D scatter plot with number of nodes and iterations to find Nash equilibiria as axes, call the function to read the data files in the 'data' directory, and pass it through to the 2d plot function:

```
>>>scatter2d(data.read())
```

The size of each point is proportional to the number of edges of the generated graph.



----------

### Further information
https://en.wikipedia.org/wiki/Coordination_game
https://en.wikipedia.org/wiki/Hypergraph

[1]: https://en.wikipedia.org/wiki/Coordination_game
[2]: https://en.wikipedia.org/wiki/Hypergraph
