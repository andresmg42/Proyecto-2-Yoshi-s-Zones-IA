import math
import numpy as np
import random as rm
import copy

YM="ym"
YH="yh"
EMPTY=None
special_positions=[
        (0,0),(0,1),(0,2),(0,5),(0,6),
        (0,7),(1,0),(1,7),(2,0),(2,7),
        (5,0),(5,7),(6,0),(6,7),(7,0),
        (7,1),(7,2),(7,5),(7,6),(7,7)
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
                        if (i,j) not in special_positions]
        
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
    # terminal_winner=winner(board)
    # if terminal_winner is not None:
    #     return True
    
    return all(board[p[0]][p[1]]!=EMPTY for p in special_positions)

def winner(board):    
        count_green=0
        count_red=0
        
        for p in special_positions:
            
            if board[p[0]][p[1]]=='GREEN' or board[p[0]][p[1]]=='ym':
                count_green+=1
            elif board[p[0]][p[1]]=='RED' or board[p[0]][p[1]]=='yh':
                count_red+=1
        if count_green<count_red:
            return 'yh'
        if count_green>count_red:
            return 'ym'
        return None

def result(action,board,player):
        "Set the board that results from making move (i,j) on the board."
        player_actions=actions(board,player)
        if action not in player_actions:
            raise Exception('invalid action')
        
        board_copy=copy.deepcopy(board)
        
        
        
        i,j=action
        
        if player=='ym':
            x,y=search_pos('ym',board_copy)
            
            if (x,y) in special_positions:
                board_copy[x][y]='GREEN'
            else:
                board_copy[x][y]=EMPTY
        
        else:
            x,y=search_pos('yh',board)
        
            
            if (x,y) in special_positions:
                board_copy[x][y]='RED'
            else:
                board_copy[x][y]=EMPTY
            
        board_copy[i][j]=player
        
        return board_copy
    
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_utility= winner(board)
    
    if winner_utility =='ym': return 1
    
    if winner_utility=='yh':return -1
    
    return 0

def min_value(board,alpha,beta,depth,player):
    v= math.inf
        
    
    if terminal(board) or depth==0:
        return utility(board)
    
    for action in actions(board,player):
        v=min(v,max_value(result(action,board,player),alpha,beta,depth-1,player))
        if v <=alpha:
            return v
        beta=min(beta,v)
    
    return v

def max_value(board,alpha,beta,depth,player):
    v= -math.inf
    
    if terminal(board) or depth==0:
        return utility(board)
    
    for action in actions(board,player):
        v=max(v,min_value(result(action,board,player),alpha,beta,depth-1,player))
        if v>=beta:
            return v
        alpha=max(alpha,v)
        
    return v


def minimax(board,player_board,depth=3):
    """
    Returns the optimal action for the current player on the board.
    """
    
    actions_board=list(actions(board,player_board))
    
    
    
    if player_board=='ym' and not terminal(board):
        
        list_min=[]
        
        for action in actions_board:
            new_board=result(action,board,player_board)
            min_v=min_value(new_board,-math.inf,math.inf,depth-1,player_board)
            list_min.append(min_v)
        
        max_v=max(list_min)
        
        max_index=list_min.index(max_v)
        
        return actions_board[max_index]
        
    if player_board=='yh' and not terminal(board):
        
        list_max=[]
        
        for action in actions_board:
            new_board=result(action,board,player_board)
            max_v=max_value(new_board,-math.inf,math.inf,depth-1,player_board)
            list_max.append(max_v)
            
        min_v=min(list_max)
        
        min_index=list_max.index(min_v)
        
        return actions_board[min_index]
    
    return None