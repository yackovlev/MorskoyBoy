import random


class Dot:
    # класс точки на игровом поле с координатами x и y
    empty_dot = " O "
    ship_dot = " ■ "
    destroyed_ship_dot = " X "
    missed_dot = " T "
    hidden_ship_dot = " О "

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False


class Ship:
    # класс корабля на игровом поле с длиной, направлением и начальной точкой
    def __init__(self, length, direction, point_of_ship):
        self.length = length
        self.hp = length
        self.direction = direction
        self.point_of_ship = point_of_ship

    def dots(self):
        # метод, который возвращает список клеток занятых кораблем на игровом поле
        ship_dotes = []
        if self.direction == 0:
            # вертикальное направление корабля (нос сверху)
            for i in range(self.length):
                ship_dotes.append(Dot(self.point_of_ship[0], self.point_of_ship[1] + i))
        else:
            # горизонтальное направление корабля (нос слева)
            for i in range(self.length):
                ship_dotes.append(Dot(self.point_of_ship[0] + i, self.point_of_ship[1]))
        return ship_dotes

    def contour(self):
        # метод, который создает контур корабля
        contour_dotes = []
        for dot in self.dots():
            for i in range(-1, 2):
                for j in range(-1, 2):
                    contour_dotes.append(Dot(dot.x + i, dot.y + j))
        return contour_dotes


