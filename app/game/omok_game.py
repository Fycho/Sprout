import numpy as np

# 一些约定俗成
# 先手O，后手X。
# 棋子数据0：无子，1：O，2：X
class OmokGame:
    board_size: int = 15
    max_player: int = 2
    win_size: int = 5
    players: list = []
    position_i: tuple = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O')
    position_j: tuple = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15')
    position_i_f: tuple = ('Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ', 'Ｆ', 'Ｇ', 'Ｈ', 'Ｉ', 'Ｊ', 'Ｋ', 'Ｌ', 'Ｍ', 'Ｎ', 'Ｏ')
    position_j_f: tuple = ('１', '２', '３', '４', '５', '６', '７', '８', '９', '10', '11', '12', '13', '14', '15')

    def __init__(self) -> None:
        pass

    def init(self):
        self.board = np.zeros([OmokGame.board_size, OmokGame.board_size], dtype=int)
        self.players = []
        self.current_turn = 0
        self.win_status = False

    def join(self, user_id):
        self.players.append(user_id)

    def quit(self, user_id):
        self.players.remove(user_id)

    def place(self, ii, ij):
        self.board[ii][ij] = self.current_turn + 1
        if self.check_win(ii, ij):
            self.win_status = True

    def change_turn(self):
        self.current_turn = (self.current_turn + 1) % self.max_player

    def check_win(self, i, j) -> bool:
        piece = self.board[i][j]
        return self.check_vertical(piece, i, j) \
               or self.check_horizontal(piece, i, j) \
               or self.check_diagonal1(piece, i, j) \
               or self.check_diagonal2(piece, i, j)

    def check_vertical(self, piece, i, j) -> bool:
        count: int = 0
        coord: int = i
        while coord >= 0 and self.board[coord][j] == piece:
            count += 1
            coord -= 1

        coord = i + 1
        while coord < len(self.board) and self.board[coord][j] == piece:
            count += 1
            coord += 1

        return count >= self.win_size

    def check_horizontal(self, piece, i, j) -> bool:
        count: int = 0
        coord: int = j
        while coord >= 0 and self.board[i][coord] == piece:
            count += 1
            coord -= 1

        coord = j + 1
        while coord < len(self.board) and self.board[i][coord] == piece:
            count += 1
            coord += 1

        return count >= self.win_size

    def check_diagonal1(self, piece, i, j) -> bool:
        count: int = 0
        x_coord: int = i
        y_coord: int = j
        while x_coord >= 0 and y_coord >= 0 and self.board[x_coord][y_coord] == piece:
            count += 1
            x_coord -= 1
            y_coord -= 1

        x_coord = i + 1
        y_coord = j + 1
        while x_coord < len(self.board) and y_coord < len(self.board) and self.board[x_coord][y_coord] == piece:
            count += 1
            x_coord += 1
            y_coord += 1

        return count >= self.win_size

    def check_diagonal2(self, piece, i, j) -> bool:
        count: int = 0
        x_coord: int = i
        y_coord: int = j
        while x_coord >= 0 and y_coord < len(self.board[i]) and self.board[x_coord][y_coord] == piece:
            count += 1
            x_coord -= 1
            y_coord += 1

        x_coord = i + 1
        y_coord = i + 1
        while x_coord < len(self.board[i]) and y_coord >= 0 and self.board[x_coord][y_coord] == piece:
            count += 1
            x_coord += 1
            y_coord -= 1

        return count >= self.win_size

    def format_output(self):
        result = '｜　｜'
        for i in range(0, self.board_size):
            num = self.position_j_f[i]
            result += num + '｜'

        result += '\n'

        for i in range(0, self.board_size):
            char = self.position_i_f[i]
            result += '｜' + char + '｜'
            for j in range(0, self.board_size):
                sig = '　'
                if self.board[i][j] == 1:
                    sig = 'Ｏ'
                elif self.board[i][j] == 2:
                    sig = 'Ｘ'

                result += sig + '｜'

            result += '\n'

        return result
