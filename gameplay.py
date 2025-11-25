from random import randint

from main import GamePole


class BattleShip:
    def __init__(self, pole1: GamePole, pole2: GamePole):
        self.__pole_obj1 = pole1
        self.__pole_obj2 = pole2

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

    def autoshot(self, pole_obj):
        """Выстрел компьтера"""
        x = randint(1, pole_obj.size)
        y = randint(1, pole_obj.size)
        return self.shot(x, y, pole_obj)

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
            if ship.cells.count(2) == ship.get_length():
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
game.auto(game.pole_obj_2)

game.pole_obj_1.show()
print()
game.pole_obj_2.show()
print()

game.game(game.pole_obj_1, game.pole_obj_2)

game.pole_obj_1.show()
print()
game.pole_obj_2.show()


