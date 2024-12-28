import pygame
import random
import math

#obsolete but returns the absolute value
def abs(x):
  if x<0:
    return -x
  else:
    return x
    
# allows us to resize images to fit in our game
def scale(image, factor):
  size = round(image.get_width() * factor), round(image.get_height() * factor)
  return pygame.transform.scale(image, size)
    
#converts coordinates from our hexagonal system into a Cartesian system
def convert_coords(x,y,h_size):
  size = 900
  increment = size/(2*h_size -1)
  # center of hexagon is at (5,5) if the hexagon is size 5
  # distance from center:
  x_distance = x-h_size
  y_distance = y-h_size
  return_x = 450
  return_y = 450
  if y > h_size:
    return_y += increment*y_distance
  else:
    return_y += increment*y_distance/2
    return_x -= increment*y_distance*0.9
  return_x += increment*x_distance*0.9
  return_y += increment*x_distance/2
  return (return_x,return_y)
  
def back_convert(x,y,hset):
  # above: 
  # x' = 500 - i(dy).9 + i(dx).9
  # y' = 500 + i(dy) ...
  # Problem: solving backwards requires a knowledge of being above or below the hexagonal parallel y=h_size
  # Solution: don't
  converted_list = []
  for element in hset.get_tuples():
    converted_list.append(convert_coords(element[0],element[1],hset.board.size))
  #print(converted_list)
  #print(get_pos_number(1,5,hset.board.shape,hset.board.size))
  distance_to_h = []
  for element in converted_list:
    distance_to_h.append(math.sqrt((x+75-element[0])*(x+75-element[0]) + (y+75-element[1])*(y+75-element[1])))
  #print(distance_to_h)
  minimum = 1000
  min_loc = (0,0)
  for element in distance_to_h:
    if element < minimum:
      minimum = element
      min_loc = hset.get_tuples()[distance_to_h.index(element)]
  return min_loc
  

HEXAGON = scale(pygame.image.load("imgs/hexagon.png"), 0.3)
#150,150
RUBY = scale(pygame.image.load("imgs/ruby.png"), 0.4*0.2)
GEM = scale(pygame.image.load("imgs/gem.png"), 0.2*.95)
WIN = pygame.display.set_mode((1100, 1100))


# Gameboard class: the whole board
class Gameboard():
  def __init__(self,shape,size,blocked):
    self.shape = shape
    self.size = size
    if shape == "hexagon":
      self.number_of_spaces = (3*size*(size-1) +1)


# Functions pertaining to hexagons, a class defined below. They will be used in methods later

#By rotating the hexagon 30 degrees counterclockwise, we can view it as a grid.
#The middle row is the longest. 
#This function returns the length of the row. 
def row_length(size,y,shape):
  if shape == "hexagon":
    return (2*size - abs(y - size)-1)
#x and y start from 1

#The position of the space in the gameboard can be returned as a single integer which will correspond to its place in the list HexagonSet below.
# recursive and uses row_length
def get_pos_number(x,y,shape,size):
  if shape == "hexagon":
    if x > 1:
      return (x-1+get_pos_number(1,y,shape,size))
    elif y > 1:
      return (row_length(size,y-1,shape) + get_pos_number(1,y-1,shape,size))
    else:
    #if x == y == 1:
      return 0
#position starts from 0

# Gives a tuple of the range of the numbers of the positions that are in a row of the board
# Recursive and uses row_length()
def get_row(y,shape,size):
  if shape == "hexagon":
    if y > 1:
      return (get_row(y-1,shape,size)[1]+1,get_row(y-1,shape,size)[1]+row_length(size,y,shape))
    else:
      return (1,5)
      
# The inverse of get_pos_number: takes a number and returns (x,y) as a tuple
def get_xy(n,shape,size):
  if shape == "hexagon":
    for i in range(2*size):
      if n >= get_row(i+1,shape,size)[0] and n<= get_row(i+1,shape,size)[1]:
        return (n-get_row(i+1,shape,size)[0]+1,i+1)
        break

