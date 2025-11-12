class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self.size = 10
        self._length = length                              # длина {1, 2, 3, 4}
        self._x, self._y = self.set_start_cords(x, y)    # начало кор. [0, size)
        self._tp = self.set_tp(tp)                                  # ориентация {1, 2}
        self._is_move = True
        self._cells = [1 for _ in range(self._length)]     # попадания

    @staticmethod
    def set_tp(value):
        if isinstance(value, int) and value in (1, 2):
            return value
        print("Неверный ввод положения")

    #@property
    def set_start_cords(self, x, y):
        if x < self.size and self.size > y:
            return x, y

    def get_start_cords(self):
        return self._x, self._y

    def get_cords(self):
        x0, y0 = self.get_start_cords()
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

    @staticmethod
    def distance(coords1, coords2):
        return ((coords1[0] - coords2[0]) ** 2) + ((coords2[1] - coords2[1]) ** 2) ** 0.5

    def is_collide(self, ship):
        if not isinstance(ship, Ship):
            print("Это не корабль!")
            return
        if all(self.distance(coord[0], coord[1]) > 1 for coord in zip(self.get_cords(), ship.get_cords())):
            return False
        return True

    def is_out_pole(self, size):
        if all(map(lambda r: 0 <= r[0] < size and 0 <= r[1] < size, self.get_cords())):
            return False
        return True

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        if value not in (1, 2):
            raise ValueError("Значения для _cells могут быть только 1 или 2")
        if value == 2:
            self._is_move = False
        self._cells[key] = value


ship = Ship(4, 1, 0, 0)
print(ship.get_start_cords())
print(tuple(ship.get_cords()))
ship.set_start_cords(4, 9)     # не работает
print(tuple(ship.get_cords()))
print(ship[1])
ship[2] = 2
print(ship._cells)
print(ship.is_out_pole(10))