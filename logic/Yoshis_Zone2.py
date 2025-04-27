import math
import numpy as np
import random as rm
import copy
from collections import deque

YM="ym"
YH="yh"
EMPTY=None




special_positions=[
    [(0,0),(0,1),(0,2),(1,0),(2,0)],
    [(7,0),(5,0),(6,0),(7,1),(7,2)],
    [(7,7),(7,5),(7,6),(5,7),(6,7)],
    [(0,7),(1,7),(2,7),(0,6),(0,5)]
    
    
]

def initial_state():
        "Return the initial state of board"
        
        
        board = [
            [EMPTY,EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY],
        ]
        
        
        
        
        empty_positions=[(i,j) 
                        for i in range(len(board))
                        for j in range(len(board[0]))
                        if (i,j) not in [cell for zone in special_positions for cell in zone]]
        
        random_number_ym=1
        random_number_yh=1
        
        while random_number_yh==random_number_ym:
            random_number_ym=rm.randint(0,len(empty_positions)-1)  
            random_number_yh=rm.randint(0,len(empty_positions)-1)
        
        position_ym=empty_positions[random_number_ym]
        position_yh=empty_positions[random_number_yh]
        
        x_ym=position_ym[0]
        y_ym=position_ym[1]
        
        x_yh=position_yh[0]
        y_yh=position_yh[1]
        
        board[x_ym][y_ym]='ym'
        board[x_yh][y_yh]='yh' 
        
        return board
    
def change_player(player):
    if player=='ym':
        return 'yh'
    return 'ym'

def validate_position(i,j,board):
        if i>=0 and i<len(board) and j>=0 and j<len(board[0]):
            if board[i][j]==EMPTY:
                return (i,j)
            
        return None
    
def search_pos(string,board):
        for i in range(len(board)):
            for j in  range(len(board[0])):
                if board[i][j]==string:
                    return (i,j)
        return None
def actions(board,player):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    player_actions=set()

    if player=='ym':
        pos=search_pos('ym',board)
    else:
        pos=search_pos('yh',board)

    x,y=pos
    


    valid_positions = [
    validate_position(x-1, y+2,board),validate_position(x+1, y+2,board),
    validate_position(x+2, y+1,board),validate_position(x+2, y-1,board),
    validate_position(x+1, y-2,board),validate_position(x-1, y-2,board),
    validate_position(x-2, y-1,board),validate_position(x-2, y+1,board)
    ]

    for pos in valid_positions:
        if pos is not None:
            player_actions.add(pos)
    return player_actions



def terminal(board):
    "Returns the winner of the game, if there is one."
    three_color_zones_green=0
    three_color_zones_red=0
    for zone in special_positions:
        green=0
        red=0
        for cell in zone:
            i,j=cell
            if board[i][j]=='G':
                green+=1
            elif board[i][j]=='R':
                red+=1
        if green>2:
            three_color_zones_green+=1
        elif red>2:
            three_color_zones_red+=1
            
    if three_color_zones_red>2 or three_color_zones_green>2 or three_color_zones_green==three_color_zones_red==2:
        return True
    return False
            

def winner(board):    
        
        zones_green=0
        zones_red=0
        
        for zone in special_positions:
            count_green=0
            count_red=0
            for cell in zone:
                i,j=cell
                if board[i][j]=='G' or board[i][j]=='ym':
                    count_green+=1
                elif board[i][j]=='R' or board[i][j]=='yh':
                    count_red+=1
            if count_green>2:
                zones_green+=1
            elif count_red>2:
                zones_red+=1
        
        if zones_green>zones_red:
            return 'ym'
        elif zones_green<zones_red:
            return 'yh'
        
        return None
                
                


