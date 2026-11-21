import copy

class Board:
    def __init__(self, size=6):
        self.size = size
        # 0: Casa livre, 1: Jogador 1, 2: Jogador 2, -1: Casa bloqueada/queimada
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        
        # Posições iniciais padrão em cantos opostos
        self.pos = {
            1: (0, 0),
            2: (size - 1, size - 1)
        }
        self.grid[0][0] = 1
        self.grid[size - 1][size - 1] = 2

    def get_legal_moves(self, player):
        """Retorna todas as posições (r, c) válidas para o jogador atual (movimento de Rainha)."""
        r_curr, c_curr = self.pos[player]
        legal_moves = []
        
        # 8 direções: (delta_linha, delta_coluna)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), # Cima, Baixo, Esquerda, Direita
            (-1, -1), (-1, 1), (1, -1), (1, 1) # Diagonais
        ]
        
        for dr, dc in directions:
            r, c = r_curr + dr, c_curr + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == 0:
                legal_moves.append((r, c))
                r += dr
                c += dc
                
        return legal_moves

    def make_move(self, player, new_pos):
        """Executa o movimento: queima a casa antiga e move o jogador para a nova."""
        r_old, c_old = self.pos[player]
        r_new, c_new = new_pos
        
        # A casa antiga fica bloqueada/queimada (-1)
        self.grid[r_old][c_old] = -1
        
        # Atualiza a nova posição do jogador
        self.grid[r_new][c_new] = player
        self.pos[player] = (r_new, c_new)

    def is_terminal(self, current_player):
        """O jogo acaba quando o jogador da vez não possui movimentos válidos."""
        return len(self.get_legal_moves(current_player)) == 0

    def clone(self):
        """Cria uma cópia profunda do tabuleiro para a IA simular jogadas futuras."""
        return copy.deepcopy(self)