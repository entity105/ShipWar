import tkinter as tk
from backend.gamepole import GamePole
from backend.gameplay import BattleShip

class BattlefieldCanvas:
    def __init__(self, parent, size=500):
        self.parent = parent
        self.battle_ship_obj = BattleShip(GamePole(10))       # Объект BattleShip. По сути тот же GamePole, но с дополнительными методами
        self.field_data = self.battle_ship_obj.pole_obj_1     # Взяли объект GamePole
        self.matrix = self.field_data.pole                    # Взяли матрицу из GamePole

        self.cell_count = self.field_data.size
        self.cell_size = size // self.cell_count

        self.canvas = tk.Canvas(
            self.parent,
            width=size,
            height=size,
            bg='#ADD8E6'
        )

        self.show_ships = None

    def make_cell(self, x0, y0, state):
        x, y = x0 + self.cell_size, y0 + self.cell_size     # Конечные координаты клеточки

        # Цвета для разных состояний
        colors = {
            0: '#ADD8E6',  # вода
            1: '#696969',  # корабль (если показываем)
            2: '#FF0000',  # попадание
            3: '#FFFFFF',  # промах
        }

        if not self.show_ships:
            colors[1] = colors[0]

        self.canvas.create_rectangle(
            x0, y0, x, y,
            outline='#2C5282',  # ГРАНИЦА
            width=2,
            fill=colors.get(state)
        )

    def draw_pole(self):
        dx = dy = 0
        size = self.cell_size
        matrix_data = self.matrix
        for i in range(self.cell_count):
            for j in range(self.cell_count):
                self.make_cell(0 + dx, 0 + dy, matrix_data[i][j])
                dx += size
            dx = 0
            dy += size


class BattlefieldPlayer(BattlefieldCanvas):
    def __init__(self, parent, size=500, begin=True):
        super().__init__(parent, size)
        self.computer = None     # объект BattlefieldComputer
        # self.field_data.set_ship()
        self.show_ships = True
        if begin:
            self.canvas.place(x=100, y=40)
        else:
            self.canvas.place(x=60, y=80)

    def computer_shot(self):
        self.field_data.pole = self.matrix
        print(self.field_data.pole)
        self.battle_ship_obj.autoshot(self.field_data)   # Делает все выстрелы
        print(self.field_data.pole)
        self.canvas.delete("all")
        self.draw_pole()
        self.computer.enable_clicks()


class BattlefieldComputer(BattlefieldCanvas):
    def __init__(self, parent, size=500):
        super().__init__(parent, size)
        self.field_data.init()
        self.player = None    # объект BattlefieldPlayer
        self.matrix = self.field_data.pole
        self.show_ships = False
        self.res = None
        self.canvas.place(x=200+size, y=80)

        self.cell_x = self.cell_y = None

        self.click_binding = self.canvas.bind('<Button-1>', self.click_lkm)

    def click_lkm(self, event):
        self.cell_x = event.x // self.cell_size  # от 0 до 9
        self.cell_y = event.y // self.cell_size  # от 0 до 9

        if 0 <= self.cell_x < 10 and 0 <= self.cell_y < 10:
            self.res = self.battle_ship_obj.shot(self.cell_x, self.cell_y, self.field_data)
            self.canvas.delete("all")
            self.draw_pole()
        self.processing_move()

    def is_hit(self):
        for ship in self.field_data.get_ships():
            if (self.cell_x, self.cell_y) in ship.get_cords():
                return True
        return False

    def processing_move(self):   # Обработка хода (что делать дальше)
        if self.is_hit():  # Если попали
            return
        # Если промах
        self.disable_clicks()       # Отключаем у нас клики (на поле бота)
        self.parent.after(1000, self.player.computer_shot)  # Бот стреляет

    def disable_clicks(self):
        """Отключить клики"""
        if self.click_binding:
            self.canvas.unbind('<Button-1>', self.click_binding)
            self.click_binding = None

    def enable_clicks(self):
        """Включить клики"""
        if not self.click_binding:
            self.click_binding = self.canvas.bind('<Button-1>', self.click_lkm)


