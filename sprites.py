import pygame
from config import *
import math
import os


class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet,(0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite
    
class Player(pygame.sprite.Sprite):
    list_item = []

    def __init__(self, game,x,y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hits_type = ''
        self.key = 1

    def update(self):
        self.movement()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_items('x')
        self.collide_doors('x')

        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_items('y')
        self.collide_doors('y')
        self.animate()

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self,direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.x_change >0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change <0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED 

        if direction == "y":
            hits = pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.y_change >0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change <0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_items(self,direction):
        pressd = pygame.key.get_pressed()
        if direction == "x":
            hits = pygame.sprite.spritecollide(self,self.game.items,False)
            if hits:
                if pressd[pygame.K_RETURN]:
                    if self.hits_type != hits[0].label:
                        print(get_description(hits[0].label))
                        self.hits_type = hits[0].label
            if pressd[pygame.K_LEFT] or pressd[pygame.K_RIGHT] or pressd[pygame.K_UP] or pressd[pygame.K_DOWN]:
                self.hits_type = ''
                           
                        
        if direction == "y":
            hits = pygame.sprite.spritecollide(self,self.game.items,False)
            if hits:
                if pressd[pygame.K_RETURN]:
                    if self.hits_type != hits[0].label:
                        print(get_description(hits[0].label))
                        self.hits_type = hits[0].label
            if pressd[pygame.K_LEFT] or pressd[pygame.K_RIGHT] or pressd[pygame.K_UP] or pressd[pygame.K_DOWN]:
                    self.hits_type = ''

    def collide_doors(self,direction):

        if direction == "x":
            hits = pygame.sprite.spritecollide(self,self.game.doors,False) 
            if hits and hits[0].label == 'g' and list_item["e"] >= 1:
                hits = pygame.sprite.spritecollide(self,self.game.doors,True)
            if hits and hits[0].label == 'm' and list_item["h"] >= 1:
                hits = pygame.sprite.spritecollide(self,self.game.doors,True)
            if hits and hits[0].label == 'n' and list_item["w"] >= 1:
                hits = pygame.sprite.spritecollide(self,self.game.doors,True)
            if hits and hits[0].label == 'o' and list_item["s"] >= 1:
                hits = pygame.sprite.spritecollide(self,self.game.doors,True)
            if hits and list_item["d"] :
                self.kill()
                self.game.playing = False

            if hits:
                if self.x_change >0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change <0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED 

        if direction == "y":
            hits = pygame.sprite.spritecollide(self,self.game.doors,False)
            if hits and hits[0].label == 'g' and list_item["e"] >= 1:
                hits = pygame.sprite.spritecollide(self,self.game.doors,True)
            if hits and hits[0].label == 'm' and list_item["h"] >= 1:
                hits = pygame.sprite.spritecollide(self,self.game.doors,True)
            if hits and hits[0].label == 'n' and list_item["w"] >= 1:
                hits = pygame.sprite.spritecollide(self,self.game.doors,True)
            if hits and hits[0].label == 'o' and list_item["s"] >= 1:
                hits = pygame.sprite.spritecollide(self,self.game.doors,True)
            if hits and list_item["d"] :
                self.kill()
                self.game.playing = False
                

            if hits:
                if self.y_change >0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change <0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3,2,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(35,2,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(68,2,self.width,self.height)]
        
        up_animations = [self.game.character_spritesheet.get_sprite(3,34,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(35,34,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(68,34,self.width,self.height)]
        
        left_animations = [self.game.character_spritesheet.get_sprite(3,98,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(35,98,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(68,98,self.width,self.height)]
        
        right_animations = [self.game.character_spritesheet.get_sprite(3,66,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(35,66,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(68,66,self.width,self.height)]
        
        if self.facing == "down":
            if self.y_change == 0: 
                self.image = self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0: 
                self.image = self.game.character_spritesheet.get_sprite(3,34,self.width,self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0: 
                self.image = self.game.character_spritesheet.get_sprite(3,98,self.width,self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0: 
                self.image = self.game.character_spritesheet.get_sprite(3,66,self.width,self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y, is_window):
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        self.is_window = is_window
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        if self.is_window:
            self.image = pygame.image.load(os.path.join('img','bedroom_window.png')).convert()
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.image.set_colorkey(BLACK)
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(450,450,self.width,self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Item(pygame.sprite.Sprite):
    
    label_dict = {
        "a" : "bedroom_window",
        "b" : "photo_frame",
        "c" : "bed_bedroom",
        "d" : "safe_deposit_box",
        "e" : "desk",
        "f" : "closet",
        "g" : "door",
        "h" : "refrigerator",
        "i" : "couch",
        "j" : "television",
        "k" : "playstation",
        "l" : "door",
        "m" : "door",
        "n" : "door",
        "o" : "door",
        "p" : "plug",
        "q" : "switchboard",
        "r" : "carton",
        "s" : "bed_kidroom",
        "t" : "tin_box",
        "u" : "puzzle",
        "v" : "tub",
        "w" : "toilet",
        '1' : 'grass',
        '2' : 'flower1',
        '3' : 'flower2',
        '4' : 'flower3',
        'x' : 'faucet'
            }

    def __init__(self,game,x,y, label):

        self.game = game
        self._layer = ITEM_LAYER
        self.groups = self.game.all_sprites, self.game.items
        self.label = label
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.image.load(os.path.join('img',f'{self.label_dict[self.label]}.png')).convert()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    

class Door(pygame.sprite.Sprite):

    def __init__(self,game,x,y,label):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        self.label = label
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.image.load('./img/door.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.image.load(os.path.join("img","living_room.png")).convert()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
