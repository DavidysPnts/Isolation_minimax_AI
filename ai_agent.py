import math

def evaluate(board, ai_player):
    """
    Função de Avaliação (Heurística de Mobilidade):
    Calcula a diferença entre os movimentos disponíveis da IA e do oponente.
    """
    opponent = 2 if ai_player == 1 else 1
    
    ai_moves = len(board.get_legal_moves(ai_player))
    opp_moves = len(board.get_legal_moves(opponent))
    
    # Se a IA venceu
    if opp_moves == 0:
        return 10000
    # Se a IA perdeu
    if ai_moves == 0:
        return -10000
        
    return ai_moves - opp_moves

def minimax(board, depth, alpha, beta, is_maximizing, ai_player):
    """Algoritmo Minimax com Poda Alfa-Beta."""
    opponent = 2 if ai_player == 1 else 1
    current_player = ai_player if is_maximizing else opponent
    
    # Condição de parada: limite de profundidade ou estado terminal
    if depth == 0 or board.is_terminal(current_player):
        return evaluate(board, ai_player), None

    legal_moves = board.get_legal_moves(current_player)
    best_move = None

    if is_maximizing:
        max_eval = -math.inf
        for move in legal_moves:
            temp_board = board.clone()
            temp_board.make_move(ai_player, move)
            
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, False, ai_player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Poda Beta
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in legal_moves:
            temp_board = board.clone()
            temp_board.make_move(opponent, move)
            
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, True, ai_player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Poda Alfa
        return min_eval, best_move

def get_best_move(board, ai_player, depth=4):
    """Função principal chamada pelo jogo para obter a melhor jogada da IA."""
    _, best_move = minimax(board, depth, -math.inf, math.inf, True, ai_player)
    return best_move