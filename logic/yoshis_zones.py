import math
import numpy as np
import random as rm
import copy

YM="ym"
YH="yh"
EMPTY=None


class Yoshi_Zones():
    
    def __init__(self,width,height):
    
        self.turn='ym'
        self.width=width
        self.height=height
        
        
        
            
    
    
    def initial_state(self):
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
        
        self.special_positions=[
        (0,0),(0,1),(0,2),(0,5),(0,6),
        (0,7),(1,0),(1,7),(2,0),(2,7),
        (5,0),(5,7),(6,0),(6,7),(7,0),
        (7,1),(7,2),(7,5),(7,6),(7,7)
        ]
        
        
        # self.original=copy.deepcopy(self.board)
        
        empty_positions=[(i,j) 
                        for i in range(len(board))
                        for j in range(len(board[0]))
                        if (i,j) not in self.special_positions]
        
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
        
        


        
    def change_player(self):
        "set turn whit the next Player who has the next turn"
        if self.turn=='ym':
            self.turn='yh'
        else:
            self.turn='ym'
        
    def validate_position(self,i,j,board):
        if i>=0 and i<self.height and j>=0 and j<self.width:
            if board[i][j]==EMPTY:
                return (i,j)
            
        return None
    
    def search_pos(self,string,board):
        for i in range(len(board)):
            for j in  range(len(board[0])):
                if board[i][j]==string:
                    return (i,j)
        return None

    def actions(self,board):
        """
        Returns set of all possible actions (i, j) available on the board.
        """
        player=self.turn
        player_actions=set()
        
        if player=='ym':
            pos=self.search_pos('ym',board)
        else:
            pos=self.search_pos('yh',board)
        
        x,y=pos
        valid_positions=[]
        
        
        valid_positions = [
        self.validate_position(x-1, y+2,board), self.validate_position(x+1, y+2,board),
        self.validate_position(x+2, y+1,board), self.validate_position(x+2, y-1,board),
        self.validate_position(x+1, y-2,board), self.validate_position(x-1, y-2,board),
        self.validate_position(x-2, y-1,board), self.validate_position(x-2, y+1,board)
        ]
        
        for i in range(len(valid_positions)):
            if valid_positions[i]!=None:
                player_actions.add(valid_positions[i])
        return player_actions
    
    def result(self,action,board):
        "Set the board that results from making move (i,j) on the board."
        player_actions=self.actions(board)
        if action not in player_actions:
            raise Exception('invalid action')
        
        board_copy=copy.deepcopy(board)
        
        
        
        i,j=action
        
        if self.turn=='ym':
            x,y=self.search_pos('ym',board)
            
            if (x,y) in self.special_positions:
                board_copy[x][y]='GREEN'
            else:
                board_copy[x][y]=EMPTY
        
        else:
            x,y=self.search_pos('yh',board)
        
            
            if (x,y) in self.special_positions:
                board_copy[x][y]='RED'
            else:
                board_copy[x][y]=EMPTY
            
        board_copy[i][j]=self.turn
        
        return board_copy
        
                               
               
        
        
    def terminal(self,board):
        "Returns the winner of the game, if there is one."
        return all(board[p[0]][p[1]]!=EMPTY for p in self.special_positions)
    
    def winner(self,board):    
        count_green=0
        count_red=0
        
        for p in self.special_positions:
            
            if board[p[0]][p[1]]=='GREEN' or board[p[0]][p[1]]=='ym':
                count_green+=1
            elif board[p[0]][p[1]]=='RED' or board[p[0]][p[1]]=='yh':
                count_red+=1
        if count_green<count_red:
            return 'yh'
        if count_green>count_red:
            return 'ym'
        return 'deat heat'
        
    
    def utility(self,board):
        "Return 1 if x won the game, -1 if 0 has won, 0 otherwise."
        
        winner_utility=self.winner(board)
        
        if winner_utility=='ym': return 1
        elif winner_utility=='yh':return -1
        return 0
    
    def min_value(self,board,alpha,beta,depth):
        v= math.inf
            
        
        if self.terminal(board):
            return self.utility(board)
        
        if depth==0:
            return self.utility(board)
        
        player_actions=self.actions(board)
        
        for action in player_actions:
            new_board = self.result(action, board)
            v=min(v,self.max_value(new_board,alpha,beta,depth-1))
            if v <=alpha:
                return v
            beta=min(beta,v)
        
        return v
    
    def max_value(self,board,alpha,beta,depth):
        v= -math.inf
        
        
        if self.terminal(board):
            return self.utility(board)
        
        if depth==0:
            return self.utility(board)
        
        player_actions=self.actions(board)
        
        for action in player_actions:
            new_board=self.result(action,board)
            v=max(v,self.min_value(new_board,alpha,beta,depth-1))
            if v>=beta:
                return v
            alpha=max(alpha,v)
            
        return v
            
                
    def minimax(self,board,depth=6):
        """
        Returns the optimal action for the current player on the board.
        """
        player_actions=self.actions(board)
        actions_board=list(player_actions)
        
        player_board=self.turn
        
        terminal=self.terminal(board)
        
        if player_board=='ym' and not terminal:
            
            list_min=[]
            
            for action in actions_board:
                
                new_board=self.result(action,board)
                min_v=self.min_value(new_board,-math.inf,math.inf,depth-1)
                list_min.append(min_v)
            
            max_v=max(list_min)
            
            max_index=list_min.index(max_v)
            
            return actions_board[max_index]
            
        if player_board=='yh' and not terminal:
            
            list_max=[]
            
            for action in actions_board:
                new_board=self.result(action,board)
                max_v=self.max_value(new_board,-math.inf,math.inf,depth-1)
                list_max.append(max_v)
                
            min_v=min(list_max)
            
            min_index=list_max.index(min_v)
            
            return actions_board[min_index]
        
        return None          
            
        
        
        
            
            


    