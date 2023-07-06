import pygame
from pygame.locals import *
import time
import random

bsize = 40
background_color = (3, 99, 93)


class Apple:
    def __init__(self, background):
        self.background = background
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def move(self):
        self.x = random.randint(1, 19) * bsize
        self.y = random.randint(1, 19) * bsize

    def draw(self):
        self.background.blit(self.image, (self.x, self.y))
        pygame.display.flip()

class Snake:
    def __init__(self, background, length):
        self.background = background
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.length = 1
        self.x = [40]
        self.y = [40]
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.background.fill(background_color)
        for i in range(self.length):
            self.background.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= bsize
        if self.direction == 'down':
            self.y[0] += bsize
        if self.direction == 'right':
            self.x[0] += bsize
        if self.direction == 'left':
            self.x[0] -= bsize

        self.draw()
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.background_sound()
        self.screen = pygame.display.set_mode((800, 800))
        self.snake = Snake(self.screen, 4)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (250, 255, 255))
        self.screen.blit(score, (650, 10))
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    def background_sound(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)
    def reset(self):
        self.snake = Snake(self.screen, 1)
        self.apple = Apple(self.screen)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise Exception("Game Over")

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + bsize:
            if y1 >= y2 and y1 < y2 + bsize:
                return True
        return False

    def show_game_over(self):
        self.screen.fill(background_color)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your Score is: {self.snake.length}", True, (250, 255, 255))
        self.screen.blit(line1, (200, 250))
        line2 = font.render("To play again, press Enter. To exit, press Escape!", True, (250, 255, 255))
        self.screen.blit(line2, (200, 300))
        pygame.display.flip()
        pygame.mixer.music.pause()
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key ==K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.25)

if __name__ == "__main__":
    game = Game()
    game.run()
