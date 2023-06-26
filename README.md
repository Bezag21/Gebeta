# Gebeta

This is a Python program that implements a traditional Ethiopian board game 
called Gebeta. 

The program uses the Pygame library to create a graphical user interface 
for the game. The Gebeta board is displayed on the screen, and the players 
take turns choosing pits to distribute the stones in them to the other pits. 

There are 7 pits per row. The last two are used to store the stones of 
each player before passing to an opponents pit/row.

The game starts when player 1 moves the stones in his row. And if 
all the stones land in his row, it is again his turn to play until it places a 
stone in opponent's pit or his/her stone store. Then it will be the oponent's turn to play. 
The previous rule also applies for player 2.
And if a player places 1 stone in an empty pit, it will takes 
all the stones of the oponent's side found on the same index.

The game is over when one player no longer has stones left in his/her row(except the stone store- the 7th pit). 
The winner is the one whohas more number of stones in the stone store or in his row when the game is over.
A tie occcurs when both player have equal number of stones at the end of the game.