def result(action,board,player):
        "Set the board that results from making move (i,j) on the board."
        player_actions=actions(board,player)
        if action not in player_actions:
            return board
        
        board_copy=copy.deepcopy(board)
        
        
        
        i,j=action
        
        if player=='ym':
            x,y=search_pos('ym',board_copy)
            
            if (x,y) in [cell for zone in special_positions for cell in zone]:
                board_copy[x][y]='G'
            else:
                board_copy[x][y]=EMPTY
        
        else:
            x,y=search_pos('yh',board_copy)
        
            
            if (x,y) in [cell for zone in special_positions for cell in zone]:
                board_copy[x][y]='R'
            else:
                board_copy[x][y]=EMPTY
            
        board_copy[i][j]=player
        
        return board_copy

def knight_distance(start, goal):
    """Returns the number of knight moves from start to goal."""
    moves = [(-2, -1), (-2, 1), (-1, 2), (1, 2),
             (2, 1), (2, -1), (1, -2), (-1, -2)]
    visited = set()
    queue = deque([(start, 0)])  # (position, steps)

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == goal:
            return steps
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))
    return math.inf

def valid_zones(board):
    zones=[]   
    for zone in special_positions:
        count_green=0
        count_red=0
        for cell in zone:
            i,j=cell
            if board[i][j]=='G' or board[i][j]=='ym':
                count_green+=1
            elif board[i][j]=='R' or board[i][j]=='yh':
                count_red+=1
        if count_green<=2 and count_red<=2:
            zones.append(zone)
            
    return zones
        
            
                
def knight_distance_to_nearest_empty_special(board, player):
    i, j = search_pos(player, board)
    min_dist = math.inf
    valid_z=valid_zones(board)
    for zone in valid_z:
        for x, y in zone:
                if board[x][y] == EMPTY:
                    dist = knight_distance((i, j), (x, y))
                    min_dist = min(min_dist, dist)
    return min_dist

    
def utility(board):
    """
    Smarter heuristic: evaluates zone victories, partial control, and distance.
    """
    winner_val = winner(board)
    if winner_val == 'ym':
        return 100
    if winner_val == 'yh':
        return -100

    score = 0

    for zone in special_positions:
        green = 0
        red = 0
        for i, j in zone:
            if board[i][j] == 'G' or board[i][j] == 'ym':
                green += 1
            elif board[i][j] == 'R' or board[i][j] == 'yh':
                red += 1

        if green > 2:
            score += 5  # secured zone: BIG bonus
        elif red > 2:
            score -= 5  # opponent secured zone: BIG penalty
        else:
            score += (green - red)  # still fighting for zone: small bonuses
            
    if not terminal(board):
        # Distance evaluation (only if not terminal)
        distance_ym = knight_distance_to_nearest_empty_special(board, 'ym')
        distance_yh = knight_distance_to_nearest_empty_special(board, 'yh')

        if distance_ym != math.inf:
            score -= distance_ym * 0.5  # weight distance lightly
        if distance_yh != math.inf:
            score += distance_yh * 0.5

    return score


def min_value(board,alpha,beta,depth):
    v= math.inf
       
    
    if terminal(board) or depth==0:
        return utility(board)
    
    for action in actions(board,'yh'):
        v=min(v,max_value(result(action,board,'yh'),alpha,beta,depth-1))
        if v <=alpha:
            return v
        beta=min(beta,v)
    
    return v

def max_value(board,alpha,beta,depth):
    v= -math.inf
    
    
    if terminal(board) or depth==0:
        return utility(board)
    
    
    for action in actions(board,'ym'):
        v=max(v,min_value(result(action,board,'ym'),alpha,beta,depth-1))
        if v>=beta:
            return v
        alpha=max(alpha,v)
        
    return v


def minimax(board,depth=3):
    """
    Returns the optimal action for the current player on the board.
    """
    
    actions_board=list(actions(board,'ym'))
    
    if  not terminal(board):
        
        list_min=[]
        
        for action in actions_board:
            new_board=result(action,board,'ym')
            min_v=min_value(new_board,-math.inf,math.inf,depth-1)
            list_min.append(min_v)
        
        max_v=max(list_min)
        
        max_index=list_min.index(max_v)
        
        return actions_board[max_index]
        
    
    
    return None