#Takes list1 and removes the elements that aren't in list2        
def purify_list(list1,list2):
    new_list1 = []
    for element in list1:
      if element in list2 and not (element in new_list1):
        new_list1.append(element)
    return new_list1
    
# Hexagon class: a space on which one can move
class Hexagon():
  def __init__(self,x,y,board):
    self.x = x
    self.y = y
    self.board = board
    
  def max_x(self):
    return row_length(self.board.size,self.y,self.board.shape)
  
  def get_position_number(self):
    return get_pos_number(self.x,self.y,self.board.shape,self.board.size)
    
  def get_coord_tuple(self):
    return (self.x,self.y)
    # return get_xy(self.get_pos_number())
  
  def __str__(self):
    return ("h#" + str(self.get_position_number()) + "at: (" + str(self.x) + "," + str(self.y)+")")
    
  def h_appear(self):
    WIN.blit(HEXAGON,convert_coords(self.x,self.y,self.board.size))
    # display.update?

# HexagonSet class: holds all the hexagons

class HexagonSet():
  def __init__(self,number,board):
    self.board = board
    self.space_list = []
    for i in range(number):
      self.space_list.append(Hexagon(get_xy(i+1,board.shape,board.size)[0],get_xy(i+1,board.shape,board.size)[1],board))
    
  def draw_all_h(self):
    # ANIMATION
    for element in self.space_list:
      element.h_appear()
  
  #returns a list of the hexagons
  def get_data(self):
    data_list = []
    for h in self.space_list:
      data_list.append(str(h))
      #print(h.get_position_number())
    return data_list
  
  #returns a list of the hexagons' coords
  def get_tuples(self):
    tuple_list = []
    for h in self.space_list:
      tuple_list.append((h.x,h.y))
    return tuple_list
    
  #returns adjacent hexagons
  def get_adjacent_h(self,x,y):
    list_adj1 = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    if y > self.board.size:
      list_adj1.append((x+1,y-1))
    else:
      list_adj1.append((x-1,y-1))
    if y >= self.board.size:
      list_adj1.append((x-1,y+1))
    else:
      list_adj1.append((x+1,y+1))
    return purify_list(list_adj1,self.get_tuples())
  
  #returns hexagons up to two spaces away
  def get_2adjacent_h(self,x,y):
    list_adj2 = []
    for element in self.get_adjacent_h(x,y):
      if not ((element[0],element[1]) == (x,y)):
        list_adj2.extend(self.get_adjacent_h(element[0],element[1]))
    return purify_list(list_adj2,self.get_tuples())

  #returns hexagons two but not one spaces away
  def get_3adjacent_h(self,x,y):
    list_adj3 = []
    for element in self.get_2adjacent_h(x,y):
      if not element in self.get_adjacent_h(x,y):
        list_adj3.append(element)
    return list_adj3
    

#corners: (1,1),(5,1),(9,5),(5,9),(1,9),(1,5)

