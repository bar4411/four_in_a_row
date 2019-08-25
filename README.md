Bar Schwartz
Ori Becher


I did the exercise with: Bar Schwartz


README: Four in a Row
======================

usage: ex12.py


Description:
==================
ex12 is about implementing connect 4 game with 2
players connected one as a server and the other as
client.

classed:

Class game:
is like real game board but of course virtual
you need to detramine who's turn is and to insert
the col to put disc into. It also contains methods
used along the implementation.

class Gui:
interface wraps the game and excutes the connection
beween players.

 Class ai:
yields an ai move to the game if the player is an ai
The algorithm works as explained in the following.


Explanation to the ai algorithm:
==================
The ai works with the alpha beta pruning algorithm. the
principle is backtracking along solutions tree. and picking
the best next step The first 7 nodes are the 7 possibles
columns which the player willput the disk into. the 49 nodes
after are the rival reaction(7 for each player choice) and
it goes on and on.

We choose 2 agents alpha and beta.When choosing the player's
next move,  alpha agent is picking the node with maximum value.
When choosing possible move for rival we assum the rival piks
the node with maximum value. Therfore beta agent will pick the
node with minimum value When getting to winning/loosing sequence
of alternatively reaching  the maximum tree depth we allow to
ourselves  the nodes value will be [-1,0,1] for loosing no one
winns, sequense and winning respectively.

In addition. When alpha of some node greater than beta of the next
node  we wont check other "beta" nodes for the player because the
beta agent wont find higher value and alpha agent will always prefer
the current alpha.

Eventually we will know the outcome of every possible next  move and
we pick  the best of them for the player.





==================
=  List of submitted files:  =
==================



game.py
ai.py
four_in_a_row.py
communicator.py
README this file
AUTHORS




