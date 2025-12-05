import tkinter as tk

class GameWindow:
    def __init__(self):
        self.SIZE = 10
        win = tk.Tk()
        win.geometry('1980x920')

        size = 10
        size_pix = 600
        canv_x, canv_y = 30, 60
        line_x_0, line_y_0 = 0, 0
        line_x, line_y = 0, size_pix

        pole_1 = tk.Canvas(
            win,
            height=size_pix,
            width=size_pix,
            bg='#449ac1',  # синий фон моря
            highlightthickness=1,  # тонкая рамка 1px
            highlightbackground='#2c5282',  # темно-синяя рамка
            highlightcolor='#2c5282',  # тот же цвет при фокусе
            takefocus=False  # не получает фокус клавиатуры
        )
        pole_1.place(x=canv_x, y=canv_y)

        dx = size_pix // 10
        for _ in range(size):
            pole_1.create_line(line_x_0, line_y_0 + 3, line_x, line_y + 10, width=1)
            line_x += dx
            line_x_0 += dx              

        win.mainloop()

    def cells_pole(self, canvas: tk.Canvas):
        size_cell = self.SIZE
        size = canvas.winfo_width()
        cell_size = size // size_cell
        dx = dy = 0
        for _ in range(size_cell):
            canvas.create_line(0, 0, 0, size, width=1)




a = GameWindow()