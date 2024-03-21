import sys
import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()

        self.score = 0

        self.jump_images = [
            pygame.image.load('Player/PRight1.png').convert_alpha(),
            pygame.image.load('Player/PRight2.png').convert_alpha(),
            pygame.image.load('Player/PRight3.png').convert_alpha()
        ]

        self.jump_frame = 0
        self.is_jumping = False
        self.jump_cooldown = 0
        self.start_jump_y = 0
        self.jump_power = 10
        self.gravity = 1

        self.image = self.jump_images[self.jump_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 380)

        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)

    def jump(self):
        if self.jump_cooldown == 0:
            self.start_jump_y = self.rect.y
            self.velocity.y =- self.jump_power
            self.is_jumping = True
            self.jump_cooldown = 1

    def update(self):
        self.acceleration.y = self.gravity
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.jump()

        self.velocity += self.acceleration
        self.rect.y += self.velocity.y

        if self.rect.top < 20:
            self.rect.top = 20
        if self.rect.bottom > 380:
            self.rect.bottom = 380
            self.is_jumping = False
            self.velocity.y = 0

        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    def draw(self, screen):
        if self.start_jump_y < self.rect.y and self.is_jumping:
            self.image = self.jump_images[2]
        elif self.start_jump_y > self.rect.y and self.is_jumping:
            self.image = self.jump_images[1]
        elif self.is_jumping == False:
            self.image = self.jump_images[0]

        screen.blit(self.image, self.rect)

