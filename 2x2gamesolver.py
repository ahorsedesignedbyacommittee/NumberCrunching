import tkinter as tk
from numpy import array

#----------------------- Setting up GUI --------------------------------
#Setting up matrix
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

#Importing images
weak_dominance_horizontal = tk.PhotoImage(file = 'weak_dominance_horizontal.gif')
strict_dominance_horizontal = tk.PhotoImage(file = 'strict_dominance_horizontal.gif')
weak_dominance_vertical = tk.PhotoImage(file = 'weak_dominance_vertical.gif')
strict_dominance_vertical = tk.PhotoImage(file = 'strict_dominance_vertical.gif')

def get_row_payoffs():
    #Obtains the row player's payoff matrix from the entry fields
    return [float(ul1entry.get()), float(ur1entry.get()), 
    float(dl1entry.get()), float(dr1entry.get())]

#-------------------- Prepopulating entry fields------------------------

#These two functions facilitate the population of the entry fields for
#the column player payoffs. When insert_zero_sum_payoffs() populates
#the entry field for the column player in each cell with the negative
#of the row player'S payoff in that cell; insert_constant_sum_payoffs()
#populates it with the remainder so that the payoffs of the two players
#in each cell reach a constant sum != 0. In the latter case, the constant
#sum must be provided in the dedicated field. Row player payoffs must always
#be provided. Manual overwriting of the prepopulated entries is possible.

    
def insert_zero_sum_payoffs():
    row_payoffs = get_row_payoffs()
    ul2entry.insert(0, -row_payoffs[0])
    ur2entry.insert(0, -row_payoffs[1])
    dl2entry.insert(0, -row_payoffs[2])
    dr2entry.insert(0, -row_payoffs[3])
    return
    
def insert_constant_sum_payoffs():
    row_payoffs = get_row_payoffs()
    sum = float(constantsumentry.get())
    ul2entry.insert(0, sum-float(row_payoffs[0]))
    ur2entry.insert(0, sum-float(row_payoffs[1]))
    dl2entry.insert(0, sum-float(row_payoffs[2]))
    dr2entry.insert(0, sum-float(row_payoffs[3]))
    return
    
zerosumbutton = tk.Button(text="Zero sum", command=insert_zero_sum_payoffs, width=10)
zerosumbutton.place(x = 20, y = 400)

constantsumbutton = tk.Button(text="Constant sum", command=insert_constant_sum_payoffs, width=10)
constantsumbutton.place(x = 110, y = 400)

constantsumentry = tk.Entry(width = 10)
constantsumentry.place(x = 110, y = 430)


#------------- Generating payoff matrixes for both players -------------
def get_payoffs():
    p_row = array([
        [float(ul1entry.get()), float(dl1entry.get())],
        [float(ur1entry.get()), float(dr1entry.get())],
        ])
    p_column = array([
        [float(ul2entry.get()), float(dl2entry.get())],
        [float(ur2entry.get()), float(dr2entry.get())],
        ])    
    return [p_row, p_column]
    
def dom_checker(p_row, p_column):
    #This function runs dominance (weak or strict) tests for both players
    #The output is dic_of_dominance where each of the four strategies U/D and L/R
    #is coded based on whether it is dominant:
    #0 = no dominance, 1 = weak dominance, 2 = strict dominance
    dic = {"u":0, "d":0, "l":0, "r":0}
    if (p_row[0,:]>p_row[1,:]).any() and (p_row[0,:]>=p_row[1,:]).all():
        dic["u"] = 1
    if (p_row[0,:]>p_row[1,:]).all():
        dic["u"] = 2
    if (p_row[1,:]>p_row[0,:]).any() and (p_row[1,:]>=p_row[0,:]).all():
        dic["d"] = 1
    if (p_row[1,:]>p_row[0,:]).all():
        dic["d"] = 2
    if (p_column[:,0]>p_column[:,1]).any() and (p_column[:,0]>=p_column[:,1]).all():
        dic["l"] = 1
    if (p_column[:,0]>p_column[:,1]).all():
        dic["l"] = 2
    if (p_column[:,1]>p_column[:,0]).any() and (p_column[:,1]>=p_column[:,0]).all():
        dic["r"] = 1
    if (p_column[:,1]>p_column[:,0]).all():
        dic["r"] = 2
    return dic
    
#----------- Checking for pure and mixed strategy equilibria -----------

def pure_equil_checker(p_row, p_column):
    #This function returns a dictionary of the four possible cells 
    #(outcomes) in pure strategies (00 = U/L, 01 = D/L, 10 = UR, 11 = D/R)
    #The value for each cell that is returned will be True if the cell 
    #is a Nash equilibrium, False otherwise
    dic = {"00": False, "01":False, "10":False, "11":False}
    def check_one_cell(s, t):
        #This sub-function runs a Nash equilibrium check on one cell by comparing
        #each player's payoff in that cell against his payoff where he plays his other option
        #but the opponent keeps the strategy constant.
        if p_row[s, t] >= p_row[s, ((t+1)%2)] and p_column[s, t] >= p_column[((s+1)%2), t]:
            dic[f"{s}{t}"] = True
    #This bit calls the check_one_cell sub-function for each of the four cells
    for v in [0,1]:
        for w in [0,1]:
            check_one_cell(v, w)
    return dic
        
