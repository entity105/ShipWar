from random import randint, choice
import copy


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


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = []
        self.pole = self.get_pole()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, a):
        if isinstance(a, int) and a > 0:
            self._size = a

    @staticmethod
    def count_next(row, start, difference):
        """Количество свободных клеток строки начиная с заданной и заканчивая первой несвободной (для метода row_traversal)"""
        k = 0
        n = start + difference + 1
        for y in row[start:]:
            if n == y[1]:
                k += 1
                n += 1
            else:
                break
        return k

    def row_traversal(self, row, length):
        """Вычисление всех возможных координат корабля для строки. Возвращает множество кортежей"""
        k = 0
        y_start = 0
        y_now = row[0][1]
        cp = 0
        res = []
        for x, y in row:
            if y == y_now:
                cp += 1
                k += 1
                y_now += 1
                if cp >= length:
                    res.append(row[y_start])
                    dy = y - k
                    next_free_count = self.count_next(row, k - (cp - length), dy)
                    for i in range(1, next_free_count + 1):
                        res.append(row[y_start + i])
                    cp = 0
            else:
                y_now = y + 1
                y_start = k
                cp = 1
                k += 1
        return set(self.list_coords_to_tuple(res))

    @staticmethod
    def cort_sorting(general: list):
        """Сортировка отсортированного списка кортежей координат. Возвращает список из кортежей кортежей координат"""
        groups = {}
        for item in general:
            key = item[0]
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return [tuple(group) for group in groups.values()]

    @staticmethod
    def swap_coords(matr):
        """В каждой паре координат (кортеж) меняет местами x и y """
        m = [[[x, y] for x, y in i] for i in matr]    # Сделали списки вместо кортежей для изменения координат
        for i in m:  # (x, y) -> (y, x)
            for j in i:
                f = j[0]
                j[0] = j[1]
                j[1] = f

        return m

    @staticmethod
    def transpose_skip_missing(matrix):
        """Транспонирование с пропуском недостающих элементов"""
        max_cols = max(len(row) for row in matrix)
        transposed = []

        for j in range(max_cols):
            new_row = []
            for i in range(len(matrix)):
                if j < len(matrix[i]):
                    new_row.append(matrix[i][j])
            transposed.append(new_row)

        return transposed

    @staticmethod
    def list_coords_to_tuple(lst):
        """[ ] - > ( )"""
        return [tuple(el) for el in lst]

    @staticmethod
    def tuple_coords_to_list(tple):
        """( ) - > [ ]"""
        return [list(el) for el in tple]

    def get_ships(self):
        return self._ships

    def ships_cords(self):
        """Координаты поля, совпадающие с координатами кораблей"""
        return (coord for ship in self._ships if ship.get_start_cords() != (None, None) for coord in ship.get_cords())

    def check_place(self, ship, coord):
        """True, если хотя бы 1 клетка области нового корабля занимает хотя бы 1 клетку другого корабля"""
        ship_copy = copy.copy(ship)
        ship_copy.size = self.size
        ship_copy.set_start_cords(*coord)
        place = sorted([g for k in ship_copy.ship_place_cords() for g in k])  # координаты занимаемой области текущего корабля
        koords = sorted(set(self.ships_cords()) - set(ship.get_cords()))  # координаты всех кораблей кроме текущего
        return any(map(lambda x: x in koords, place))

    def random_cords(self, a, b, w_c: set, ship: Ship):
        """Возвращает случайные координаты начала для одного корабля: пара (x, y)"""
        lenght = ship.get_length()
        tp = ship.get_tp()
        wrong_cords = w_c.copy()
        maybe_start_cords = sorted(tuple(set((i, j) for i in range(1, a + 1) for j in range(1, b + 1)) - wrong_cords))
        maybe_start_cords_matrix = self.cort_sorting(maybe_start_cords)      # строки (кортежи координат) этого списка циклом пихаются в row_traversal
        correct_cords_set = set()
        if tp == 1:
            for string in maybe_start_cords_matrix:
                correct_cords_set.update(self.row_traversal(string, lenght))       # возвращает мн-во всевозможных координат для n-мерного корабля в данной строчке
            x_y = choice(list(correct_cords_set))
            if self.check_place(ship, x_y):  # на любой корабль не должна накладываться область текущего корабля
                wrong_cords.add(x_y)  # если накладывается -> эту начальную координату нужно исключить -> взять другую случ. координату -> та же проверка ...
                return self.random_cords(a, b, wrong_cords, ship)  # через рекурсию
            return x_y

        else:   # для tp = 2
            transpose_m = self.transpose_skip_missing(self.swap_coords(maybe_start_cords_matrix))
            for string in transpose_m:
                list_swap = self.tuple_coords_to_list(list(self.row_traversal(string, lenght)))
                for j in list_swap:     #обратный своп координат:  [y, x] -> [x, y]
                    f = j[0]
                    j[0] = j[1]
                    j[1] = f
                correct_cords_set.update(set(self.list_coords_to_tuple(list_swap)))
            x_y = choice(list(correct_cords_set))  # берём произвольную координату из нашего множества
            if self.check_place(ship, x_y):  # на любой корабль не должна накладываться область текущего корабля
                wrong_cords.add(x_y)  # если накладывается -> эту начальную координату нужно исключить -> взять другую случ. координату -> та же проверка ...
                return self.random_cords(a, b, wrong_cords, ship)  # через рекурсию
            return x_y

    def ship_place(self):
        """Возвращает начальные координаты всех кораблей после расстановки (список)"""
        start_cords = []
        busy_cords = set()
        for ship in self._ships:
            ship.size = self.size
            a, b = None, None
            if ship.get_tp() == 1:
                a = self.size - ship.get_length() + 1     # a - граница справа
                b = self.size                           # b - граница сверху
            else:
                b = self.size - ship.get_length()
                a = self.size
            start_cords.append(ship.set_start_cords(*self.random_cords(a, b, busy_cords, ship)))
            for el in ship.ship_place_cords():
                busy_cords.update(el)
        return start_cords

    def is_correct_place(self, ship):
        return not ship.is_out_pole(self.size) and not self.check_place(ship, ship.get_start_cords())

    def move_ships(self):
        for ship in self._ships:
            shift = choice((1, -1))
            cord0 = tuple(ship.get_start_cords())
            ship.move(shift)
            if not self.is_correct_place(ship):    # если пересекает
                ship.move(-shift - 1)
                if not self.is_correct_place(ship):  # если опять пересекает
                    ship.set_start_cords(*cord0)

    def set_ship(self):
        """Самостоятельная расстановка"""
        # ships = [Ship(5 - i) for i in range(1, 5) for _ in range(i)]
        ships = [Ship(1), Ship(1)]
        n = len(ships)
        for _ in range(n):
            i = int(input("Номер корабля: "))
            ship_select = ships[i]
            while True:
                x, y = map(int, input().split())
                tp = int(input("Введите положение корабля: "))
                ship_select.set_start_cords(x, y)
                ship_select.set_tp(tp)
                if self.is_correct_place(ship_select):
                    break
                print('wrong')
            self._ships.append(ship_select)
            # ships.pop(i)
            print("next")
        self.pole = self.get_pole()

    def get_pole(self):
        """Возвращает матрицу поля: 1 - корабль, 0 - пусто"""
        pole = [[0]*self.size for _ in range(self.size)]
        for s in self._ships:
            i = 0
            for x, y in s.get_cords():
                pole[y-1][x-1] = s[i]
                i += 1
        return pole[::-1]

    def show(self):
        for row in self.pole:
            print(' '.join(str(elem) for elem in row))

    def init(self):
        """Инициализатор"""
        self._ships = [Ship(5 - i, tp=randint(1, 2)) for i in range(1, 5) for _ in range(i)]
        self.ship_place()
        self.pole = self.get_pole()