# Piece class. Child classes: player and computer pieces
# Represents individual pieces either controlled by the player or computer
# Functions which represent changes to the piece
class Piece():
  def __init__(self,x,y,hset):
    self.x = x
    self.y = y
    self.hset = hset
    self.pos = get_pos_number(x,y,hset.board.shape,hset.board.size)
    
  # When the opponent takes one of your piece
  # Deletes your piece, appends it to the opponent
  def switch_teams(self,team,opp):
    team.del_piece(self)
    opp.piece_list.append(self)
    opp.piece_t_list.append((self.x,self.y))
    
    # ANIMATION - pygame testing stuff
    self.appear(opp)
    
  #converts all neighboring opponents to your team
  #Basically it uses switch_teams for all opponent pieces
  def convert_opponent(self,team,opp):
    for element in self.hset.get_adjacent_h(self.x,self.y):
      if not (opp.get_piece_t(element) == "NONE"):
        # IGNORE THIS IGNORE THIS
        ## APPEARANCE / ANIMATION
        #if team.player == "p1":
        #  for i in range(50):
        #    draw_all(team,opp)
        #    WIN.blit(scale(RUBY,0.10), convert_coords(self.x+(element[0]-self.x)*i/50, self.y + (element[1]-self.y)*i/50,self.hset.board.size))
        #elif team.player == "p2":
        #  for i in range(50):
        #    WIN.blit(scale(GEM,0.10), convert_coords(self.x+(element[0]-self.x)*i/50, self.y + (element[1]-self.y)*i/50,self.hset.board.size))
        #    draw_all(opp,team)
        # draw_all(team,opp)
        opp.get_piece_t(element).switch_teams(opp,team)
        
  # Duplicates a piece one space away from original piece
  # Appends piece to the team list
  def duplicate(self,team,opp,start,end):
    team.piece_list.append(Piece(end[0],end[1],self.hset))
    team.piece_t_list.append(end)
    (team.get_piece_t(end)).appear(self.player)
    team.piece_list[-1].convert_opponent(team,opp)
    
  # Move two spaces to an empty spot
  def move_two(self,team,opp,start,end):
    ## ANIMATION: change coordinates gradually (not super fast)
    starting = (self.x,self.y)
    for i in range(10):
      self.x = starting[0] + (end[0]-starting[0])*i/10
      self.y = starting[1] + (end[1]-starting[1])*i/10
      self.appear(team.player)
      draw_all(team,opp)
    draw_all(team,opp)
      
    #team.del_piece(self)
    #team.piece_list.append(Piece(end[0],end[1],self.hset))
    #team.piece_t_list.append(end)
    #instead:
    self.x = end[0]
    self.y = end[1]
    team.change_piece_coords(self,starting,end)
    self.appear(team.player)
    
    self.convert_opponent(team,opp)
    
  ## ANIMATION
  # initializing ruby/gem picture on the board along with coords
  # allows one to complete the animation of the pieces
  def appear(self,player):
    self.player = player
    coords = convert_coords(self.x,self.y,self.hset.board.size)
    coords = (coords[0]+25,coords[1]+25)
    if player == "p1":
      ## appear as ruby
      WIN.blit(RUBY,coords)
    elif player == "p2":
      ## appear as gem
      WIN.blit(GEM,coords)
    # display.update ?

