import copy
from heatmaps import *

# returns all legal moves
def getLegal(board, hand, inverted):
  # if inverted, turn is black
  # else turn is white
  if inverted:
    newHand = [(e[0], tuple((-offset[0], -offset[1]) for offset in e[1]), e[2]) for e in hand]
  else:
    newHand = hand
  
  if inverted:
    searchPieces = (3,4)
  else:
    searchPieces = (1,2)
  legalMoves = []
  for y, layer in enumerate(board):
    for x, piece in enumerate(layer):
      if piece in searchPieces:
        for move in newHand:
          for offset in move[1]:
            if (0 <= y + offset[0] <= 4) and (0 <= x + offset[1] <= 4):
              newSquare = board[y + offset[0]][x + offset[1]]
              if not (newSquare in searchPieces):
                legalMoves.append((move[0], (y, x), (y + offset[0], x + offset[1])))


  if len(legalMoves) == 0:
    legalMoves = [(card[0], (0,0), (0,0)) for card in newHand]
  return legalMoves



# returns a new board give two coordinates
def makeMove(board, coorda, coordb):
  piece = board[coorda[0]][coorda[1]]
  board[coorda[0]][coorda[1]] = 0
  board[coordb[0]][coordb[1]] = piece
  return board

# eval goes from -100 to +100, -100 means black win, +100 means white win
def evaluate(board):
  pieceCount = {
    0:0,
    1:0,
    2:0,
    3:0,
    4:0,
  }

  value = 0
  
  if board[0][2] == 2:
    return 1000
  if board[4][2] == 4:
    return -1000

  for y, layer in enumerate(board):
    for x, piece in enumerate(layer):
      #piece count
      pieceCount[piece] += 1

      #further pawns are slightly favoured, largest increase for first rank
      if piece == 0:
        pass
      elif piece == 1:
        value += whitePawnHeat[y][x]
      elif piece == 3:
        value += blackPawnHeat[y][x]
      elif piece == 2:
        value += whiteMasterHeat[y][x]
      elif piece == 4:
        value += blackMasterHeat[y][x]
  if pieceCount[2] == 0:
    return -1000
  if pieceCount[4] == 0:
    return 1000
  

  # ignore masters since there must be one of each in this case
  value += (pieceCount[1] - pieceCount[3]) * 20

  return value


def checkWin(board):
  found2 = False
  found4 = False
  for layer in board:
    for piece in layer:
      if piece == 2:
        found2 = True
      if piece == 4:
        found4 = True
  
  if (board[0][2] == 2) or (board[4][2] == 4):
    return True
  if found2 == 0 or found4 == 0:
    return True
  else:
    return False
  

# game is [board, inverted, whiteHand, blackHand, sideHand]
# if inverted, turn = black
def getChildren(game):
  if game[1]: #black turn
    legalMoves = getLegal(game[0], game[3], game[1])
  else:
    legalMoves = getLegal(game[0], game[2], game[1])
  
  children = []
  for move in legalMoves:
    newBoard = makeMove(game[0], move[1], move[2])
    
    if game[1]:
      for card in game[3]:
        if card[0] == move[0]:
          newHand = game[3].remove(card)
          newSide = card
          break
      
      children.append([newBoard, not game[1], game[2], newHand, newSide])
    else:
      for card in game[2]:
        if card[0] == move[0]:
          newHand = game[2].remove(card)
          newSide = card
          break
          
      children.append([newBoard, not game[1], newHand, game[3], newSide])
  
  return children

def makeGameMove(game, move):
  newgame = copy.deepcopy(game)
  newBoard = makeMove(newgame[0], move[1], move[2])
  if newgame[1]:
    for i, card in enumerate(newgame[3]):
      if card[0] == move[0]:
        newHand = [newgame[3][(i + 1) % 2], newgame[4]]
        newSide = card
        break
    
    
    return [newBoard, not newgame[1], newgame[2], newHand, newSide]
  else:
    for i, card in enumerate(newgame[2]):
      if card[0] == move[0]:
        newHand = [newgame[2][(i + 1) % 2], newgame[4]]
        newSide = card
        break
    
    return [newBoard, not newgame[1], newHand, newgame[3], newSide]

def minimax(game, depth, alpha, beta, maximizing):
  if depth == 0 or checkWin(game[0]):
    return None, evaluate(game[0])
    
  if maximizing:
    legalMoves = getLegal(game[0], game[2], False)
    maxEval = -1001
    for move in legalMoves:
      currentEval = minimax(makeGameMove(game, move), depth - 1, alpha, beta, False)[1]

      if currentEval > maxEval:
        maxEval = currentEval
        best_move = move
      
      alpha = max(alpha, currentEval)
      if beta <= alpha:
        break
    return best_move, maxEval
  else:
    legalMoves = getLegal(game[0], game[3], True)
    minEval = 1001
    for move in legalMoves:
      currentEval = minimax(makeGameMove(game, move), depth - 1, alpha, beta, True)[1]
      if currentEval < minEval:
        minEval = currentEval
        best_move = move
      
      beta = min(beta, currentEval)
      if beta <= alpha:
        break
    
    return best_move, minEval

