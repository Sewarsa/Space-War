
from email.mime import image
import sys
import random
import time

import pygame
from pygame.locals import *
 
pygame.init()


player_ship = 'playership2.png'
enemy_ship = 'pesawat musuh1.png'
enemy2_ship = 'pesawat musuh2.png'
sideenemy_ship = 'sideenemy.png'
player_bullet = 'peluruplayer.png'
enemy_bullet = 'pelurumusuh.png'
sideenemy_bullet = 'pelurusideenemy.png'

music = pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)
exp_sound = pygame.mixer.Sound('audio_explosion.wav')
laser_sound = pygame.mixer.Sound('audio_laser.wav')
gameover_sound = pygame.mixer.Sound('Game Over Theme.mp3')

 
screen = pygame.display.set_mode((0,0), FULLSCREEN)
s_width, s_height = screen.get_size()
 
clock = pygame.time.Clock()
FPS = 60
 
 
background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
sideenemy_group = pygame.sprite.Group()
enemy2_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
sideenemybullet_group = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()
pygame.mouse.set_visible(False)
 
class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
 
        self.image = pygame.Surface([x,y])
        self.image.fill('white')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()

 
    def update(self):
        self.rect.y += 1
        self.rect.x += 1 
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(-400, s_width)
            

class player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')
        self.alive = True
        self.count_to_live = 0
        self.activate_bullet = True
        self.alpha_duration = 0
        
    

    def update(self):
        if self.alive:
            self.image.set_alpha(70)
            self.alpha_duration += 1
            if self.alpha_duration > 170:
                self.image.set_alpha(255)
            mouse = pygame.mouse.get_pos()
            self.rect.x = mouse[0] - 12
            self.rect.y = mouse[1] + 30
        else:
            self.alpha_duration = 0
            expl_x = self.rect.x + 30
            expl_y = self.rect.y + 35
            explosion = Explosion(expl_x, expl_y)
            explosion_group.add(explosion)
            sprite_group.add(explosion)
            pygame.time.delay(10)
            self.rect.y = s_height + 200
            self.count_to_live += 1
            if self.count_to_live > 80:
                self.alive = True
                self.count_to_live=0
                self.activate_bullet = True
     
    def shoot(self):
        if self.activate_bullet:
            bullet = PlayerBullet(player_bullet)
            mouse = pygame.mouse.get_pos()
            bullet.rect.x = mouse[0]
            bullet.rect.y = mouse[1]
            playerbullet_group.add(bullet)
            sprite_group.add(bullet)
            laser_sound.play()

    def dead(self):
        self.alive = False
        self.activate_bullet = False

    


class Enemy(player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-2000, 0)
        self.shoot()

    def shoot(self):
        if self.rect.y in (0, 50, 200, 400):
            enemybullet = EnemyBullet(enemy_bullet)
            enemybullet.rect.x = self.rect.x + 25
            enemybullet.rect.y = self.rect.y + 35
            enemybullet_group.add(enemybullet)
            sprite_group.add(enemybullet)


class SideEnemy(Enemy):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = -200
        self.rect.y = 200
        self.move = 1

    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_width + 200:
            self.move *= -1
        elif self.rect.x < -200:
            self.move *= -1
        self.shoot()

    def shoot(self):
        if self.rect.x % 100 == 0:
            sideenemybullet = EnemyBullet(sideenemy_bullet)
            sideenemybullet.rect.x = self.rect.x + 50
            sideenemybullet.rect.y = self.rect.y + 60
            sideenemybullet_group.add(sideenemybullet)
            sprite_group.add(sideenemybullet)

class Enemy2(player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-2000, 0)
        self.shoot()

    def shoot(self):
        if self.rect.y in (0, 50,200, 400, 600):
            enemybullet = EnemyBullet(enemy_bullet)
            enemybullet.rect.x = self.rect.x + 25
            enemybullet.rect.y = self.rect.y + 35
            enemybullet_group.add(enemybullet)
            sprite_group.add(enemybullet)


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')
        self.alive = True

    def update(self):
        self.rect.y -= 3
        if self.rect.y < 0:
            self.kill()

