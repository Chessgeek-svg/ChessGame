def get_rook_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    for dr, dc in directions:
        valid_moves.append(straight_line_moves(gamestate, board, start_row, start_col, dr, dc))
    
    return valid_moves

def get_bishop_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    directions = [(-1,-1), (1,-1), (-1,1), (1,1)]
    
    for dr, dc in directions:
        valid_moves.append(straight_line_moves(gamestate, board, start_row, start_col, dr, dc, valid_moves))
    
    return valid_moves

def get_queen_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (-1,1), (1,1)]
    
    for dr, dc in directions:
        valid_moves.append(straight_line_moves(gamestate, board, start_row, start_col, dr, dc, valid_moves))
    
    return valid_moves

def straight_line_moves(board, row, col, start_row, start_col, dr, dc, valid_moves):
    moves = []
    
    new_r = start_row + dr
    new_c = start_col + dc
    
    while 0 <= new_r < 8 and 0 <= new_c < 8:
        target_square = board[new_r][new_c]
        #Empty square is valid
        if target_square == 0:
            valid_moves.append(([row,col]))
            
        #An opposing piece is valid, and nothing past that piece will be valid
        elif target_square.islower() != board[start_row][start_col].islower():
            valid_moves.append(([row,col]))
            break
        
        #If its our own piece, its not valid, and nothing past that piece will be valid
        else:
            break
        
        #If not interrupted, keep searching in the same direction
        new_r += dr
        new_c += dc
