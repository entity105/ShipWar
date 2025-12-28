import tkinter as tk
from tkinter import ttk
from backend.gamepole import GamePole
from backend.gameplay import BattleShip

class BattlefieldCanvas:
    def __init__(self, parent: tk.Tk, size=500):
        self.parent = parent
        self.count = 0      # Для отображения счёта
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

    def create_coordinate_system(self, canvas_x, canvas_y, cell_size, field_size=500):
        cell_size = cell_size
        field_size = field_size

        # БУКВЫ для вертикальной оси
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']

        # БУКВЫ СЛЕВА от поля
        for i, letter in enumerate(letters):
            label_y = canvas_y + i * cell_size + cell_size // 2

            tk.Label(self.parent,  # или self.win - главное окно
                     text=letter,
                     font=("Arial", 12, "bold"),
                     bg='SystemButtonFace',  # цвет фона как у окна
                     width=2,
                     height=1).place(x=canvas_x - 35,  # слева от Canvas
                                     y=label_y - 10)  # выравниваем по центру клетки

        # ЦИФРЫ ПОД полем
        for i in range(1, 11):
            label_x = canvas_x + (i - 1) * cell_size + cell_size // 2

            tk.Label(self.parent,
                     text=str(i),
                     font=("Arial", 12, "bold"),
                     bg='SystemButtonFace',
                     width=2,
                     height=1).place(x=label_x - 10,
                                     y=canvas_y + field_size + 15)

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

    def destroyed_ships(self) -> int:       # Возвращает количество уничтоженных кораблей
        ships = self.field_data.get_ships()
        n = 0
        self.count = 0
        for ship in ships:
            if ship.is_destroyed():
                n += 1
                self.count += 1
        return n

    def show_game_result(self, player_won):
        """Показывает окно с результатом игры"""

        if player_won:
            title = "🎉 ПОБЕДА!"
            message = "Вы уничтожили все корабли противника!"
            color = "#4CAF50"  # шрифт - Зелёный
        else:
            title = "💀 ПОРАЖЕНИЕ"
            message = "Все ваши корабли потоплены!"
            color = "#F44336"  # Красный

        # координаты для центрирования
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        result_window = tk.Toplevel(self.parent)
        result_window.title("Игра окончена")
        result_window.geometry(f"400x300+{x}+{y}")
        result_window.resizable(False, False)

        result_window.transient(self.parent)  # Поверх главного окна
        result_window.grab_set()

        # Заголовок
        title_label = ttk.Label(result_window, text=title,
                                font=("Arial", 24, "bold"),
                                foreground=color)
        title_label.pack(pady=20)

        # Сообщение
        msg_label = ttk.Label(result_window, text=message,
                              font=("Arial", 14))
        msg_label.pack(pady=10)

        # Мб время игры, кол-во выстрелов
        # stats_frame = ttk.Frame(result_window)
        # stats_frame.pack(pady=20)
        #
        # ttk.Label(stats_frame, text=f"Ваши попадания: {self.player_hits}").grid(row=0, column=0, padx=10)
        # ttk.Label(stats_frame, text=f"Попадания противника: {self.computer_hits}").grid(row=0, column=1, padx=10)

        # кнопки действий
        button_frame = ttk.Frame(result_window)
        button_frame.pack(pady=30)

        # Кнопка "Новая игра"
        ttk.Button(button_frame, text="🔄 Новая игра",
                   command=lambda: [self.close_windows(), self.new_game_after()],
                   width=15).pack(side=tk.LEFT, padx=10)

        # Кнопка "Выход"
        ttk.Button(button_frame, text="🚪 Выход",
                   command=self.close_windows,
                   width=15).pack(side=tk.LEFT, padx=10)

    def new_game_after(self):
        from gui.tkinter_game import PredGame
        n_g = PredGame()
        self.parent = n_g.win

    def close_windows(self):    # уничтожаем все открытые окна
        return [win.destroy() for win in self.parent.winfo_children()] + [self.parent.destroy()]


