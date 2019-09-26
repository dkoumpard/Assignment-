#Author:Koumpardas Dimitrios
############################
#Program: Find all possible knight movement given a start and end point for a max number of moves
#
#Known Bugs:
#1.When displaying Moves sequences in window if the number  of sequences is very large some are displayed outside window boarders.
#  In command line all sequences are displayed.
#2.Some sequences are not displayed correctly on chessboard. Latter movements cover previous movements that was already drawn.
#3.Window is not responsive until movement calculation is completed.

from enum import Enum
from tkinter import *
import tkinter
import numpy as np
import copy

window = tkinter.Tk()
window.title("Knight Movement")

#enum that represents the correspondence chessboard column name and a number
class column(Enum):
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8

#variables
temp_in = np.empty(2, dtype=int)
cb_gui = np.empty((8,8), dtype = object)
start_pos = np.empty(2, dtype=int)
end_pos = np.empty(2, dtype=int)
chess_board = np.zeros((8,8), dtype=int)
movement = [[2,-1],[2,1],[1,2],[1,-2],[-2,1],[-2,-1],[-1,-2],[-1,2]]
results = []
step_num = 3
for_in = 0
i = 0
output_str = StringVar()
output_str.set(" ")
board_symbols = np.empty((8,8), dtype = object)
set_up_str = ""
to_animate = ""



#Function get_input(): Is a function to be called when button <Save and Search> is pressed
#Operation: Saves start and end position and number of moves then calls search() function
#and display the results in both window and command line
def get_input():
    global step_num
    global results
    global set_up_str
    set_up_str = ""
    results = []
    for i in range(8):
        for j in range(8):
            chess_board[i][j] = 0
            board_symbols[i][j].set(" ")
            
    temp = entry1.get()
    start_pos[1] = column[temp[0].lower()].value
    start_pos[0] = 9 - int(temp[1])
    temp = entry2.get()
    end_pos[1] = column[temp[0].lower()].value
    end_pos[0] = 9 - int(temp[1])
    temp = entry3.get()
    step_num = int(temp)

    chess_board[start_pos[0]-1][start_pos[1]-1] = 1
    chess_board[end_pos[0]-1][end_pos[1]-1] = 2

    temp_in[0] = start_pos[0] - 1
    temp_in[1] = start_pos[1] - 1

    search(step_num, temp_in, "")

    for b in results:
        set_up_str = set_up_str + b + "\n"
      
    output_str.set("S: " + column(start_pos[1]).name + str(9 - start_pos[0]) + "\n" + "E: " + \
                   column(end_pos[1]).name + str(9 - end_pos[0]) + "\n" + "Maximum number of moves: " + \
                   str(step_num)+ "\n" + "Moves: \n" + set_up_str)
    print("S: " + column(start_pos[1]).name + str(9 - start_pos[0]) + "\n" + "E: " + \
                   column(end_pos[1]).name + str(9 - end_pos[0]) + "\n" + "Maximum number of moves: " + \
                   str(step_num)+ "\n" + "Moves: \n" + set_up_str)
    

#Funtion search(iteration, position, sequence): Is a function called by get_input().
#Operation: Given three arguments, number of moves, start position and a string
#(empty at first call) searches, recursivly, for all possible movements that reach the end position
#**************************************************************************************************
def search(iteration, position, sequence):
    position = copy.deepcopy(position)
    sequence = copy.deepcopy(sequence)
    posit = np.empty(2, dtype=int)

    if chess_board[position[0]][position[1]] == 2:
        results.append(sequence + "->" + column(position[1] + 1).name + str(8 - position[0]))
        return

    i = iteration - 1
    if i < 0:
        return

    if  not sequence:
        new_sequence = column(position[1] + 1).name + str(8 - position[0])
    else:
        new_sequence = sequence + '->' + column(position[1] + 1).name + str(8 - position[0])

    #for each possible movement call search
    posit[0] = position[0] + 2
    posit[1] = position[1] + 1
    if (posit[0] in range(8) and posit[1] in range(8)):
        search(i, posit, new_sequence)
    posit[0] = position[0] + 2
    posit[1] = position[1] - 1
    if (posit[0] in range(8) and posit[1] in range(8)):
        search(i, posit, new_sequence)
    posit[0] = position[0] - 2
    posit[1] = position[1] + 1
    if (posit[0] in range(8) and posit[1] in range(8)):
        search(i, posit, new_sequence)
    posit[0] = position[0] - 2
    posit[1] = position[1] - 1
    if (posit[0] in range(8) and posit[1] in range(8)):
        search(i, posit, new_sequence)
    posit[0] = position[0] + 1
    posit[1] = position[1] + 2
    if (posit[0] in range(8) and posit[1] in range(8)):
        search(i, posit, new_sequence)
    posit[0] = position[0] + 1
    posit[1] = position[1] - 2
    if (posit[0] in range(8) and posit[1] in range(8)):
        search(i, posit, new_sequence)
    posit[0] = position[0] - 1
    posit[1] = position[1] + 2
    if (posit[0] in range(8) and posit[1] in range(8)):
        search(i, posit, new_sequence)
    posit[0] = position[0] - 1
    posit[1] = position[1] - 2
    if (posit[0] in range(8) and posit[1] in range(8)):
        search(i, posit, new_sequence)


