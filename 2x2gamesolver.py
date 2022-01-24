import tkinter as tk
import tkinter.messagebox
from functools import partial

# ----------------------- Setting up GUI --------------------------------
# Setting up home screen
window = tk.Tk()
window.title("2x2 simultaneous game solver")
canvas = tk.Canvas()
canvas.config(width = 450, height = 450)
canvas.create_rectangle(125, 125, 325, 325)
canvas.pack()
rowplayerlabel = tk.Label(text="Row\nplayer")
columnplayerlabel = tk.Label(text="Column\nplayer")
columnplayerlabel.place(x=210, y = 70)
rowplayerlabel.place(x=30, y = 200)
ulabel = tk.Label(text = "U")
ulabel.place(x=100, y = 165)
dplabel = tk.Label(text = "D")
dplabel.place(x=98, y = 265)
llabel = tk.Label(text = "L")
llabel.place(x=175, y = 95)
rlabel = tk.Label(text = "R")
rlabel.place(x=275, y = 95)
#Setting up payoff entry fields
ul1entry = tk.Entry(width=6)
ul1entry.place(x = 150, y = 190)
ul2entry = tk.Entry(width=6)
ul2entry.place(x = 180, y = 160)
ur1entry = tk.Entry(width=6)
ur1entry.place(x = 250, y = 190)
ur2entry = tk.Entry(width=6)
ur2entry.place(x = 280, y = 160)
dl1entry = tk.Entry(width=6)
dl1entry.place(x = 150, y = 290)
dl2entry = tk.Entry(width=6)
dl2entry.place(x = 180, y = 260)
dr1entry = tk.Entry(width=6)
dr1entry.place(x = 250, y = 290)
dr2entry = tk.Entry(width=6)
dr2entry.place(x = 280, y = 260)

# Importing images
weak_dominance_horizontal = tk.PhotoImage(file = 'weak_dominance_horizontal.gif')
strict_dominance_horizontal = tk.PhotoImage(file = 'strict_dominance_horizontal.gif')
weak_dominance_vertical = tk.PhotoImage(file = 'weak_dominance_vertical.gif')
strict_dominance_vertical = tk.PhotoImage(file = 'strict_dominance_vertical.gif')

# One global variable that will become of relevance for oddment calculations (which do not work in presence of strict dominance)
strict_dominance_exists = False


# ------------- Generating payoff matrixes for both players -------------

def insert_constant_sum_payoffs():
    if constantsumentry.get() == "" or constantsumentry.get() == None:
        sum = 0
    else:
        sum = float(constantsumentry.get())
    map_dict = {ul2entry:ul1entry, ur2entry:ur1entry, dl2entry:dl1entry, dr2entry:dr1entry}
    try:
        for column_entry_field in map_dict:
            new_value = sum - float(map_dict[column_entry_field].get())
            # The following block is to nicely display inserted values wihtout decimals if they are integers. For the calculations later on, all payoffs will be entered as floats into the payoff matrix
            if new_value.is_integer():
                new_value = int(new_value)  
            column_entry_field.insert(0, new_value)
    except ValueError:
        warning2 = tkinter.messagebox.showinfo(message="Please fill in all Row player fields.")
    

def get_payoffs():
    # Returns payoff matrix as a list in form: 
    # [ 
    #       [[Row-up-left, Row-up-right], [Row-down-left, Row-down-right]],
    #       [[Column-up-left, Column-up-right], [Column-down-left, Column-down-right]]
    # ]
    try:
        
        payoffs = [
        
            [
                [float(ul1entry.get()), float(ur1entry.get())],
                [float(dl1entry.get()), float(dr1entry.get())],
            ],
        
            [
                [float(ul2entry.get()), float(ur2entry.get())],
                [float(dl2entry.get()), float(dr2entry.get())],
            ]
        ]
        return payoffs
        
    except ValueError:
        return None
        
        
def flip(x): # Turns an index number of 0 or 1 into its opposite
    return ((x + 1) % 2)
        
        
def dominancechecker(checked1, alternative1, checked2, alternative2): # Checks a given strategy for strict or weak dominance over its alternative
    if (checked1 == alternative1) and (checked2 == alternative2):
        return 0
    if (checked1 > alternative1) and (checked2 > alternative2):
        global strict_dominance_exists 
        strict_dominance_exists = True
        return 2
    if (checked1 >= alternative1) and (checked2 >= alternative2):
        return 1
    return 0
    
    
def arrow_painter(list):
    
    if list[0] + list[1] > 0: # Tests if there is any dominance among U and D (the row player's strategies)
        if list[0] > 0:
            if list[0] == 1:
                i = weak_dominance_horizontal
            else: 
                i = strict_dominance_horizontal
            x1 = 20
            y1 = 140
        if list[1] > 0:
            if list[1] == 1:
                i = weak_dominance_horizontal
            else:
                i = strict_dominance_horizontal
            x1 = 20
            y1 = 275
        arrow1 = tk.Label(image=i)
        arrow1.place(x = x1, y = y1)
        
    if list[2] + list[3] > 0: # Tests if there is any dominance among L and R (the column player's strategies)
        if list[2] >0:
            if list[2] == 1:
                j = weak_dominance_vertical
            else:
                j = strict_dominance_vertical
            x2 = 150
            y2 = 5
        else:
            if list[3] == 1:
                j = weak_dominance_vertical
            else:
                j = strict_dominance_vertical
            x2 = 275
            y2 = 5
        arrow2 = tk.Label(image=j)
        arrow2.place(x = x2, y = y2)
    
    return
    
    
