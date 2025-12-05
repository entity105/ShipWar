import tkinter as tk
from backend.ship import Ship

class GameWindow:
    def __init__(self):
        self.CELL_COUNT = 10
        self.SIZE_POLE_PIX = 500
        self.colors = {
            "sea": '#449ac1'
        }

        self.win = tk.Tk()
        self.win.geometry('1980x920')

        x0, y0 = 50, 80
        dx = 120
        self.pole_1 = self.create_canvas()
        self.pole_1.place(x=x0, y=y0)
        self.pole_2 = self.create_canvas()
        self.pole_2.place(x=x0+self.SIZE_POLE_PIX+dx, y=y0)

        self.cells_pole(self.pole_1)
        self.cells_pole(self.pole_2)

        s = Ship(3, 1, 5, 6)
        self.draw_ship(s, self.pole_1)

        self.win.mainloop()  # ⬅️ Теперь корабль нарисован

    def create_canvas(self):        # Рисуем поле
        return tk.Canvas(
            self.win,
            height=self.SIZE_POLE_PIX,
            width=self.SIZE_POLE_PIX,
            bg='#449ac1',  # синий фон моря
            highlightthickness=1,  # тонкая рамка 1px
            highlightbackground='#2c5282',  # темно-синяя рамка
            highlightcolor='#2c5282',  # тот же цвет при фокусе
            takefocus=False  # не получает фокус клавиатуры
        )

    def cells_pole(self, canvas: tk.Canvas):        # Делаем сетку
        cell_count = self.CELL_COUNT
        size = self.SIZE_POLE_PIX
        cell_size = size // cell_count
        dx = dy = 0
        for _ in range(cell_count):
            canvas.create_line(0 + dx, 0, 0 + dx, size, width=1)
            canvas.create_line(0, 0 + dy, size, 0 + dy, width=1)
            dx += cell_size
            dy += cell_size

    def draw_ship(self, ship: Ship, pole: tk.Canvas):
        size_cell = self.SIZE_POLE_PIX // self.CELL_COUNT
        coords = ship.get_cords()
        for coord in list(coords):
            x0, y0 = coord
            pole.create_rectangle(x0 * 50, y0 * 50, x0 * 50 + 50, y0 * 50 + 50,
                                  activefill='#666666', disabledfill='red', width=4)



# s = Ship(3, 1, 5, 6)
a = GameWindow()
# a.draw_ship(s, a.pole_1)
# a.win.mainloop()