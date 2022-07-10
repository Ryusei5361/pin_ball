# 20K0112 大村琉聖
# 最終課題-サブ：ピンボール

from dataclasses import dataclass
import pygame
import random

SCREEN_WIDTH = 800  # 画面の横幅
SCREEN_HEIGHT = 600  # 画面の縦幅

SPEEDS = [-2, -1, 1, 2, 3]  # ボールのx方向初速選択肢
FPS = 100  # 描画間隔(秒)

BLACK = (0, 0, 0)  # 黒
WHITE = (255, 255, 255)  # 白
PURPLE = (167, 87, 168)  # 紫
YELLOW = (255, 255, 0)  # 黄色
BLUE = (0, 0, 255)  # 青
GREEN = (0, 255, 0)  # 緑
RED = (255, 0, 0)  # 赤

BALL_X0 = 570  # ボールの初期位置(x)
BALL_Y0 = 500  # ボールの初期位置(y)
BALL_VX = random.choice(SPEEDS)  # ボールのx軸方向の初速度
BALL_VY = -3  # ボールのy軸方向の初速度
BALL_D = 8  # ボールの直径
BALL_C = GREEN  # ボールの色

PADDLE_X0 = 350  # パドルの初期位置(x)
PADDLE_Y0 = 500  # パドルの初期位置(y)
PADDLE_W = 50  # パドルの横幅
PADDLE_H = 5  # パドルの縦幅
PADDLE_VX = 5  # パドルの移動速度
PADDLE_C = RED  # パドルの色

X_LIST = [240, 280, 320, 360, 400]  # ブロックのx座標のリスト
Y_LIST = [160, 200, 240, 280, 320]  # ブロックのy座標のリスト
random.shuffle(X_LIST)  # ブロックのx座標のリストをシャッフル
random.shuffle(Y_LIST)  # ブロックのy座標のリストをシャッフル

BLOCK_X = X_LIST  # ブロックのx座標
BLOCK_Y = Y_LIST  # ブロックのy座標
BLOCK_W = 50  # ブロックの横幅
BLOCK_H = 10  # ブロックの縦幅
BLOCK_C = BLUE  # ブロックの色

WALL_X = 200  # 壁のx座標
WALL_Y = 10  # 壁のy座標
WALL_W = 400  # 壁の横幅
WALL_H = 550  # 壁の縦幅
WIDTH = 5  # 線の太さ

LINE_Y = 450  # 左右の下にある斜め線のy座標の初期位置
LINE_W = 80  # 線の長さ
LINE_S = 190  # 線と線の間隔

PLUS = 0  # 点数の初期値

NUM_BLOCKS = len(X_LIST)  # 配置するブロックの個数

pygame.init()  # pygameを初期化
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # SCREEN_WIDTH×SCREEN_HEIGHTのscreenを生成
image2 = pygame.image.load("GAME_OVER.jpg").convert_alpha()  # GameOverの画像を読み込む
image2 = pygame.transform.scale(image2, (SCREEN_WIDTH, SCREEN_HEIGHT))  # GameOverの画像の大きさを調整

clock = pygame.time.Clock()  # 時計オブジェクト
font = pygame.font.SysFont('commissars', 35)  # フォントの設定
font2 = pygame.font.SysFont('commissars', 60)  # フォントの設定


# -------------------------------------------------------------------
@dataclass  # ボールのクラス
class Ball:
    x: int
    y: int
    vx: int
    vy: int


@dataclass  # パドルのクラス
class Paddle:
    x: int
    y: int
    vx: int


# -------------------------------------------------------------------
# ボールの描画
def draw_ball(x, y):
    return pygame.draw.circle(screen, GREEN, (x, y), BALL_D)


# -------------------------------------------------------------------
# パドルの描画
def draw_paddle(x, y):
    return pygame.draw.rect(screen, RED, (x, y, PADDLE_W, PADDLE_H))


# -------------------------------------------------------------------
# 全体の再描画
def redraw():
    draw_walls(WALL_X, WALL_Y, WALL_W, WALL_H)
    draw_line(WALL_X, PADDLE_Y0, LINE_W, LINE_S, WIDTH)
    make_blocks(NUM_BLOCKS, BLOCK_X, BLOCK_Y, BLOCK_W, BLOCK_H, BLOCK_C)
    make_score(PLUS)


