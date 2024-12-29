![image](https://github.com/user-attachments/assets/c1526160-12a3-4759-8181-d676e9a3b5db)

https://adventofcode.com/2024

This was fun !

Some puzzles (4 of them) were originally done in C++ in a quest for efficiency and multithreading (I'm better at C++ ...) but I converted them a few days later to python for homogeneity of this repository.

Some puzzles were brute-forced, I didn't come up with a proper solution (06, 07, 09, 20, and 21 part 1), or maybe the bad one was enough given the small amount of time available.

The 14th puzzle second part was done looking at generated images.

The 21th puzzle second part was done a bit by hand, looking at how sequence expend and selecting the best ones before propagating the transformation 25 times.

The 24th puzzle second part was done displaying the graph of the circuit and debugging it based on the location of the first ouput error bit, fixing it, and iterating that process again 4 times.

The source code has been cleaned up but remains largely in its original state.

Some puzzle involves well known classics:
- 05: a Kahn's algorithm for topological sorting  
- 16: Dijkstra algorithm for shortest path  
- 23: Bron-Kerbosch for maximal clique in an undirected graph  
- many puzzles (12, 18, 20, 21) involve a Breadth-First Search (bfs) algorithm  
- we also find some two-pointer things, dichotomy, divide-and-conquer, ...
