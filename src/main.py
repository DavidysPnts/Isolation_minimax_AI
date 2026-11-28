from src.board import Board
from src.ai_agent import get_best_move

def print_board(board):
    """Exibe o tabuleiro no terminal de forma legível."""
    symbols = {0: ".", 1: "P1", 2: "P2", -1: " X"}
    print("\n   " + "  ".join([str(i) for i in range(board.size)]))
    for r in range(board.size):
        row_str = f"{r} "
        for c in range(board.size):
            val = board.grid[r][c]
            row_str += f" {symbols[val]} "
        print(row_str)
    print()

def main():
    print("=" * 40)
    print("      JOGO ISOLATION - INTRODUÇÃO À IA      ")
    print("=" * 40)
    
    board = Board(size=6)
    human_player = 1
    ai_player = 2
    current_player = 1  # P1 começa
    
    while True:
        print_board(board)
        
        # Verifica se o jogador atual perdeu
        if board.is_terminal(current_player):
            winner = 2 if current_player == 1 else 1
            print(f"--- FIM DE JOGO! O Jogador {winner} VENCEU! ---")
            break
            
        print(f"Vez do Jogador {current_player} {'(Humano)' if current_player == human_player else '(IA)'}")
        
        if current_player == human_player:
            legal_moves = board.get_legal_moves(human_player)
            print(f"Movimentos válidos: {legal_moves}")
            
            # Leitura da jogada do Humano
            while True:
                try:
                    r = int(input("Digite a linha desejada: "))
                    c = int(input("Digite a coluna desejada: "))
                    if (r, c) in legal_moves:
                        board.make_move(human_player, (r, c))
                        break
                    else:
                        print("Movimento inválido! Escolha uma posição da lista de válidos.")
                except ValueError:
                    print("Por favor, digite números inteiros válidos.")
        # No turno da IA dentro do loop do main.py:
        else:
            print("IA pensando...")
            result = get_best_move(board, ai_player, depth=4, use_alpha_beta=True)
            
            move = result["move"]
            score = result["score"]
            nodes = result["nodes"]
            time_ms = result["time_ms"]
            
            if move:
                print(f"🤖 IA escolheu mover para {move} (Score: {score})")
                print(f"📊 Métricas | Nós visitados: {nodes} | Tempo: {time_ms:.2f} ms\n")
                board.make_move(ai_player, move)
            else:
                print("IA não possui movimentos válidos!")
                
        # Alterna o turno
        current_player = 2 if current_player == 1 else 1

if __name__ == "__main__":
    main()