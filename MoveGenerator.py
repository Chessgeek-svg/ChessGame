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
    
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    
    for dr, dc in directions:
        valid_moves.append(straight_line_moves(gamestate, board, start_row, start_col, dr, dc, valid_moves))
    
    return valid_moves

def get_knight_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    piece_color = board[start_row][start_col].isupper()
    
    directions = [(-2,-1), (-2,1), (-1,-2), (-1,2),
                  (1,-2), (1,2), (2,-1), (2,1)]
    
    for r, c in directions:
        new_r = start_row + r
        new_c = start_col + c
        
        if 0 <= new_r < 8 and 0 <= new_c < 8 and board[new_r][new_c].isupper() != piece_color:
            valid_moves.append([new_r][new_c])
    return(valid_moves)

def get_king_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    piece_color = board[start_row][start_col].isupper()
        
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    
    for r, c in directions:
        new_r = start_row + r
        new_c = start_col + c
        
        if 0 <= new_r < 8 and 0 <= new_c < 8 and board[new_r][new_c].isupper() != piece_color:
            valid_moves.append([new_r][new_c])
    return(valid_moves)

def get_pawn_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    #if isupper() then piece is black and moves down the board (row increases)
    piece_color = board[start_row][start_col].isupper()
     
    
    direction = -1 if piece_color else 1
    
    #Normal pawn move
    if board[start_row + direction][start_col] == 0:
        valid_moves.append[start_row + direction][start_col]
        if (start_row + direction == 0 and piece_color) or (start_row + direction == 7 and not piece_color):
            #TODO Promotion Check but not here since this is just a list of valid moves
            pass
        
        #Check if piece is on starting square. Tiny optimization to only check if square in front of pawn is empty
        starting_square = True if (piece_color and start_row == 6) or (not piece_color and start_row == 1) else False
        if starting_square:
            if board[start_row + 2 * direction][start_col] == 0:
                valid_moves.append[start_row + direction][start_col]

    
    #Pawn capture
    capture_directions = [(direction,-1),(direction,1)]
    
    for r, c in capture_directions:
        new_r = start_row + r
        new_c = start_col + c
        if 0 <= new_r <8 and 0 <= new_c < 8 and board[new_r][new_c] != 0 and board[new_r][new_c].isupper() != piece_color:
            valid_moves.append([new_r][new_c])
            if (start_row + direction == 0 and piece_color) or (start_row + direction == 7 and not piece_color):
                #TODO Promotion Check but not here since this is just a list of valid moves
                pass
    
    return(valid_moves)

def straight_line_moves(board, row, col, start_row, start_col, r, c, valid_moves):
    moves = []
    
    new_r = start_row + r
    new_c = start_col + c
    
    while 0 <= new_r < 8 and 0 <= new_c < 8:
        target_square = board[new_r][new_c]
        #Empty square is valid
        if target_square == 0:
            valid_moves.append(([new_r,new_c]))
            
        #An opposing piece is valid, and nothing past that piece will be valid
        elif target_square.isupper() != board[start_row][start_col].isupper():
            valid_moves.append(([new_r,new_c]))
            break
        
        #If its our own piece, its not valid, and nothing past that piece will be valid
        else:
            break
        
        #If not interrupted, keep searching in the same direction
        new_r += r
        new_c += c
