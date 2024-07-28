import random
from datetime import datetime
from pathlib import Path
import base64

class Tile:
    def __init__(self):
        self.is_reveal = False
        self.is_mine = False
        self.mine_count = 0
        self.flag_state = False

class Board:
    def __init__(self, rows, cols, num_mines, file_name=""):
        self.__rows = rows
        self.__cols = cols
        self.__num_mines = num_mines
        self.__tiles = []
        self.__directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        if not file_name:
            self.__initializeBoard()
        else:
            self.loadBoardFromFile(file_name)
        self.__randomizeMines()
        self.__findAdjacentTiles()
    def __initializeBoard(self):
        for row in range(self.__rows):
            tile_row = []
            for col in range(self.__cols):
                tile = Tile()
                tile_row.append(tile)
            self.__tiles.append(tile_row)
    def __randomizeMines(self):
        mines_placed = 0
        while mines_placed < self.__num_mines:
            random_row = random.randint(0, self.__rows - 1)
            random_col = random.randint(0, self.__cols - 1)
            if self.__tiles[random_row][random_col].is_mine == False:
                self.__tiles[random_row][random_col].is_mine = True
                mines_placed += 1
    def __findAdjacentTiles(self):
        for row in range(self.__rows):
            for col in range(self.__cols):
                for direction in self.__directions:
                    next_row = row + direction[0]
                    next_col = col + direction[1]
                    if 0 <= next_row < self.__rows and 0 <= next_col < self.__cols:
                        if self.__tiles[next_row][next_col].is_mine == True:
                            self.__tiles[row][col].mine_count += 1
    def revealTile(self, row: int, col: int):
        if self.__tiles[row][col].is_reveal:
            return
        self.__tiles[row][col].is_reveal = True
        if not self.__tiles[row][col].mine_count:
            for direction in self.__directions:
                next_row = row + direction[0]
                next_col = col + direction[1]
                if 0 <= next_row < self.__rows and 0 <= next_col < self.__cols:
                    self.revealTile(next_row, next_col)
    def toggleFlagState(self, row: int, col: int):
        self.__tiles[row][col].flag_state = not self.__tiles[row][col].flag_state
    def checkGameState(self):
        game_won = True
        game_lost = False
        for row in range(self.__rows):
            for col in range(self.__cols):
                tile = self.__tiles[row][col]
                if not tile.is_reveal and not tile.is_mine:
                    game_won = False
                if tile.is_reveal and tile.is_mine:
                    game_lost = True
        if game_won:
            return "won"
        elif game_lost:
            return "lost"
        else:
            return "ongoing"
    def resetBoard(self):
        self.__tiles.clear()
        self.__initializeBoard()
        self.__randomizeMines()
        self.__findAdjacentTiles()
    def getTile(self, row: int, col: int):
        return self.__tiles[row][col]
    def getRows(self):
        return self.__rows
    def getCols(self):
        return self.__cols
    def saveBoard(self):
        result_string = ""
        current_date_time = datetime.now()
        formatted_time = current_date_time.strftime('%Y-%m-%d-%H-%M-%S')
        relative_path = Path("../saved_games")
        output_file = relative_path / f"{formatted_time}.savedgame"
        relative_path.mkdir(parents=True, exist_ok=True)
        result_string += f"{self.__rows},{self.__cols}\n"
        for row in range(self.__rows):
            for col in range(self.__cols):
                tile = self.__tiles[row][col]
                result_string += f"{row},{col},{tile.is_mine},{tile.is_reveal},{tile.flag_state},{tile.mine_count}\n"
        encoded_bites = base64.b64encode(result_string.encode("utf-8"))
        with open(output_file, 'wb') as file:
            file.write(encoded_bites)
    def loadBoardFromFile(self, file_name):
        with open(file_name, 'rb') as file:
            encoded_data = file.read()
        decoded_string = base64.b64decode(encoded_data).decode("utf-8")
        lines = decoded_string.strip().split("\n")
        rows, cols = map(int, lines[0].split(","))
        self.__rows = rows
        self.__cols = cols
        self.__initializeBoard()
        for line in lines[1:]:
            row, col, is_mine, is_reveal, flag_state, mine_count = line.split(",")
            row, col = int(row), int(col)
            is_mine = is_mine == "True"
            is_reveal = is_reveal == "True"
            flag_state = flag_state == "True"
            mine_count = int(mine_count)
            tile = self.__tiles[row][col]
            tile.is_mine = is_mine
            tile.is_reveal = is_reveal
            tile.flag_state = flag_state
            tile.mine_count = mine_count
