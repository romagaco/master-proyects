import os
import sys
import math
import pygame
import pygame.mixer
from pygame.locals import *
import random
import tkinter as tk
from tkinter import messagebox as mBox



HEIGHT = 700
WIDTH = 700
BLACK = (0, 0, 0)
RED = (255, 0, 122)
PURPLE = (100, 0, 255)
YELLOW = (255, 236 ,0)
GREEN = (43, 159, 3)
GRID_SIZE = 20

main_image = pygame.image.load("123.jpg")
pause_image = pygame.image.load("1234.jpg")


class Snake:  # clase snake que representa los movimientos del snake
    def __init__(self):
        self.velocity = 20
        self.lenght = 1
        self.snake_body = [[220,220]]
        self.actual_mov = random.choice(["right", "left", "down", "up"])
        self.incorrect_mov = {"right": ["left"],
                              "left": ["right"],
                              "up": ["down"],
                              "down": ["up"],
                              }
        self.best_score = 1
        self.temp_score = 1


    # creamos la direccion de los movimientos de arriba abajo izq der.
    def move_snake(self, window):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    if self.check_valid_mov(pygame.key.name(event.key)):
                        continue
                    self.actual_mov = "left"
                
                if event.key == pygame.K_RIGHT:
                    if self.check_valid_mov(pygame.key.name(event.key)):
                        continue
                    self.actual_mov = "right"

                if event.key == pygame.K_UP:
                    if self.check_valid_mov(pygame.key.name(event.key)):
                        continue
                    self.actual_mov = "up"
                
                if event.key == pygame.K_DOWN:
                    if self.check_valid_mov(pygame.key.name(event.key)):
                        continue
                    self.actual_mov = "down"
                
                if event.key == pygame.K_p:
                    pause_game(window)

        self.snake_moves(window)


    # esta funcion es para crear el movimiento de la serpiente 
    def snake_moves(self, window):
        if self.actual_mov == "right":
            temp = self.snake_body[0][0] + self.velocity
            x = self.check_bounds(temp, "max_limit")
            self.update_snake(x, "X", window)

        elif self.actual_mov == "left":
            temp = self.snake_body[0][0] - self.velocity
            x = self.check_bounds(temp, "min_limit")
            self.update_snake(temp, "X", window)

        elif  self.actual_mov == "up":
            temp = self.snake_body[0][1] - self.velocity
            y = self.check_bounds(temp, "min_limit")
            self.update_snake(y, "Y", window)

        elif  self.actual_mov == "down":
            temp = self.snake_body[0][1] + self.velocity
            y = self.check_bounds(temp, "max_limit")
            self.update_snake(y, "Y", window)


    def update_snake(self, value, key, window):
        if key == "X":
            self.snake_body.insert(0, [value, self.snake_body[0][1]])
        elif key == "Y":
            self.snake_body.insert(0, [self.snake_body[0][0], value])
        self.snake_body.pop()
        self.draw_snake(window)


    def draw_snake(self, window): # dibujamos la serpiente 
        for idx, body in enumerate(self.snake_body):
            if idx == 0:
                pygame.draw.rect(window, YELLOW, [body[0], body[1], 20,20])
                continue

            pygame.draw.rect(window, PURPLE, [body[0], body[1], 20,20])

        self.check_error(window)



    def check_valid_mov(self, next_mov):
        if next_mov in self.incorrect_mov[self.actual_mov]:
            return True


    def check_bounds(self, value_to_check, limit):
        if limit == "max_limit":
            if value_to_check > 680:
                return 0
            else:
                return value_to_check
        else:
            if value_to_check < 0:
                return 680
            else:
                return value_to_check
    

    def get_snake_head(self):
        return self.snake_body[0]
    

    def grow_snake(self, value, window):
        self.snake_body.insert(0,list(value))
        self.draw_snake(window)


    def check_error(self, window):
        if self.get_snake_head() in self.snake_body[2:]:
            self.reset()


    def reset(self):
        message(self.lenght)
        self.snake_body = [[220, 220]]
        self.actual_mov = random.choice(["right", "left", "up", "down"])

        if self.lenght > self.temp_score:
            self.temp_score = self.lenght
            self.best_score = self.lenght
        
        self.lenght = 1



class Food: 
    def __init__(self):
        self.food_position = (0,0)
        self.random_position()

    def random_position(self):
        self.food_position = (random.randrange(0,680, 20), random.randrange(0,680, 20))

    def draw_food(self, window):
        pygame.draw.rect(window, RED, [self.food_position[0], self.food_position[1], 20 ,20])



class Block:
    def __init__(self):
        self.block_position = (0,0)
        self.random_position()

    def random_position(self):
        self.block_position = list(((random.randrange(0,680, 20), random.randrange(0,680, 20)) for i in range(80)))

    def draw_block(self, window):
        for i, value in enumerate(self.block_position):
            pygame.draw.rect(window, BLACK, [value[0], value[1], 20, 20])



def check_food(snake, food, window):
    if tuple(snake.get_snake_head()) == food.food_position:

        snake.grow_snake(food.food_position, window)

        food.random_position()
        food.draw_food(window)

        snake.lenght += 1
        if snake.lenght > snake.best_score:
            snake.best_score += 1

def message(score):
    root = tk.Tk()
    root.withdraw()
    mBox.showerror("You lost", f"Your score is: {score}")
    try:
        root.destroy()
    except:
        pass


def check_block(snake, block):
    if tuple(snake.get_snake_head()) in block.block_position:
        block.random_position()
        snake.reset()




def draw_grid(window):  # dibujamos la cuadricula
    window.fill(GREEN)
    x = 0
    y = 0
    for i in range(WIDTH):
        x += GRID_SIZE
        y += GRID_SIZE

        pygame.draw.line(window, BLACK, (x,0), (x, WIDTH))
        pygame.draw.line(window, BLACK, (0,y), (HEIGHT, y))


def start_menu(start, window):
    window.blit(main_image, (0,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key:
                return False
    return True


def pause_game(window):
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()      

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit() 
        window.blit(pause_image, (0,0))
        pygame.display.update()


def Main():
    # dibujamos el tablero
    pygame.init()
    window= pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption("Snake attack")
    clock = pygame.time.Clock()
    game_font = pygame.font.SysFont("Helvetica", 28)
    start = True

    snake = Snake()
    food = Food()
    block = Block()

    while True:
        clock.tick(11)
        while start:
            start = start_menu(start, window)

        draw_grid(window)
        snake.move_snake(window)

        check_block(snake, block)
        check_food(snake, food, window)


        score = game_font.render(f"Score: {snake.lenght}", True, BLACK)
        window.blit(score, (5,0))
        best_score = game_font.render(f"Best Score: {snake.best_score}", True, BLACK)
        window.blit(best_score, (5,30))

        block.draw_block(window)

        while True:
            if food.food_position in block.block_position:
                food.random_position()
            break
        food.draw_food(window)

        pygame.display.update()

Main() 