#Function draw_seq(): Is a function to be called when button <Draw> is pressed
#Operation: Display on the chessboard, for a given move sequence, a visual
#representation of the move
#*****************************************************************************
def draw_seq():
    for i in range(8):
        for j in range(8):
            board_symbols[i][j].set(" ")

    board_symbols[end_pos[0] -1][end_pos[1] -1].set("End")
    board_symbols[start_pos[0] -1][start_pos[1] -1].set("Start")
    to_animate = results[int(entry4.get())-1].split("->")
    for k in range(0, len(to_animate)-1):
        if (column[to_animate[k+1][0].lower()].value - column[to_animate[k][0].lower()].value) == 2:
            board_symbols[8-int(to_animate[k][1])][column[to_animate[k][0].lower()].value].set(">")
            board_symbols[8-int(to_animate[k][1])][column[to_animate[k][0].lower()].value + 1].set(">")
        if (column[to_animate[k+1][0].lower()].value - column[to_animate[k][0].lower()].value) == -2:
            board_symbols[8-int(to_animate[k][1])][column[to_animate[k][0].lower()].value -2].set("<")
            board_symbols[8-int(to_animate[k][1])][column[to_animate[k][0].lower()].value -3].set("<")
        if((8-int(to_animate[k + 1][1])) - (8-int(to_animate[k][1]))) == 2:
            board_symbols[8-int(to_animate[k][1])+1][column[to_animate[k][0].lower()].value -1].set("V")
            board_symbols[8-int(to_animate[k][1])+2][column[to_animate[k][0].lower()].value -1].set("V")   
        if((8-int(to_animate[k + 1][1])) - (8-int(to_animate[k][1]))) == -2:
            board_symbols[8-int(to_animate[k][1])-1][column[to_animate[k][0].lower()].value -1].set("^")
            board_symbols[8-int(to_animate[k][1])-2][column[to_animate[k][0].lower()].value -1].set("^")
    for k in range(0, len(to_animate)-1):
        board_symbols[8-int(to_animate[k][1])][column[to_animate[k][0].lower()].value - 1].set("X")
    board_symbols[start_pos[0] -1][start_pos[1] -1].set("Start")


#MAIN CODE: The main code contains code, creating all the elements of the window to be displayed
#and calls function window.mainloop() wich is responsible drawing the window
#***********************************************************************************************
#Draw chessboard labels
tkinter.Label(window, text = " ", width = 6, height = 3).grid(column = 0, row = 0)
tkinter.Label(window, text = "A", width = 6, height = 3).grid(column = 1, row = 0)
tkinter.Label(window, text = "B", width = 6, height = 3).grid(column = 2, row = 0)
tkinter.Label(window, text = "C", width = 6, height = 3).grid(column = 3, row = 0)
tkinter.Label(window, text = "D", width = 6, height = 3).grid(column = 4, row = 0)
tkinter.Label(window, text = "E", width = 6, height = 3).grid(column = 5, row = 0)
tkinter.Label(window, text = "F", width = 6, height = 3).grid(column = 6, row = 0)
tkinter.Label(window, text = "G", width = 6, height = 3).grid(column = 7, row = 0)
tkinter.Label(window, text = "H", width = 6, height = 3).grid(column = 8, row = 0)
tkinter.Label(window, text = "8", width = 6, height = 3).grid(column = 0, row = 1)
tkinter.Label(window, text = "7", width = 6, height = 3).grid(column = 0, row = 2)
tkinter.Label(window, text = "6", width = 6, height = 3).grid(column = 0, row = 3)
tkinter.Label(window, text = "5", width = 6, height = 3).grid(column = 0, row = 4)
tkinter.Label(window, text = "4", width = 6, height = 3).grid(column = 0, row = 5)
tkinter.Label(window, text = "3", width = 6, height = 3).grid(column = 0, row = 6)
tkinter.Label(window, text = "2", width = 6, height = 3).grid(column = 0, row = 7)
tkinter.Label(window, text = "1", width = 6, height = 3).grid(column = 0, row = 8)

#Draw chessboard pattern
for i in range(1,9):
    for j in range(1,9):
        if not((i+j)%2):
            board_symbols[i-1][j-1] = StringVar()
            cb_gui[i-1][j-1] = tkinter.Label(window, text = " ", width = 6, height = 3,fg = "#3f0", bg = "#fff", textvariable = board_symbols[i-1][j-1])
            cb_gui[i-1][j-1].grid(column = j, row = i)
        if    ((i+j)%2):
            board_symbols[i-1][j-1] = StringVar()
            cb_gui[i-1][j-1] = tkinter.Label(window, text = " ", width = 6, height = 3,fg = "#3f0", bg = "#000", textvariable = board_symbols[i-1][j-1])
            cb_gui[i-1][j-1].grid(column = j, row = i)

#Buttons and search boxes
output = tkinter.Label(window, width = 6, height = 20, textvariable = output_str)
output.grid(column = 0, row = 20, columnspan = 20, rowspan = 20, sticky = W+E+S )

tkinter.Label(window,text = "Start point").grid(column = 10, row = 0)
entry1 = tkinter.Entry(window)
entry1.grid(column = 11, row = 0)
 
tkinter.Label(window,text = "End point").grid(column = 12, row = 0)
entry2 = tkinter.Entry(window)
entry2.grid(column = 13, row = 0)     
   
tkinter.Label(window,text = "Number of steps:").grid(column = 14, row = 0)
entry3 = tkinter.Entry(window)
entry3.grid(column = 15, row = 0)

btn = tkinter.Button(window, text = "Save and Search", command = get_input)
btn.grid(column = 10, row = 1)

output_str.set("Please enter Start/End points and number of steps and press <Save and Search> (It may take a few moments)")

tkinter.Label(window,text = "Choose output sequence(1 to Max)").grid(column = 10, row = 5)
entry4 = tkinter.Entry(window)
entry4.grid(column = 11, row = 5)
tkinter.Button(window, text = "Draw", command = draw_seq).grid(column = 10, row = 6)

#Start window mainl loop
window.mainloop()
