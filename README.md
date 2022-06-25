# NumberCrunching
Some slightly more mathematical applications

--------------------------------------------------
## 2x2gamesolver.py

2x2gamesolver.py is a little program with GUI that applies game theory to solve simple 2x2 simultaneous (i.e., normal form) games from a game theoretical perspective.
Games can be zero sum, constant sum (with a constant other than zero) or non-constant sum. Required imports are tkinter and Numpy arrays. 
"Solving" means the program will find dominant strategies (weak or strict), pure strategy Nash equilibria, and mixed strategy Nash equilibria.

Available actions are U (Up) and D (Down) for the row player and L (Left) and R (Right) for the column player.

Start by inserting the payoffs for the row player into the lower-left entry field in each cell (the presentation uses Schelling-style staggered payoffs).
To ease the populaton of the entry fields, the program offers "Zero sum" and "Constant sum" buttons:
A click on the "Zero sum" button will prepopulate the entry fields for the column player with the negative of the row player's payoff for the same cell.
A click on the "Constant sum" button has to be preceded by entering the constant sum into the field underneath that button; a click on the button will the prepopulate the payoff entries for the column player with the remainder that is necessary to achieve the constant sum of both players' payoffs in each cell.
Manual overwriting of the prepopulation is possible.

(From the perspective of identifying Nash equilibria, there is no difference between a zero sum and a non.zero constant sum game, but the values of the games may differ;
hence the two are available as separate options.)

After all entry fields have been populated, click "Calculate". The program will now indicate dominant stratgies (if any) by means of arrows:
A red arrow labelled "s.d." indicates strict dominance, an amber arrow labelled "w.d." weak dominance.

Pure strategy Nash equilibria (there can be more than one) will be highlighted by a black frame.
Mixed strategy Nash equilibria will be displayed by means of probabilities for U (p), D (1-p), L (q) and R (1-q), rounded to two significant digits.
In case of mixed strategies, the values of the game to the two players will also be displayed.


### Version 2.0, January 2022

--------------------------------------------------
## 2x2gamesolver.c

The same basic idea as 2x2gamesolver.py above, but in C, and with a text-based interface in lieu of the fancy GUI. 

### Version 1.0, October 2021


--------------------------------------------------
## eratosthenes.c

A simple implementation of the classic "sieve of Eratosthenes" algorithm to find primes. There's no user interaction; upon start, it will proceed to print all primes up to a predefined ceiling. It will also print the number of primes found. To change the ceiling, modify the CEILING macro in the preprocessor.

### Version 1.0, June 2022

--------------------------------------------------
## quine.c

I don't know if this trick with a program reading itself as a file counts, strictly speaking, as a quine, but this is my attempt at writing one.

### Version 1.1, June 2022
