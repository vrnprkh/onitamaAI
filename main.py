from board import Board
from cards import cards
from engine import *
import random
searchDepth = 7

gameBoard = Board(random.sample(cards,5))

# cardnum = [3,8,15,5,9]
# gameBoard = Board([cards[cardnum[0]], cards[cardnum[1]], cards[cardnum[2]], cards[cardnum[3]], cards[cardnum[4]]])

letterToNum = {
  'a':1,
  'b':2,
  'c':3,
  'd':4,
  'e':5,
}
numToLetter = {
  0:'a',
  1:'b',
  2:'c',
  3:'d',
  4:'e',
}

def inputToMove(name, coord1, coord2):
  try:
    if name == "ai":
      # game is [board, inverted, whiteHand, blackHand, sideHand]

      if gameBoard.turn == 1:
        maximizing = False
      else:
        maximizing = True

      result = minimax([gameBoard.board, not maximizing, gameBoard.whiteHand, gameBoard.blackHand, gameBoard.side], searchDepth, -1001, 1001, maximizing)
      print("Eval: " + str(result[1]))
      move = result[0]
      
      print(str(move[0]) + ' ' + numToLetter[move[1][1]] + str(5 - move[1][0]) + ' to ' + numToLetter[move[2][1]] + str(5 - move[2][0]))
        
      
    else:
      move = (name.capitalize(), (5 - int(coord1[1]), letterToNum[coord1[0].lower()] - 1 ), (5 - int(coord2[1]), letterToNum[coord2[0].lower()] - 1 ))
    return move

  except:
    print('Input Error')
    return False

running = True
print(gameBoard.textDraw())
while running:
  
  # name = input('name: ')
  # coord1 = input('coord1: ')
  # coord2 = input('coord2: ')
  name = "ai"
  coord1 = 0
  coord2 = 0
  print("____________________________________\n")
  move = inputToMove(name, coord1, coord2)
  if move == False:
    pass
  else:
    result = gameBoard.makeMove(move)
    if not result:
      print("Illegal Move")
  
  
  print(gameBoard.textDraw())
  
  winStatus = gameBoard.checkWin()

  if winStatus == -1:
    pass
  elif winStatus == 0:
    print("White Wins!")
    running = False
  elif winStatus == 1:
    print("Black Wins!")
    running = False

  