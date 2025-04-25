import math
import numpy as np
import random as rm

YM="ym"
YH="yh"
EMPTY=None


class Yoshi_Zones():
    
    def __init__(self,width,height):
        self.board=None
        self.turn='ym'
        self.width=width
        self.height=height
        
            
    
    
    def initial_state(self):
        "Return the initial state of board"
        
        self.board = [
            ["ESPE","ESPE","ESPE", EMPTY, EMPTY,"ESPE","ESPE","ESPE"],
            ["ESPE", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,"ESPE"],
            ["ESPE", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,"ESPE"],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            ["ESPE", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,"ESPE"],
            ["ESPE", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,"ESPE"],
            ["ESPE","ESPE","ESPE", EMPTY, EMPTY,"ESPE","ESPE","ESPE"],
        ]
        
        empty_positions=[(i,j) 
                        for i in range(len(self.board))
                        for j in range(len(self.board[0]))
                        if self.board[i][j]==EMPTY]
        
        random_number_ym=1
        random_number_yh=1
        
        while random_number_yh==random_number_ym:
            random_number_ym=rm.randint(0,len(empty_positions)-1)  
            random_number_yh=rm.randint(0,len(empty_positions)-1)
        
        self.position_ym=empty_positions[random_number_ym]
        self.position_yh=empty_positions[random_number_yh]
        
        x_ym=self.position_ym[0]
        y_ym=self.position_ym[1]
        
        x_yh=self.position_yh[0]
        y_yh=self.position_yh[1]
        
        self.board[x_ym][y_ym]='ym'
        self.board[x_yh][y_yh]='yh'     
        
        


        
    def change_player(self):
        "set turn whit the next Player who has the next turn"
        if self.turn=='ym':
            self.turn=='yh'
        else:
            self.turn='ym'
        
    def validate_position(self,i,j):
        if i>=0 and i<=self.height and j>=0 and j<=self.width:
            
            return (i,j)
        return None

    def actions(board,self):
        """
        Returns set of all possible actions (i, j) available on the board.
        """
        player=self.turn
        self.set_actions=set()
        
        if player=='ym':
            pos=self.position_ym
        else:
            pos=self.position_yh
        x=pos[0]
        y=pos[1]
        valid_positions=[]
        
        valid_positions.append(self.validate_position(x-1,y+2))
        valid_positions.append(self.validate_position(x+1,y+2))
        valid_positions.append(self.validate_position(x+2,y+1))
        valid_positions.append(self.validate_position(x+2,y-1))
        valid_positions.append(self.validate_position(x+1,y-2))
        valid_positions.append(self.validate_position(x-1,y-2))
        valid_positions.append(self.validate_position(x-2,y-1))
        valid_positions.append(self.validate_position(x-2,y+1))
        
        for i in range(len(valid_positions)):
            if valid_positions[i]!=None:
                self.set_actions.add(valid_positions[i])
    
    def result(self,action):
        "Set the board that results from making move (i,j) on the board."
        
        if action not in self.set_actions:
            raise Exception('invalid action')
        
        i,j=action
        
        if self.board[i][j]=='ESPE':
            if self.turn=='ym':
                self.board[i][j]=='GREEN'
            else:
                self.board[i][j]=='RED'
                
        self.board[i][j]=self.turn
        
    def Terminal(self):
        "Returns the winner of the game, if there is one."
        
        self.special_positions=[
        (0, 0),(0, 1),(0, 2),(0, 5),(0, 6),
        (0, 7),(1, 0),(1, 7),(2, 0),(2, 7),
        (5, 0),(5, 7),(6, 0),(6, 7),(7, 0),
        (7, 1),(7, 2),(7, 5),(7, 6),(7, 7)
        ]
        
        
        return all(self.board[p[0]][p[1]]!='ESPE' for p in self.special_positions)
    
    def winner(self):
        
        if self.Terminal():
            
            count_green=0
            count_red=0
            
            for p in self.special_positions:
                
                if self.board[p[0]][p[1]]=='GREEN':
                    count_green+=1
                elif self.board[p[0]][p[1]]=='RED':
                    count_red+=1
            if count_green<count_red:
                return 'yh'
            if count_green>count_red:
                return 'ym'
            return 'deat heat'
        return None
            
                
            
            
        
        
        
            
            


    