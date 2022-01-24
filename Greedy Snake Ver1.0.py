import sys
import time
import pygame
# 导入random库所有函数
from random import *

# Position类，通过构造函数设置x和y
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# 生成一个坐标随机的食物（不与蛇头重合）
def new_food(head):
    while True:
        # 循环，不断实例化new_food对象直到生成一个不与蛇头重合的食物
        new_food = Position(randint(0, 45) * 20, randint(0, 28) * 20)
        # 若new_food和蛇头重合则不创键
        if new_food.x != head.x and new_food.y != head.y:
            break
        else:
            continue
    return new_food


# 在窗体中绘制贪吃蛇、食物
# 形参：一个是颜色另一个是实例化对象
def draw(color, object):
    pygame.draw.circle(window, color, (object.x, object.y), 10)


# 初始界面和游戏中途点击退出游戏时
def exit_end():
    pygame.quit()
    quit()


# 游戏结束时，显示得分的窗体的设置
def show_end():
    # 设计窗口
    # 定义窗口大小
    small_window = pygame.display.set_mode((960, 600))
    init_background = pygame.image.load("image/init_bgimg.jpg")
    small_window.blit(init_background, (0, 0))
    # 定义标题
    pygame.display.set_caption("贪吃蛇大冒险")
    # 定义提示文字
    font = pygame.font.SysFont("simHei", 40)
    fontsurf = font.render('游戏结束! 你的得分为: %s' % score, False, black)
    small_window.blit(fontsurf, (250, 200))
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    sys.exit()


# 正常模式死亡设置
# head: 蛇头， snake_body:蛇身
def die_snake(head, snake_body):
    # 定义标志，默认为false，true时判定贪吃蛇碰到自己，死亡
    die_flag = False
    # 遍历存放贪吃蛇位姿的列表，从第1个开始，(第0个位蛇头)
    for body in snake_body[1:]:
        # 如果蛇头的xy和蛇身xy相等，则判定相撞，设置flag为ture
        if head.x == body.x and head.y == body.y:
            die_flag = True
    # 若蛇头的xy在显示窗体外，或flag为true，则显示结束界面，并退出游戏
    if die_flag == True or head.x < 0 or head.x > 960 or head.y < 0 or head.y > 600:
        # 停止播放音乐
        pygame.mixer.music.stop()
        show_end()


# 正常模式主体设置
def start_game():
    # 定义存分数的全局变量
    global score
    global color
    global i
    color = (randint(10, 255), randint(10, 255), randint(10, 255))
    # 定义存放玩家键盘输入运动方向的变量，初始为向右
    run_direction = "right"
    # 定义贪吃蛇运动方向的变量，初始为玩家键入方向
    run = run_direction
    # 实例化贪吃蛇和食物对象
    head = Position(randint(0, 30) * 20, randint(0, 20) * 20)
    # 实例化蛇身长度为2个单位
    snake_body = [Position(head.x, head.y + 20), Position(head.x, head.y + 40)]
    # 实例化单个食物，方便循环内生成单个新食物
    food = Position(randint(0, 30) * 20, randint(0, 20) * 20)
    while True:
        window.blit(background, (0,0))
        # 监听玩家键盘输入的运动方向值，并根据输入转为up、down、right或left，方便程序中调用
        # pygame.event.get()返回一个列表，存放本次game执行中程序遇到的一连串事件（按时间顺序依次存放）
        for event in pygame.event.get():
            # pygame.QUIT事件是指用户点击窗口右上角的"×"
            if event.type == pygame.QUIT:
                # 显示结果界面
                show_end()
            # 若事件类型是按下键盘，分↑ ↓ ← →四种情况讨论
            elif event.type == pygame.KEYDOWN:
                # 若事件类型是按下键盘↑
                # key是键值，表示按下去的键值是什么
                if event.key == pygame.K_UP:
                    run_direction = "up"
                # 若事件类型是按下键盘↓
                elif event.key == pygame.K_DOWN:
                    run_direction = "down"
                # 若事件类型是按下键盘←
                elif event.key == pygame.K_LEFT:
                    run_direction = "left"
                # 若事件类型是按下键盘→
                elif event.key == pygame.K_RIGHT:
                    run_direction = "right"
        # 绘制被贪吃蛇吃掉后新增的食物图像
        draw(color,food)
        # 绘制蛇头图像
        draw(black, head)
        # 绘制蛇身图像
        for item in snake_body:
            draw(white, item)
        # 判断贪吃蛇原运动方向(run)与玩家键盘输入的运动方向(run_direction)是否违反正常运动情况
        if run == "up" and not run_direction == "down":
            run = run_direction
        elif run == "down" and not run_direction == "up":
            run = run_direction
        elif run == "left" and not run_direction == "right":
            run = run_direction
        elif run == "right" and not run_direction == "left":
            run = run_direction
        # 插入蛇头位置到蛇身列表中
        snake_body.insert(0, Position(head.x, head.y))
        # 根据玩家键入方向进行蛇头xy的更新
        if run == "up":
            head.y -= 20
        elif run == "down":
            head.y += 20
        elif run == "left":
            head.x -= 20
        elif run == "right":
            head.x += 20
        # 判断是否死亡
        die_snake(head, snake_body)
        # 判断蛇头和食物坐标，若相等，则加分，并生成新的食物
        if head.x == food.x and head.y == food.y:
            score += 1
            food = new_food(head)
            color = (randint(10, 255), randint(10, 255), randint(10, 255))
        else:
            snake_body.pop()
        font = pygame.font.SysFont("simHei", 25)
        mode_title = font.render('正常模式', False, grey)
        socre_title = font.render('得分: %s' % score, False, grey)
        window.blit(mode_title, (50, 30))
        window.blit(socre_title, (50, 65))
        # 更新蛇头蛇身和食物的数据
        pygame.display.update()
        # 通过帧率设置贪吃蛇速度
        clock.tick(10)


