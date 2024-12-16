import pygame
import random
from time import sleep
from os import walk


# Khởi tạo
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()


# Background
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
def loadImage(path):
    return pygame.image.load(path).convert_alpha()


# Nền bắt đầu game
pygame.display.set_caption('Last mile delivery')
icon = loadImage(r'd:\assets\pl.PNG')
pygame.display.set_icon(icon)


# Tải ảnh
bg = loadImage(r'd:\assets\bg.png')
h0 = loadImage(r'd:\assets\house0.png')
t0 = loadImage(r'd:\assets\tree0.png')
h1 = loadImage(r'd:\assets\house1.png')
t1 = loadImage(r'd:\assets\tree1.png')
h2 = loadImage(r'd:\assets\house2.png')
jump_obstacle_img = loadImage(r'd:\assets\jump.png')
duck_obstacle_img = loadImage(r'd:\assets\chim.png')
stop_obstacle_img = loadImage(r'd:\assets\den.png')
fuel_img = loadImage(r'd:\assets\fuel.png')
water_img = loadImage(r'd:\assets\water.png')
tips_img = loadImage(r'd:\assets\tip.png')
player_img = loadImage(r'd:\assets\player_level1.PNG')
start_screen_bg = pygame.image.load(r'd:\assets\start_screen_bg.png').convert()
player_img_level3 = loadImage(r'd:\assets\player_level3.PNG')
player_img_level2 = loadImage(r'd:\assets\pl.PNG')
win_img = loadImage(r'd:\assets\win.png')
game_over_img = loadImage(r'd:\assets\game_over.png')


# Âm thanh
audio = {}
for _, __, sound_files in walk(r'd:\assets'):
    for sound_file in sound_files:
        if sound_file.endswith(".wav"):
            key = sound_file.replace(".wav", "")
            audio[key] = pygame.mixer.Sound(r'd:\assets\\' + sound_file)


if "bg_music" in audio:
    audio["bg_music"].play(-1)
else:
    print("Không tìm thấy file bg_music.wav trong thư mục d:\\assets")


# Các biến cơ bản
bg_x, bg_y = 0, 10
x_def = 5
x_def_hold = x_def
score = 0
level = 1
items_collected = 0
player_y = 450
player_velocity_y = 0
is_jumping = False
is_ducking = False
is_stopped = False
result = "lose"


# Người chơi
player_img = pygame.transform.scale(player_img, (100, 100))
player_rect = player_img.get_rect(topleft=(200, player_y))


# Font chữ
font = pygame.font.Font(None, 36)
try:
    result_font = pygame.font.Font(r'd:\assets\font.otf', 200)
except FileNotFoundError:
    print("Font file not found. Using default font.")
    result_font = pygame.font.SysFont("arial", 200)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Hiển thị màn hình bắt đầu
def show_start_screen():
    while True:
        SCREEN.blit(start_screen_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # Thoát vòng lặp và bắt đầu trò chơi
        pygame.display.flip()
        clock.tick(60)


# Lớp chướng ngại vật
class Obstacle:
    def __init__(self, x, y, width, height, image, type):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = type
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


# Lớp vật phẩm hỗ trợ
class Item:
    def __init__(self, x, y, width, height, image, item_type):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.item_type = item_type
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


# Hàm tạo chướng ngại vật
def create_obstacle():
    obstacle_type = random.choice(["jump", "duck", "stop"])
    x = SCREEN_WIDTH + random.randint(100, 300)
    if obstacle_type == "jump":
        return Obstacle(x, 480, 70, 70, jump_obstacle_img, "jump")
    elif obstacle_type == "duck":
        return Obstacle(x, 410, 60, 60, duck_obstacle_img, "duck")
    elif obstacle_type == "stop":
        return Obstacle(x, 400, 150, 150, stop_obstacle_img, "stop")


# Hàm tạo vật phẩm
def create_item():
    item_type = random.choice(["fuel", "water", "tip"])
    width, height = 50, 50
    x = SCREEN_WIDTH + random.randint(100, 300)
    if item_type == "fuel":
        return Item(x, 450, width, height, fuel_img, "fuel")
    elif item_type == "water":
        return Item(x, 450, width, height, water_img, "water")
    elif item_type == "tip":
        return Item(x, 350, width, height, tips_img, "tip")


# Tập hợp các đối tượng nhà và cây
objects = [
    {"image": h0, "x": 1100, "y": player_y - 190},
    {"image": t0, "x": 900, "y": player_y - 190},
    {"image": h1, "x": 550, "y": player_y - 250},
    {"image": t1, "x": 350, "y": player_y - 120},
    {"image": h2, "x": 20, "y": player_y - 320},
]
#nền kết thúc game
def show_game_over_screen(result, score):
    while True:
        if result == "win":
            SCREEN.blit(win_img, (0, 0))
        elif result == "lose":
            SCREEN.blit(game_over_img, (0, 0))
        else:
            SCREEN.fill(BLACK)


        # Hiển thị điểm và các hướng dẫn
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        restart_text = font.render("Press SPACE to Restart", True, BLACK)
        quit_text = font.render("Press Q to Quit", True, BLACK)


        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT - 150))
        SCREEN.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT - 100))
        SCREEN.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT - 50))


        pygame.display.flip()


        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Restart game
                    return "restart"  # Trả về chuỗi "restart"
                if event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    exit()


