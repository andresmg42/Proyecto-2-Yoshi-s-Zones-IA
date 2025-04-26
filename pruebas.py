import logic.yoshis_zones as yz
import numpy as np
game=yz.Yoshi_Zones(8,8)

board=game.initial_state()

#print initial state
print(np.asarray(board))
print()
#print player turn
print(game.turn)
#get actions
act=game.actions(board)
#set board whit actual action
board=game.result(list(act)[0],board)
#print new board
print(np.asanyarray(board))
print()
#change player
game.change_player()
#print game turn
print(game.turn)
#get actions
act=game.actions(board)
#set board whit actual actions
board=game.result(list(act)[0],board)
#print new board
print(np.asanyarray(board))