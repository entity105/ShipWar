from random import randint, choice

from backend.gamepole import GamePole


class BattleShip:
    def __init__(self, pole1: GamePole):
        self.__pole_obj1 = pole1

        self.start_cords_s = None    # сохранение первого попадания (для автоматического режима)

    @staticmethod
    def auto(pole: GamePole):
        """Авто расстановка кораблей для заданного поля"""
        pole.init()

    # @staticmethod
    # def set_ship(pole: GamePole):
    #     """Самостоятельная расстановка"""
    #     pole.set_ship()

    @property
    def pole_obj_1(self):
        return self.__pole_obj1

    @staticmethod
    def find_ship(x_y0: tuple, pole_obj):
        """x, y -> ссылка на корабль + индекс координаты"""
        x_y = x_y0[0] + 1, 10 - x_y0[1]
        for ship in pole_obj.get_ships():
            coords = tuple(ship.get_cords())
            if x_y in coords:
                for i, coord in enumerate(coords):
                    if x_y == coord:
                        return ship, i
        raise Exception("Не найден корабль (метод find_ship)")



    def smart_shooting(self, x0, y0, pole_obj):
        """True - уничтожил корабль, False - промах"""
        damage = False
        dx, dy = 0, 0
        x, y = 0, 0

        while not damage:  # Пока хоть куда-нибудь не попадём
            dx = choice((1, 0, -1))  # Выбираем произвольное направление дальнейшей стрельбы
            dy = choice((1, -1)) if dx == 0 else 0

            x = x0 + dx  # Устанавливаем координаты
            y = y0 + dy

            if not (0 <= x < pole_obj.size) or not (0 <= y < pole_obj.size):
                continue

            damage = self.shot(x, y, pole_obj)


        if damage != 2:         # Промах (ошибся ориентацией)
            self.start_cords_s = x0, y0
            return False

        # Если попал, то нужно продолжить стрельбу в этом направлении
        while damage == 2:  # Пока попадаем
            if self.find_ship((x, y), pole_obj)[0].is_destroyed():  # Если корабль уничтожен
                self.start_cords_s = None
                return True
            if dx != 0:     # Сдвигаемся по направлению
                x += dx
            else:
                y += dy

            if not (-1 < x < pole_obj.size) or not (-1 < y < pole_obj.size):    # Вся хуйня в этой проверке
                damage = False
                break

            damage = self.shot(x, y, pole_obj)  # Стреляем

        if not damage:      # если попытался стрельнуть в закрытую клетку
            x = x0 - dx     # Отступаем от начала в противоположную сторону
            y = y0 - dy
            damage = 2
            while damage == 2:  # пока попадаем
                damage = self.shot(x, y, pole_obj)      # Стреляем
                if self.find_ship((x, y), pole_obj)[0].is_destroyed():  # если корабль уничтожен
                    break
                x -= dx
                y -= dy

            if damage != 2:
                raise ValueError("Error: корабль должен быть гарантированно уничтожен")
            self.start_cords_s = None
            return True

        # Если не уничтожил, сохраняем координаты начала корабля, чтобы потом пойти в противоположную сторону от начала
        self.start_cords_s = x0, y0
        return False

    def autoshot(self, pole_obj):
        """Серия умных выстрелов компьтера"""
        while True:
            if self.start_cords_s is None:     # если это не продолжение серии выстрелов
                x = randint(0, pole_obj.size - 1)       # берём произвольные x y
                y = randint(0, pole_obj.size - 1)
                damage = self.shot(x, y, pole_obj)      # Стреляем

                if not damage:                         # Если туда нельзя стрельнуть -> повторить попытку
                    continue
                if damage != 2:                         # Если стрельнул, но не попал -> завершить попытку
                    break
                if self.find_ship((x,y), pole_obj)[0].is_destroyed():  # Если попал и уничтожил занаво берём произвольные x y
                    continue
                # Если попал и не уничтожил
                b = self.smart_shooting(x, y, pole_obj)     # Уничтожает весь корабль или сохраняет координаты при промахе
                if b:   # Если уничтожил
                    continue
                break   # Если промахнулся

            elif self.start_cords_s is not None:
                if self.smart_shooting(*self.start_cords_s, pole_obj):
                    continue
                break

    def shot(self, x, y, pole_obj):
        """Одиночный выстрел по заданным координатам"""
        place = pole_obj.pole[y][x]
        if place == 0:
            pole_obj.pole[y][x] = 3
            return 1
        elif place == 1:
            pole_obj.pole[y][x] = 2
            ship, i = self.find_ship((x, y), pole_obj)  # Вводим матричные координаты
            ship[i] = 2
            if ship.is_destroyed():
                for x, y in ship.place_around():
                    pole_obj.pole[-y][x-1] = 3
            return 2
        else: # если там 2 или 3
            return False
    #
    # def game(self, p_1, p_2):
    #     while not all(map(lambda x: x.is_destroyed(), p_1.get_ships())) and not all(map(lambda x: x.is_destroyed(), p_2.get_ships())):
    #         # count_strike1 = self.shot(int(input()), int(input()), p_1)
    #         # while count_strike1 == 2:
    #         #     count_strike1 = self.shot(int(input()), int(input()), p_1)
    #
    #         count_strike1 = self.autoshot(p_1)
    #         while count_strike1 == 2:
    #             count_strike1 = self.autoshot(p_1)
    #
    #         count_strike2 = self.autoshot(p_2)
    #         while count_strike2 == 2:
    #             count_strike2 = self.autoshot(p_2)
    #     pass


