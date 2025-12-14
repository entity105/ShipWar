import tkinter as tk

from backend.gameplay import BattleShip
# from tkinter import ttk
from gui.canvas_field import BattlefieldPlayer, BattlefieldComputer
from abc import abstractmethod
from random import choice


class BaseWindow:
    def __init__(self):
        self.win = tk.Tk()
        self.win_place()
        self.win_init()
        self.win.mainloop()

    @abstractmethod
    def win_place(self):
        """Расположение и размеры окна"""
        pass

    @abstractmethod
    def win_init(self):
        """Наполнение окна"""
        pass


class MenuWindow(BaseWindow):
    def __init__(self):
        super().__init__()

    def win_place(self):
        self.win.geometry('720x700+360+80')
        self.win.config(bg='#b0f3f7')

    def win_init(self):
        """Наполнение окна"""
        style = {
            "fg": "navy",
            "bg": "lightblue",
            "relief": "raised",
            "bd": 2,
            "activebackground": 'red'
        }

        tk.Label(self.win, text="МЕНЮ", **style, font=("Impact", 36),
                 padx=30, pady=15).pack(pady=(100, 100))

        tk.Button(self.win, text="Новая игра", **style, font=("Impact", 24),
                  padx=30, command=self.new_game).pack()

        tk.Button(self.win, text="Выход", **style, font=("Impact", 24),
                  padx=40, command=self.win.quit).pack()

        # Мб добавить ссылку на тг

    def new_game(self):
        self.win.destroy()
        new_win = PredGame()
        self.win = new_win.win


class PredGame(BaseWindow):
    def __init__(self):
        self.player_field = None
        super().__init__()

        self.data_save = None

    def win_place(self):
        self.win.geometry('1980x920')
        self.win.config(bg='#c5d8e7')

    def win_init(self):
        self.player_field = BattlefieldPlayer(self.win, size=650)
        self.player_field.draw_pole()
        tk.Button(self.win, text="В бой!", command=self.start_game,     # Кнопка начала игры
                 padx=30, pady=10, font=("Impact", 50),
                 bg='#21ed32', bd=5, fg='#191f8f', relief="raised",
                 activebackground='red').pack(padx=(1190, 10), pady=(610, 5))

        tk.Button(self.win, text="Назад", command=self.back,     # Кнопка вернуться
                 padx=10, pady=5, font=("Impact", 20),
                 bg='#cecfee', bd=5, fg='#191f8f',
                 activebackground='red').place(x=1090, y=702)

        tk.Button(self.win, text="Авто", command=self.auto,     # Авторасстановка
                 padx=15, pady=3, font=("Impact", 20),
                 bg='#cecfee', bd=5, fg='#191f8f',
                 activebackground='#439ae5').place(x=780, y=45)
        # Перетаскивание

    def auto(self):
        self.player_field.field_data.init()
        self.data_save = self.player_field.field_data.pole, self.player_field.field_data.get_ships()  # Сохраняем матрицу и список кораблей
        self.player_field.matrix = self.data_save[0]
        self.player_field.canvas.delete("all")
        self.player_field.draw_pole()

    def back(self):
        self.win.destroy()
        game = MenuWindow()
        self.win = game.win

    def start_game(self):
        self.win.destroy()
        game = GameWindow(*self.data_save)
        self.win = game.win


class GameWindow(BaseWindow):
    def __init__(self, matrix_player, ships_list):
        self.player_field = self.computer_field = None
        self.matrix_player = matrix_player
        self.ships = ships_list
        super().__init__()
        # self.win = tk.Tk()
        # self.win_place()
        # self.win_init()
        # self.win.mainloop()


    def win_place(self):
        self.win.geometry('1980x920')

    def win_init(self):
        self.player_field = BattlefieldPlayer(self.win, begin=False)
        self.computer_field = BattlefieldComputer(self.win)

        self.player_field.computer = self.computer_field
        self.computer_field.player = self.player_field

        self.player_field.matrix = self.matrix_player
        self.player_field.field_data.set_ships(self.ships)
        print(f'win_init {self.player_field.matrix}')
        print(f'win_init {self.player_field.field_data.get_ships()}')
        self.player_field.draw_pole()
        self.computer_field.draw_pole()


    # def game(self):




    def run(self):
        self.win.mainloop()


a = MenuWindow()

# Нужно сделать:
# 1) start_game
# 2) отображение/скрытие кораблей на поле - ВЫПОЛНЕНО