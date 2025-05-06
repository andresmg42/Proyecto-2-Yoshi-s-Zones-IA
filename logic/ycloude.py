import math
import numpy as np
import random as rm
import copy
from collections import deque

YM = "ym"
YH = "yh"
EMPTY = None

WIN_ZONES = [0, 0]

special_positions = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
    [(7, 0), (5, 0), (6, 0), (7, 1), (7, 2)],
    [(7, 7), (7, 5), (7, 6), (5, 7), (6, 7)],
    [(0, 7), (1, 7), (2, 7), (0, 6), (0, 5)]
]

# Add a history tracker to prevent loops
move_history = {}

def initial_state():
    """Return the initial state of board"""
    
    board = [
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]
    
    empty_positions = [(i, j) 
                    for i in range(len(board))
                    for j in range(len(board[0]))
                    if (i, j) not in [cell for zone in special_positions for cell in zone]]
    
    random_number_ym = 1
    random_number_yh = 1
    
    while random_number_yh == random_number_ym:
        random_number_ym = rm.randint(0, len(empty_positions) - 1)  
        random_number_yh = rm.randint(0, len(empty_positions) - 1)
    
    position_ym = empty_positions[random_number_ym]
    position_yh = empty_positions[random_number_yh]
    
    x_ym = position_ym[0]
    y_ym = position_ym[1]
    
    x_yh = position_yh[0]
    y_yh = position_yh[1]
    
    board[x_ym][y_ym] = 'ym'
    board[x_yh][y_yh] = 'yh' 
    
    # Clear the move history when starting a new game
    global move_history
    move_history = {}
    
    return board

def board_to_string(board):
    """Convert the board to a string for hashing purposes"""
    result = ""
    for row in board:
        for cell in row:
            if cell is None:
                result += "_"
            else:
                result += cell
    return result

def change_player(player):
    if player == 'ym':
        return 'yh'
    return 'ym'

def validate_position(i, j, board):
    if i >= 0 and i < len(board) and j >= 0 and j < len(board[0]):
        if board[i][j] == EMPTY:
            return (i, j)
        
    return None