def mixed_equil_checker(p_row, p_column):
    #This calculates the probabilities with which the players should play
    #their pure strategies in a mixed strategy Nash equilibirum
    #Probability for row player playing U is p, for D 1-p
    #Probability for column player playing L is q, for R 1-q
    numerator_p = p_column[1,1] - p_column[0,1]
    denominator_p = p_column[0,0] - p_column[0,1] - p_column[1,0] + p_column[1,1]
    numerator_q = p_row[1,1] - p_row[1,0]
    denominator_q = p_row[0,0] - p_row[1,0] - p_row[0,1] + p_row[1,1]
    return (numerator_p / denominator_p, numerator_q / denominator_q)
    
#------------------ Displaying results on the screen -------------------
    
def arrow_painter(dic):
    #This function marks strategies that have been identified as dominant with an arrow
    if dic["u"] + dic["d"] > 0:
        if dic["u"] > 0:
            if dic["u"] == 1:
                i = weak_dominance_horizontal
            else: 
                i = strict_dominance_horizontal
            x1 = 20
            y1 = 140
        if dic["d"] > 0:
            if dic["d"] == 1:
                i = weak_dominance_horizontal
            else:
                i = strict_dominance_horizontal
            x1 = 20
            y1 = 275
        arrow1 = tk.Label(image=i)
        arrow1.place(x = x1, y = y1)
        
    if dic["l"] + dic["r"] > 0:
        if dic["l"] >0:
            if dic["l"] == 1:
                j = weak_dominance_vertical
            else:
                j = strict_dominance_vertical
            x2 = 150
            y2 = 5
        else:
            if dic["r"] == 1:
                j = weak_dominance_vertical
            else:
                j = strict_dominance_vertical
            x2 = 275
            y2 = 5
        arrow2 = tk.Label(image=j)
        arrow2.place(x = x2, y = y2)
        

def pure_equil_painter(dic):
    #This function marks cells that have been identified as 
    #pure stragety Nash equilibria with a frame
    for item in ["00", "01", "10", "11"]:
        if dic[item]:
            if item == "00":
                x11=135
                x22=220
                y11=145
                y22=210
            elif item == "01":
                x11=135
                x22=220
                y11=245
                y22=310
            elif item == "10":
                x11=235
                x22=320
                y11=145
                y22=210
            else:
                x11=235
                x22=320
                y11=245
                y22=310
            canvas.create_rectangle(x11, y11, x22, y22, fill=None, width=5, outline="blue")
            

def oddment_painter (p_here, q_here):
    #This function displays the calculated probabilities in mixed
    #strategy Nash equilibria
    p_label = tk.Label(text = f"p = {round(p_here, 2)}")
    pm1_label = tk.Label(text = f"1-p = {round(1 - p_here, 2)}")
    q_label = tk.Label(text = f"q = {round(q_here, 2)}")
    qm1_label = tk.Label(text = f"1-q = {round(1 - q_here, 2)}")
    p_label.place(x = 350, y = 165)
    pm1_label.place(x = 350, y = 265)
    q_label.place(x = 155, y = 350)
    qm1_label.place(x = 255, y = 350)
    
def calculate():
    #This function performs the calculations by calling a series of other
    #functions above that do parts of the calculcations
    payoffs_row = get_payoffs()[0]
    payoffs_column = get_payoffs()[1]
    dic_of_dominance = dom_checker(payoffs_row, payoffs_column)
    dic_of_pure_equilibria = pure_equil_checker(payoffs_row, payoffs_column)
    if sum(dic_of_dominance.values()) > 0:
        arrow_painter(dic_of_dominance)
    if sum(dic_of_pure_equilibria.values()) > 0:
        pure_equil_painter(dic_of_pure_equilibria)
    p = mixed_equil_checker(payoffs_row, payoffs_column)[0]
    q = mixed_equil_checker(payoffs_row, payoffs_column)[1]
    if 0 < p < 1 and 0 < q < 1:
        oddment_painter(p, q)
        value_row = q * payoffs_row[0, 0] + (1 - q) * payoffs_row[1, 0]
        value_column = p * payoffs_column[0, 0] + (1 - p) * payoffs_column[0, 1]
        vlt = f"Value Row: {round(value_row, 2)}\nValue Column: {round(value_column, 2)}"
        value_label = tk.Label(text = vlt)
        value_label.place(x = 320, y = 380)
    return

#------------------------------ Main program ---------------------------
calculatebutton = tk.Button(text="Calculate", command=calculate, width=10)
calculatebutton.place(x = 350, y = 10)

window.mainloop()
