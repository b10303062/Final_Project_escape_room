import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("密室逃脫")
        self.running = True
        self.font = pygame.font.Font('Arial.ttf', 32)

        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.intro_background = pygame.image.load('./img/501454122.jpg')
        self.go_background = pygame.image.load('./img/finish.png')
        self.door = pygame.image.load('./img/door.png')

    def createTilemap(self):
        list = ['g', 'm', 'n', 'o', 'l']
        for i,row in enumerate(tilemap):
            for j,column in enumerate(row):
                Ground(self,j,i)
                if column == "B":
                    Block(self,j,i, False)
                elif column == "a":
                    Block(self,j,i, True)
                elif column == "1":
                    Item(self, j, i, column)
                elif column == "P":
                    Player(self,j,i)
                elif column == ".":
                    pass
                elif column in list:
                    Door(self, j, i, column)
                else:
                    Item(self, j, i, column)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()


        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()


    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_finish(self):
        text = self.font.render('Mission Complete', True, ORANGE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runnung = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            pygame.display.update()
            
    def intro_screen(self):
        intro = True

        title = self.font.render('Escape Room', True, RED)
        title_rect = title.get_rect(x=210, y=150)

        play_button = Button(250, 200, 100, 50, GREEN, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_finish()

pygame.quit()
sys.exit()