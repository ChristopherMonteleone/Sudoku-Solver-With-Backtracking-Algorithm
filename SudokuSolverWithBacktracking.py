from tkinter import *
from tkinter import ttk
from random import randint, shuffle

# Project By Chris Monteleone

# Project based on "Python Sudoku Solver with Backtracking" by TechWithTim
# Why My Project Is Unique: 
# TechWithTim's GUI was made in PyGame, mine is made in Tkinter, and I've included additional functionality, 
# including additional GUI and the ability to create randomly generated, solvable boards.


root = Tk() #Root
root.title("Sudoku") #Title of Window
frame = LabelFrame(root, text="Sudoku Project - Chris Monteleone", padx=5, pady=5)
frame.pack(padx=10, pady=10)


#2D array containing default values.
#ROW LEFT / RIGHT
#COLUMN UP / DOWN
grid = [[3, 0, 6, 5, 0, 8, 4, 0, 0], 
        [5, 2, 0, 0, 0, 0, 0, 0, 0], 
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]]

buttonList = [] #List of buttons, a button is an individual square with a number on it
x = 0 # x is the position in the buttonlist. 0 is [0][0], and the largest x is the bottom-
		#right most button.

#Function to initially print the grid to the root. Also animates the starting sequence.
def printGraphic(grid):
	#X is the location of the button in the 1d array
	x = 0

	colorGridGray(grid)

	#Animates the starting sequence, alternates between light gray and gray. 
	for i in range (4):
		frame.update()
		frame.after(500)
		x = 0
		for i in range(9):
			for j in range(9):
				if (buttonList[x]["bg"] == "light gray"):
					buttonList[x].configure(bg = "SystemButtonFace")
				else:
					buttonList[x].configure(bg = "light gray")
				x = x+1

def colorGridGray(grid):
	#X is the location of the button in the 1d array
	x = 0
	#Prints each button to the screen, assigning either light gray or gray based on 3x3 grid.
	for i in range(9):
		for j in range(9):
			buttonList.append(Button(frame, text=grid[i][j], padx=10, pady=10))
			if i < 3 and j < 3:
				buttonList[x].configure(bg = "light gray")
			if i > 5 and j > 5:
				buttonList[x].configure(bg = "light gray")
			if (i < 6 and i > 2) and (j < 6 and j > 2):
				buttonList[x].configure(bg = "light gray")
			if i > 5 and j < 3:
				buttonList[x].configure(bg = "light gray")
			if i < 3 and j > 5:
				buttonList[x].configure(bg = "light gray")
			if (buttonList[x].cget("bg") != "light gray"):
				buttonList[x].configure(bg = "SystemButtonFace")
			buttonList[x].grid(row=i, column=j)
			x = x + 1

#Check if already in Row, True if so, False if not
def usedInRow(grid, row, num): #left / right
	for i in range(	9):
		if(grid[row][i] == num):
			return True
	return False

#Check if already in Column, True if so, False if not
def usedInColumn(grid, col, num): #up / down
	for i in range(9):
		if(grid[i][col] == num):
			return True
	return False

#Check if already in 3x3 Grid, True if so, False if not
def usedInBox(grid, row, col, num):
	for i in range(3):
		for j in range(3):
			if(grid[i+row][j+col] == num):
				return True
	return False

#Check if the number passed in can be placed at the row / col / 3x3 grid location
def checkLocationValidity(grid, row, col, num):
	if usedInRow(grid, row, num) == False:
		if usedInColumn(grid, col, num) == False:
			if usedInBox(grid, row - row % 3, col - col % 3, num) == False:
				return True
	return False

#True / False: Check if there are any locations left with 0 in that spot. L = [0,0], used for
#returning the coordinates of the location of the found 0 (if any are found).
def findEmpty(grid, l):
	for i in range(9):
		for j in range(9):
			if(grid[i][j] == 0):
				l[0] = i
				l[1] = j
				return True
	return False

#Function to solve the grid, updates the root each attempt to "animate".
def solve(grid, solveNewButton, generateNewButton):
	generateNewButton.configure(state="disabled")
	solveNewButton.config(state="disabled")
	l = [0, 0] #will represent the location of the next 0 to attempt to solve.

	if (not findEmpty(grid, l)): #check if there are any 0's left
		return True

	row = l[0]
	col = l[1]

	for num in range(1, 10):
		#If the current location is solvable:
		if (checkLocationValidity(grid, row, col, num)):
			#Try a number, starting at 1 working up to 10.
			grid[row][col] = num
			#Change button to light green when the current number is working. 
			buttonList[row*9+col].configure(bg = "light green")
			#Update the root to the new light green color.
			frame.update()
			frame.after(12) #to turn on/off animation, uncomment /uncomment
			#Update text of current button to the current number we're trying.
			buttonList[row*9+col].configure(text = grid[row][col])
			#Recursively pass the current grid to this solve() function, returns True if solved
			#Returns false if we need to keep going (trying new numbers and backtracking)
			if(solve(grid, solveNewButton, generateNewButton)):
				return True
			#If the number didn't work, set back to 0 to reset for another attempt
			grid[row][col] = 0
	#Change color to yellow if we've had to backtrack. 
	buttonList[row*9+col].configure(bg = "yellow")
	return False
	

#(NOT IN USE) Prints the 2d Grid to the command line
def printGrid(arr):
	for i in range(9):
		for j in range(9):
			if (j < 8):
				print(arr[i][j], end=" ")
			else:
				print(arr[i][j], end="\n")

