def _terminal_score(ai_moves: int, opp_moves: int, ai_player: int, current_player: int, depth: int):
    """
    Verifica estados terminais priorizando vitórias mais rápidas (+depth)
    e respeitando quem é o jogador da vez em caso de bloqueio mútuo.
    """
    opponent = 2 if ai_player == 1 else 1

    if current_player == ai_player and ai_moves == 0:
        return -10000 - depth
    if current_player == opponent and opp_moves == 0:
        return 10000 + depth
    if ai_moves == 0:
        return -10000 - depth
    if opp_moves == 0:
        return 10000 + depth

    return None


def simple_mobility(board, ai_player: int, current_player: int, depth: int = 0) -> float:
    """Heurística 1: Avalia apenas a quantidade de movimentos válidos da própria IA."""
    opponent = 2 if ai_player == 1 else 1
    ai_moves = len(board.get_legal_moves(ai_player))
    opp_moves = len(board.get_legal_moves(opponent))

    terminal = _terminal_score(ai_moves, opp_moves, ai_player, current_player, depth)
    if terminal is not None:
        return terminal

    return float(ai_moves)


def differential_mobility(board, ai_player: int, current_player: int, depth: int = 0) -> float:
    """Heurística 2 (Baseline): Diferença direta entre movimentos da IA e do oponente."""
    opponent = 2 if ai_player == 1 else 1
    ai_moves = len(board.get_legal_moves(ai_player))
    opp_moves = len(board.get_legal_moves(opponent))

    terminal = _terminal_score(ai_moves, opp_moves, ai_player, current_player, depth)
    if terminal is not None:
        return terminal

    return float(ai_moves - opp_moves)


def aggressive_chase(board, ai_player: int, current_player: int, depth: int = 0) -> float:
    """
    Heurística 3: Perseguição agressiva (penaliza em dobro a mobilidade rival)
    somada a um bônus posicional pelo controle do centro do tabuleiro.
    """
    opponent = 2 if ai_player == 1 else 1
    ai_moves = len(board.get_legal_moves(ai_player))
    opp_moves = len(board.get_legal_moves(opponent))

    terminal = _terminal_score(ai_moves, opp_moves, ai_player, current_player, depth)
    if terminal is not None:
        return terminal

    # Bônus de centralidade: quanto mais perto do centro do grid, maior a pontuação
    center = (board.size - 1) / 2.0
    r_ai, c_ai = board.pos[ai_player]
    r_opp, c_opp = board.pos[opponent]

    ai_dist = abs(r_ai - center) + abs(c_ai - center)
    opp_dist = abs(r_opp - center) + abs(c_opp - center)
    center_bonus = (opp_dist - ai_dist) * 0.5

    return float((ai_moves - 2 * opp_moves) + center_bonus)

def order_moves(board, moves: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Ordena os movimentos válidos priorizando as casas mais próximas do centro
    do tabuleiro para maximizar os cortes da Poda Alfa-Beta.
    """
    center = (board.size - 1) / 2.0
    return sorted(
        moves,
        key=lambda move: abs(move[0] - center) + abs(move[1] - center)
    )

HEURISTICS = {
    "simples": simple_mobility,
    "diferencial": differential_mobility,
    "agressiva": aggressive_chase,
}