#list chướng ngại vật, vật phẩm
items = []
obstacles = []


# Hiển thị màn hình bắt đầu
show_start_screen()
while True:
    # Đặt lại trạng thái ban đầu
    result = "lose"
    score = 0
    level = 1
    items_collected = 0
    player_y = 450
    player_velocity_y = 0
    is_jumping = False
    is_ducking = False
    is_stopped = False
    bg_x = 0
    x_def = 5
    x_def_hold = x_def
    items = []
    obstacles = []


    # Hiển thị màn hình bắt đầu
    show_start_screen()


    # Vòng lặp chính của trò chơi
    running = True
    item_timer = 0
    obstacle_timer = 0
    while running:
        x_def += 0.01
        x_def_hold += 0.001


        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        # Xử lý phím bấm
        player_rect.y = player_y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not is_jumping:
            is_jumping = True
            player_velocity_y = -20
        if keys[pygame.K_DOWN]:
            is_ducking = True
            player_img = pygame.transform.scale(player_img, (100, 50))
            player_rect = player_img.get_rect(topleft=(200, player_y + 50))
        else:
            is_ducking = False
            player_img = pygame.transform.scale(player_img, (100, 100))
            player_rect = player_img.get_rect(topleft=(200, player_y))
        if keys[pygame.K_LEFT]:
            is_stopped = True
            x_def = 2
        else:
            is_stopped = False
            x_def = x_def_hold


        # Xử lý nhảy
        if is_jumping:
            player_velocity_y += 1
            player_y += player_velocity_y
            if player_y >= 450:
                player_y = 450
                is_jumping = False


        # Tạo vật phẩm và chướng ngại vật
        item_timer += 1
        obstacle_timer += 1
        if item_timer > 60 * 5:
            items.append(create_item())
            item_timer = 0
        if obstacle_timer > 60 * 3:
            obstacles.append(create_obstacle())
            obstacle_timer = 0


        # Cập nhật các đối tượng nền
        SCREEN.blit(bg, (bg_x, bg_y))
        SCREEN.blit(bg, (bg_x + SCREEN_WIDTH, bg_y))
        bg_x -= x_def
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0


        # Vẽ các đối tượng (nhà, cây)
        for obj in objects:
            obj["x"] -= x_def
            SCREEN.blit(obj["image"], (obj["x"], obj["y"]))
            if obj["x"] <= -obj["image"].get_width():
                obj["x"] = SCREEN_WIDTH


        # Vẽ vật phẩm và xử lí va chạm
        for item in items[:]:
            item.rect.x -= x_def
            item.draw(SCREEN)
            if item.rect.right < 0:
                items.remove(item)
            elif player_rect.colliderect(item.rect):
                if item.item_type == "fuel":
                    score += 20
                    audio["point"].play()
                elif item.item_type == "water":
                    score += 15
                    audio["point"].play()
                elif item.item_type == "tip":
                    score += 25
                    audio["point"].play()
                items_collected += 1
                items.remove(item)


        # Vẽ chướng ngại vật và xử lí va chạm
        for obstacle in obstacles[:]:
            obstacle.rect.x -= x_def
            obstacle.draw(SCREEN)
            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.remove(obstacle)
            elif player_rect.colliderect(obstacle.rect):
                if (obstacle.type == "jump" and not is_jumping) or \
                   (obstacle.type == "duck" and not is_ducking) or \
                   (obstacle.type == "stop" and not is_stopped):
                    running = False
                    x_def = 0
                    audio["hit"].play()


        # Vẽ người chơi
        SCREEN.blit(player_img, (player_rect.x, player_rect.y))
        # Hiển thị điểm số và cấp độ
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        SCREEN.blit(score_text, (10, 10))
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        SCREEN.blit(level_text, (10, 50))


        # Kiểm tra level
        if score >= 100 and level < 2:
            level = 2
            audio["lv_up"].play()
            player_img = player_img_level2
        if score >= 300 and level < 3:
            level = 3
            audio["lv_up"].play()
            player_img = player_img_level3
        if score >= 600:
            result = "win"
            audio["lv_up"].play()
            running = False


        pygame.display.flip()
        if not running:
            sleep(1)


    # Hiển thị màn hình kết thúc
    action = show_game_over_screen(result, score)
    if action == "restart":
        continue
    else:
        break  





