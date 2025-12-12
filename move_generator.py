from Move import Move
import copy

def get_moves(gamestate, board, row, col):
    if board[row][col].upper() == "B":
        return get_bishop_moves(gamestate, board, row, col)
    if board[row][col].upper() == "P":
        return get_pawn_moves(gamestate, board, row, col)
    if board[row][col].upper() == "N":
        return get_knight_moves(gamestate, board, row, col)
    if board[row][col].upper() == "K":
        return get_king_moves(gamestate, board, row, col)
    if board[row][col].upper() == "R":
        return get_rook_moves(gamestate, board, row, col)
    if board[row][col].upper() == "Q":
        return get_queen_moves(gamestate, board, row, col)
    

def get_rook_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    for dr, dc in directions:
        straight_line_moves(gamestate, board, start_row, start_col, dr, dc, valid_moves)
    
    return valid_moves

def get_bishop_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    directions = [(-1,-1), (1,-1), (-1,1), (1,1)]
    
    for dr, dc in directions:
        straight_line_moves(gamestate, board, start_row, start_col, dr, dc, valid_moves)
    
    return valid_moves

def get_queen_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    
    for dr, dc in directions:
        straight_line_moves(gamestate, board, start_row, start_col, dr, dc, valid_moves)
    
    return valid_moves

def get_knight_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    
    piece_color = board[start_row][start_col].isupper()
    
    directions = [(-2,-1), (-2,1), (-1,-2), (-1,2),
                  (1,-2), (1,2), (2,-1), (2,1)]
    
    for r, c in directions:
        new_r = start_row + r
        new_c = start_col + c

        
        if 0 <= new_r < 8 and 0 <= new_c < 8:
            target_square = board[new_r][new_c]
            if target_square == 0 or (target_square != 0 and target_square.isupper() != piece_color):
                new_move = Move((start_row, start_col), (new_r, new_c), board)
                if gamestate.check_analysis:
                    valid_moves.append(new_move)
                elif not puts_in_check(gamestate, board, new_move):
                    valid_moves.append(new_move)
    return(valid_moves)

def get_king_moves(gamestate, board, start_row, start_col):
    valid_moves = []
    castling = []
    
    piece_color = board[start_row][start_col].isupper()

    if piece_color and start_row == 7 and start_col == 4 and not gamestate.check_analysis:
        castling = castle(gamestate, board, piece_color)
    elif not piece_color and start_row == 0 and start_col == 4 and not gamestate.check_analysis:
        castling = castle(gamestate, board, piece_color)
    if castling:
        for new_move in castling:
            if gamestate.check_analysis:
                valid_moves.append(new_move)
            elif not puts_in_check(gamestate, board, new_move):
                valid_moves.append(new_move)
        
    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    
    for r, c in directions:
        new_r = start_row + r
        new_c = start_col + c
        
        
        if 0 <= new_r < 8 and 0 <= new_c < 8:
            target_square = board[new_r][new_c]
            if target_square == 0 or (target_square != 0 and target_square.isupper() != piece_color):
                new_move = Move((start_row, start_col), (new_r, new_c), board)
                if gamestate.check_analysis:
                    valid_moves.append(new_move)
                elif not puts_in_check(gamestate, board, new_move):
                    valid_moves.append(new_move)
    return(valid_moves)

