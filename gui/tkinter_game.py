import tkinter as tk
from gui.canvas_field import BattlefieldPlayer, BattlefieldComputer
from backend.ship import Ship
from abc import ABC, abstractmethod


class BaseWindow(ABC):
    def __init__(self):
        self.win = tk.Tk()
        self.win_place()
        self.win_init()
        icon = tk.PhotoImage(file='ship.png')
        self.win.iconphoto(False, icon)

    @abstractmethod
    def win_place(self):
        """Расположение и размеры окна"""
        pass

    @abstractmethod
    def win_init(self):
        """Наполнение окна"""
        pass

    def run(self):
        self.win.mainloop()


class MenuWindow(BaseWindow):
    def __init__(self):
        super().__init__()

    def win_place(self):
        self.win.geometry('720x700+360+80')
        self.win.config(bg='#b0f3f7')
        self.win.title("Морской бой v1.0")

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
        self.ship_placer = None  # ⬅️ Добавляем!
        self.data_save = None
        super().__init__()

    def win_place(self):
        self.win.geometry('1980x920')
        self.win.config(bg='#c5d8e7')
        self.win.title("Размещение кораблей")

    def win_init(self):
        # Создаём поле игрока
        self.player_field = BattlefieldPlayer(self.win, size=650)
        self.player_field.draw_pole()

        # Создаём "установщик" кораблей
        self.ship_placer = ManualShipPlacer(
            game_pole=self.player_field.field_data,
            battlefield_canvas=self.player_field
        )

        # КНОПКИ:

        # 1. "В бой!" (изначально выключена)
        self.start_button = tk.Button(self.win, text="В бой!",
                                      command=self.start_game,
                                      padx=30, pady=10, font=("Impact", 50),
                                      bg='#21ed32', bd=5, fg='#191f8f',
                                      relief="raised", state='disabled')  # ⬅️ DISABLED!
        self.start_button.pack(padx=(1190, 10), pady=(610, 5))

        # Передаём ссылку на кнопку в ship_placer
        self.ship_placer.done_button = self.start_button

        # 2. "Назад"
        tk.Button(self.win, text="Назад", command=self.back,
                  padx=10, pady=5, font=("Impact", 20),
                  bg='#cecfee', bd=5, fg='#191f8f',
                  activebackground='red').place(x=1090, y=702)

        # 3. "Авто" (авторасстановка)
        tk.Button(self.win, text="Авто", command=self.auto,
                  padx=15, pady=3, font=("Impact", 20),
                  bg='#cecfee', bd=5, fg='#191f8f',
                  activebackground='#439ae5').place(x=780, y=45)

        # 4. "Ручная" (опционально - для сброса/повторной ручной)
        tk.Button(self.win, text="Ручная", command=self.manual_reset,
                  padx=15, pady=3, font=("Impact", 20),
                  bg='#cecfee', bd=5, fg='#191f8f',
                  activebackground='#439ae5').place(x=650, y=45)

        # 5. Статусная строка (показывает текущий корабль)
        self.status_label = tk.Label(self.win,
                                     text="Начните расстановку кораблей",
                                     font=("Arial", 16, "bold"),
                                     bg='#c5d8e7',
                                     fg='#191f8f')
        self.status_label.place(x=50, y=20)

        # Передаём ссылку на статусную строку
        self.ship_placer.status_label = self.status_label

        # Подсказки
        tk.Label(self.win,
                 text="ЛКМ - поставить корабль | ПКМ - повернуть | Пробел - повернуть",
                 font=("Arial", 12),
                 bg='#c5d8e7').place(x=50, y=760)

    def auto(self):
        """Автоматическая расстановка"""
        self.player_field.field_data.init()
        self.data_save = (self.player_field.field_data.pole,
                          self.player_field.field_data.get_ships())
        self.player_field.matrix = self.data_save[0]
        self.player_field.canvas.delete("all")
        self.player_field.draw_pole()

        # Включаем кнопку "В бой!"
        self.start_button.config(state='normal', bg='#21ed32')

        # Обновляем статус
        self.status_label.config(text="Корабли расставлены автоматически!")

        # Отключаем ручную расстановку
        if self.ship_placer:
            self.ship_placer.disable()

    def manual_reset(self):
        """Сброс для ручной расстановки"""
        # Очищаем поле
        self.player_field.field_data._ships = []
        self.player_field.matrix = self.player_field.field_data.pole
        self.player_field.canvas.delete("all")
        self.player_field.draw_pole()

        # Выключаем кнопку "В бой!"
        self.start_button.config(state='disabled', bg='gray')

        # Запускаем ручную расстановку
        self.ship_placer.reset_placement()

        # Обновляем статус
        self.status_label.config(text="Расставьте корабли вручную")

    def back(self):
        self.win.destroy()
        game = MenuWindow()
        self.win = game.win

    def start_game(self):
        """Начинаем игру с расставленными кораблями"""
        # Сохраняем данные
        self.data_save = (self.player_field.field_data.pole,
                          self.player_field.field_data.get_ships())

        # Переходим к игре
        self.win.destroy()
        game = GameWindow(*self.data_save)
        self.win = game.win