class Board:
    # класс игрового поля
    def __init__(self, size=6, hid=True):
        self.board = [["  ", " 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6", " "],
                      ["1 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["2 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["3 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["4 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["5 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["6 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["  ", "   ", "   ", "   ", "   ", "   ", "  ", " "]]
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == " O " or self.board[x][y] == " O":
                    self.board[x][y] = Dot.empty_dot

        self.size = size
        self.hid = hid
        self.ships = []
        self.alive_ships = 0

    def clear(self):
        # метод очистки игрового поля
        self.board = [["  ", " 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6", " "],
                      ["1 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["2 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["3 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["4 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["5 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["6 ", " O ", " O ", " O ", " O ", " O ", " O", " "],
                      ["  ", "   ", "   ", "   ", "   ", "   ", "  ", " "]]
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == " O " or self.board[x][y] == " O":
                    self.board[x][y] = Dot.empty_dot
        self.alive_ships = 0
        self.ships = []

    def hide_board(self):
        # метод скрытия кораблей
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == Dot.ship_dot:
                    self.board[x][y] = Dot.hidden_ship_dot

    def hidden(self):
        return self.hid

    def generate_board(self):
        # метод отображения поля
        for cell in self.board:
            print(*cell)

    def add_ship(self, ship):
        # метод установки корабля на игровое поле
        try:
            for dot in ship.dots():
                for c_dot in ship.contour():
                    if self.board[dot.x][dot.y] != Dot.empty_dot or self.out(dot) or self.board[c_dot.x][c_dot.y] == Dot.ship_dot:
                        if self.is_hidden():
                            print("\nЗдесь нельзя установить корабль (клетка занята другим кораблем или контуром)!\n")
                            return False
                        else:
                            return False
            for dot in ship.dots():
                # установка корабля
                self.board[dot.x][dot.y] = Dot.ship_dot
            self.ships.append(ship)
            # добаление нового корабля в счетчик кораблей
            self.alive_ships += 1
            if self.is_hidden():
                # вывод игрового поля с новым кораблем
                print("Корабль успешно установлен на игровое поле!\n")
                self.generate_board()
                print(f"Установлено кораблей - {self.alive_ships}\n")
                return True
        except IndexError:
            if self.is_hidden():
                print("\nОдна или несколько точек устанавливаемого корабля находятся вне игрового поля!\n")
                return False
            return False

    def out(self, dot):
        return not (1 <= dot.x < self.size + 1 and 1 <= dot.y < self.size + 1)

    def shot(self, dot):
        # метод выстрела игроков по игровому полю
        shot = False
        if self.board[dot.x][dot.y] == Dot.empty_dot:
            self.board[dot.x][dot.y] = Dot.missed_dot
        elif self.board[dot.x][dot.y] == Dot.ship_dot or self.board[dot.x][dot.y] == Dot.hidden_ship_dot:
            self.board[dot.x][dot.y] = Dot.destroyed_ship_dot
            shot = True
            for ship in self.ships:
                if dot in ship.dots():
                    ship.hp -= 1
                    if ship.hp == 0:
                        # если корабль уничтожен
                        self.alive_ships -= 1
                        for c_dot in ship.contour():
                            # обводка контура уничтоженного корабля
                            if self.board[c_dot.x][c_dot.y] == Dot.missed_dot:
                                continue
                            if self.board[c_dot.x][c_dot.y] == Dot.empty_dot:
                                # проверка на отсутствие обводки за границами игрового поля
                                self.board[c_dot.x][c_dot.y] = Dot.destroyed_ship_dot
                        if self.is_hidden():
                            print("\nКорабль Игрока-пользователя уничтожен!\n")
                            self.generate_board()
                            print(f"Кораблей Игрока-пользователя на игровом поле осталось {self.alive_ships}")
                        else:
                            print("\nКорабль Игрока ИИ уничтожен!\n")
                            self.generate_board()
                            print(f"Кораблей Игрока ИИ на игровом поле осталось - {self.alive_ships}")
                    else:
                        # при попадании в корабль
                        if self.is_hidden():
                            print("\nКорабль Игрока-пользователя ранен!\n")
                            self.generate_board()
                            print(f"Кораблей Игрока-пользователя на игровом поле осталось - {self.alive_ships}")
                        else:
                            print("\nКорабль Игрока ИИ ранен!\n")
                            self.generate_board()
                            print(f"Кораблей Игрока ИИ на игровом поле осталось - {self.alive_ships}")
        return shot


class Player:
    # класс игрока
    def __init__(self, player_board, enemy_board):
        self.player_board = player_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self, board):
        # метод хода
        while True:
            try:
                if board.alive_ships == 0:
                    # завершение игры
                    print("\nИгра окончена!\n")
                    exit()
                shot_coord = self.ask()
                if board.out(shot_coord):
                    if not board.hidden():
                        print("\nЦель находится за границами игрового поля!")
                elif board.board[shot_coord.x][shot_coord.y] == Dot.destroyed_ship_dot:
                    if not board.hidden():
                        print("\nЦель находится в контуре уничтоженного корабля!")
                elif board.board[shot_coord.x][shot_coord.y] == Dot.missed_dot:
                    if not board.hidden():
                        print("\nВыстрел в эту точку уже производился!")
                result = board.shot(shot_coord)
                if board.hidden():
                    # если игрок ИИ попал в корабль, то он производит случайный выстрел в соседние клетки
                    while result:
                        random_direction = random.randrange(1, 5)  # Случайное направление для выстрела
                        i = 1
                        if random_direction == 1:
                            result = board.shot(Dot(shot_coord.x + i, shot_coord.y))
                            while result:
                                # при очередном попадании игрок ИИ стреляет дальше
                                i += 1
                                result = board.shot(Dot(shot_coord.x + i, shot_coord.y))
                        elif random_direction == 2:
                            result = board.shot(Dot(shot_coord.x - i, shot_coord.y))
                            while result:
                                i += 1
                                result = board.shot(Dot(shot_coord.x - i, shot_coord.y))
                        elif random_direction == 3:
                            result = board.shot(Dot(shot_coord.x, shot_coord.y + i))
                            while result:
                                i += 1
                                result = board.shot(Dot(shot_coord.x, shot_coord.y + i))
                        elif random_direction == 4:
                            result = board.shot(Dot(shot_coord.x, shot_coord.y - i))
                            while result:
                                i += 1
                                result = board.shot(Dot(shot_coord.x, shot_coord.y - i))
                if board.board[shot_coord.x][shot_coord.y] == Dot.missed_dot:
                    if board.hidden():
                        print("\nИгрок ИИ совершил выстрел и не попал по кораблям Игрока-пользователя!\n")
                        board.generate_board()
                        # игровое поле Игрока-пользователя
                        break
                    else:
                        print("\nИгрок-пользователь совершил выстрел и не попал по кораблям Игрока ИИ!\n")
                        board.generate_board()
                        # игровое поле Игрока ИИ
                        break
            except IndexError:
                pass


class AI(Player):
    @staticmethod
    def ask(**kwargs):
        # функция случайного выстрела Игрока ИИ
        x, y = random.randrange(1, 7), random.randrange(1, 7)
        return Dot(x, y)


class User(Player):
    # класс Игрока-пользователя
    @staticmethod
    def ask(**kwargs):
        # метод запроса у Игрока-пользователя данных для выстрела
        print("\nВведите координаты для произведения выстрела!")
        dot_x, dot_y = "", ""
        while not dot_x.isdigit() or not dot_y.isdigit():
            dot_x, dot_y = input("Введите координату х для выстрела: "), input("Введите координату y для выстрела: ")
            if not dot_x.isdigit() or not dot_y.isdigit():
                print("\nВведен неверный символ, введите число!")
            continue
        return Dot(int(dot_x), int(dot_y))

    @staticmethod
    def ask_ship(length):
        # метод запроса у Игрока-пользователя данных для установки корабля на игровом поле
        x_coord, y_coord = "", ""
        while not x_coord.isdigit() or not y_coord.isdigit():
            x_coord = input("Ведите координату х корабля: ")
            y_coord = input("Ведите координату y корабля: ")
            if not x_coord.isdigit() or not y_coord.isdigit():
                print("\nВведен неверный символ, введите число!")
            continue
        point_of_ship = (int(x_coord), int(y_coord))
        direction = ""
        if length == 1:
            direction = "1"
        while not direction.isdigit():
            direction = input("\nВыберите расположение корабля. Горизонтальный - 0. Вертикальный - 1. Введите (0/1): ")
            if not direction.isdigit():
                print("\nВведен неверный символ, введите число!\n")
        ship = Ship(length, int(direction), point_of_ship)
        return ship


class Game:
    def __init__(self):
        self.player_board = Board(6, True)
        self.enemy_board = Board(6, False)
        self.user = User(self.player_board, self.enemy_board)
        self.ai = AI(self.player_board, self.enemy_board)

    @staticmethod
    def random_board(board):
        # метод создания случайного игрового поля для игрока ИИ
        step = 0
        while True:
            step += 1
            ship_3 = Ship(3, random.randrange(0, 2), (random.randrange(1, 7), random.randrange(1, 7)))
            board.add_ship(ship_3)
            if step > 100:
                return False
            if board.alive_ships == 1:
                break
        while True:
            step += 1
            ship_2 = Ship(2, random.randrange(0, 2), (random.randrange(1, 7), random.randrange(1, 7)))
            board.add_ship(ship_2)
            if step > 100:
                return False
            if board.alive_ships == 3:
                break
        while True:
            step += 1
            ship_1 = Ship(1, random.randrange(0, 2), (random.randrange(1, 7), random.randrange(1, 7)))
            board.add_ship(ship_1)
            if step > 100:
                return False
            if board.alive_ships == 7:
                print("\nИгровое поле Игрока ИИ создано успешно!\n")
                board.hide_board()
                return True

    def user_board_request(self):
        # метод для размещения кораблей Игрока-пользователя на игровом поле
        print("\nРасставьте корабли Игрока-пользователя на игровом поле!")
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            result = False
            fail_try_counter = 0
            while not result:
                ship = self.user.ask_ship(length)
                result = self.player_board.add_ship(ship)
                fail_try_counter += 1
                if fail_try_counter > 1:
                    restart_board = ""
                    while not restart_board.isdigit():
                        restart_board = input("\nНачать расстановку кораблей на игровом поле заново - 0. Продолжить - 1. Введите (0/1): ")
                        if not restart_board.isdigit():
                            print("\nВведен неверный символ, введите число!\n")
                        continue
                    if restart_board == "1":
                        self.player_board.clear()
                        return False
                    elif restart_board != "1" and restart_board != "0":
                        print("\nВведите 0 или 1!\n")
                    else:
                        fail_try_counter = 0
        return True

    @staticmethod
    def greet():  # Функция приветствия с правилами
        board = [["  ", " 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 "],
                 ["1 ", " O ", " O ", " O ", " O ", " O ", " O "],
                 ["2 ", " O ", " O ", " O ", " O ", " O ", " O "],
                 ["3 ", " O ", " O ", " O ", " O ", " O ", " O "],
                 ["4 ", " O ", " O ", " O ", " O ", " O ", " O "],
                 ["5 ", " O ", " O ", " O ", " O ", " O ", " O "],
                 ["6 ", " O ", " O ", " O ", " O ", " O ", " O "]]

        print("\nМорской бой для одного игрока - ver. 1.0\n"
              "\nПример игрового поля:\n")
        for i in board:
            print(*i)
        print("\nПравила игры:\n"
              "~ В игре участвуют по 7 кораблей разного размера: 3 клетки - 1 шт, 2 клетки - 2 шт., 1 клетка - 4 шт.\n"
              "~ Для установки корабля на поле Игрока необходимо выбрать координату установки (х,y) и направление.\n"
              "~ Корабли нельзя размещать вплотную и на одно и тоже место.\n"
              "~ Корабли Игрока ИИ расставляются случайным образом автоматически.")

    def loop(self):
        while True:
            self.user.move(self.enemy_board)
            self.ai.move(self.player_board)

    def start(self):

        self.greet()

        user_board_created = False
        while not user_board_created:
            user_board_created = self.user_board_request()

        enemy_board_created = False
        while not enemy_board_created:
            self.enemy_board.clear()
            enemy_board_created = self.random_board(self.enemy_board)

        self.loop()


game = Game()
game.start()