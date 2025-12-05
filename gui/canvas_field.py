import tkinter as tk
from backend.gamepole import GamePole

class BattlefieldCanvas:                # Добавить начальные координаты 2-х канвасов
    def __init__(self, parent: tk.Tk, size=500):
        self.field_data = GamePole(10)
        self.cell_count = self.field_data.size
        self.cell_size = size // self.cell_count

        self.canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            bg='#ADD8E6'
        )

    def __call__(self, *args, **kwargs):
        return self.canvas

    def make_cell(self, x0, y0, state):
        x, y = x0 + self.cell_size, y0 + self.cell_size     # Конечные координаты клеточки

        # Цвета для разных состояний
        colors = {
            0: '#ADD8E6',  # вода
            1: '#696969',  # корабль (если показываем)
            2: '#FF0000',  # попадание
            3: '#FFFFFF',  # промах
        }

        self().create_rectangle(
            x0, y0, x, y,
            outline='#2C5282',  # ГРАНИЦА
            width=2,
            fill=colors.get(state)
        )

    def draw_pole(self):
        dx = dy = 0
        size = self.cell_size
        matrix_data = self.field_data.get_pole()
        for i in range(self.cell_count):
            for j in range(self.cell_count):
                self.make_cell(0 + dx, 0 + dy, matrix_data[j][i])
                dx += size
            dx = 0
            dy += size


class BattlefieldPlayer(BattlefieldCanvas):
    def __init__(self, parent, size=500):
        super().__init__(parent, size)
        self.set_ship()
        self.show_ships = True

    def set_ship(self):
        """Самостоятельная расстановка"""
        pass


class BattlefieldComputer(BattlefieldCanvas):
    def __init__(self, parent, size=500):
        super().__init__(parent, size)
        self.field_data.init()
        self.show_ships = False


