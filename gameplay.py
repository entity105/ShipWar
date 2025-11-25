from random import randint, choice

from main import GamePole


class BattleShip:
    def __init__(self, pole1: GamePole, pole2: GamePole):
        self.__pole_obj1 = pole1
        self.__pole_obj2 = pole2
        self.start_cords_s = None    # промах при стрельбе по направлению корбля если он не уничтожен
        self.start_cords_p = None    # промах при неверном выборе направления
        self.count_strike = 0     # для бота
        self.dx, self.dy = 0, 0

    @staticmethod
    def auto(pole: GamePole):
        pole.init()

    @staticmethod
    def set_ship(pole: GamePole):
        pole.set_ship()

    @property
    def pole_obj_1(self):
        return self.__pole_obj1

    @property
    def pole_obj_2(self):
        return self.__pole_obj2

    @staticmethod
    def find_ship(x_y0: tuple, pole_obj):
        """x, y -> ссылка на корабль + индекс координаты"""
        x_y = x_y0[0] + 1, -x_y0[1]
        for ship in pole_obj.get_ships():
            coords = tuple(ship.get_cords())
            if x_y in coords:
                for i, coord in enumerate(coords):
                    if x_y == coord:
                        return ship, i

    def smart_shooting(self, pole_obj):


    def autoshot(self, pole_obj):
        """Серия выстрелов компьтера"""
        while True:
            if self.start_cords_s is None and self.start_cords_p is None:     # если это не продолжение серии выстрелов
                x = randint(1, pole_obj.size)       # берём произвольные x y
                y = randint(1, pole_obj.size)
                damage = self.shot(x, y, pole_obj)      # Стреляем
                if damage == 0:                         # Если 0 -> повторить попытку
                    continue
                if damage != 2:                         # Если не попал -> завершить попытку
                    break
                if self.find_ship((x-1,-y), pole_obj)[0].is_destroyed():  # Если попал и уничтожил занаво берём произвольные x y
                    continue
                # Если попал и не уничтожил
                dx = choice((1, 0, -1))                     # Выбираем произвольное направление дальнейшей стрельбы
                dy = choice((1, -1)) if dx == 0 else 0
                x_new = x + dx          # Устанавливаем координаты
                y_new = y + dy
                damage = self.shot(x_new, y_new, pole_obj)      # Стреляем по этим новым координатам
                while damage == 0:
                    dx = choice((1, 0, -1))  # Выбираем произвольное направление дальнейшей стрельбы
                    dy = choice((1, -1)) if dx == 0 else 0
                    x_new = x + dx  # Устанавливаем координаты
                    y_new = y + dy
                    damage = self.shot(x_new, y_new, pole_obj)
                if damage != 2:     # Если не попал
                    self.start_cords_p = x, y      # Сохраняем исходные координаты
                    break
                self.count_strike = 1         # Счётчик попаданий подряд
                while damage == 2:         # Пока попадаем
                    x_new += dx if x_new < pole_obj.size else 0  # Сдвигаемся по выбранному направлению
                    y_new += dy if y_new < pole_obj.size else 0
                    self.count_strike += 1
                    damage = self.shot(x_new, y_new, pole_obj)  # и стреляем
                    if self.find_ship((x-1,-y), pole_obj)[0].is_destroyed():   # Если уничтожил
                        break       # Прекращаем стрельбу по этому кораблю
                if damage == 0:
                    continue
                if damage != 2:     # Если промахнулся
                    self.start_cords_s = x, y  # Координаты начала (на которых закончлась 1 часть корабля)
                    self.dx = dx        # Сохраняем направление корабля для следующего выстрела
                    self.dy = dy
                    break
            elif self.start_cords_p is not None:   # Если выбрали неверное направление
                x, y = self.start_cords_p
                dx = choice((1, 0, -1))  # Выбираем произвольное направление дальнейшей стрельбы
                dy = choice((1, -1)) if dx == 0 else 0
                x_new = x + dx  # Устанавливаем координаты
                y_new = y + dy
                damage = self.shot(x_new, y_new, pole_obj)  # Стреляем по этим новым координатам
                while damage == 0:
                    dx = choice((1, 0, -1))  # Выбираем произвольное направление дальнейшей стрельбы
                    dy = choice((1, -1)) if dx == 0 else 0
                    x_new = x + dx  # Устанавливаем координаты
                    y_new = y + dy
                    damage = self.shot(x_new, y_new, pole_obj)
                if damage != 2:     # Если не попал
                    self.start_cords_p = x, y      # Сохраняем исходные координаты
                    break
                self.count_strike = 1         # Счётчик попаданий подряд
                self.start_cords_p = None
                while damage == 2:         # Пока попадаем
                    x_new += dx if x_new < pole_obj.size else 0     # Сдвигаемся по выбранному направлению
                    y_new += dy if y_new < pole_obj.size else 0
                    self.count_strike += 1
                    damage = self.shot(x_new, y_new, pole_obj)  # и стреляем
                    if self.find_ship((x-1,-y), pole_obj)[0].is_destroyed():   # Если уничтожил
                        break       # Прекращаем стрельбу по этому кораблю
                if damage == 0:
                    continue
                if damage != 2:     # Если промахнулся
                    self.start_cords_s = x, y  # Координаты начала (на которых закончлась 1 часть корабля)
                    self.dx = dx        # Сохраняем направление корабля для следующего выстрела
                    self.dy = dy
                    break
            # Добиваем
            else:
                x, y = self.start_cords_s
                dx, dy = -self.dx, -self.dy
                x += dx
                y += dy
                damage = self.shot(x, y, pole_obj)
                while damage == 2:
                    x += dx  # Сдвигаемся по выбранному направлению
                    y += dy
                    damage = self.shot(x, y, pole_obj)  # и стреляем
                    if self.find_ship((x, y), pole_obj)[0].is_destroyed():  # Если уничтожил
                        break  # Прекращаем стрельбу по этому кораблю

    def shot(self, x, y, pole_obj):
        x, y = x - 1, -y
        place = pole_obj.get_pole()[y][x]
        if place == 0:
            pole_obj.pole[y][x] = 3
            return 1
        elif place == 1:
            pole_obj.pole[y][x] = 2
            # print(self.find_ship((x, y), pole_obj))
            ship, i = self.find_ship((x, y), pole_obj)
            ship[i] = 2
            if ship.is_destroyed():
                for x, y in ship.place_around():
                    pole_obj.pole[-y][x-1] = 3
            return 2
        else: # если там 2 или 3
            return 0

    def game(self, p_1, p_2):
        while not all(map(lambda x: x.cells.count(2) == x.get_length(), p_1.get_ships())) and not all(map(lambda x: x.cells.count(2) == x.get_length(), p_2.get_ships())):
            # count_strike1 = self.shot(int(input()), int(input()), p_1)
            # while count_strike1 == 2:
            #     count_strike1 = self.shot(int(input()), int(input()), p_1)

            count_strike1 = self.autoshot(p_1)
            while count_strike1 == 2:
                count_strike1 = self.autoshot(p_1)

            count_strike2 = self.autoshot(p_2)
            while count_strike2 == 2:
                count_strike2 = self.autoshot(p_2)



SIZE = 10
p1 = GamePole(SIZE)
p2 = GamePole(SIZE)

game = BattleShip(p1, p2)
game.auto(game.pole_obj_1)
# game.auto(game.pole_obj_2)

game.pole_obj_1.show()
game.autoshot(game.pole_obj_1)
game.autoshot(game.pole_obj_1)
game.autoshot(game.pole_obj_1)
game.autoshot(game.pole_obj_1)
game.autoshot(game.pole_obj_1)
game.autoshot(game.pole_obj_1)
print()
game.pole_obj_1.show()
# print()
#
# game.game(game.pole_obj_1, game.pole_obj_2)
#
# game.pole_obj_1.show()
# print()
# game.pole_obj_2.show()