#Runs after solving has been completed, animates the completion sequence.
def solvingDoneAnimation(grid, generateNewButton):
	x = 0
	#CHANGE TO LIGHT GREEN / GREEN FOR FINISHING ANIMATION
	for i in range(9):
		for j in range(9):
			frame.update()
			frame.after(12) #to turn on animation, uncomment
			if (i < 3 and j < 3) or (i > 5 and j > 5) or (i < 3 and j > 5) or (i > 5 and j < 3) or (j < 6 and i < 6 and j > 2 and i > 2):
				buttonList[x].configure(bg = "light green")
			else:
				buttonList[x].configure(bg = "green")
			x = x+1
	generateNewButton.config(state="active")

#Set each button equal to zero, connected to the "Generate New Grid" button
def generateNewGrid(grid, solveNewButton):
	x = 0
	for i in range(9):
		for j in range(9):
			grid[i][j] = 0
			buttonList[x].configure(text=grid[i][j])
			x = x+1
	frame.update()

	fillGrid(grid)
	removeNumbers(grid)

	x = 0
	for i in range(9):
		for j in range(9):
			buttonList[x].configure(text=grid[i][j])
			x = x+1
	frame.update()

	solveNewButton.config(state="active")
	colorGridGray(grid)

#Check if grid is full, return true if grid is full
def checkGrid(grid):
  for row in range(0,9):
      for col in range(0,9):
        if grid[row][col] == 0:
          return False

  #Grid is full 
  return True

#Filling empty grid to generate new sudoku board.
def fillGridRefined(grid):
	x = 0
	numberList=[1,2,3,4,5,6,7,8,9]
	for row in range(0,9):
		for col in range(0, 9):
			if (grid[row][col] == 0):
				shuffle(numberList)
				for value in numberList:
					if (checkLocationValidity(grid, row, col, value)):
						grid[row][col] = value
						if (checkGrid(grid)):
							return True
						else:
							if (fillGrid(grid)):
								return True
				break
	grid[row][col] = 0

#Recursive Function to Generate New Board
def fillGrid(grid):
  #Find next empty cell
  numberList=[1,2,3,4,5,6,7,8,9]
  for i in range(0,81):
    row=i//9
    col=i%9
    if grid[row][col]==0:
      shuffle(numberList)  
      for value in numberList:
        #Check that this value has not already be used on this row
        if not(value in grid[row]):
          #Check that this value has not already be used on this column
          if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
            #Identify which of the 9 squares we are working on
            square=[]
            if row<3:
              if col<3:
                square=[grid[i][0:3] for i in range(0,3)]
              elif col<6:
                square=[grid[i][3:6] for i in range(0,3)]
              else:  
                square=[grid[i][6:9] for i in range(0,3)]
            elif row<6:
              if col<3:
                square=[grid[i][0:3] for i in range(3,6)]
              elif col<6:
                square=[grid[i][3:6] for i in range(3,6)]
              else:  
                square=[grid[i][6:9] for i in range(3,6)]
            else:
              if col<3:
                square=[grid[i][0:3] for i in range(6,9)]
              elif col<6:
                square=[grid[i][3:6] for i in range(6,9)]
              else:  
                square=[grid[i][6:9] for i in range(6,9)]
            #Check that this value has not already be used on this 3x3 square
            if not value in (square[0] + square[1] + square[2]):
              grid[row][col]=value
              if checkGrid(grid):
                return True
              else:
                if fillGrid(grid):
                  return True
      break
  grid[row][col]=0

#Reset x numbers to zero if not already zero.
def removeNumbers(grid):
	x = 0
	while (x < 45):
		row = randint(0,8)
		col = randint(0,8)
		if (grid[row][col] != 0):
			grid[row][col]=0
			x = x+1

def solveAndAnimate(grid, solveNewButton, generateNewButton):
	solve(grid, solveNewButton, generateNewButton)
	solvingDoneAnimation(grid, generateNewButton)
	solveNewButton.config(state="disabled")
	generateNewButton.config(state="active")

def main():

	buttonFrame = LabelFrame(root, text="Options", padx=5, pady=5)
	buttonFrame.pack(padx=10, pady=10)

	generating = True; #While generating, set to true, gray out Generate New and Solve Buttons


	#Create Generate New Button (does not place it on the screen)
	generateNewButton = Button(buttonFrame, text="Generate New Grid", padx=10, pady = 10, state="disabled") #state="disabled" padx and pady=10 to increase size
	solveNewButton = Button(buttonFrame, text="Solve New Grid", padx=10, pady = 10, state="disabled")
	#Connect the Generate New Grid button to the clearGrid Function (just changes to 0 for now)
	generateNewButton.config(command=lambda: generateNewGrid(grid, solveNewButton)) #not sure that this is right...
	solveNewButton.config(command=lambda: solveAndAnimate(grid, solveNewButton, generateNewButton))
	#Generate New button, assign to root at the position under the grid
	generateNewButton.grid(row = 10, column = 0, columnspan=3, sticky = W)
	solveNewButton.grid(row = 10, column = 6, columnspan=3, sticky = E)

	#Prints initial grid to the screen
	printGraphic(grid)
	#Update the root
	frame.update()
	#Pauses 1 sec before solving grid, after starting animation.
	frame.after(1000)
	#Solves the grid, updates after each attempt to solve
	solve(grid, solveNewButton, generateNewButton)
	generating = False
	root.update() #updates buttons, no longer grayed out while generating
	#Flashes the screen green / light green to show completion.
	solvingDoneAnimation(grid, generateNewButton)
	

	root.mainloop()



main()