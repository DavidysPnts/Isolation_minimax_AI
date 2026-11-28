import math
import time

def evaluate(board, ai_player):
    """
    Calcula a Mobilidade Relativa: Movimentos(IA) - Movimentos(Oponente).
    """
    opponent = 2 if ai_player == 1 else 1
    ai_moves = len(board.get_legal_moves(ai_player))
    opp_moves = len(board.get_legal_moves(opponent))
    
    if opp_moves == 0:
        return 10000   # Vitória de MAX (IA)
    if ai_moves == 0:
        return -10000  # Vitória de MIN (Oponente)
        
    return ai_moves - opp_moves

def minimax(board, depth, alpha, beta, is_maximizing, ai_player, use_alpha_beta=True, stats=None):
    """
    Algoritmo Minimax com parâmetro toggle (use_alpha_beta) e contador de nós explorados.
    """
    # Incrementa a contagem de nós visitados a cada chamada da função
    if stats is not None:
        stats['nodes'] += 1

    opponent = 2 if ai_player == 1 else 1
    current_player = ai_player if is_maximizing else opponent
    
    # Condição de parada (Cutoff)
    if depth == 0 or board.is_terminal(current_player):
        return evaluate(board, ai_player), None

    legal_moves = board.get_legal_moves(current_player)
    best_move = None

    if is_maximizing:
        max_eval = -math.inf
        for move in legal_moves:
            temp_board = board.clone()
            temp_board.make_move(ai_player, move)
            
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, False, ai_player, use_alpha_beta, stats)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            # PODA ALFA-BETA: executada apenas se use_alpha_beta == True
            if use_alpha_beta:
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Poda Beta
                    
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in legal_moves:
            temp_board = board.clone()
            temp_board.make_move(opponent, move)
            
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, True, ai_player, use_alpha_beta, stats)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            # PODA ALFA-BETA: executada apenas se use_alpha_beta == True
            if use_alpha_beta:
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Poda Alfa
                    
        return min_eval, best_move

def get_best_move(board, ai_player, depth=4, use_alpha_beta=True):
    """
    Inicia a busca, mede o tempo com time.perf_counter() e retorna o dicionário exato solicitado.
    """
    stats = {'nodes': 0}
    start_time = time.perf_counter()
    
    best_score, best_move = minimax(
        board=board,
        depth=depth,
        alpha=-math.inf,
        beta=math.inf,
        is_maximizing=True,
        ai_player=ai_player,
        use_alpha_beta=use_alpha_beta,
        stats=stats
    )
    
    elapsed_ms = (time.perf_counter() - start_time) * 1000  # Converte para milissegundos
    
    # Retorno exatamente como especificado na Issue #4
    return {
        "move": best_move,
        "score": best_score,
        "nodes": stats['nodes'],
        "time_ms": elapsed_ms
    }