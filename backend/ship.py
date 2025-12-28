class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._size = 10
        self._length = length                              # длина {1, 2, 3, 4}
        self._x, self._y = None, None                       # начало корабля [0, size)
        self._tp = tp                                  # ориентация {1, 2}
        self._is_move = True
        self._cells = [1 for _ in range(self._length)]     # попадания
        self.set_start_cords(x, y)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, x):
        self._size = x

    @property
    def cells(self):
        return self._cells

    def is_destroyed(self):
        return self.cells.count(2) == self.get_length()

    def set_tp(self, value):
        if isinstance(value, int) and value in (1, 2):
            self._tp = value
            return
        print("Неверный ввод положения")

    def get_tp(self):
        return self._tp

    def get_length(self):
        return self._length

    def get_start_cords(self):
        return self._x, self._y

    def set_start_cords(self, x, y):
        if x is None or y is None:
            self._x, self._y = None, None
        elif isinstance(x, int) and isinstance(y, int) and 0 <= x <= self.size and 0 <= y <= self.size:
            self._x, self._y = x, y
            return x, y     # для метода ship_place (~100 строка)
        else:
            raise ValueError("Координатами начала корабля должны быть целые положительные входящие в диапозон числа")

    def get_cords(self):
        """Возвращает кортеж из всех пар координат корабля"""
        x0, y0 = self.get_start_cords()
        if x0 is None:
            return None, None
        if self._tp == 1:
            return ((x0 + i, y0) for i in range(self._length))
        else:
            return ((x0, y0 + i) for i in range(self._length))

    def move(self, go):
        if not self._is_move:
            print("Движение невозможно!")
            return
        if not isinstance(go, int):
            print("Неверное значение!")
            return

        if self._tp == 1:
            self._x += go
        else:
            self._y += go

    def is_out_pole(self, size):
        """Проверяет выход корабля self за пределы поля размером size"""
        if all(map(lambda r: 0 < r[0] <= size and 0 < r[1] <= size, self.get_cords())):  # r - пара (x, y)
            return False
        return True

    def ship_place_cords(self):
        """Список списков (матрица) всех занятых координат данного корабля"""
        x0, y0 = self.get_start_cords()
        if self._tp == 2:
            return [[(x0 + j, y0 + i) for j in range(-1, 2) if 10 >= x0 + j > 0 and 10 >= y0 + i > 0] for i in range(-1, self._length + 1)][::-1]
        else:
            return [[(x0 + j, y0 + i) for j in range(-1, self._length + 1) if 10 >= x0 + j > 0 and 10 >= y0 + i > 0] for i in range(-1, 2)][::-1]

    def place_around(self):
        ship_set = set(self.get_cords())
        full_set = set(cord for string in self.ship_place_cords() for cord in string)
        return full_set - ship_set

    def __getitem__(self, item):
        """Получить состояние 1 палубы корабля (1-норм, 2-подбит)"""
        return self._cells[item]

    def __setitem__(self, key, value):
        """Изменить состояние 1 палубы корабля (1-норм, 2-подбит)"""
        if value not in (1, 2):
            raise ValueError("Значения для _cells могут быть только 1 или 2")
        if value == 2:
            self._is_move = False
        self._cells[key] = value