class PlayerPieces():
  def __init__(self,board,hset,setup,player):
    self.board = board
    self.hset = hset
    self.piece_list = []
    self.player = player
    # For future use, right now this is hard coded
    if board.shape == "hexagon" and setup == "default":
      #p2: gems
      if player == "p2":
        self.piece_list = [Piece(1,1,hset), Piece(2*board.size - 1, board.size, hset), Piece(1,2*board.size - 1,hset)]
      #p1: rubies
      if player == "p1":
        self.piece_list = [Piece(1,board.size,hset), Piece(board.size, 1, hset), Piece(board.size, 2*board.size - 1,hset)]
    self.piece_t_list = []
    for element in self.piece_list:
      self.piece_t_list.append((element.x,element.y))
  
  # allows for all the pieces to be visible on the board
  # uses .appear from before
  def draw_all_p(self):
    ## APPEARANCE [ANIMATION]
    for element in self.piece_list:
      element.appear(self.player)
      
  # Removes specified piece from the piece list
  def del_piece(self,piece):
    self.piece_list.pop(self.piece_list.index(piece))
    self.piece_t_list.pop(self.piece_t_list.index((piece.x,piece.y)))
  
  # When a piece moves, the coords change as well
  def change_piece_coords(self,piece,start,end):
    self.piece_t_list[self.piece_t_list.index(start)] = end
        
  # Selecting a piece using x and y
  def get_piece(self,x,y):
    for piece in self.piece_list:
      if piece.x == x and piece.y == y:
        return piece
        break
    return "NONE"
        
  # Selecting a piece using coordinates
  def get_piece_t(self,t):
    for piece in self.piece_list:
      if piece.x == t[0] and piece.y == t[1]:
        return piece
        break
    return "NONE"
        
  # Selecting a piece using position (n)
  def get_piece_n(self,n):
    for piece in self.piece_list:
      if piece.pos == n:
        return piece
        break
    return "NONE"
        
  #This method was really a group effort
  #Represents an algorithm which picks the best spot for the computer
  def take_autoturn(self):
    # "AI" computer turn algorithm
    self.move_options = []
    #move options 1 is the list of spaces that are 1 away
    self.move_options1 = []
    #print(self.opp.piece_t_list)
    #print(self.piece_t_list)
    for a in self.piece_list:
      #print("a = " + str(a.x) + str(a.y))
      for b in self.hset.get_2adjacent_h(a.x,a.y):
        if not (b in self.piece_t_list or b in self.opp.piece_t_list):
          if not (b in self.move_options):
            self.move_options.append(b)
            #print(b)
          if b in self.hset.get_adjacent_h(a.x,a.y):
            self.move_options1.append(b)
          #print(b)
          #print(self.hset.get_adjacent_h(a.x,a.y))
    if (len(self.move_options) == 0):
      print("No options")
      return("END OF GAME")
    else:
      self.maximum_points = 0
      self.best_option = []
      resulting_points = 0
        #print(self.move_options)
      for element in (self.move_options):
        resulting_points = len(purify_list(self.hset.get_adjacent_h(element[0],element[1]),self.opp.piece_t_list))
        #print(resulting_points)
        if resulting_points > self.maximum_points:
          self.best_option = [element]
          self.maximum_points = resulting_points
        elif resulting_points == self.maximum_points:
          self.best_option.append(element)
      #print(self.best_option)
      #print(self.move_options1)
      #print(purify_list(self.best_option,self.move_options1))
      self.moving_one = (len(purify_list(self.best_option,self.move_options1)) > 0)
      if self.moving_one:
        self.best_option = purify_list(self.best_option,self.move_options1)
      self.move = self.best_option[random.randint(0,len(self.best_option)-1)]
      self.origin_options = []
      #print(self.hset.get_adjacent_h((self.move)[0],(self.move)[1]))
      #print(self.piece_t_list)
      #print(self.moving_one)
      if self.moving_one:
        self.origin_options = purify_list(self.hset.get_adjacent_h((self.move)[0],(self.move)[1]),self.piece_t_list)
      else:
        self.origin_options = purify_list(self.hset.get_2adjacent_h((self.move)[0],(self.move)[1]),self.piece_t_list)
      # Error occurred where there were no origin_options.
      # Longest (and only long) debugging. 
      # The cause was a discrepancy between piece_list and piece_t_list, due to forgetting to change piece_t_list when moving two spaces.
      # Fixed on Sunday.
      if len(self.origin_options) == 0:
        print("Error")
        print(self.origin_options)
        print(self.move_options)
        print(self.best_option)
        print(self.move)
        print(self.hset.get_2adjacent_h(self.move[0],self.move[1]))
        print(self.piece_t_list)
        return("END OF GAME")
      else:
        self.origin = self.origin_options[random.randint(0,len(self.origin_options)-1)]
  
  # Setting the opponent
  def set_opp(self,opp):
    self.opp = opp
    
  # Carries out the turn, either moving 1 space and duplicating or moving 2 spaces
  def finish_turn(self):
    #print(self.get_piece_t(self.origin).x + self.get_piece_t(self.origin).y)
    if self.moving_one:
      (self.get_piece_t(self.origin)).duplicate(self,self.opp,self.origin,self.move)
    else:
      (self.get_piece_t(self.origin)).move_two(self,self.opp,self.origin,self.move)
    ## Note for debugging: If self.origin is nonsensical e.g. (0,0), this ceases to work.
    
  # For when the opponent can't go anywhere and you take everything else on the board.
  # Effectively functions as the 'game over' screen
  def take_all(self):
    for coords in self.hset.get_tuples():
      if not (coords in self.piece_t_list or coords in self.opp.piece_t_list):
        self.piece_t_list.append(coords)
        self.piece_list.append(Piece(coords[0],coords[1],self.hset))
  