def nashequil(payoffs):
    number_of_pure_strategy_equilibria = 0
    row_player_payoff = None
    column_player_payoff = None
    for j in range(2):
        for k in range(2):
            if (payoffs[0][k][j] >= payoffs[0][flip(k)][j]) and (payoffs[1][k][j] >= payoffs[1][k][flip(j)]):
                    number_of_pure_strategy_equilibria += 1
                    if (j == 0) and (k == 0):
                        canvas.create_rectangle(135, 145, 220, 210, fill=None, width=5, outline="blue") # Up-Left
                        row_player_payoff = payoffs[0][0][0]
                        column_player_payoff = payoffs[1][0][0]
                    if (j== 0) and (k == 1):
                        canvas.create_rectangle(135, 245, 220, 310, fill=None, width=5, outline="blue") # Down-Left
                        row_player_payoff = payoffs[0][1][0]
                        column_player_payoff = payoffs[1][1][0]
                    if (j == 1) and (k == 0):
                        canvas.create_rectangle(235, 145, 320, 210, fill=None, width=5, outline="blue") # Up-Right
                        row_player_payoff = payoffs[0][0][1]
                        column_player_payoff = payoffs[1][0][1]
                    if (j == 1) and (k == 1):
                        canvas.create_rectangle(235, 245, 320, 310, fill=None, width=5, outline="blue") # Down-right
                        row_player_payoff = payoffs[0][1][1]
                        column_player_payoff = payoffs[1][1][1]
                
    return (number_of_pure_strategy_equilibria, row_player_payoff, column_player_payoff)
    
    
        
        
def calculate():
    payoffs = get_payoffs()
    if payoffs == None:
        msgwrng3 = "Please ensure all fields are filled before proceeding."
        warning3 = tkinter.messagebox.showinfo(message=msgwrng3)
        return
    
    dominance_results = [0, 0, 0, 0] # Preparing list of results of dominance checks
    # Running dominance checks for row player:
    for i in range(2):
        dominance_results[i] = dominancechecker(payoffs[0][i][0], payoffs[0][flip(i)][0], payoffs[0][i][1], payoffs[0][flip(i)][1])
    
    # Running dominance checks for column player
    for i in range(2):
        dominance_results[i + 2] = dominancechecker(payoffs[1][0][i], payoffs[1][0][flip(i)], payoffs[1][1][i], payoffs[1][1][flip(i)])
        
    # dominance_results is now a list of four variables where 2 reflects a strictly cominant strategy, 1 a weakly dominant one, and 0 a non-dominant strategy
    # These variables correspond to the following strategies: [Row-Up, Row-Down, Column-Left, Column-Right]
    if sum(dominance_results) > 0: # Calls the arrow_painter function (which displays dominance results graphically) if some dominance is present
        arrow_painter(dominance_results)
    results_of_nash_analysis = nashequil(payoffs) # Calls the function to check for Nash equilibria
        
    # The following part calculates the value of the game:   
    if results_of_nash_analysis[0] == 1: # Means there is only one pure strategy Nash equilibrium
        p = results_of_nash_analysis[1]
        q = results_of_nash_analysis[2]
        value_to_row_player = results_of_nash_analysis[1]
        value_to_column_player = results_of_nash_analysis[2]
    else:
        # This part calculates the probabilities with which the players should play
        # their pure strategies in a mixed strategy Nash equilibirum
        # Probability for row player playing U is p, for D 1-p
        # Probability for column player playing L is q, for R 1-q
        numerator_q = payoffs[0][1][1] - payoffs[0][0][1]
        denominator_q = payoffs[0][0][0] - payoffs[0][0][1] - payoffs[0][1][0] + payoffs[0][1][1]
        numerator_p = payoffs[1][1][1] - payoffs[1][1][0]
        denominator_p = payoffs[1][0][0] - payoffs[1][1][0] - payoffs[1][0][1] + payoffs[1][1][1]
        p = numerator_p / denominator_p
        q = numerator_q / denominator_q
        p_label = tk.Label(text = f"p = {round(p, 2)}")
        pm1_label = tk.Label(text = f"1-p = {round(1 - p, 2)}")
        q_label = tk.Label(text = f"q = {round(q, 2)}")
        qm1_label = tk.Label(text = f"1-q = {round(1 - q, 2)}")
        p_label.place(x = 350, y = 165)
        pm1_label.place(x = 350, y = 265)
        q_label.place(x = 155, y = 350)
        qm1_label.place(x = 255, y = 350)
        value_to_row_player = payoffs[0][0][0] * p + payoffs[0][1][0] * (1 - p)
        value_to_column_player = payoffs[1][0][0] * q + payoffs[1][0][1] * (1 - q)
        
    value_label = tk.Label(text = f"Values:\nRow player: {round(value_to_row_player, 2)}\nColumn player: {round(value_to_column_player, 2)}")
    value_label.place(x = 330, y = 380)

    return
    
    
calculatebutton = tk.Button(text="Calculate", command=calculate, width=10)
calculatebutton.place(x = 350, y = 10)        
        
zerosumbutton = tk.Button(text="Zero sum", command=insert_constant_sum_payoffs, width=10)
zerosumbutton.place(x = 20, y = 400)

constantsumentry = tk.Entry(width = 10)
constantsumentry.place(x = 110, y = 430)

constantsumbutton = tk.Button(text="Constant sum", command=insert_constant_sum_payoffs, width=10)
constantsumbutton.place(x = 110, y = 400)

# ---------------------------- Main program ----------------------------

window.mainloop()
