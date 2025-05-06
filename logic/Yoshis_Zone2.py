import math
import numpy as np
import random as rm
import copy
from collections import deque

YM="ym"
YH="yh"
EMPTY=None


WIN_ZONES=[0,0]

special_positions=[
    [(0,0),(0,1),(0,2),(1,0),(2,0)],
    [(7,0),(5,0),(6,0),(7,1),(7,2)],
    [(7,7),(7,5),(7,6),(5,7),(6,7)],
    [(0,7),(1,7),(2,7),(0,6),(0,5)]
    
    
]

def initial_state():
        
        
        
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
    zones_green=0
    zones_red=0
        
    for zone in special_positions:
        count_green=0
        count_red=0
        for cell in zone:
            i,j=cell
            if board[i][j]=='G':
                count_green+=1
            elif board[i][j]=='R':
                count_red+=1
        if count_green>2:
            zones_green+=1
        elif count_red>2:
            zones_red+=1
       
    return zones_green>2 or zones_red>2 or zones_red==zones_green==2
    

def winner(board):    
        global WIN_ZONES
        zones_green=0
        zones_red=0
        
        for zone in special_positions:
            count_green=0
            count_red=0
            for cell in zone:
                i,j=cell
                if board[i][j]=='G':
                    count_green+=1
                elif board[i][j]=='R':
                    count_red+=1
            if count_green>2:
                zones_green+=1
            elif count_red>2:
                zones_red+=1
        
        WIN_ZONES[0]=zones_green
        WIN_ZONES[1]=zones_red
        
        if zones_green>zones_red:
            return 'ym'
        elif zones_green<zones_red:
            return 'yh'
        
        return None
                
                


def result(action,board,player):
    
        player_actions=actions(board,player)
        if action not in player_actions:
            return None
        
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



    
def utility(board):
    
    
    score = 0

    for zone in special_positions:
        green = 0
        red = 0
        for i, j in zone:
            if board[i][j] == 'G':
                green += 1
            elif board[i][j] == 'R':
                red += 1
        
        if green > 2:
            score += 2  
        elif red > 2:
            score -= 2  
        else:
             score += (green - red)*0.5  
             
        
    
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