# Class which represents a computer player
# Child class of PlayerPieces
# Really only uses the take_autoturn method from the PlayerPieces
class ComputerPlayer(PlayerPieces):
  def __init__(self,board,hset,setup,player):
    super().__init__(board,hset,setup,player)
    
  # Either the computer takes the turn or the game ends
  def take_turn(self):
      if self.take_autoturn() == "END OF GAME":
        return "END OF GAME"
      else:
        self.finish_turn()
        #print(self.maximum_points)
        #print(self.move)
  
# Represents a human player 
# Child class of PlayerPieces
class HumanPlayer(PlayerPieces):
  def __init__(self,board,hset,setup,player):
    super().__init__(board,hset,setup,player)
    
  # Big function which allows player to take a turn
  # Prints options to user in the terminal
  # Currently attempting to make it so the user can "click" on the piece that they want to move
  # For now, it is just using the grid system to type into the terminal
  # Input the X and Y value for where you want to move  
  def take_turn(self):
    if self.take_autoturn() == "END OF GAME":
      return "END OF GAME"
    else:
      print(self.piece_t_list)
      #print(self.move_options)
      print(self.opp.piece_t_list)
      self.origin = (0,0)
      finished = False
      ## These two lines are optional
      self.move_options = []
      self.move_options1 = []
      while finished == False:
        clicked = (0,0)
        if mode == "CLICK":
          # (On click) clicked = (CLICKED PIECE / piece at location of click.x,".y)
          clicked = checking_mouse(self)
          
        else:
          clickx = input("Input x")
          clicky = input("Input y")
          if clickx.isdigit() and clicky.isdigit():
            clicked = (int(clickx),int(clicky))
          else:
            clicked = (0,0)
        
        ## Imagine this line as being before the "elif" below, but we put it up here to keep the continuity of the "if" and "elif".
        ## We don't need to specify self.origin =/= (0,0) here because if no piece has been selected, then the move_options lists become empty.
        self.moving_one = (clicked in self.move_options1)
        
        ## Is the person clicking on a piece?
        if clicked in self.piece_t_list:
          self.move_options = []
          self.move_options1 = []
          ## This considers whether someone clicked on the already selected hexagon.
          ## If this happens, the space is de-selected.
          if self.origin == clicked:
            self.origin = (0,0)
            ## self.origin is zero when no piece has been selected.
            # DELIGHT spaces
          ## If someone clicked on a hexagon not already selected, then it is selected.
          else:
            self.origin = clicked
            for element in self.hset.get_3adjacent_h(self.origin[0],self.origin[1]):
              if not (element in self.piece_t_list or element in self.opp.piece_t_list):
                self.move_options.append(element)
            for element in self.hset.get_adjacent_h(self.origin[0],self.origin[1]):
              if not (element in self.piece_t_list or element in self.opp.piece_t_list):
                self.move_options1.append(element)
            for element in self.move_options:
              ## Light it up / light up self.get_piece_t(element)
              pass
            for element in self.move_options1:
              ## Light it green - self.get_piece_t(element)
              pass
          
        ## If a piece has been selected and you clicked on a move option:
        ## (We don't need to specify that self.origin =/= (0,0) here because if the piece was deselected, then the move_options lists become empty.
        elif ((clicked in self.move_options) or self.moving_one) and not (self.origin == (0,0)):
          # DE-LIGHT all spaces
          self.move = clicked
          self.finish_turn()
          finished == True
          break
            
        ## If a random square was selected then you also deselect your square.
        else:
          self.origin = (0,0)
      
      
    
  
