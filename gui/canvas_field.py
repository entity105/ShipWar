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

    def click_lkm(self, event):
        cell_x = event.x // self.cell_size  # от 0 до 9
        cell_y = event.y // self.cell_size  # от 0 до 9

        if 0 <= cell_x < 10 and 0 <= cell_y < 10:
            self.battle_ship_obj.shot(cell_x, cell_y, self.field_data)
            self.canvas.delete("all")
            self.draw_pole()

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
        # self.field_data.set_ship()
        self.show_ships = True
        if begin:
            self.canvas.place(x=100, y=40)
        else:
            self.canvas.place(x=60, y=80)


class BattlefieldComputer(BattlefieldCanvas):
    def __init__(self, parent, size=500):
        super().__init__(parent, size)
        self.field_data.init()
        self.matrix = self.field_data.pole
        self.show_ships = False
        self.canvas.place(x=200+size, y=80)

        self.canvas.bind('<Button-1>', self.click_lkm)