class BattlefieldPlayer(BattlefieldCanvas):
    def __init__(self, parent, size=500, begin=True):
        super().__init__(parent, size)
        self.computer = None     # объект BattlefieldComputer
        # self.field_data.set_ship()
        self.show_ships = True
        if begin:
            self.canvas.place(x=100, y=40)
            self.create_coordinate_system(100, 40, 65, 650)
        else:
            self.canvas.place(x=60, y=80)
            self.create_coordinate_system(60, 80, 50)
            self.score_label = tk.Label(
                self.parent,
                text=f"Количество поражённых кораблей: {self.count}/10",
                font=("Arial", 22),
                bd=3,
                bg="#e56e61",
                relief="ridge",
                padx=5, pady=3
            )
            self.score_label.place(x=60, y=720)

            self.computer_label = tk.Label(
                self.parent,
                text="You",
                font=("Arial", 30),
                bg="#def6f7", fg="#481d19"
            )
            self.computer_label.place(x=300, y=25)

    def computer_shot(self):
        self.field_data.pole = self.matrix
        self.battle_ship_obj.autoshot(self.field_data)   # Делает все выстрелы (хотя бы 1 при промахе)
        self.destroyed_ships()
        self.score_label.config(text=f"Количество поражённых кораблей: {self.count}/10")
        if self.count == 10:  # Если поле игрока уничтожено => поражение
            self.computer.disable_clicks()
            self.parent.after(100, self.show_game_result, False)
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
        self.create_coordinate_system(200+size, 80, 50)

        self.cell_x = self.cell_y = None

        self.click_binding = self.canvas.bind('<Button-1>', self.click_lkm)

        self.score_label = tk.Label(
            self.parent,
            text=f"Количество уничтоженных кораблей: {self.count}/10",
            font=("Arial", 22),
            bd=3,
            bg="lightgreen",
            relief="ridge",
            padx=5, pady=3
        )
        self.score_label.place(x=60, y=640)

        self.computer_label = tk.Label(
            self.parent,
            text="Enemy",
            font=("Arial", 30),
            bg="#def6f7", fg="#481d19"
        )
        self.computer_label.place(x=900, y=25)

    def click_lkm(self, event):
        # print('Игрок стреляет')
        self.cell_x = event.x // self.cell_size  # от 0 до 9
        self.cell_y = event.y // self.cell_size  # от 0 до 9

        if 0 <= self.cell_x < 10 and 0 <= self.cell_y < 10:
            self.res = self.battle_ship_obj.shot(self.cell_x, self.cell_y, self.field_data)
            self.canvas.delete("all")
            self.draw_pole()
        self.processing_move()

    def is_hit(self):
        if self.res == 1:   # Промах
            return False
        elif self.res == 2:     # Попали
            self.destroyed_ships()
            self.score_label.config(text=f"Количество уничтоженных кораблей: {self.count}/10")
            return True
        elif not self.res:      # Попытка стрельнуть в закрытую клетку
            return True

    def processing_move(self):   # Обработка хода (что делать дальше)
        if self.is_hit():  # Если попали или стрельнули в закрытую клетку
            if self.count == 10:    # Если поле бота уничтожено => победа
                self.disable_clicks()
                self.parent.after(100, self.show_game_result, True)
            return
        # Если промах
        self.disable_clicks()       # Отключаем у нас клики (на поле бота)
        self.parent.after(500, self.player.computer_shot)  # Бот стреляет

    def disable_clicks(self):
        """Отключить клики"""
        if self.click_binding:
            self.canvas.unbind('<Button-1>', self.click_binding)
            self.click_binding = None

    def enable_clicks(self):
        """Включить клики"""
        if not self.click_binding:
            self.click_binding = self.canvas.bind('<Button-1>', self.click_lkm)