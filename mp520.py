"""
Compute the value brought by a given move by placing a new token for player
at (row, column). The value is the number of opponent pieces getting flipped
by the move. 

A move is valid if for the player, the location specified by (row, column) is
(1) empty and (2) will cause some pieces from the other player to flip. The
return value for the function should be the number of pieces hat will be moved.
If the move is not valid, then the value 0 (zero) should be returned. Note
here that row and column both start with index 0. 
"""
import copy

# storing coordinate of tokens that flipped in this round.
affected_token = []
# storing terminal states of the game.
terminal_state_ct = 0
truncation_ct = 0


def get_move_value(state, player, row, column):
    # Check if (row, column) is a valid place or not.
    opponent = 'B' if player == 'W' else 'W'

    if state[row][column] != ' ':
        return 0

    count_flip = 0
    affected_token.clear()

    # Toward Up direction.
    try:
        up_side = state[row - 1][column]
        if up_side == opponent:
            for i in range(row):
                if state[row - i - 1][column] == opponent:
                    continue
                elif state[row - i - 1][column] == player:
                    count_flip += i
                    # print('Up: ', i)
                    for n in range(i):
                        affected_token.append((row - i + n, column))
                    break
                else:
                    break
    except IndexError:
        pass

    # Toward Right direction.
    try:
        right_side = state[row][column + 1]
        if right_side == opponent:
            for i in range(len(state) - column - 1):
                if state[row][column + i + 1] == opponent:
                    continue
                elif state[row][column + i + 1] == player:
                    count_flip += i
                    # print('Right: ', i)
                    for n in range(i):
                        affected_token.append((row, column + i - n))
                    break
                else:
                    break
    except IndexError:
        pass

    # Toward Down direction.
    try:
        down_side = state[row + 1][column]
        if down_side == opponent:
            for i in range(len(state) - row - 1):
                if state[row + i + 1][column] == opponent:
                    continue
                elif state[row + i + 1][column] == player:
                    count_flip += i
                    # print('Down: ', i)
                    for n in range(i):
                        affected_token.append((row + i - n, column))
                    break
                else:
                    break
    except IndexError:
        pass

    # Toward Left direction.
    try:
        left_side = state[row][column - 1]
        if left_side == opponent:
            for i in range(column):
                if state[row][column - i - 1] == opponent:
                    continue
                elif state[row][column - i - 1] == player:
                    count_flip += i
                    # print('Left: ', i)
                    for n in range(i):
                        affected_token.append((row, column - i + n))
                    break
                else:
                    break
    except IndexError:
        pass

    # Toward Up Right direction.
    try:
        upright_side = state[row - 1][column + 1]
        if upright_side == opponent:
            for i in range(min(row, (len(state) - column - 1))):
                if state[row - i - 1][column + i + 1] == opponent:
                    continue
                elif state[row - i - 1][column + i + 1] == player:
                    count_flip += i
                    # print('Up Right: ', i)
                    for n in range(i):
                        affected_token.append((row - i + n, column + i - n))
                    break
                else:
                    break
    except IndexError:
        pass

    # Toward Down Right direction.
    try:
        downright_side = state[row + 1][column + 1]
        if downright_side == opponent:
            for i in range(min((len(state) - row - 1), (len(state) - column - 1))):
                if state[row + i + 1][column + i + 1] == opponent:
                    continue
                elif state[row + i + 1][column + i + 1] == player:
                    count_flip += i
                    # print('Down Right: ', i)
                    for n in range(i):
                        affected_token.append((row + i - n, column + i - n))
                    break
                else:
                    break
    except IndexError:
        pass

    # Toward Down Left direction.
    try:
        downleft_side = state[row + 1][column - 1]
        if downleft_side == opponent:
            for i in range(min((len(state) - row - 1), column)):
                if state[row + i + 1][column - i - 1] == opponent:
                    continue
                elif state[row + i + 1][column - i - 1] == player:
                    count_flip += i
                    # print('Down Left: ', i)
                    for n in range(i):
                        affected_token.append((row + i - n, column - i + n))
                    break
                else:
                    break
    except IndexError:
        pass

    # Toward Up Left direction.
    try:
        upleft_side = state[row - 1][column - 1]
        if upleft_side == opponent:
            for i in range(min(row, column)):
                if state[row - i - 1][column - i - 1] == opponent:
                    continue
                elif state[row - i - 1][column - i - 1] == player:
                    count_flip += i
                    # print('Up Left: ', i)
                    for n in range(i):
                        affected_token.append((row - i + n, column - i + n))
                    break
                else:
                    break
    except IndexError:
        pass

    return count_flip