def castle(gamestate, board, piece_color):
    if piece_color and board[7][4] == "K":
        kings = "e1"
    elif not piece_color and board[0][4] == 'k':
        kings = "e8"

    #If the king isn't on its starting square, or if it has moved back to its starting square, 
    #castling is not possible. Would need to be changed to support 960 if desired
    if not kings:
        return None
    else:
        for move in gamestate.move_log:
            if move[-2:] == kings:
                return None
    #The same logic for rooks, if a rook isn't on it's starting square or has moved it cannot be used to castle
    #This block also ensures there are no pieces between the rook and king
    rooks = []
    if piece_color:
        if board[7][0] == "R" and board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0:
            rooks.append("a1")
        if board[7][7] == "R" and board[7][6] == 0 and board[7][5] == 0:
            rooks.append("h1")
    else:
        if board[0][0] == "r" and board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0:
            rooks.append("a8")
        if board[0][7] == "r" and board[0][6] == 0 and board[0][5] == 0:
            rooks.append("h8")

    for rook in rooks[::-1]:
        for move in gamestate.move_log:
            if move[-2:] == rook:
                rooks.remove(rook)

    #For each rook that might be castled with, make sure the king doesn't go into, out of, or through check
    into_out_of_through_check = []
    legal_castle_moves = []
    if "a1" in rooks:
        legal_castle_moves.append(Move((7, 4), (7, 2), board))

        into_out_of_through_check.append(Move((7, 4), (7, 4), board))
        into_out_of_through_check.append(Move((7, 4), (7, 3), board))
        into_out_of_through_check.append(Move((7, 4), (7, 2), board))

        for move in into_out_of_through_check:
           if puts_in_check(gamestate, board, move):
                legal_castle_moves.remove(Move((7, 4), (7, 2), board))
                break
        into_out_of_through_check = []
        

    if "h1" in rooks:
        legal_castle_moves.append(Move((7, 4), (7, 6), board))

        into_out_of_through_check.append(Move((7, 4), (7, 4), board))
        into_out_of_through_check.append(Move((7, 4), (7, 5), board))
        into_out_of_through_check.append(Move((7, 4), (7, 6), board))

        for move in into_out_of_through_check:
           if puts_in_check(gamestate, board, move):
                legal_castle_moves.remove(Move((7, 4), (7, 6), board))
                break
        into_out_of_through_check = []

    if "a8" in rooks:
        legal_castle_moves.append(Move((0, 4), (0, 2), board))

        into_out_of_through_check.append(Move((0, 4), (0, 4), board))
        into_out_of_through_check.append(Move((0, 4), (0, 3), board))
        into_out_of_through_check.append(Move((0, 4), (0, 2), board))

        for move in into_out_of_through_check:
           if puts_in_check(gamestate, board, move):
                legal_castle_moves.remove(Move((0, 4), (0, 2), board))
                break
        into_out_of_through_check = []

    if "h8" in rooks:
        legal_castle_moves.append(Move((0, 4), (0, 6), board))

        into_out_of_through_check.append(Move((0, 4), (0, 4), board))
        into_out_of_through_check.append(Move((0, 4), (0, 5), board))
        into_out_of_through_check.append(Move((0, 4), (0, 6), board))
        for move in into_out_of_through_check:
           if puts_in_check(gamestate, board, move):
                legal_castle_moves.remove(Move((0, 4), (0, 6), board))
                break
        into_out_of_through_check = []

    return legal_castle_moves

def get_pawn_moves(gamestate, board, start_row, start_col):   
    valid_moves = []
    
    #if not isupper() then piece is black and moves down the board (row increases)
    piece_color = board[start_row][start_col].isupper()
     
    
    direction = -1 if piece_color else 1

    if start_row + direction < 0 or start_row + direction > 7:
        return []
    
    #Normal pawn move
    if board[start_row + direction][start_col] == 0:
        promotion_piece_list = promotion_piece_options(start_row, direction, piece_color)
        for piece in promotion_piece_list:
            if piece == "Not Promotion":
                new_move = Move((start_row, start_col), (start_row + direction, start_col), board)
            else:
                new_move = Move((start_row, start_col), (start_row + direction, start_col), board, piece)
            if gamestate.check_analysis:
                valid_moves.append(new_move)
            elif not puts_in_check(gamestate, board, new_move):
                valid_moves.append(new_move)

        #Check if piece is on starting square. Tiny optimization to only check if square in front of pawn is empty
        starting_square = True if (piece_color and start_row == 6) or (not piece_color and start_row == 1) else False
        if starting_square and board[start_row + 2 * direction][start_col] == 0:
            new_move = Move((start_row, start_col), (start_row + 2 * direction, start_col), board)
            if gamestate.check_analysis:
                valid_moves.append(new_move)
            elif not puts_in_check(gamestate, board, new_move):
                valid_moves.append(new_move)

    
    #Pawn capture
    capture_directions = [(direction,-1),(direction,1)]
    
    for r, c in capture_directions:
        new_r = start_row + r
        new_c = start_col + c
        
        if 0 <= new_r < 8 and 0 <= new_c < 8:
            target_square = board[new_r][new_c]
            target_square_state = target_square_status(gamestate, board, piece_color, target_square, valid_moves)
            
            if target_square_state == 1 or gamestate.en_passant == ([new_r, new_c]):
                promotion_piece_list = promotion_piece_options(start_row, direction, piece_color)
                for piece in promotion_piece_list:
                    if piece == "Not Promotion":
                        new_move = Move((start_row, start_col), (new_r, new_c), board)
                    else:
                        new_move = Move((start_row, start_col), (new_r, new_c), board, piece)
                    if gamestate.check_analysis:
                        valid_moves.append(new_move)
                    elif not puts_in_check(gamestate, board, new_move):
                        valid_moves.append(new_move)
        
    return(valid_moves)

