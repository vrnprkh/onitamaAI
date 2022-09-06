# Board class contains the game given a deck of 5 cards
# A card is a tuple ("Name", (offset1, offset2, offset3, ...), turn)
# turn is 0 or 1 (player0 or player1)
# offset is a tuple (y, x)
# the seed is the inital state of the board (card1, card2, card3, card4, card5)
# Player 0 is white
# Player 1 is black

# organized as follows:

# P0: card1, card2
# SIDE: card5
# P1: card3, card4

#black will be far side
#white will be close side

# a move is in the form:
# ("Name", pieceCoord (y,x), finalCoord (y,x) )

from hashlib import new
from re import search


class Board:
  def __init__(self, deck):
    self.whiteHand = [deck[0], deck[1]]
    self.blackHand = [deck[2], deck[3]]
    self.side = deck[4]

    self.turn = deck[4][2]

    # 1 = White Pawn
    # 2 = White Master
    # 3 = Black Pawn
    # 4 = Black Master
    self.board = [
      [3, 3, 4, 3, 3],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [1, 1, 2, 1, 1],
    ]
  
  # swaps turn
  def changeTurn(self):
    if self.turn == 0:
      self.turn = 1
    else:
      self.turn = 0
    
  # returns if a coord is in the board
  def inBoard(self, y, x):
    if (x >= 0) and (y >= 0) and (x <= 4) and (y <= 4):
      return True
    else:
      return False
  

  # swaps the card with Name, from current turn players hand with side, returns True if succesful, False if card not found
  # find a better way to do this lol
  def swap(self, Name):
    if self.turn == 0:
      for e in self.whiteHand:
        if e[0] == Name:
          tempCard = e
          self.whiteHand.append(self.side)
          self.whiteHand.remove(tempCard)
          self.side = tempCard
          return True
    else:
      for e in self.blackHand:
        if e[0] == Name:
          tempCard = e
          self.blackHand.append(self.side)
          self.blackHand.remove(tempCard)
          self.side = tempCard
          return True
    return False
      

  # returns a legal list of moves
  def getLegal(self):
    if self.turn == 0:
      tempMoves = [e for e in self.whiteHand]
      searchPieces = (1, 2)
    else: # invert moves (-y, -x)
      tempMoves = [(e[0], tuple([(-offset[0], -offset[1]) for offset in e[1]]), e[2]) for e in self.blackHand]
      searchPieces = (3, 4)
    
    legalMoves = []
    
    for y, layer in enumerate(self.board):
      for x, piece in enumerate(layer):
        if piece in searchPieces:
          for move in tempMoves:
            for offset in move[1]:
              if self.inBoard(y + offset[0], x + offset[1]):
                newSquare = self.board[y + offset[0]][x + offset[1]]
                
                # if not (newSquare in searchPieces): test this
                if not (((self.turn == 0) and (newSquare == 1 or newSquare == 2)) or ((self.turn == 1) and (newSquare == 3 or newSquare == 4))):
                  legalMoves.append((move[0], (y, x), (y + offset[0], x + offset[1])))

    if len(legalMoves) == 0:
      return [(mov[0], (0,0), (0,0)) for mov in self.tempMoves]
    else:
      return legalMoves

  
  # attempts to make move, returns True if succeesful, False otherwise.
  def makeMove(self, move):
    if move not in self.getLegal():
      return False
    
    self.swap(move[0])
    piece = self.board[move[1][0]][move[1][1]]
    self.board[move[1][0]][move[1][1]] = 0
    self.board[move[2][0]][move[2][1]] = piece
    self.changeTurn()
    return True
  
  # returns 0 for white win, 1 for black win, -1 for neither
  def checkWin(self):
    found2 = False
    found4 = False
    for layer in self.board:
      for e in layer:
        if e == 2:
          found2 = True
        if e == 4:
          found4 = True
    
    if (self.board[0][2] == 2) or (found4 == False):
      return 0
    if (self.board[4][2] == 4) or (found2 == False):
      return 1
    
    return -1
    
    
    
    

  #DRAWING:

  # draws 2 cards, inverted is true or false, returns a string
  # fix this, pre shitty way to implement this
  # assumes the offsets are max of 2 otherwise will throw error
  def drawCards(self, cards, inverted):
    drawBoard = [
      [' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' '], # names
      ['.', '.', '.', '.', '.', ' ', '|', '.', '.', '.', '.', '.', ' '], # movements 
      ['.', '.', '.', '.', '.', ' ', '|', '.', '.', '.', '.', '.', ' '],
      ['.', '.', 'O', '.', '.', ' ', '|', '.', '.', 'O', '.', '.', ' '],
      ['.', '.', '.', '.', '.', ' ', '|', '.', '.', '.', '.', '.', ' '],
      ['.', '.', '.', '.', '.', ' ', '|', '.', '.', '.', '.', '.', ' '],
    ]
    
    tempCards = []
    if inverted:
      tempCards = [(e[0], tuple([(-offset[0], -offset[1]) for offset in e[1]]), e[2]) for e in cards]
      
      
    else:
      tempCards = [e for e in cards]
    

    for k in range(2):
      #names
      for i in range(min(len(tempCards[k][0]), 6)):
        drawBoard[0][k * 7 + i] = tempCards[k][0][i]
      
      #movements
      for offset in tempCards[k][1]:
        drawBoard[offset[0] + 3][offset[1] + 2 + k * 7] = "X"
      
    drawStr = ""
    for layer in drawBoard:
      layerStr = ""
      for e in layer:
        layerStr += e
      
      
      drawStr += layerStr + "\n"

    return drawStr


  #draws board, and side move
  def drawBoard(self):
    drawGrid = [
      [' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' '], # names
      ['.', '.', '.', '.', '.', '|', '.', '.', '.', '.', '.', ' '], # movements 
      ['.', '.', '.', '.', '.', '|', '.', '.', '.', '.', '.', ' '],
      ['.', '.', '.', '.', '.', '|', '.', '.', 'O', '.', '.', ' '],
      ['.', '.', '.', '.', '.', '|', '.', '.', '.', '.', '.', ' '],
      ['.', '.', '.', '.', '.', '|', '.', '.', '.', '.', '.', ' '],
    ]
    if self.turn == 0:
      inverted = False
    else:
      inverted = True
  
    if inverted:
      tempCard = (self.side[0], ((-offset[0], -offset[1]) for offset in self.side[1]), self.side[2])
    else:
      tempCard = self.side
    
    for offset in tempCard[1]:
      drawGrid[offset[0] + 3][offset[1] + 8] = 'X'
    for i in range(min(6, len(tempCard[0]))):
      drawGrid[0][i + 6] = tempCard[0][i]
    
    for y, layer in enumerate(self.board):
      for x, e in enumerate(layer):
        if e == 0:
          pass
        else:
          drawGrid[y + 1][x] = str(e)
    
    drawStr = ''
    for layer in drawGrid:
      layerStr = ''
      for e in layer:
        layerStr += e
      
      drawStr += layerStr + '\n'

    return drawStr
    
  
  def textDraw(self):
    blackMoves = self.drawCards(self.blackHand, True)
    whiteMoves = self.drawCards(self.whiteHand, False)
    boardStr = self.drawBoard()
    if self.turn == 1:
      turn = "Black ^"
    else:
      turn = "White V"
    return blackMoves + '\n' + boardStr + '\n' + whiteMoves + '\n' + turn + " turn."



