from random import randint, choice


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self.size = 10
        self._length = length                              # длина {1, 2, 3, 4}
        self._x, self._y = None, None                       # начало корабля [0, size)
        self._tp = self.set_tp(tp)                                  # ориентация {1, 2}
        self._is_move = True
        self._cells = [1 for _ in range(self._length)]     # попадания
        self.set_start_cords(x, y)

    @staticmethod
    def set_tp(value):
        if isinstance(value, int) and value in (1, 2):
            return value
        print("Неверный ввод положения")

    def get_tp(self):
        return self._tp

    def get_length(self):
        return self._length

    def get_start_cords(self):
        return self._x, self._y

    def set_start_cords(self, x, y):        # должен быть инкапсулирован ?
        if x is None or y is None:
            self._x, self._y = None, None
        elif isinstance(x, int) and isinstance(y, int) and 0 <= x <= self.size and 0 <= y < self.size:
            self._x, self._y = x, y
            return x, y     # для метода ship_place (~100 строка)
        else:
            raise ValueError("Координатами начала корабля должны быть целые положительные входящие в диапозон числа")

    def get_cords(self):                    # Возвращает кортеж из всех пар координат
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
        if all(map(lambda r: 0 <= r[0] < size and 0 <= r[1] < size, self.get_cords())):  # r - пара (x, y)
            return False
        return True

    def ship_place_cords(self):   # отрицательные координаты
        x0, y0 = self.get_start_cords()
        if self._tp == 2:
            return [[(x0 + j, y0 + i) for j in range(-1, 2)] for i in range(-1, self._length + 1)][::-1]
        else:
            return [[(x0 + i, y0 + j) for j in range(-1, self._length + 1)] for i in range(-1, 2)][::-1]

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        if value not in (1, 2):
            raise ValueError("Значения для _cells могут быть только 1 или 2")
        if value == 2:
            self._is_move = False
        self._cells[key] = value


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = []

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, a):
        if isinstance(a, int) and a > 0:
            self._size = a

    @staticmethod
    def random_cords(a, b, wrong_cords: set):
        allowed_cords = tuple(set((i, j) for i in range(a) for j in range(b)) - wrong_cords)
        return choice(allowed_cords)

    def ship_place(self):
        start_cords = []
        busy_cords = set()
        for ship in self._ships:
            a, b = None, None
            if ship.get_tp() == 1:
                a = self.size - ship.get_length() - 1
                b = self.size - 1
            else:
                b = self.size - ship.get_length() - 1
                a = self.size - 1
            start_cords.append(ship.set_start_cords(*self.random_cords(a, b, busy_cords)))
            for el in ship.ship_place_cords():
                busy_cords.update(el)
        print(start_cords)
        return start_cords

    def init(self):
        self._ships = [Ship(5 - i, tp=randint(1, 2)) for i in range(4, 0, -1) for j in range(1, i + 1)]  # инициализация кораблей
        self.ship_place()

    def get_pole(self):
        pole = [[0]*self.size for _ in range(self.size)]
        for s in self._ships:
            i = 0
            for x, y in s.get_cords():
                pole[x][y] = s[i]
                i += 1
        return pole[::-1]

def print_matrix(m: list):
    for row in m:
        for x in row:
            print(x, end=' ')
        print()

g = GamePole(10)
g.init()
print_matrix(g.get_pole())
# print([el._length for el in g._ships])

# s = Ship(3, 1, 0, 3)