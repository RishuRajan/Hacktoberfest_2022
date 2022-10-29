# Import the modules

import tkinter

import random




# List of colours

colours = ['Pink', 'Blue', 'Green', 'Orange', 'Black', 'Yellow', 'Purple', 'White', 'Brown']




# Initialising score to 0

score = 0




# Initialy the time will be 25 seconds

remainingtime = 25




# This function will begin the game

def beginGame(event):




if remainingtime == 25:




# If the above statement is satisfied, we are beginning the countdown

countdown()




# Here, we are calling function to choose the next colour

nextColour()




# This function will choose the next color

def nextColour():




global score

global remainingtime




# If statement

if remainingtime > 0:




# If the above statement is satisfied, we are making the text entry box active

i.focus_set()




# If the input color name and colou of the text are matching,

if i.get().lower() == colours[1].lower():




# we are increasing the score by 5

score += 5




# Using, delete function, we are deleting the text of the box

i.delete(0, tkinter.END)




# The random generates a random colour using shuffle

random.shuffle(colours)




# Here, we are changing the text colour to a random colour value

label.config(fg = str(colours[1]), text = str(colours[0]))




# Here, we are updating the score

scoreLabel.config(text = "Score : " + str(score))







# This is countdown function

def countdown():




global remainingtime




if remainingtime > 0:




# If the above statement is satisfied, we will decrement the time by 1 second

remainingtime -= 1




# Here, we are updating the remaining time label

timeLabel.config(text = "Remaining time : " + str(remainingtime))




# after function, calls function once after given time in milliseconds.

timeLabel.after(1000, countdown)




# To create GUI window

root = tkinter.Tk()




# To set the title

root.title("COLOR GAME")




# To set the size

root.geometry("900x600")




# Here, we are adding an instruction label

instruction = tkinter.Label(root, text = "\n Type the colour of the words, and not the word text! \n", font = ('TimesNewRoman', 20))

instruction.pack()




scoreLabel = tkinter.Label(root, text = "Press Enter to Play \n", font = ('TimesNewRoman', 20))

scoreLabel.pack()




# Remaining time label

timeLabel = tkinter.Label(root, text = "Remaining time: " + str(remainingtime), font = ('TimesNewRoman', 20))

timeLabel.pack()




# Color text font and size specification

label = tkinter.Label(root, font = ('TimesNewRoman', 80))

label.pack()




# Input text box

i = tkinter.Entry(root)




# To run the 'beginGame' function when the Enter key is pressed

root.bind('<Return>', beginGame)

i.pack()




# To set focus on the input box

i.focus_set()




# To start the GUI

root.mainloop()