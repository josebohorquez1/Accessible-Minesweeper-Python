import tkinter as tk
from StartScreen import StartScreen
from jawsSpeak import speak
from game import MineSweeperGUI

def main():
    root = tk.Tk()
    start_screen = StartScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()