"""
Execute a move that updates the state. A new state should be crated. The move
must be valid. Note that the new state should be a clone of the old state and
in particular, should not share memory with the old state. 
"""


def execute_move(state, player, row, column):
    temp_state = copy.deepcopy(state)
    flipped = get_move_value(state, player, row, column)
    if flipped > 0:
        for coord in affected_token:
            temp_state[coord[0]][coord[1]] = 'B' if player == 'B' else 'W'
        temp_state[row][column] = player

    return temp_state


"""
A method for counting the pieces owned by the two players for a given state. The
return value should be two tuple in the format of (blackpeices, white pieces), e.g.,

    return (4, 3)

"""

# return: list of available places, number of black tokens, number of white tokens.
def check_board(state):
    valid_list = []
    B_count = 0
    W_count = 0
    for r in range(len(state)):
        for c in range(len(state)):
            if state[r][c] == ' ':
                valid_list.append((r, c))
            elif state[r][c] == 'B':
                B_count += 1
            elif state[r][c] == 'W':
                W_count += 1

    return valid_list, B_count, W_count


def count_pieces(state):
    valid_coord, blackpieces, whitepieces = check_board(state)
    # Your implementation goes here
    return (blackpieces, whitepieces)


"""
Check whether a state is a terminal state. 
"""


def is_terminal_state(state, state_list=None):
    valid_coord, B_count, W_count = check_board(state)
    for coord in valid_coord:
        if get_move_value(state, 'B', coord[0], coord[1]) > 0 or get_move_value(state, 'W', coord[0], coord[1]) > 0:
            return False
    # state_list.append(state)
    return True


"""
The minimax algorithm. Your implementation should return the best value for the
given state and player, as well as the next immediate move to take for the player. 
"""


def minimax(state, player):
    tree_depth = 0
    if player == 'B':
        value, row, column = max_val(state, tree_depth)
        return value, row, column
    elif player == 'W':
        value, row, column = min_val(state, tree_depth)
        return value, row, column


# return maximum possible value of the game - (value, row, column)
def max_val(state, depth):
    global terminal_state_ct
    if is_player_terminated(state, 'B'):
        terminal_state_ct += 1
        return count_pieces(state)[0] - count_pieces(state)[1], -1, -1
    v, row, column = -100, -1, -1
    available_places, a, b = check_board(state)
    for move in available_places:
        # Check current state if movable for 'B'
        executed_state = execute_move(state, 'B', move[0], move[1])
        if executed_state == state:
            continue
        depth += 1
        curr_val, r, c = min_val(executed_state, depth)
        if r == -1 and c == -1:
            if not is_player_terminated(executed_state, 'B'):
                curr_val, r, c = max_val(executed_state, depth)
        depth -= 1
        if curr_val > v:
            v, row, column = curr_val, move[0], move[1]

    return v, row, column


# return minimum possible value of the game - (value, row, column)
def min_val(state, depth):
    global terminal_state_ct
    if is_player_terminated(state, 'W'):
        terminal_state_ct += 1
        return count_pieces(state)[0] - count_pieces(state)[1], -1, -1
    v, row, column = 100, -1, -1
    available_places, a, b = check_board(state)
    for move in available_places:
        # Check if current state is movable for 'W'
        executed_state = execute_move(state, 'W', move[0], move[1])
        if executed_state == state:
            continue
        depth += 1
        curr_val, r, c = max_val(executed_state, depth)
        if r == -1 and c == -1:
            if not is_player_terminated(executed_state, 'W'):
                curr_val, r, c = min_val(executed_state, depth)
        depth -= 1
        if curr_val < v:
            v, row, column = curr_val, move[0], move[1]

    return v, row, column


"""
This method should call the minimax algorithm to compute an optimal move sequence
that leads to an end game. 
"""


# return: True - current player cannot make further move; False - current player still movable.
def is_player_terminated(state, player):
    curr_state, b, c = check_board(state)
    for m in curr_state:
        new_state = execute_move(state, player, m[0], m[1])
        if new_state != state:
            return False
    return True


