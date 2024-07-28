from jawsSpeak import speak
from game import MineSweeperGUI
import tkinter as tk
from pathlib import Path

class StartScreen:
    def __init__(self, master):
        self.__master = master
        self.__master.title("Accessible Minesweeper: Start")
        self.frame = tk.Frame(self.__master)
        self.frame.pack(fill="both", expand=True)
        self.__rows = 0
        self.__cols = 0
        self.__num_mines = 0
        self.__options = ["Easy", "Medium", "Hard", "Load Saved Game"]
        self.__current_option = 0
        self._saved_game_file_path= ""
        self.frame.bind("<Up>", self.moveUp)
        self.frame.bind("<Down>", self.moveDown)
        self.frame.bind("<Return>", self.onEnter)
        self.frame.focus_set()
        speak("Welcome to an accessible version of the Minesweeper game. This is a game in progress. More features are coming soon. Select an option:\n" + self.__options[self.__current_option])
    def __speakOption(self):
        speak(self.__options[self.__current_option])
    def moveUp(self, event):
        if self.__current_option > 0:
            self.__current_option -= 1
        self.__speakOption()
    def moveDown(self, event):
        if self.__current_option < len(self.__options) - 1:
            self.__current_option += 1
        self.__speakOption()
    def __initializeGameWindow(self):
        self.frame.pack_forget()
        MineSweeperGUI(self.__master, self.__rows, self.__cols, self.__num_mines)
    def onEnter(self, event):
        if self.__current_option == 0:
            self.__rows = 9
            self.__cols = 9
            self.__num_mines = 10
            self.__initializeGameWindow()
        elif self.__current_option == 1:
            self.__rows = 16
            self.__cols = 16
            self.__num_mines = 40
            self.__initializeGameWindow()
        elif self.__current_option == 2:
            self.__rows = 16
            self.__cols = 30
            self.__num_mines = 99
            self.__initializeGameWindow()
        if self.__current_option == 3:
            self.selectSavedGame()
    def selectSavedGame(self):
        save_dir = Path("../saved_games")
        saved_games = list(save_dir.glob("*.savedgame"))
        if not saved_games:
            speak("No saved games found.")
            return
        self.frame.pack_forget()
        LoadSaveGameScreen(self.__master)

class LoadSaveGameScreen:
    def __init__(self, master):
        self._master = master
        save_dir = Path("../saved_games")
        self._saved_games = list(save_dir.glob("*.savedgame"))
        self._options = [game.stem for game in self._saved_games]
        self._options.append("Cancel")
        self._current_option = 0
        self.frame = tk.Frame(self._master)
        self.frame.pack(fill="both", expand=True)
        self.frame.focus_set()
        self.frame.bind("<Up>", self.moveUp)
        self.frame.bind("<Down>", self.moveDown)
        self.frame.bind("<Return>", self.onSelect)
        speak("Select  a saved Game:")
    def _speakOption(self):
        speak(self._options[self._current_option])
    def moveUp(self, event):
        if self._current_option > 0:
            self._current_option -= 1
        self._speakOption()
    def moveDown(self, event):
        if self._current_option < len(self._options) - 1:
            self._current_option += 1
        self._speakOption()
    def onSelect(self, event):
        if self._options[self._current_option] != "Cancel":
            selected_game = self._saved_games[self._current_option]
            self.frame.pack_forget()
            MineSweeperGUI(self._master, 0, 0, 0, str(selected_game))
        else:
            self.frame.pack_forget()
            StartScreen(self._master)