def promotion_piece_options(start_row, direction, piece_color):
    if (start_row + direction == 0 and piece_color):
        return ["Q", "R", "B", "N"]
    elif (start_row + direction == 7 and not piece_color):
        return ["q", "r", "b", "n"]
    else:
        return ["Not Promotion"]

def check_en_passant(board, start_row, end_row, end_col):
    if board[end_row][end_col].upper() == "P" and abs(end_row - start_row) == 2:
        return_row = (end_row + start_row) / 2
        return ([return_row, end_col])
    return False

def target_square_status(gamestate, board, piece_color, target_square, valid_moves):
    if target_square == 0:
        return 0
    if target_square.isupper() != piece_color:
        return 1
    else:
        return 2
    

def straight_line_moves(gamestate, board, start_row, start_col, r, c, valid_moves):
    piece_color = board[start_row][start_col].isupper()
    
    new_r = start_row + r
    new_c = start_col + c
    
    while 0 <= new_r < 8 and 0 <= new_c < 8:
        target_square = board[new_r][new_c]
        #Empty square is valid
        target_square_state = target_square_status(gamestate, board, piece_color, target_square, valid_moves)
        if target_square_state == 0:
            new_move = Move((start_row, start_col), (new_r, new_c), board)
            if gamestate.check_analysis:
                valid_moves.append(new_move)
            elif not puts_in_check(gamestate, board, new_move):
                valid_moves.append(new_move)
            
        #An opposing piece is valid, and nothing past that piece will be valid
        elif target_square_state == 1:
            new_move = Move((start_row, start_col), (new_r, new_c), board)
            if gamestate.check_analysis:
                valid_moves.append(new_move)
            elif not puts_in_check(gamestate, board, new_move):
                valid_moves.append(new_move)
            break
        
        #If its our own piece, its not valid, and nothing past that piece will be valid
        else:
            break
        
        #If not interrupted, keep searching in the same direction
        new_r += r
        new_c += c
        
def puts_in_check(gamestate, board, Move, move_log = []):
    check_candidate_moves = []
    #Copy the board, try the move on that board, see if still in check
    temp_board = copy.deepcopy(board)
    #Copy the gamestate and set the check flag to false, to prevent recursion
    temp_gamestate = copy.deepcopy(gamestate)
    temp_gamestate.check_analysis = True
    temp_board[Move.end_row][Move.end_col] = temp_board[Move.start_row][Move.start_col]
    #The below check shouldn't need to be made, since a piece can't move without moving. Its a bandaid fix for right now
    #I needed a way to see if a king is currently in check when determining if it can castle, and I don't currently have that, 
    #I only have a way to see if a move will leave the king in check. Thus I needed a "move" that doesn't change the position
    if (Move.start_row, Move.start_col) != (Move.end_row, Move.end_col):
        temp_board[Move.start_row][Move.start_col] = 0
    if temp_board[Move.end_row][Move.end_col].upper() == 'P' and [Move.end_row, Move.end_col] == gamestate.en_passant:
            temp_board[Move.start_row][Move.end_col] = 0
    temp_gamestate.white_to_move = not gamestate.white_to_move

    #Basically iterate through every move the player who just moved can make to see if it can capture the opposing king, and if so, set a flag that the player on move is in check
    king_square = None
    for i in range(0,8):
        for j in range(0,8):
            if temp_board[i][j] == 0:
                continue
            if temp_board[i][j].isupper() == temp_gamestate.white_to_move:
                moves_for_piece = get_moves(temp_gamestate, temp_board, i, j)
                check_candidate_moves.extend(moves_for_piece)
            elif temp_board[i][j].isupper() != temp_gamestate.white_to_move and temp_board[i][j].upper() == "K":
                king_square = (i, j)

    if not king_square:
        print("Error: king_square not found")
    
    for move in check_candidate_moves:
        if move.end_row == king_square[0] and move.end_col == king_square[1]:
            return True
        
    return False