def full_minimax(state, player):
    # copy a new state from the old state
    now_state = copy.deepcopy(state)
    # generate the first step
    move = minimax(now_state, player)
    # notedown the final value
    final_value = move[0]
    # append the first move into the move list.
    move_list = [(player, move[1], move[2])]
    # generate a new state base on the first move
    now_state = execute_move(now_state, player, move[1], move[2])
    # switch player
    next_player = 'B' if player == 'W' else 'W'

    while True:
        if not is_player_terminated(now_state, next_player):
            move = minimax(now_state, next_player)
            now_state = execute_move(now_state, next_player, move[1], move[2])
            move_list.append((next_player, move[1], move[2]))
        next_player = 'B' if next_player == 'W' else 'W'
        if is_terminal_state(now_state):
            move = minimax(now_state, player)
            move_list.append((next_player, move[1], move[2]))
            break

    return final_value, move_list


"""
The minimax algorithm with alpha-beta pruning. Your implementation should return the
best value for the given state and player, as well as the next immediate move to take
for the player. 
"""


def minimax_ab(state, player, alpha=-10000000, beta=10000000):
    tree_depth = 0
    alpha = -100
    beta = 100
    if player == 'B':
        value, row, column = max_val_ab(state, tree_depth, alpha, beta)
        return value, row, column
    elif player == 'W':
        value, row, column = min_val_ab(state, tree_depth, alpha, beta)
        return value, row, column


def max_val_ab(state, depth, a, b):
    global terminal_state_ct, truncation_ct
    if is_player_terminated(state, 'B'):
        terminal_state_ct += 1
        return count_pieces(state)[0] - count_pieces(state)[1], -1, -1

    v, row, column = -100, -1, -1
    available_places, y, z = check_board(state)
    for move in available_places:
        # Check if current state is movable for 'B'
        executed_state = execute_move(state, 'B', move[0], move[1])
        if executed_state == state:
            continue
        depth += 1
        curr_val, r, c = min_val_ab(executed_state, depth, a, b)
        if r == -1 and c == -1:
            if not is_player_terminated(executed_state, 'B'):
                curr_val, r, c = max_val_ab(executed_state, depth, a, b)
        depth -= 1
        if curr_val > v:
            v, row, column = curr_val, move[0], move[1]
            a = max(a, v)
        if v >= b:
            truncation_ct += 1
            return v, row, column

    return v, row, column


def min_val_ab(state, depth, a, b):
    global terminal_state_ct, truncation_ct
    if is_player_terminated(state, 'W'):
        terminal_state_ct += 1
        return count_pieces(state)[0] - count_pieces(state)[1], -1, -1

    v, row, column = 100, -1, -1
    available_places, y, z = check_board(state)
    for move in available_places:
        # Check if current state is movable for 'W'
        executed_state = execute_move(state, 'W', move[0], move[1])
        if executed_state == state:
            continue
        depth += 1
        curr_val, r, c = max_val_ab(executed_state, depth, a, b)
        if r == -1 and c == -1:
            if not is_player_terminated(executed_state, 'W'):
                curr_val, r, c = min_val_ab(executed_state, depth, a, b)
        depth -= 1
        if curr_val < v:
            v, row, column = curr_val, move[0], move[1]
            b = min(b, v)
        if v <= a:
            truncation_ct += 1
            return v, row, column

    return v, row, column


"""
This method should call the minimax_ab algorithm to compute an optimal move sequence
that leads to an end game, using alpha-beta pruning.
"""


def full_minimax_ab(state, player):
    # copy a new state from the old state
    now_state = copy.deepcopy(state)
    # generate the first step
    move = minimax_ab(now_state, player)
    # notedown the final value
    final_value = move[0]
    # append the first move into the move list.
    move_list = [(player, move[1], move[2])]
    # generate a new state base on the first move
    now_state = execute_move(now_state, player, move[1], move[2])
    # switch player
    next_player = 'B' if player == 'W' else 'W'

    while True:
        if not is_player_terminated(now_state, next_player):
            move = minimax_ab(now_state, next_player)
            now_state = execute_move(now_state, next_player, move[1], move[2])
            move_list.append((next_player, move[1], move[2]))
        next_player = 'B' if next_player == 'W' else 'W'
        if is_terminal_state(now_state):
            move = minimax_ab(now_state, player)
            move_list.append((next_player, move[1], move[2]))
            break

    return final_value, move_list