class GameWindow(BaseWindow):
    def __init__(self, matrix_player, ships_list):
        self.player_field = self.computer_field = None
        self.matrix_player = matrix_player
        self.ships = ships_list
        self.exit = None
        super().__init__()
        # self.win = tk.Tk()
        # self.win_place()
        # self.win_init()

    def win_place(self):
        self.win.geometry('1980x920')

    def win_init(self):
        self.player_field = BattlefieldPlayer(self.win, begin=False)
        self.computer_field = BattlefieldComputer(self.win)

        self.player_field.computer = self.computer_field
        self.computer_field.player = self.player_field

        self.player_field.matrix = self.matrix_player
        self.player_field.field_data.set_ships(self.ships)
        self.player_field.draw_pole()
        self.computer_field.draw_pole()

        self.win.config(background='#def6f7')
        self.win.title("Игра")

        tk.Button(self.win, text="Выход", font=("Arial", 22), command=self.close_windows).place(x=1400, y=730)

    def close_windows(self):    # уничтожаем все открытые окна
        return [win.destroy() for win in self.win.winfo_children()] + [self.win.destroy()]


class ManualShipPlacer:
    def __init__(self, game_pole, battlefield_canvas):
        self.game_pole = game_pole
        self.canvas = battlefield_canvas.canvas
        self.done_button = None  # Будет установлено из PredGame
        self.status_label = None  # Будет установлено из PredGame

        # Создаём очередь кораблей
        self.ships_queue = self._create_ships_queue()
        self.current_ship = None
        self.orientation = 1
        self.ghost_id = None

        # Привязываем события к Canvas
        self._bind_events()

        # Начинаем с первого корабля
        self._start_next_ship()

    def _create_ships_queue(self):
        """Очередь кораблей: 1x4, 2x3, 3x2, 4x1"""
        return [4] + [3] * 2 + [2] * 3 + [1] * 4

    def _bind_events(self):
        """Привязка событий мыши"""
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<Motion>', self._on_mouse_move)
        self.canvas.bind('<Button-3>', self._rotate_ship)
        self.canvas.bind('<space>', self._rotate_ship)

    def _on_click(self, event):
        """Обработка клика для установки корабля"""
        if not self.current_ship:
            return

        # Координаты мыши → координаты клетки
        cell_x = event.x // self.canvas.cell_size
        cell_y = event.y // self.canvas.cell_size

        # Проверка границ
        if not (0 <= cell_x < 10 and 0 <= cell_y < 10):
            return

        # Пытаемся поставить корабль
        if self._try_place_ship(cell_x, cell_y):
            self._start_next_ship()

    def _try_place_ship(self, x, y):
        """Попытка установки корабля"""
        # Используем твои существующие методы Ship и GamePole
        temp_ship = Ship(
            length=self.current_ship,
            tp=self.orientation,
            x=x + 1,
            y=y + 1
        )

        # Проверка валидности (используй свои методы)
        if temp_ship.is_out_pole(10):
            return False

        # Проверка столкновений с уже поставленными кораблями
        for existing in self.game_pole._ships:
            if temp_ship.is_collide(existing):
                return False

        # Если всё ок - создаём настоящий корабль
        real_ship = Ship(
            length=self.current_ship,
            tp=self.orientation,
            x=x + 1,
            y=y + 1
        )

        # Добавляем в GamePole
        self.game_pole._ships.append(real_ship)

        # Обновляем отображение
        self.canvas.draw_pole()

        return True

    def _on_mouse_move(self, event):
        """Рисуем призрак корабля при движении мыши"""
        cell_x = event.x // self.canvas.cell_size
        cell_y = event.y // self.canvas.cell_size

        # Удаляем старый призрак
        if self.ghost_id:
            self.canvas.canvas.delete(self.ghost_id)

        # Рисуем новый призрак если позиция валидна
        if self._is_valid_position(cell_x, cell_y):
            color = 'lightgreen'
        else:
            color = 'lightcoral'

        self.ghost_id = self._draw_ghost(cell_x, cell_y, color)

    def _draw_ghost(self, x, y, color):
        """Рисует полупрозрачный призрак"""
        cell_size = self.canvas.cell_size

        if self.orientation == 1:  # Горизонтальный
            x1 = x * cell_size
            y1 = y * cell_size
            x2 = (x + self.current_ship) * cell_size
            y2 = y1 + cell_size
        else:  # Вертикальный
            x1 = x * cell_size
            y1 = y * cell_size
            x2 = x1 + cell_size
            y2 = (y + self.current_ship) * cell_size

        return self.canvas.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            stipple='gray50',
            outline='black',
            width=1
        )

    def _is_valid_position(self, x, y):
        """Быстрая проверка валидности позиции"""
        if not self.current_ship:
            return False

        # Простая проверка границ
        if self.orientation == 1:  # Горизонтальный
            if x + self.current_ship > 10:
                return False
        else:  # Вертикальный
            if y + self.current_ship > 10:
                return False

        return True

    def _start_next_ship(self):
        """Начинаем следующий корабль"""
        if not self.ships_queue:
            # Все корабли расставлены
            self._on_complete()
            return

        self.current_ship = self.ships_queue.pop(0)
        self.orientation = 1

        # Обновляем статус
        if self.status_label:
            ship_names = {1: "однопалубный", 2: "двухпалубный",
                          3: "трёхпалубный", 4: "четырёхпалубный"}
            self.status_label.config(
                text=f"Установите {ship_names[self.current_ship]} корабль"
            )

    def _rotate_ship(self, event):
        """Поворот корабля"""
        self.orientation = 2 if self.orientation == 1 else 1

    def _on_complete(self):
        """Все корабли расставлены"""
        # Отключаем события
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Motion>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<space>')

        # Удаляем призрак
        if self.ghost_id:
            self.canvas.canvas.delete(self.ghost_id)

        # Включаем кнопку "В бой!"
        if self.done_button:
            self.done_button.config(state='normal', bg='#21ed32')

        # Обновляем статус
        if self.status_label:
            self.status_label.config(text="Все корабли расставлены!")

    def reset_placement(self):
        """Сброс расстановки"""
        # Очищаем корабли
        self.game_pole._ships = []

        # Сбрасываем очередь
        self.ships_queue = self._create_ships_queue()
        self.current_ship = None

        # Обновляем отображение
        self.canvas.draw_pole()

        # Выключаем кнопку "В бой!"
        if self.done_button:
            self.done_button.config(state='disabled', bg='gray')

        # Начинаем заново
        self._start_next_ship()

    def disable(self):
        """Отключает ручную расстановку"""
        # Отвязываем все события
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Motion>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<space>')

        # Удаляем призрак
        if self.ghost_id:
            self.canvas.canvas.delete(self.ghost_id)