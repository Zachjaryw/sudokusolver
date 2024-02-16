import numpy as np
import pandas as pd
import random
import streamlit as st

game = []
initial = []

st.title = "Sudoku Solver"

a,b,c,d,e,f,g,h,i = st.columns([1,1,1,1,1,1,1,1,1])

a1 = a.text_input()
b1 = b.text_input()
c1 = c.text_input()
d1 = d.text_input()

def nextIncomplete():
  for i in range(len(game)):
    if '-' in game[i]:
      return [i,game[i].index('-')]

def setupEmptyGame():
    global game
    global initial
    initial = []
    game = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append('-')
        game.append(row)
        initial.append(row)
    return game

def initilize3x3():
  game_3x3 = []
  for i in range(3):
    row = []
    for j in range(3):
      row.append('-')
    game_3x3.append(row)
  return game_3x3

def generate3x3(game_3x3):
  in3x3 = []
  for i in range(3):
    for j in range(3):
      selection = random.randint(1,9)
      while selection in in3x3:
        selection = random.randint(1,9)
      game_3x3[i][j] = selection
      in3x3.append(selection)
  return game_3x3

def getRows():
  topleft = [[0,0],[3,3],[6,6]]
  setupEmptyGame()
  for pos in topleft:
    game_3x3 = initilize3x3()
    game_3x3 = generate3x3(game_3x3)
    game[pos[0]][pos[1]] = game_3x3[0][0]
    game[pos[0]+1][pos[1]] = game_3x3[0][1]
    game[pos[0]+2][pos[1]] = game_3x3[0][2]
    game[pos[0]][pos[1]+1] = game_3x3[1][0]
    game[pos[0]+1][pos[1]+1] = game_3x3[1][1]
    game[pos[0]+2][pos[1]+1] = game_3x3[1][2]
    game[pos[0]][pos[1]+2] = game_3x3[2][0]
    game[pos[0]+1][pos[1]+2] = game_3x3[2][1]
    game[pos[0]+2][pos[1]+2] = game_3x3[2][2]
  return game #returns a 2d array of rows

def randomizeRemove(gameInput,openSpots = 17):
  for i in range(openSpots):
    row = random.randint(0,8)
    col = random.randint(0,8)
    while gameInput[row][col] == '-':
      row = random.randint(0,8)
      col = random.randint(0,8)
    gameInput[row][col] = '-'
  return gameInput

def displayGame():
  global game
  for row in game:
    print(row)
  print()

def checkComplete(): #returns True if the sudoku board is complete
  for row in game:
    if '-' in row:
      return False
  return True

def getColumns():
  global game
  global columns
  columns = []
  for i in range(9):
    col = []
    for j in range(9):
      col.append(game[j][i])
    columns.append(col)
  return columns # returns a 2d array of columns

def get3x3():
  topleft = [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
  of3x3s = []
  for pos in topleft:
    part = []
    small = []
    for j in range(3):
      smaller = [game[pos[0]+j][pos[1]],
                game[pos[0]+j][pos[1]+1],
                game[pos[0]+j][pos[1]+2]]
      small.extend(smaller)
    of3x3s.append(small)
  return of3x3s # returns a 2d array of 3x3s

def check3x3(checknext): #checks if the 3x3 contains the value
    row = checknext[0]
    col = checknext[1]
    check = 0;
    if row == 0 or row == 1 or row == 2:
        if col == 0 or col == 1 or col == 2:
            check = 0
        elif col == 3 or col == 4 or col == 5:
            check = 1
        elif col == 6 or col == 7 or col == 8:
            check = 2
    elif row == 3 or row == 4 or row == 5:
        if col == 0 or col == 1 or col == 2:
            check = 3
        elif col == 3 or col == 4 or col == 5:
            check = 4
        elif col == 6 or col == 7 or col == 8:
            check = 5
    elif row == 6 or row == 7 or row == 8:
        if col == 0 or col == 1 or col == 2:
            check = 6
        elif col == 3 or col == 4 or col == 5:
            check = 7
        elif col == 6 or col == 7 or col == 8:
            check = 8
    return get3x3()[check]

def solve(gameInput):
    global game
    game = gameInput
    backtrack = []
    go = True
    stop = False
    count = 0
    while checkComplete() == False:
        count +=1
        if go:
            next = nextIncomplete()
            value = 1
            backtrack.append(next)
        else:
            stop = False
            if game[next[0]][next[1]] == 9:
                backtrack.remove(backtrack[-1])
                game[next[0]][next[1]] = '-'
                next = backtrack[-1]
                stop = False
                go = False
            value = game[next[0]][next[1]] + 1
        while (value in game[next[0]] or value in getColumns()[next[1]] or value in check3x3(next)) == True or stop == True:
            value +=1
        if value >= 10:
            game[next[0]][next[1]] = '-'
            go = False
            stop = True
            backtrack.remove(backtrack[-1])
            next = backtrack[-1]
        if value not in game[next[0]] and value not in getColumns()[next[1]] and value not in check3x3(next) and value < 10:
            game[next[0]][next[1]] = value
            go = True
        if count > 200000:
            return (game,np.nan)
    return (game,count)



for i in range(9):
    for j in range(9):
        exec(f'def check{i}{j}(instance,value): game[{i}][{j}] = int(value); initial[{i}][{j}] = int(value)')

def execute(instance):
    global game
    solved = solve(game)
    print(f'It took {solved[1]} steps to complete this puzzle')
    for row in solved[0]:
        print(row)
    print()

def check(instance):
    global initial
    for row in initial:
        print(row)
    print()

game = setupEmptyGame()