class EnemyBullet(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)

    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img_list = []
        for i in range(1, 6):
            img = pygame.image.load(f'exp{i}.png').convert()
            img.set_colorkey('black')
            img = pygame.transform.scale(img, (120,120))
            self.img_list.append(img)
        self.index = 0
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count_delay = 0
        

    def update(self):
        exp_sound.play()
        self.count_delay += 1
        if self.count_delay >= 12:
            if self.index < len(self.img_list) - 1:
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index]
        if self.index >= len(self.img_list) - 1:
            if self.count_delay >= 12:
                self.kill()



class Game:
    def __init__(self):
        self.count_hit = 0
        self.count_hit2 = 0
        self.lives = 3
        self.score = 0
        self.font = pygame.font.Font('Pixeled.ttf',25)
        self.run_game()
        
 
    def create_background(self):
        for i in range(30):
            x = random.randint(2,8)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0, s_width)
            background_image.rect.y = random.randrange(0, s_height)
            background_group.add(background_image)
            sprite_group.add(background_image)
    
    def create_player(self):
        self.player = player(player_ship)
        player_group.add(self.player)
        sprite_group.add(self.player)

    def create_enemy(self):
        for i in range(5):
            self.enemy = Enemy(enemy_ship)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)

    def create_sideenemy(self):
        for i in range (1):
            self.sideenemy = SideEnemy(sideenemy_ship)
            sideenemy_group.add(self.sideenemy)
            sprite_group.add(self.sideenemy)

    def create_enemy2(self):
        for i in range(2):
            self.enemy2 = Enemy2(enemy2_ship)
            enemy2_group.add(self.enemy2)
            sprite_group.add(self.enemy2)


    def playerbullet_hits_enemy(self):
        hits = pygame.sprite.groupcollide(enemy_group, playerbullet_group, False, True)
        for i in hits:
            self.count_hit += 1
            if self.count_hit == 3:
                expl_x = i.rect.x + 50
                expl_y = i.rect.y + 50
                explosion = Explosion (expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000, -100)
                self.count_hit = 0
                self.score += 1

    def playerbullet_hits_sideenemy(self):
        hits = pygame.sprite.groupcollide(sideenemy_group, playerbullet_group, False, True)
        for i in hits:
            self.count_hit2 += 1
            if self.count_hit2 == 15:
                expl_x = i.rect.x + 60
                expl_y = i.rect.y + 50
                explosion = Explosion (expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = -199
                self.count_hit2 = 0
                self.score += 5

    def playerbullet_hits_enemy2(self):
        hits = pygame.sprite.groupcollide(enemy2_group, playerbullet_group, False, True)
        for i in hits:
            self.count_hit += 1
            if self.count_hit == 5:
                expl_x = i.rect.x + 50
                expl_y = i.rect.y + 50
                explosion = Explosion (expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000, -100)
                self.count_hit = 0
                self.score += 2              

    def enemybullet_hits_player(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemybullet_group, True)
            if hits:
                self.lives -= 1
                self.player.dead()
                if self.lives < 0:
                        pygame.mixer.music.stop()
                        gameover_sound.play()
                        red =pygame.Color(255,0,0)
                        my_font = pygame.font.Font("Pixeled.ttf",90)
                        game_over_surface =  my_font.render('GAME OVER', True, red)
                        game_over_rect = game_over_surface.get_rect()
                        game_over_rect.midtop = (s_width/2, s_height/4)
                        screen.fill((0,0,0))
                        screen.blit(game_over_surface, game_over_rect)
                        pygame.display.flip()
                        time.sleep(11)
                        pygame.quit()
                        sys.exit()

    def sideenemy_hits_player(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, sideenemybullet_group, True)
            if hits:
                self.lives -= 1
                self.player.dead()
                if self.lives < 0:
                    pygame.mixer.music.stop()
                    gameover_sound.play()
                    red =pygame.Color(255,0,0)
                    my_font = pygame.font.Font("Pixeled.ttf",90)
                    game_over_surface =  my_font.render('GAME OVER', True, red)
                    game_over_rect = game_over_surface.get_rect()
                    game_over_rect.midtop = (s_width/2, s_height/4)
                    screen.fill((0,0,0))
                    screen.blit(game_over_surface, game_over_rect)
                    pygame.display.flip()
                    time.sleep(11)
                    pygame.quit()
                    sys.exit()

    def player_enemy_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemy_group, False)
            if hits:
                for i in hits:
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.lives -= 1
                    self.player.dead()
                    if self.lives < 0:
                        pygame.mixer.music.stop()
                        gameover_sound.play()
                        red =pygame.Color(255,0,0)
                        my_font = pygame.font.Font("Pixeled.ttf",90)
                        game_over_surface =  my_font.render('GAME OVER', True, red)
                        game_over_rect = game_over_surface.get_rect()
                        game_over_rect.midtop = (s_width/2, s_height/4)
                        screen.fill((0,0,0))
                        screen.blit(game_over_surface, game_over_rect)
                        pygame.display.flip()
                        time.sleep(11)
                        pygame.quit()
                        sys.exit()

    def player_sideenemy_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, sideenemy_group, False)
            if hits:
                for i in hits:
                    i.rect.x = -199
                    self.lives -= 1
                    self.player.dead()
                    if self.lives < 0:
                        pygame.mixer.music.stop()
                        gameover_sound.play()
                        red =pygame.Color(255,0,0)
                        my_font = pygame.font.Font("Pixeled.ttf",90)
                        game_over_surface =  my_font.render('GAME OVER', True, red)
                        game_over_rect = game_over_surface.get_rect()
                        game_over_rect.midtop = (s_width/2, s_height/4)
                        screen.fill((0,0,0))
                        screen.blit(game_over_surface, game_over_rect)
                        pygame.display.flip()
                        time.sleep(11)
                        pygame.quit()
                        sys.exit()

    def player_enemy2_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemy2_group, False)
            if hits:
                for i in hits:
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.lives -= 1
                    self.player.dead()
                    if self.lives < 0:
                        pygame.mixer.music.stop()
                        gameover_sound.play()
                        red =pygame.Color(255,0,0)
                        my_font = pygame.font.Font("Pixeled.ttf",90)
                        game_over_surface =  my_font.render('GAME OVER', True, red)
                        game_over_rect = game_over_surface.get_rect()
                        game_over_rect.midtop = (s_width/2, s_height/4)
                        screen.fill((0,0,0))
                        screen.blit(game_over_surface, game_over_rect)
                        pygame.display.flip()
                        time.sleep(11)
                        pygame.quit()
                        sys.exit()

    def create_lives(self):
        self.live_img = pygame.image.load(player_ship)
        self.live_img = pygame.transform.scale(self.live_img,(50,50))
        n = 0
        for i in range(self.lives):
            screen.blit(self.live_img, (0+n, s_height-50))
            n += 100

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)

    

    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()
 
    def run_game(self):
        self.create_background()
        self.create_player()
        self.create_enemy()
        self.create_sideenemy()
        self.create_enemy2()
        while True:
            screen.fill('black')
            self.playerbullet_hits_enemy()
            self.playerbullet_hits_sideenemy()
            self.playerbullet_hits_enemy2()
            self.enemybullet_hits_player()
            self.sideenemy_hits_player()
            self.player_enemy_crash()
            self.player_sideenemy_crash()
            self.player_enemy2_crash()
            self.create_lives()
            self.display_score()
            self.run_update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:
                    self.player.shoot()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
 
 
            pygame.display.update()
            clock.tick(FPS)


def main():
    game = Game()
 
if __name__ == '__main__':
    main()