def search_pos(string, board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == string:
                return (i, j)
    return None

def actions(board, player):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    player_actions = set()

    if player == 'ym':
        pos = search_pos('ym', board)
    else:
        pos = search_pos('yh', board)

    if pos is None:
        return player_actions

    x, y = pos
    
    valid_positions = [
        validate_position(x-1, y+2, board), validate_position(x+1, y+2, board),
        validate_position(x+2, y+1, board), validate_position(x+2, y-1, board),
        validate_position(x+1, y-2, board), validate_position(x-1, y-2, board),
        validate_position(x-2, y-1, board), validate_position(x-2, y+1, board)
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
    zones_green = 0
    zones_red = 0
    
    for zone in special_positions:
        count_green = 0
        count_red = 0
        for cell in zone:
            i, j = cell
            if board[i][j] == 'G':
                count_green += 1
            elif board[i][j] == 'R':
                count_red += 1
        if count_green > 2:
            zones_green += 1
        elif count_red > 2:
            zones_red += 1
    
    WIN_ZONES[0] = zones_green
    WIN_ZONES[1] = zones_red
    
    if zones_green > zones_red:
        return 'ym'
    elif zones_green < zones_red:
        return 'yh'
    
    return None

def result(action, board, player):
    """Set the board that results from making move (i, j) on the board."""
    player_actions = actions(board, player)
    if action not in player_actions:
        return board
    
    board_copy = copy.deepcopy(board)
    
    i, j = action
    
    if player == 'ym':
        x, y = search_pos('ym', board_copy)
        
        if (x, y) in [cell for zone in special_positions for cell in zone]:
            board_copy[x][y] = 'G'
        else:
            board_copy[x][y] = EMPTY
    
    else:
        x, y = search_pos('yh', board_copy)
    
        if (x, y) in [cell for zone in special_positions for cell in zone]:
            board_copy[x][y] = 'R'
        else:
            board_copy[x][y] = EMPTY
        
    board_copy[i][j] = player
    
    return board_copy

def utility(board):
    """
    Enhanced heuristic: evaluates zone victories, partial control, distance, and adds positional value
    """
    score = 0

    # Get current positions
    ym_pos = search_pos('ym', board)
    yh_pos = search_pos('yh', board)
    
    # Zone control evaluation (base scoring)
    for zone_idx, zone in enumerate(special_positions):
        green = 0
        red = 0
        for i, j in zone:
            if board[i][j] == 'G':
                green += 1
            elif board[i][j] == 'R':
                red += 1
        
        if green > 2:
            score += 100  # secured zone: BIG bonus
        elif red > 2:
            score -= 100  # opponent secured zone: BIG penalty
        else:
            # Progressive scoring for partial control
            score += (green - red) * 10
            
            # Add small bonus for being in or near a zone that's not captured
            if ym_pos in zone:
                score += 5
            if yh_pos in zone:
                score -= 5
    
    # Strategic positioning
    if ym_pos:
        # Bonus for being in center of board (better mobility)
        center_score = 4 - (abs(ym_pos[0] - 3.5) + abs(ym_pos[1] - 3.5)) / 2
        score += center_score
    
    # Add small random factor to break ties (but keep it deterministic)
    board_hash = hash(board_to_string(board))
    random_factor = (board_hash % 10) / 100
    score += random_factor
    
    return score

def min_value(board, alpha, beta, depth):
    v = math.inf
    
    if terminal(board) or depth == 0:
        return utility(board)
    
    # Get board state as string for history tracking
    board_str = board_to_string(board)
    
    # Check if we've seen this board at this depth or greater
    if board_str in move_history and move_history[board_str][0] >= depth:
        # Return cached value with a small penalty to discourage repetition
        return move_history[board_str][1] - 1
    
    for action in actions(board, 'yh'):
        new_board = result(action, board, 'yh')
        v = min(v, max_value(new_board, alpha, beta, depth - 1))
        if v <= alpha:
            # Store result in history
            move_history[board_str] = (depth, v)
            return v
        beta = min(beta, v)
    
    # Store result in history
    move_history[board_str] = (depth, v)
    return v

def max_value(board, alpha, beta, depth):
    v = -math.inf
    
    if terminal(board) or depth == 0:
        return utility(board)
    
    # Get board state as string for history tracking
    board_str = board_to_string(board)
    
    # Check if we've seen this board at this depth or greater
    if board_str in move_history and move_history[board_str][0] >= depth:
        # Return cached value with a small penalty to discourage repetition
        return move_history[board_str][1] - 1
    
    for action in actions(board, 'ym'):
        new_board = result(action, board, 'ym')
        v = max(v, min_value(new_board, alpha, beta, depth - 1))
        if v >= beta:
            # Store result in history
            move_history[board_str] = (depth, v)
            return v
        alpha = max(alpha, v)
    
    # Store result in history
    move_history[board_str] = (depth, v)
    return v

def minimax(board, depth=4):
    """
    Returns the optimal action for the current player on the board.
    Enhanced to avoid loops and provide better decision making.
    """
    global move_history
    
    # Clear history for fresh evaluation if it gets too large
    if len(move_history) > 1000:
        move_history = {}
    
    actions_board = list(actions(board, 'ym'))
    
    if not actions_board or terminal(board):
        return None
    
    # Check if we've been in this position before
    board_str = board_to_string(board)
    repeated_position = board_str in move_history
    
    # Track action scores
    action_scores = []
    
    for action in actions_board:
        new_board = result(action, board, 'ym')
        new_board_str = board_to_string(new_board)
        
        # Add repetition penalty if this move would lead to a previously seen position
        repetition_penalty = 0
        if new_board_str in move_history:
            repetition_penalty = 1
        
        # Calculate value with penalty for repeating positions
        min_v = min_value(new_board, -math.inf, math.inf, depth - 1) - repetition_penalty
        
        # Add variation in evaluation based on action position to break ties
        i, j = action
        variation = 0.01 * ((i*8 + j) % 5) / 5.0  # Small variation based on position
        
        action_scores.append((min_v + variation, action))
    
    # Sort by score and pick the best action
    action_scores.sort(reverse=True)
    
    # If there are multiple actions with very close scores, add some variety
    best_actions = [a for score, a in action_scores if score >= action_scores[0][0] - 0.1]
    
    if len(best_actions) > 1 and repeated_position:
        # Pick a different action than before if we're in a repeated position
        return best_actions[1 % len(best_actions)]
    
    # Record this move
    move_history[board_str] = (depth, action_scores[0][0])
    
    return action_scores[0][1]