from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=None):
        """Создать объект с заданными координатами и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовать объект (реализуется в дочерних классах)."""
        pass


class Apple(GameObject):
    """Яблоко, которое появляется в случайной клетке поля."""

    def __init__(self):
        """Создать яблоко и выбрать для него начальную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Переместить яблоко в случайную клетку поля."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Нарисовать яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка, управляемая игроком."""

    def __init__(self):
        """Создать змейку длиной один сегмент в центре поля."""
        start = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(position=start, body_color=SNAKE_COLOR)
        self.positions = [start]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применить выбранное направление движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Переместить голову на клетку и при необходимости хвост."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        self.position = new_head

    def reset(self):
        """Вернуть змейку к исходному состоянию."""
        start = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [start]
        self.position = start
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Нарисовать сегменты змейки и стереть её прежний хвост."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработать закрытие окна и клавиши смены направления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type != pygame.KEYDOWN:
            continue
        directions = {
            pygame.K_UP: (UP, DOWN),
            pygame.K_DOWN: (DOWN, UP),
            pygame.K_LEFT: (LEFT, RIGHT),
            pygame.K_RIGHT: (RIGHT, LEFT),
        }
        direction = directions.get(event.key)
        if direction is not None and direction[0] != game_object.direction:
            if direction[0] != tuple(-axis for axis in game_object.direction):
                game_object.next_direction = direction[0]


def main():
    """Запустить игровой цикл «Змейки»."""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
