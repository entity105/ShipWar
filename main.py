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
        elif isinstance(x, int) and isinstance(y, int) and 0 <= x <= self.size and 0 <= y <= self.size:
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
            return [[(x0 + j, y0 + i) for j in range(-1, self._length + 1)] for i in range(-1, 2)][::-1]

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
    def get_matrix(coords):
        lim = max(coords)[0]
        matrix = [[] for _ in range(lim)]
        for i in range(1, lim + 1):
            for el in coords:
                if el[0] == i:
                    matrix[i].append(el)
                else:
                    continue
        return matrix

    @staticmethod
    def count_next(row, start, difference):
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
        """Вычисление всех возможных координат корабля (tp = 1) для строки. Возвращает множество кортежей"""
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
        return [tuple(el) for el in lst]

    @staticmethod
    def tuple_coords_to_list(tple):
        return [list(el) for el in tple]

    def ships_cords(self):
        return (coord for ship in self._ships if ship.get_start_cords() != (None, None) for coord in ship.get_cords())


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
            place = sorted([g for k in (Ship(lenght, tp, x_y[0], x_y[1]).ship_place_cords()) for g in k])
            koord = sorted(self.ships_cords())
            if any(map(lambda x: x in koord, place)):
                wrong_cords.add(x_y)
                return self.random_cords(a, b, wrong_cords, ship)
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
            place = sorted([g for k in (Ship(lenght, tp, x_y[0], x_y[1]).ship_place_cords()) for g in k])  # координаты занимаемой области 1 корабля
            koord = sorted(self.ships_cords())  # координаты всех кораблей
            if any(map(lambda x: x in koord, place)):  # на любой корабль не должна накладываться область текущего корабля
                wrong_cords.add(x_y)  # если накладывается -> эту начальную координату нужно исключить -> взять другую случ. координату -> та же проверка ...
                return self.random_cords(a, b, wrong_cords, ship)  # через рекурсию
            return x_y


    def ship_place(self):
        """Возвращает начальные координаты всех кораблей (список)"""
        start_cords = []
        busy_cords = set()
        for ship in self._ships:
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
        #     print(f'Начальные координаты - {ship.get_start_cords()}, tp = {ship.get_tp()}, длина = {ship.get_length()}')
        #     print('Занятые координаты сейчас: ', end='\n')
        #     for i in ship.ship_place_cords():
        #         print(*i)
        #     print(f"Допустимые координаты: {sorted(tuple(set((i, j) for i in range(1, a + 1) for j in range(1, b + 1)) - busy_cords))}")
        #     print(f'Занятые координаты суммарно {sorted(tuple(busy_cords))}')
        #     print()
        # print()
        # # print(print_matrix(self.cort_sorting(sorted(list(busy_cords)))))
        # print()
        return start_cords

    def init(self):
        # self._ships = [Ship(5 - i, tp=randint(1, 2)) for i in range(4, 0, -1) for _ in range(1, i + 1)]  # инициализация кораблей
        self._ships = [Ship(5 - i, tp=randint(1, 2)) for i in range(1, 5) for _ in range(i)]
        self.ship_place()

    def get_pole(self):
        pole = [[0]*self.size for _ in range(self.size)]
        for s in self._ships:
            i = 0
            for x, y in s.get_cords():
                pole[y-1][x-1] = s[i]
                i += 1
        return pole[::-1]

def print_matrix(m: list):
    k = 10
    for row in m:
        print(f'{k}|', end=' ')
        print(' '.join(str(elem) for elem in row))
        k -= 1
    print("   " + '-'*19)
    print("   " + ' '.join([str(i) for i in range(1, 11)]))

g = GamePole(10)
g.init()
print_matrix(g.get_pole())

# ship1 = Ship(2, 1, 2, 2)
# ship2 = Ship(4, 1, 4, 2)
# g._ships = [ship1, ship2]
#
# print(*ship1.get_cords())
# print(*ship2.get_cords())


# g.init()
# print_matrix(g.get_pole())

# Не проверяются координаты занимаемой области нового корабля с "wrong" координатами
# Проверяется только начальная координата