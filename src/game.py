import tkinter as tk
from Board import Board
from jawsSpeak import speak

class MineSweeperGUI:
    def __init__(self, master, rows, cols, num_mines, file_name=""):
        self.master = master
        self.master.title("Accessible Minesweeper: Game")
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.frame.focus_set()
        self.current_row = 0
        self.current_col = 0
        self.board = Board(rows=rows, cols=cols, num_mines=num_mines, file_name=file_name)
        self.rows = self.board.getRows()
        self.cols = self.board.getCols()
        self.frame.bind("<Left>", self.moveLeft)
        self.frame.bind("<Right>", self.moveRight)
        self.frame.bind("<Up>", self.moveUp)
        self.frame.bind("<Down>", self.moveDown)
        self.frame.bind("<Return>", self.onEnter)
        self.frame.bind("<space>", self.onSpace)
        self.frame.bind("<Control-s>", self.onSave)
        speak("The game has just started. There are " + str(self.board.getRows()) + " rows, and " + str(self.board.getCols()) + " columns. To move around the board, use the arrow keys. To reveal a tile, press the enter key. To set and remove a flag, press the space key. Press Control S to save the game.")
    def reportPosition(self):
        text = ""
        if not self.board.getTile(self.current_row, self.current_col).is_reveal:
            if self.board.getTile(self.current_row, self.current_col).flag_state:
                text = "(" + str(self.current_row) + ", " + str(self.current_col) + "), hidden, has flag"
            else:
                text = "(" + str(self.current_row) + ", " + str(self.current_col) + "), hidden"
        else:
            if not self.board.getTile(self.current_row, self.current_col).is_mine:
                text = "(" + str(self.current_row) + ", " + str(self.current_col) + "), revealed, " + str(self.board.getTile(self.current_row, self.current_col).mine_count) + " mines nearby"
            else:
                text = "Oh no, that's a mine."
        speak(text)
    def moveLeft(self, event):
        if self.current_col > 0:
            self.current_col -= 1
        self.reportPosition()
    def moveRight(self, event):
        if self.current_col < self.board.getCols() - 1:
            self.current_col += 1
        self.reportPosition()
    def moveUp(self, event):
        if self.current_row > 0:
            self.current_row -= 1
        self.reportPosition()
    def moveDown(self, event):
        if self.current_row < self.board.getRows() - 1:
            self.current_row += 1
        self.reportPosition()
    def onEnter(self, event):
        self.board.revealTile(self.current_row, self.current_col)
        game_state = self.board.checkGameState()
        self.reportPosition()
        if game_state == "won":
            speak("Congratulations, you have successfully avoided all mines.")
            self.frame.unbind("<Return>")
        if game_state == "lost":
            speak("A mine has just exploded. You have lost the game.")
            self.frame.unbind("<Return>")
        if game_state == "ongoing":
            self.reportPosition()
    def onSpace(self, event):
        self.board.toggleFlagState(self.current_row, self.current_col)
        self.reportPosition()
    def onSave(self, event):
        self.board.saveBoard()
        speak("Game saved.")