# -------------------------------------------------------------------
# blockに関して
# ブロックの描画
def make_block(x, y, w, h, c):
    return pygame.draw.rect(screen, c, (x, y, w, h))


# ブロックをまとめて描画
def make_blocks(n_rows, x0, y0, w, h, c):
    blocks = []
    for x in range(n_rows):
        blocks.append(make_block(x0[x], y0[x], w, h, c))
    return blocks


# -------------------------------------------------------------------
# wallに関して
# 壁の描画
def draw_walls(ox, oy, width, height):
    pygame.draw.rect(screen, WHITE, (ox, oy, width, height))


# 線の描画
def draw_line(x, y, w, s, WIDTH):
    pygame.draw.line(screen, BLACK, (x, y), (x + w, y), WIDTH)  # 左下の直線の描画
    pygame.draw.line(screen, BLACK, (x + w + s, y), (x + s + w * 2, y), WIDTH)  # 右下の直線の描画
    pygame.draw.rect(screen, BLACK, ((x + WALL_W) * 4 / 5, WALL_Y, (x + WALL_W) * 1 / 5, y * 1 / 7), WIDTH)  # 右上の四角の描画
    pygame.draw.rect(screen, BLACK, (x, WALL_Y, (x + WALL_W) * 1 / 7, y * 1 / 7), WIDTH)  # 左上の四角の描画
    pygame.draw.line(screen, BLACK, (x + s + w * 2, (WALL_Y + WALL_H) * 2 / 5), (x + s + w * 2, WALL_Y + WALL_H),
                     WIDTH)  # 射出口の線の描画
    return pygame.draw.rect(screen, BLACK, ((x + WALL_W) * 4 / 5, WALL_Y, x + WALL_W, y * 1 / 7), WIDTH), \
           pygame.draw.rect(screen, BLACK, (x, WALL_Y, (x + WALL_W) * 1 / 7, y * 1 / 7), WIDTH)


# -------------------------------------------------------------------
# 点数の表示
def make_score(point):
    text = font.render("Score : " + str(point), True, WHITE)
    screen.blit(text, (650, 30))


# ===================================================================
# -------------------------------------------------------------------
# 下準備(壁の描画、線の描画、パドルの描画、ボールの描画、ブロックの描画、スコアの描画)
draw_walls(WALL_X, WALL_Y, WALL_W, WALL_H)
wall_rect1, wall_rect2 = draw_line(WALL_X, PADDLE_Y0, LINE_W, LINE_S, WIDTH)
draw_paddle(PADDLE_X0, PADDLE_Y0)
draw_ball(BALL_X0, BALL_Y0)
blocks = make_blocks(NUM_BLOCKS, BLOCK_X, BLOCK_Y, BLOCK_W, BLOCK_H, BLOCK_C)
make_score(PLUS)
# パドルとボールのインスタンス化
paddle = Paddle(PADDLE_X0, PADDLE_Y0, PADDLE_VX)
ball = Ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY)
# -------------------------------------------------------------------
# 各while文のための変数
game_start = False
game_over = False
loop = True
fin = False
while not game_start:  # ひたすら SPACE を待つ
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT:
            game_start = True  # ゲームを開始せずに終了させる、つまり何も描画しない
            loop = False
    pressed_keys = pygame.key.get_pressed()  # キー入力情報を一括で取得
    # スペースが押されたら、ゲーム開始
    if pressed_keys[pygame.K_SPACE]:
        game_start = True
        break
    text1 = font.render("If you push 'SPACE', ", False, RED)
    text2 = font.render("this game will start.", False, RED)
    screen.blit(text1, (280, 100))  # screenにtext1を転送する
    screen.blit(text2, (280, 130))  # screenにtext2を転送する
    pygame.display.flip()  # ディスプレイに表示

