import pygame
import sys
import time

import logic.Yoshis_Zone2 as yz

pygame.init()

size=width,height=800,800

yz_game=yz

#colors
black=(0,0,0)
white=(255,255,255)
tile_size = 80

#fonts
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

screen=pygame.display.set_mode(size)

board=yz_game.initial_state()

user=None

ai_turn=True

while True:
    
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
    screen.fill(white)
    
    if user is None:
        
        # Draw title
        title = largeFont.render("Play Yoshi's Zones", True, black)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)
        
        # Draw buttons
        playXButton = pygame.Rect(((width / 2)-(width / 4)/2), ((height / 2)-50/2), width / 4, 50)
        playX = mediumFont.render("Start", True, white)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen,black, playXButton)
        screen.blit(playX, playXRect)
        
        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user ='ym'
           
    else:
        
        
        
        
        #Draw game board
        
        tile_origin = (
        width / 2 - (8 * tile_size) / 2,
        height / 2 - (8 * tile_size) / 2
        )
        
        tiles=[]
        for i in range(8):
            row=[]
            for j in range(8):
                rect = pygame.Rect(
                        tile_origin[0] + j * tile_size,
                        tile_origin[1] + i * tile_size,
                        tile_size, tile_size
                    )
                pygame.draw.rect(screen,black,rect,3)
        
            
                if board[i][j]!=yz.EMPTY:
                    
                    move=moveFont.render(board[i][j],True,black)
                    
                    moveRect=move.get_rect()
                    moveRect.center=rect.center
                    screen.blit(move,moveRect)
                row.append(rect)
            tiles.append(row)
            
        game_over=yz_game.terminal(board)
        
        
        #show title
        if game_over:
            winner=yz_game.winner(board)
            if winner is None:
                title=f'Game Over: Tie'
            else:
                title=f'Game Over:{winner} Wins.'
        elif user=='yh':
            title=f'Play as yh'
        else:
            title=f'Computer thinking...'
        title=largeFont.render(title,True,black)
        titleRect=title.get_rect()
        titleRect.center=((width/2),30)
        screen.blit(title,titleRect)
        
        pygame.display.flip()
        
        #check for user move
        click,_,_=pygame.mouse.get_pressed()
        
        if click==1 and user=='yh' and not game_over:
            mouse=pygame.mouse.get_pos()
            for i in range(8):
                for j in range(8):
                    if(board[i][j]==yz.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board=yz_game.result((i,j),board,user)
                        user=yz_game.change_player(user)
        
           
        #check for AI move
        if user!='yh' and not game_over:
             
            if ai_turn:
                time.sleep(0.5)
                move=yz_game.minimax(board,depth=5)
                print(move)
                board=yz_game.result(move,board,'ym')
                ai_turn=False
                user=yz_game.change_player(user)
            else:
                ai_turn=True
        
    
    pygame.display.flip()
        
        
    

