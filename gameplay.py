from main import GamePole, Ship


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

    def shot(self, x, y, pole_obj):
        x, y = x - 1, -y
        place = pole_obj.get_pole()[y][x]
        if place == 0:
            pole_obj.pole[y][x] = 3
            return 1
        elif place == 1:
            pole_obj.pole[y][x] = 2
            print(self.find_ship((x, y), pole_obj))
            ship, i = self.find_ship((x, y), pole_obj)
            ship[i] = 2
            if ship.cells.count(2) == ship.get_length():
                for x, y in ship.place_around():
                    pole_obj.pole[-y][x-1] = 3
            return 1
        else: # если там 2 или 3
            return 0

SIZE = 10
p1 = GamePole(SIZE)
p2 = GamePole(SIZE)

game = BattleShip(p1, p2)
game.auto(game.pole_obj_1)
game.auto(game.pole_obj_2)

game.pole_obj_2.show()
print()

game.shot(5, 5, game.pole_obj_2)
game.shot(1, 1, game.pole_obj_2)
game.shot(5, 2, game.pole_obj_2)
game.shot(6, 5, game.pole_obj_2)
game.shot(8, 5, game.pole_obj_2)
game.shot(1, 5, game.pole_obj_2)
game.shot(1, 3, game.pole_obj_2)
game.shot(9, 2, game.pole_obj_2)


game.pole_obj_2.show()