# Creating the game
class Game():
  def __init__(self,shape,size,blocked):
    self.board = Gameboard(shape,size,blocked)
    self.hset = HexagonSet((self.board).number_of_spaces,self.board)
    if int(input("Do you want player 1 to be 1) human 2) computer?")) == 2:
      self.player1 = ComputerPlayer(self.board,self.hset,"default","p1")
    else:
      self.player1 = HumanPlayer(self.board,self.hset,"default","p1")
    if int(input("Do you want player 2 to be 1) human 2) computer?")) == 2:
      self.player2 = ComputerPlayer(self.board,self.hset,"default","p2")
    else:
      self.player2 = HumanPlayer(self.board,self.hset,"default","p2")
    self.player1.set_opp(self.player2)
    self.player2.set_opp(self.player1)
    draw_all(self.player1,self.player2)
    
    # the turn is taken within the "elif" statements
    # This loop runs the game repeatedly (until the end)
    self.no_moves = 0
    while True:
      draw_all(self.player1,self.player2)
      self.no_moves = 0
      if len(self.player1.piece_list) == 0:
        self.no_moves += 1
      elif self.player1.take_turn() == "END OF GAME":
        self.no_moves += 1
      elif not(len(self.player2.piece_list) ==0):
        print("Player 1 turn")
        print(self.scoreboard())
      draw_all(self.player1,self.player2)
      if len(self.player2.piece_list) == 0:
        self.no_moves += 1
      elif self.player2.take_turn() == "END OF GAME":
        self.no_moves += 1
      elif not(len(self.player1.piece_list) ==0):
        print("Player 2 turn")
        print(self.scoreboard())
      draw_all(self.player1,self.player2)
      if self.no_moves > 1:
        print("GAME OVER")
        if len(self.player1.piece_list) == len(self.player2.piece_list):
          print("TIE")
        elif len(self.player1.piece_list) > len(self.player2.piece_list):
          print("PLAYER 1 WINS")
          self.player1.take_all()
        else:
          print("PLAYER 2 WINS")
          self.player2.take_all()
        print(self.scoreboard())
        break
      if self.no_moves == 0:
        r = input("Cont?")
      if r == "0":
        break
      #for event in pygame.event.get():
       # if event.type == pygame.QUIT:
        #  on = False
         # break
        
  #Returns the scoreboard of the game.
  def scoreboard(self):
    return ("P1 - " + str(len(self.player1.piece_list))+"vs P2 - " + str(len(self.player2.piece_list)))
    #Optional:
    #print(self.player1.piece_t_list)
    #print(self.player2.piece_t_list)
    
# draws both the players (gems) on the map
def draw_all(player1,player2):
  player1.hset.draw_all_h()
  player1.draw_all_p()
  player2.draw_all_p()
  pygame.display.update()
  
# Attempted pygame stuff. Mouse still doesn't really work.
# checks to see if mouse button is clicking on something
def check_mouse(event):
  if (event.type == pygame.MOUSEBUTTONDOWN):
    return event.type
  else:
    return None
    
#gets the position of the mouse click
def checking_mouse(player_pieces):
  for event in pygame.event.get():
    if not (check_mouse(event) == None):
      break
  click = pygame.mouse.get_pos()
  print(click)
  click = back_convert(click[0],click[1],player_pieces.hset)
  print(click)
  return click
  
answer = 0
#starts the game
while answer == 0:
  #mode = "CLICK"
  mode = "type"
  game1 = Game("hexagon",5,())
  answer = input("Press enter to close game")
#testing commands
#print(game1.hset.get_data())
#print((game1.hset.space_list)[23].get_coord_tuple())
#print(game1.hset.get_adjacent_h(1,5))
#print(game1.hset.get_2adjacent_h(6,4))

