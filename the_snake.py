from random import choice, randint

import pygame as pg


"""Константы для размеров поля и сетки."""
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

"""Направления движения."""
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

"""Цвет фона - черный."""
BOARD_BACKGROUND_COLOR = (0, 0, 0)

"""Цвет границы ячейки."""
BORDER_COLOR = (93, 216, 228)

"""Цвет яблока."""
APPLE_COLOR = (255, 0, 0)

"""Цвет змейки."""
SNAKE_COLOR = (0, 255, 0)

"""Скорость движения змейки."""
SPEED = 20

"""Настройка игрового окна."""
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

"""Заголовок окна игрового поля."""
pg.display.set_caption('Змейка')

"""Настройка времени."""
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, body_color=None):
        self.position = CENTER
        self.body_color = body_color
        self.border_color = BORDER_COLOR

    def draw_cell(self, position):
        """Отрисовывает одну ячейку на экране."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)

    def draw(self):
        """Отриcовка игровых объектов."""
        raise NotImplementedError('Игровой объект не отрисован')


class Apple(GameObject):
    """Класс яблоко."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Устанавливает случайную позицию для яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                break

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейка."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        move_x, move_y = self.direction
        new_head = (
            (head_x + move_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + move_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            self.draw_cell(position)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pg.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.positions.append(snake.positions[-1])
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