# 可穿墙模式死亡设置
# head:蛇头，snake_body:蛇身
def through_snake(head, snake_body):
    # 定义标志位
    die_flag = False
    # 遍历，蛇头碰到蛇身时，flag为true退出游戏
    for body in snake_body[1:]:
        if head.x == body.x and head.y == body.y:
            die_flag = True
    if die_flag:
        pygame.mixer.music.stop()
        show_end()
    else:  # 当蛇头的xy出窗体时
        # 四种穿墙情况，分别设置
        if head.x < 0:
            head.x = 960
        if head.x > 960:
            head.x = 0
        if head.y < 0:
            head.y = 600
        if head.y > 600:
            head.y = 0


# 穿墙模式主体设置
def start_kgame():
    global score
    global color
    color = (randint(10, 255), randint(10, 255), randint(10, 255))
    # 定义蛇初始方向
    run_direction = "up"
    run = run_direction
    # 实例化蛇头、蛇身、食物对象
    head = Position(160, 160)
    # 三格
    snake_body = [Position(head.x, head.y + 20), Position(head.x, head.y + 40), Position(head.x, head.y + 60)]
    # 初始化食物位置
    food = Position(300, 300)
    # 死循环，监听键盘键值
    while True:
        window.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_end()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    run_direction = "up"
                elif event.key == pygame.K_RIGHT:
                    run_direction = "right"
                elif event.key == pygame.K_LEFT:
                    run_direction = "left"
                elif event.key == pygame.K_DOWN:
                    run_direction = "down"
        # 食物
        draw(color, food)
        # 蛇头
        draw(black, head)
        # 蛇身
        for pos in snake_body:
            draw(white, pos)
        # 判断贪吃蛇原运动方向与玩家键盘输入的运动方向是否违反正常运动情况
        if run == "up" and not run_direction == "down":  # 若运动方向为向上，玩家输入运动方向向下，则违背贪吃蛇正常运动情况
            run = run_direction
        elif run == "down" and not run_direction == "up":
            run = run_direction
        elif run == "left" and not run_direction == "right":
            run = run_direction
        elif run == "right" and not run_direction == "left":
            run = run_direction
        # 插入蛇头位置到蛇身列表中
        snake_body.insert(0, Position(head.x, head.y))
        # 根据玩家键入方向进行蛇头xy的更新
        if run == "up":
            head.y -= 20
        elif run == "down":
            head.y += 20
        elif run == "left":
            head.x -= 20
        elif run == "right":
            head.x += 20
        # 穿墙实现
        through_snake(head, snake_body)
        # 判断是否加分和随机生成新的食物
        if head.x == food.x and head.y == food.y:
            score += 1
            food = new_food(head)
            color = (randint(10, 255), randint(10, 255), randint(10, 255))
        else:
            snake_body.pop()
        font = pygame.font.SysFont("simHei", 25)
        mode_title = font.render('穿墙模式', False, grey)
        socre_title = font.render('得分: %s' % score, False, grey)
        window.blit(mode_title, (50, 30))
        window.blit(socre_title, (50, 65))
        # 绘制更新
        pygame.display.update()
        # 通过帧率设置贪吃蛇速度
        clock.tick(8)


# 监听函数，监听鼠标输入
# msg: 按钮信息，x: 按钮的x轴，y: 按钮的y轴，w: 按钮的宽，h: 按钮的高，ic: 按钮初始颜色，ac: 按钮按下颜色，action: 按钮按下的动作
def button(msg, x, y, w, h, ic, ac, action=None):
    # 获取鼠标位置
    mouse = pygame.mouse.get_pos()
    # 获取鼠标点击情况
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))
    # 设置按钮中的文字样式和居中对齐
    font = pygame.font.SysFont('simHei', 20)
    smallfont = font.render(msg, True, white)
    smallrect = smallfont.get_rect()
    smallrect.center = ((x + (w / 2)), (y + (h / 2)))
    window.blit(smallfont, smallrect)


# 游戏初始界面，选择模式
def into_game():
    while True:
        window.blit(init_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_end()
        # 设置字体
        font = pygame.font.SysFont("simHei", 50)
        # 初始界面显示文字
        fontsurf = font.render('欢迎来到贪吃蛇大冒险!', True, black)  # 文字
        fontrect = fontsurf.get_rect()
        fontrect.center = ((width / 2), 200)
        window.blit(fontsurf, fontrect)
        button("正常模式", 370, 370, 200, 40, blue, brightred, start_game)
        button("可穿墙模式", 370, 420, 200, 40, violte, brightred, start_kgame)
        button("退出", 370, 470, 200, 40, red,brightred, exit_end)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    # 定义需要用到的颜色
    white = (255, 255, 255)
    red = (200, 0, 0)
    green = (0, 128, 0)
    blue = (0, 202, 254)
    violte = (194, 8, 234)
    brightred = (255, 0, 0)
    brightgreen = (0, 255, 0)
    black = (0, 0, 0)
    grey = (129, 131, 129)
    score = 0
    # 设计窗口
    # 定义窗口大小
    width = 960
    height = 600
    window = pygame.display.set_mode((width, height))
    # 定义标题
    pygame.display.set_caption("贪吃蛇大冒险")
    # 定义背景图片
    init_background = pygame.image.load("image/init_bgimg.jpg")
    background = pygame.image.load("image/bgimg.jpg")
    # 背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.play(-1)
    # 创建时钟
    clock = pygame.time.Clock()
    # 初始化，自检所有模块是否完整
    pygame.init()
    # 初始界面
    into_game()