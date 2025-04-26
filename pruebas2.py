import logic.Yoshis_Zone2 as  yz
import numpy as np
board=yz.initial_state()
print()

print(np.asarray(board))

# print(yz.search_pos('ym',board))

# actions=list(yz.actions(board,'ym'))

# board=yz.result(actions[0],board,'ym')

# print(np.array(board))

move=yz.minimax(board,'ym')

print(move)