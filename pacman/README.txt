this is my implementation of the famous pacman game.
the goal is to collect all coins.
the goal of your enemies is to catch you
to start the game open cmd in the current dir of the pacman.py file and type in the console: python pacman.py
then play with W, A, S, D!


game legend:
YELLOW - pacman
BLUE - wall
WHITE - coin
RED - ghost

you win the game if you collect all of the coins
you lose the game if any ghost catches you

algorithms used:
Astar (with manhattan's distance heuristic)
DFS

the current enabled algorithm for the movement of ghosts is Astar due to the better behavior observed