class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('Game/FlyingEnemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('Game/Rock.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (80, y)
        self.speed = 8
    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 600 or self.rect.right < 0:
            self.kill()


class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('Game/Rock1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = 4

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.buttons = [
            pygame.image.load('Game/ButtonXL.png').convert_alpha(),
            pygame.image.load('Game/ButtonL.png').convert_alpha(),
            pygame.image.load('Game/ButtonM.png').convert_alpha(),
            pygame.image.load('Game/ButtonS.png').convert_alpha(),
            pygame.image.load('Game/ButtonXS.png').convert_alpha(),
            pygame.image.load('Game/ButtonXXS.png').convert_alpha()
        ]
        self.button_frame = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.clik = pygame.Rect(x, y, width, height)
        self.image = self.buttons[self.button_frame]
        self.text = text
        self.font = pygame.font.Font('Nunito-Black.ttf', 20)
        self.action = action

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        if 1 <= self.rect.width <= 40:
            self.image = self.buttons[5]
            self.clik.height = 60
            self.clik.width = 60
        elif 41 <= self.rect.width <= 70:
            self.image = self.buttons[4]
            self.clik.height = 60
            self.clik.width = 136
        elif 71 <= self.rect.width <= 115:
            self.image = self.buttons[3]
            self.clik.height = 60
            self.clik.width = 136
        elif 116 <= self.rect.width <= 150:
            self.image = self.buttons[2]
            self.clik.height = 60
            self.clik.width = 195
        elif 151 <= self.rect.width <= 220:
            self.image = self.buttons[1]
            self.clik.height = 60
            self.clik.width = 242
        elif 221 <= self.rect.width <= 300:
            self.image = self.buttons[0]
            self.clik.height = 60
            self.clik.width = 300
        screen.blit(self.image, self.rect)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) or self.clik.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False


class HighScoreEntry:
    def __init__(self, name, score):
        self.name = name
        self.score = score

high_scores = []

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('Меню')
    icon = pygame.image.load('Game/Game icon.png')
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    def start_game(level):
        pygame.quit()
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption('Игра началась!')
        icon = pygame.image.load('Game/Game icon.png')
        pygame.display.set_icon(icon)

        player = Player(level)
        game_loop(screen, player, level)
        start_game(level)

    def choose_level():
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption('Выбор времени суток')

        clock = pygame.time.Clock()

        background = pygame.image.load('Top_Screen_1.png')

        level_buttons = [
            Button(130, 80, 86, 60, "         День", lambda: start_game(1)),
            Button(130, 140, 86, 60, "        Закат", lambda: start_game(2)),
            Button(130, 200, 86, 60, "        Ночь", lambda: start_game(3)),
            Button(130, 300, 86, 60, "        Назад", main_menu)
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for button in level_buttons:
                    button.handle_event(event)

            screen.fill(WHITE)
            screen.blit(background, (0, 0))

            font = pygame.font.Font("Nunito-Black.ttf", 24)
            text = font.render("Выберите время", True, BLACK)

            screen.blit(text, (80, 25))

            for button in level_buttons:
                button.draw(screen)

            pygame.display.flip()
            clock.tick(60)

    def show_highscores():
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption('Рекорды')
        clock = pygame.time.Clock()
        background_start = pygame.image.load('Top_Screen_1.png')
        back_button = Button(170, 330, 86, 60, "         Назад", main_menu)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if back_button.handle_event(event):
                    return

            screen.fill(WHITE)
            screen.blit(background_start, (0, 0))
            font = pygame.font.Font("Nunito-Black.ttf", 20)
            text_y = 50
            text = font.render("Таблица рекордов:", True, BLACK)
            screen.blit(text, (10, 20))
            text_y += 30

            for entry in high_scores:
                text = font.render(f"{entry.name}: {entry.score}", True, BLACK)
                screen.blit(text, (70, text_y))
                text_y += 30
            back_button.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    buttons = [
        Button(150, 200, 115, 60, "    Старт", lambda: choose_level()),
        Button(100, 260, 220, 60, "    Таблица рекордов", show_highscores),
        Button(100, 320, 220, 60, "   Выйти из игры", sys.exit)
    ]

    backg = pygame.image.load('Title screen1.png').convert()
    logo = pygame.image.load('Game/logo.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for button in buttons:
                button.handle_event(event)

        screen.blit(backg, (0, 0))
        screen.blit(logo, (85, 45))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def game_loop(screen, player, level):
    backgrounds = [
        pygame.image.load('Game/Background.png').convert(),
        pygame.image.load('Game/Background_2.png').convert(),
        pygame.image.load('Game/Background_3.png').convert()
    ]

    collectible_spawn_timer = pygame.time.get_ticks()
    FlyingEnemy_spawn_timer = pygame.time.get_ticks()

    pygame.init()
    clock = pygame.time.Clock()
    player = Player(level)
    projectiles = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    flying_enemies = pygame.sprite.Group()

    player.score = 0
    projectiles_left = 3
    running = True
    flying_enemy_count = 0
    background = backgrounds[level - 1]
    font = pygame.font.Font("Nunito-Black.ttf", 10)
    pygame.mixer.music.load('Music/BackgroundSound.mp3')
    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_e:
                    if projectiles_left > 0:
                        ShootSound = pygame.mixer.Sound('Music/ShootSound.mp3')
                        pygame.mixer.Sound.play(ShootSound)
                        projectiles.add(Projectile(player.rect.right, player.rect.centery))
                        projectiles_left -= 1

        if pygame.time.get_ticks() - FlyingEnemy_spawn_timer > 1500:
            flying_enemies.add(FlyingEnemy(600, random.randint(60, 300)))
            FlyingEnemy_spawn_timer = pygame.time.get_ticks()

            if pygame.time.get_ticks() - collectible_spawn_timer > 3500  :
                collectibles.add(Collectible(600, random.randint(60, 300)))
                collectible_spawn_timer = pygame.time.get_ticks()


        for flying_enemy in flying_enemies:
            if player.rect.colliderect(flying_enemy.rect):
                running = False

        player.update()
        projectiles.update()
        collectibles.update()
        flying_enemies.update()

        for collectible in collectibles:
            if player.rect.colliderect(collectible.rect):
                GetSound = pygame.mixer.Sound('Music/Get.mp3')
                pygame.mixer.Sound.play(GetSound)
                collectible.kill()
                projectiles_left += 1
            if collectible.rect.left < -32:
                collectibles.remove(collectible)

        for projectile in projectiles:
            for flying_enemy in flying_enemies:
                if pygame.sprite.collide_rect(projectile, flying_enemy):
                    flying_enemy.kill()
                    projectile.kill()
                    player.score += 2

        for flying_enemy in flying_enemies:
            if flying_enemy.rect.left < 0:
                flying_enemy_count += 1
                player.score += 1
                flying_enemies.remove(flying_enemy)

        screen.blit(background, (0, 0))
        player.draw(screen)
        projectiles.draw(screen)
        collectibles.draw(screen)
        flying_enemies.draw(screen)
        score_text = font.render(f'СЧЕТ:{player.score}', True, (0, 0, 0))
        screen.blit(score_text, (500, 8))
        projectiles_text = font.render(f'ЗАРЯДОВ:{projectiles_left}', True, (0, 0, 0))
        screen.blit(projectiles_text, (10, 8))
        pygame.display.flip()
        clock.tick(60)

    final_score = player.score
    pygame.mixer.music.stop()
    game_over(final_score)


game_count = 0

def game_over(score):
    global game_count, high_scores
    if score >= 2:
        pygame.quit()
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption('Победа!')
        icon = pygame.image.load('Game/Game icon.png')
        pygame.display.set_icon(icon)
        EndSound = pygame.mixer.Sound('Music/Get.mp3')
        pygame.mixer.Sound.play(EndSound)
        background = pygame.image.load('Win.png')
        font = pygame.font.Font("Nunito-Black.ttf", 20)
        text = font.render(f'Вы победили! Очки: {score}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(280, 60))
        game_count += 1
        restart_button = Button(75, 140, 220, 60, "   Попробовать снова", main_menu)
        menu_button = Button(75, 240, 220, 60, "   Главное меню", main_menu)
        exit_button = Button(130, 300, 115, 60, "  Выйти", sys.exit)

    else:
        pygame.quit()
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption('Игра окончена!')
        icon = pygame.image.load('Game/Game icon.png')
        pygame.display.set_icon(icon)
        EndSound = pygame.mixer.Sound('Music/End.mp3')
        pygame.mixer.Sound.play(EndSound)
        background = pygame.image.load('GameOver.png')
        font = pygame.font.Font("Nunito-Black.ttf", 20)
        text = font.render(f'Вы проиграли! Очки: {score}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(280, 50))
        game_count += 1
        restart_button = Button(180, 100, 220, 60, "   Попробовать снова", main_menu)
        menu_button = Button(180, 180, 220, 60, "   Главное меню", main_menu)
        exit_button = Button(235, 240, 115, 60, "  Выйти", sys.exit)

    clock = pygame.time.Clock()

    high_scores.append(HighScoreEntry(f"Игрок {game_count}", score))
    high_scores.sort(key=lambda entry: entry.score, reverse=True)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            restart_button.handle_event(event)
            menu_button.handle_event(event)
            exit_button.handle_event(event)

        screen.fill((255, 255, 255))
        screen.blit(background, (0,0))
        screen.blit(text, text_rect)
        restart_button.draw(screen)
        menu_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
