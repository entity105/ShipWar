import tkinter as tk
from gui.canvas_field import BattlefieldPlayer, BattlefieldComputer


class GameWindow:
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('1980x920')

        self.player_field = BattlefieldPlayer(self.win)
        self.computer_field = BattlefieldComputer(self.win)
        self.computer_field.draw_pole()
        self.win.mainloop()

    def run(self):
        self.win.mainloop()


a = GameWindow()
