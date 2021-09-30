#Snakes Which Bites Game - developed using Python, Pygame

import pygame
import time
import random
from pygame.locals import *

# global variable
SIZE = 40

class Apple:
    def __init__(self,screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()     #to load the image of apple onto the screen
        self.screen = screen
        # to keep track of position of apple on the screen
        self.apple_x = SIZE*3
        self.apple_y = SIZE*3

    # to draw the apple on the screen
    def draw_the_apple(self):
        self.screen.blit(self.image, (self.apple_x, self.apple_y))
        pygame.display.update()  # updating the changes done

    # to move the apple to some random position when it was eaten by snake
    def move(self):
        # randint - used to select the random number from a given range
        self.apple_x = random.randint(1,24)*SIZE
        self.apple_y = random.randint(1,18)*SIZE

class Snake:
    def __init__(self,screen):
        self.screen =  screen     # setting the screen where snake appears
        self.length = 1      # to keep track no of blocks snake have
        self.block = pygame.image.load("resources/block.jpg").convert()         # to load the block image onto the surface
        self.block_x = [SIZE]    # array of x to trace the x coordinate of all blocks
        self.block_y = [SIZE]     # array of y to trace the y coordinate of all blocks
        self.direction = 'down'    # to keep track in which direction snake is moving at given instant

    # to increase the length of the snake when it is collided with apple on the screen
    def increase_length_of_snake(self):
        self.length+=1
        self.block_x.append(-1)    # to increase the length of the array x by one and its default value set to -1
        self.block_y.append(-1)    # to increase the length of the array x by one and its default value set to -1


    # to draw all blocks of the snake on the screen
    def draw_the_snake(self):
        for i in range(self.length):
            self.screen.blit(self.block, (self.block_x[i], self.block_y[i]))
        pygame.display.update()  # updating the changes done

    # when we click up , we will change direction of snake to up
    def move_up(self):
        self.direction = 'up'

    # when we click down , we will change direction of snake to down
    def move_down(self):
        self.direction = 'down'

    # when we click left , we will change direction of snake to left
    def move_left(self):
        self.direction = 'left'

    # when we click right , we will change direction of snake to right
    def move_right(self):
        self.direction = 'right'

    # to keep moving the snake in its direction automatically
    def walk(self):
        # to change the positions of all blocks (except first block) to their previous blocks
        for i in range(self.length-1,0,-1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        # to change the x,y coordinates of head wrt its direction
        if self.direction == 'up':
            self.block_y[0] -= SIZE

        if self.direction == 'down':
            self.block_y[0] += SIZE

        if self.direction == 'left':
            self.block_x[0] -= SIZE

        if self.direction == 'right':
            self.block_x[0] += SIZE

        self.draw_the_snake()  # after changing locations of all blocks draw them on the screen by updating whole screen


class Game:
    def __init__(self):
        pygame.init()            # initialising pygame setup
        pygame.display.set_caption("Codebasics Snake And Apple Game")         # setting name of the game
        self.surface = pygame.display.set_mode((1000, 760))     # setting the screen of specified size

        # pygame module for loading and playing sounds
        pygame.mixer.init()
        self.play_background_music()

        # creating object of Snake class by specifing the screen and length of the snake
        self.snake = Snake(self.surface)
        self.snake.draw_the_snake()        # to draw the snake on the screen
        # creating object of Apple class by specifing the screen
        self.apple = Apple(self.surface)
        self.apple.draw_the_apple()         # to draw the apple on the screen

    def play_background_music(self):
        pygame.mixer.music.load('resources/Bg_music.mp3')
        pygame.mixer.music.play(-1, 0)


    # to know the score by having length of the snake at the top of the screen
    def display_score(self):
        font = pygame.font.SysFont('arial',30)   # to create a font object of given size and given style of writing
        score = font.render(f"Score: {self.snake.length}",True, (255,0,0))    # to draw the text on the screen
        self.surface.blit(score, (850, 10))

    # to check the collision b/w the apple and snake
    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and  x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    # to have a background image to our screen
    def background_image(self):
        self.bg = pygame.image.load("resources/background.jpg").convert()  # to load the block image onto the surface
        self.surface.blit(self.bg, (0, 0))

    # to play the game until anything goes wrong
    def play_the_game(self):
        self.background_image()
        self.snake.walk()    # to move the snake automatically
        self.apple.draw_the_apple()    # to draw the apple on the screen
        self.display_score()  # to have the score on the screen
        pygame.display.update()

        # if collision happens between the head of the snake and apple
        if self.is_collision(self.snake.block_x[0],self.snake.block_y[0],self.apple.apple_x,self.apple.apple_y):
            self.snake.increase_length_of_snake()
            self.apple.move()

        # if collision happens between the head of the snake and remaining blocks of the snake
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.block_x[0],self.snake.block_y[0],self.snake.block_x[i],self.snake.block_y[i]):
                raise "Game over"

        # when collision occurs between the snake and the boundries of the window
        if not (0 <= self.snake.block_x[0] <= 1000 and 0 <= self.snake.block_y[0] <= 800):
            raise "Hit the boundry error"


    # to set the speed of the snake according to its length
    def speed_of_the_snake(self):
        if self.snake.length < 10:
            time.sleep(0.5)
        elif 10 <= self.snake.length < 20:
            time.sleep(0.4)
        elif 20 <= self.snake.length < 30:
            time.sleep(0.3)
        elif 30 <= self.snake.length < 40:
            time.sleep(0.2)
        elif 40 <= self.snake.length < 50:
            time.sleep(0.15)
        elif 50 <= self.snake.length < 60:
            time.sleep(0.1)
        else:
            time.sleep(0.08)


    # when the Game is over we show a message on the screen
    def show_game_over(self):
        self.background_image()
        font = pygame.font.SysFont('arial',40)
        line1 = font.render(f"Game is Over!   Your Score is {self.snake.length-1}", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("To play again press Enter",True, (255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.mixer.music.pause()
        pygame.display.update()

    # to start the new game when user enters enter
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)


    def run(self):
        running = True   # to keep track of game whether to quit or not
        pause = False     # to be in the game or not

        while running:
            # to have infinite events until game is over
            for event in pygame.event.get():
                if event.type == KEYDOWN:     # if taken input from key_board
                    if event.key == K_ESCAPE:  # if we click escape then exit the game
                        running = False
                    if event.key == K_RETURN:   # if we click enter game starts again
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:       # if we click the cross on top of the game then exit the game
                    running = False

            try:
                if not pause:
                    self.play_the_game()
            except Exception as e:        # works when any raise call happens in try part
                self.show_game_over()
                pause = True
                self.reset()

            self.speed_of_the_snake()


if __name__ == "__main__":

    game = Game()
    game.run()





