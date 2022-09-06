#   -2-1 0 1 2
# -2 X X X X X
# -1 X X X X X
#  0 X X O X X
#  1 X X X X X
#  2 X X X X X


#Move:
# ('Name', ((offset1Y, offset1X), (offset2Y, offset2X), ...), turn)
# Notes for transcriping : Let red be white, and blue be black

cards = [
  #sym 0 1 2 3 4 5 6 7
  ('Tiger', ((-2, 0), (1, 0)), 1),
  ('Crab', ((-1, 0), (0, -2), (0, 2)), 1),
  ('Monkey', ((1, 1), (-1, 1), (1, -1), (-1, -1)), 1),
  ('Crane', ((-1, 0), (1, 1), (1, -1)), 1),
  ('Dragon', ((1, 1), (1, -1), (-1, -2), (-1, 2)), 0),
  ('Eleph', ((-1, 1), (-1, -1), (0, 1), (0, -1)), 0),
  ('Mantis', ((-1, 1), (-1, -1), (1, 0)), 0),
  ('Boar', ((-1, 0), (0, -1), (0, 1)), 0),
  #lefthand 8 9 10 11
  ('Frog', ((-1, -1), (0, -2), (1, 1)), 0),
  ('Goose', ((0, -1), (0, 1), (-1, -1), (1, 1)), 1),
  ('Horse', ((-1, 0), (1, 0), (0, -1)), 0),
  ('Eel', ((-1, -1), (1, -1), (0, 1)), 1),
  #righthand 12 13 14 15
  ('Rabbit', ((1, -1), (-1, 1), (0, 2)), 1),
  ('Roost', ((0, -1), (0, 1), (1, -1), (-1, 1)), 0),
  ('Ox', ((-1, 0), (1, 0), (0, 1)), 1),
  ('Cobra', ((0, -1), (-1, 1), (1, 1)), 0),
  
]