# -------------------------------------------------------------------
# メインループ
while loop:
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT:
            loop = False
    clock.tick(FPS)  # 毎秒の呼び出し回数に合わせて遅延
    pressed_keys = pygame.key.get_pressed()  # キー入力情報を一括で取得
    # 右矢印キーを押した
    if pressed_keys[pygame.K_RIGHT]:
        # パドルを右に移動
        paddle.x += paddle.vx
    # 左矢印キーを押した
    elif pressed_keys[pygame.K_LEFT]:
        # パドルを左に移動
        paddle.x -= paddle.vx
    redraw()  # 全体を再描画
    ball.x += ball.vx  # ボールの右移動
    ball.y += ball.vy  # ボールの左移動
    ball_rect = draw_ball(ball.x, ball.y)  # ボールを取得
    paddle_rect = draw_paddle(paddle.x, paddle.y)  # パドルを取得

    if paddle.x <= WALL_X + LINE_W:  # パドルが左下の線を越えないようにする
        paddle.x = WALL_X + LINE_W
    if paddle.x + PADDLE_W >= WALL_X + LINE_W + LINE_S:  # パドルが右下の線を超えないにする
        paddle.x = WALL_X + LINE_W + LINE_S - PADDLE_W

    if ball.x + ball.vx < WALL_X:  # 左側の壁で跳ね返る
        ball.vx = -ball.vx
    if ball.x + ball.vx >= WALL_X + WALL_W:  # 右側の壁で跳ね返る
        ball.vx = -ball.vx
    if ball.y + ball.vy < WALL_Y:  # 上側の壁で跳ね返る
        ball.vy = -ball.vy
    if ball.y + ball.vy >= WALL_Y + WALL_H \
            and WALL_X + LINE_W * 2 + LINE_S <= ball.x + ball.vx <= WALL_X + WALL_W:  # 射出口の下側の壁で跳ね返る
        ball.vy = -ball.vy
    if (ball.y + ball.vy >= WALL_Y + WALL_H) \
            and (WALL_X <= ball.x + ball.vx <= WALL_X + LINE_W * 2 + LINE_S):  # 射出口以外の下側の壁に達したら終了
        game_over = True
        break
    # パドルにあたったら、ボールを跳ね返す。
    if ball_rect.colliderect(paddle_rect):
        ball.vy = -ball.vy

    # 射出口の壁の跳ね返り
    if (WALL_X + LINE_S + LINE_W * 2 - 1 <= ball.x <= WALL_X + LINE_S + LINE_W * 2 or ball.x >= WALL_X + WALL_W) \
            and (WALL_Y + WALL_H >= ball.y >= (WALL_Y + WALL_H) * 2 / 5):
        ball.vx = -ball.vx

    speed_x = [ball.vx, -ball.vx]
    # 右上の直線での跳ね返り
    if wall_rect1.colliderect(ball_rect):
        ball.vx = random.choice(speed_x)
        ball.vy = -ball.vy

    # 左上の直線での跳ね返り
    if wall_rect2.colliderect(ball_rect):
        ball.vx = random.choice(speed_x)
        ball.vy = -ball.vy

    # 左下の直線での跳ね返り
    if WALL_X <= ball.x <= WALL_X + LINE_W:
        if PADDLE_Y0 < ball.y + ball.vy < PADDLE_Y0 + 5:
            ball.vx = random.choice(speed_x)
            ball.vy = -ball.vy

    # 右下の直線での跳ね返り
    if WALL_X + LINE_W + LINE_S <= ball.x + ball.vx <= WALL_X + LINE_W * 2 + LINE_S:
        if PADDLE_Y0 < ball.y + ball.vy < PADDLE_Y0 + 5:
            ball.vx = random.choice(speed_x)
            ball.vy = -ball.vy

    # ブロックにあたったら、点数を増やす。
    for block in blocks:
        block_rect = block  # ブロックを取得
        if block_rect.colliderect(ball_rect):
            ball.vy = -ball.vy
            PLUS = PLUS + 1  # 点数を増やす。
            make_score(PLUS)  # スコアを再表示
    pygame.display.flip()  # ディスプレイに表示
    screen.fill(BLACK)  # 黒で塗りつぶす：次のflipまで反映されない

# 発射口以外の床についてしまったら、GameOverの画面を表示させる
while game_over:
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT:
            game_over = False
    # ゲームを終了させるには、右上の×を押すと表示
    text = font2.render("If you want to finish, please click ×.", True, RED)
    screen.blit(image2, (0, 0))  # GameOverの画像をscreenに転送
    screen.blit(text, (50, 500))  # text4をscreenに転送
    pygame.display.flip()

pygame.quit()
