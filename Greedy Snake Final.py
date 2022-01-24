import sys
import pygame
from random import *

# Snake类，通过构造函数设置蛇头蛇身的位置
class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Food类，通过构造函数设置食物的位置和颜色
class Food:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# 生成一个坐标随机的食物（不与蛇头重合）
def new_food(head):
    while True:
        # 循环，不断实例化new_food对象直到生成一个不与蛇头重合的食物
        new_food = Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))
        # 若new_food和蛇头重合则不创键
        if new_food.x != head.x and new_food.y != head.y:
            break
        else:
            continue
    return new_food


# 在窗体中绘制贪吃蛇
# 形参：一个是颜色另一个是实例化对象
def draw_snake(color, object):
    pygame.draw.circle(window, color, (object.x, object.y), 10)


# 在窗体中绘制食物
# 形参：实例化对象
def draw_food(food):
    pygame.draw.circle(window, food.color, (food.x, food.y), 10)


# 构造函数绘制帮助窗口
def help():
    # 死循环监听鼠标动作和不断渲染画面
    while True:
        window.blit(init_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_end()
        # 设置帮助内容文字
        font = pygame.font.SysFont("simHei", 30)
        fontsurf = font.render("游戏说明", True, black)
        fontrect = fontsurf.get_rect()
        fontrect.center = (480, 50)
        window.blit(fontsurf, fontrect)
        fontsurf1 = font.render("单人模式", True, black)
        fontrect1 = fontsurf1.get_rect()
        fontrect1.center = (180, 150)
        window.blit(fontsurf1, fontrect1)
        fontsurf2 = font.render("双人模式", True, black)
        fontrect2 = fontsurf2.get_rect()
        fontrect2.center = (780, 150)
        window.blit(fontsurf2, fontrect2)
        font = pygame.font.SysFont("simHei", 15)
        fontsurf1_1 = font.render("玩家通过键盘的wsad控制贪吃蛇的移动方向", True, black)
        fontrect1_1 = fontsurf1_1.get_rect()
        fontrect1_1.center = (180, 300)
        window.blit(fontsurf1_1, fontrect1_1)
        fontsurf1_1 = font.render("玩家1通过键盘的wsad控制蓝色贪吃蛇的移动方向", True, black)
        fontrect1_1 = fontsurf1_1.get_rect()
        fontrect1_1.center = (780, 300)
        window.blit(fontsurf1_1, fontrect1_1)
        fontsurf1_1 = font.render("玩家2通过键盘的↑↓←→控制绿色贪吃蛇的移动方向", True, black)
        fontrect1_1 = fontsurf1_1.get_rect()
        fontrect1_1.center = (780, 320)
        window.blit(fontsurf1_1, fontrect1_1)
        button("返回主菜单", 370, 520, 200, 40, blue, green, into_game)
        pygame.display.update()
        clock.tick(20)


# 在初始界面和游戏结束显示得分界面点击右上角的"×"时，直接退出整个游戏
def exit_end():
    pygame.quit()
    sys.exit()


# 游戏结束时，单人模式显示得分的窗体的设置
def show_end_single():
    while True:
        window.blit(init_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_end()
        # 定义标题
        pygame.display.set_caption("贪吃蛇大冒险")
        # 定义提示文字
        font = pygame.font.SysFont("simHei", 40)
        fontsurf = font.render('游戏结束! 你的得分为: %s' % score, False, black)
        window.blit(fontsurf, (250, 100))
        button("返回主菜单", 370, 300, 200, 40, blue, brightred, into_game)
        button("退出游戏", 370, 470, 200, 40, red, brightred, exit_end)
        pygame.display.update()
        clock.tick(20)


# 游戏结束时，双人模式显示得分的窗体的设置
def show_end_double():
    while True:
        window.blit(init_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_end()
        # 定义标题
        pygame.display.set_caption("贪吃蛇大冒险")
        # 定义提示文字
        font = pygame.font.SysFont("simHei", 40)
        fontsurf = font.render('游戏结束! 玩家1得分: %s 玩家2得分：%s' % (score1, score2), True, black)
        window.blit(fontsurf, (150, 100))
        button("返回主菜单", 370, 300, 200, 40, blue, brightred, into_game)
        button("退出游戏", 370, 470, 200, 40, red, brightred, exit_end)
        pygame.display.update()
        clock.tick(20)


# 单人正常模式主体设置
def start_game_single():
    # 播放音乐
    pygame.mixer.music.play(-1)
    # 定义存分数的全局变量
    global score
    score = 0
    # 定义存放玩家键盘输入运动方向的变量，初始为向右
    run_direction = "right"
    # 定义贪吃蛇运动方向的变量，初始为玩家键入方向
    run = run_direction
    # 实例化贪吃蛇和食物对象
    head = Snake(randint(0, 30) * 20, randint(0, 20) * 20)
    # 实例化蛇身长度为2个单位
    snake_body = [Snake(head.x, head.y + 20), Snake(head.x, head.y + 40)]
    # 实例化食物列表，列表随着其中食物被吃掉应该不断缩短
    food_list = [Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))]
    for i in range(1,24):
        food_list.append(Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255))))
    # 实例化单个食物，方便循环内生成单个新食物
    food = Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))
    while True:
        window.blit(background, (0,0))
        # 监听玩家键盘输入的运动方向值，并根据输入转为up、down、right或left，方便程序中调用
        # pygame.event.get()返回一个列表，存放本次game执行中程序遇到的一连串事件（按时间顺序依次存放）
        for event in pygame.event.get():
            # pygame.QUIT事件是指用户点击窗口右上角的"×"
            if event.type == pygame.QUIT:
                # 显示结果界面
                show_end_single()
            # 若事件类型是按下键盘，分↑ ↓ ← →四种情况讨论
            elif event.type == pygame.KEYDOWN:
                # 若事件类型是按下键盘w
                # key是键值，表示按下去的键值是什么
                if event.key == ord('w'):
                    run_direction = "up"
                # 若事件类型是按下键盘s
                if event.key == ord('s'):
                    run_direction = "down"
                # 若事件类型是按下键盘a
                if event.key == ord('a'):
                    run_direction = "left"
                # 若事件类型是按下键盘d
                if event.key == ord('d'):
                    run_direction = "right"
        # 绘制初始化的25个食物图像(24+1=25)
        # 随着该列表中的食物被吃掉，列表应该不断pop以清除已经被吃的事物
        for item in food_list:
            draw_food(item)
        # 绘制被贪吃蛇吃掉后新增的食物图像
        draw_food(food)
        # 绘制蛇头图像
        draw_snake(black, head)
        # 绘制蛇身图像
        for item in snake_body:
            draw_snake(blue, item)
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
        snake_body.insert(0, Snake(head.x, head.y))
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
        die_flag = False
        # 遍历存放蛇身的列表，从第1个开始，(第0个位蛇头)
        for body in snake_body[1:]:
            # 如果蛇头的xy和蛇身xy相等，则判定相撞，设置flag为ture
            if head.x == body.x and head.y == body.y:
                die_flag = True
        # 若蛇头的xy在显示窗体外，或flag为true，则显示结束界面，并退出游戏
        if die_flag == True or head.x < 0 or head.x > 960 or head.y < 0 or head.y > 600:
            # 停止播放音乐
            pygame.mixer.music.stop()
            show_end_single()
        # die_snake(head, snake_body)
        # 判断蛇头和食物坐标，若相等，则加分，并生成新的食物
        # 定义标志，表明是否找到和蛇头相等的事物
        global flag
        flag = 0
        # 如果蛇头和食物重合
        for item in food_list:
            if head.x == item.x and head.y == item.y or head.x == food.x and head.y == food.y:
                flag = 1
                score += 1
                # 弹出被吃掉的这个食物
                food_list.pop(food_list.index(item))
                # 再产生一个食物
                food = new_food(head)
                # 把新食物插入food_list，下一次循环中会更新绘制食物全体
                food_list.append(food)
                break
        # 若没吃到食物则从蛇身pop一个元素以更新蛇位置
        if flag == 0:
            snake_body.pop()
        font = pygame.font.SysFont("simHei", 25)
        mode_title = font.render('正常模式', False, grey)
        socre_title = font.render('得分: %s' % score, False, grey)
        window.blit(mode_title, (50, 30))
        window.blit(socre_title, (50, 65))
        # 更新蛇头蛇身和食物的数据
        pygame.display.update()
        # 通过帧率设置贪吃蛇速度
        clock.tick(8)


# 单人穿墙模式主体设置
def start_kgame_single():
    # 播放音乐
    pygame.mixer.music.play(-1)
    global score
    score = 0
    # 定义存放玩家键盘输入运动方向的变量，初始为向右
    run_direction = "right"
    # 定义贪吃蛇运动方向的变量，初始为玩家键入方向
    run = run_direction
    # 实例化蛇头、蛇身、食物对象
    head = Snake(160, 160)
    # 实例化蛇身
    snake_body = [Snake(head.x, head.y + 20), Snake(head.x, head.y + 40), Snake(head.x, head.y + 60)]
    # 实例化食物列表，列表随着其中食物被吃掉应该不断缩短
    food_list = [Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))]
    for i in range(1,24):
        food_list.append(Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255))))
    # 实例化单个食物，方便循环内生成单个新食物
    food = Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))
    # 死循环，监听键盘键值
    while True:
        window.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_end_single()
            elif event.type == pygame.KEYDOWN:
                # 若事件类型是按下键盘w
                # key是键值，表示按下去的键值是什么
                if event.key == ord('w'):
                    run_direction = "up"
                # 若事件类型是按下键盘s
                if event.key == ord('s'):
                    run_direction = "down"
                # 若事件类型是按下键盘a
                if event.key == ord('a'):
                    run_direction = "left"
                # 若事件类型是按下键盘d
                if event.key == ord('d'):
                    run_direction = "right"
        # 绘制初始化的25个食物图像(24+1=25)
        # 随着该列表中的食物被吃掉，列表应该不断pop以清除已经被吃的事物
        for item in food_list:
            draw_food(item)
        # 绘制被贪吃蛇吃掉后新增的食物图像
        draw_food(food)
        # 绘制蛇头图像
        draw_snake(black, head)
        # 绘制蛇身图像
        for item in snake_body:
            draw_snake(blue, item)
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
        snake_body.insert(0, Snake(head.x, head.y))
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
        # 定义标志位
        die_flag = False
        # 遍历，蛇头碰到蛇身时，flag为true退出游戏
        for body in snake_body[1:]:
            if head.x == body.x and head.y == body.y:
                die_flag = True
        if die_flag:
            pygame.mixer.music.stop()
            show_end_single()
        else: 
            # 当蛇头穿出窗体时有四种情况，分别讨论
            if head.x < 0:
                head.x = 960
            if head.x > 960:
                head.x = 0
            if head.y < 0:
                head.y = 600
            if head.y > 600:
                head.y = 0
        # 判断蛇头和食物坐标，若相等，则加分，并生成新的食物
        # 定义标志，表明是否找到和蛇头相等的事物
        global flag
        flag = 0
        # 如果蛇头和食物重合
        for item in food_list:
            if head.x == item.x and head.y == item.y or head.x == food.x and head.y == food.y:
                flag = 1
                score += 1
                # 弹出被吃掉的这个食物
                food_list.pop(food_list.index(item))
                # 再产生一个食物
                food = new_food(head)
                # 把新食物插入food_list，下一次循环中会更新绘制食物全体
                food_list.append(food)
                break
        # 若没吃到食物则从蛇身pop一个元素以更新蛇位置
        if flag == 0:
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


# 双人正常模式主体设置
def start_game_double():
    # 播放音乐
    pygame.mixer.music.play(-1)
    # 定义存分数的全局变量
    global score1
    global score2
    score1 = score2 = 0
    # 初始化存放玩家键盘输入运动方向的变量
    run_direction1 = "right"
    run_direction2 = "up"
    # 初始化贪吃蛇运动方向的变量
    run1 = run_direction1
    run2 = run_direction2
    # 实例化贪吃蛇和食物对象
    head1 = Snake(randint(0, 30) * 20, randint(0, 20) * 20)
    head2 = Snake(randint(0, 30) * 20, randint(0, 20) * 20)
    # 实例化蛇身长度为2个单位
    snake_body1 = [Snake(head1.x, head1.y + 20), Snake(head1.x, head1.y + 40)]
    snake_body2 = [Snake(head2.x, head2.y + 20), Snake(head2.x, head2.y + 40)]
    # 实例化食物列表，列表随着其中食物被吃掉应该不断缩短
    food_list = [Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))]
    for i in range(1,24):
        food_list.append(Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255))))
    # 实例化单个食物，方便循环内生成单个新食物
    food = Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))
    while True:
        window.blit(background, (0,0))
        # 监听玩家键盘输入的运动方向值，并根据输入转为up、down、right或left，方便程序中调用
        # pygame.event.get()返回一个列表，存放本次game执行中程序遇到的一连串事件（按时间顺序依次存放）
        for event in pygame.event.get():
            # pygame.QUIT事件是指用户点击窗口右上角的"×"
            if event.type == pygame.QUIT:
                # 显示结果界面
                show_end_double()
            # 若事件类型是按下键盘，分↑ ↓ ← →四种情况讨论
            elif event.type == pygame.KEYDOWN:
                # 若事件类型是按下键盘↑
                # key是键值，表示按下去的键值是什么
                if event.key == pygame.K_UP:
                    run_direction2 = "up"
                # 若事件类型是按下键盘↓
                if event.key == pygame.K_DOWN:
                    run_direction2 = "down"
                # 若事件类型是按下键盘←
                if event.key == pygame.K_LEFT:
                    run_direction2 = "left"
                # 若事件类型是按下键盘→
                if event.key == pygame.K_RIGHT:
                    run_direction2 = "right"
                # 若事件类型是按下键盘↑
                if event.key == ord('w'):
                    run_direction1 = "up"
                # 若事件类型是按下键盘↓
                if event.key == ord('s'):
                    run_direction1 = "down"
                # 若事件类型是按下键盘←
                if event.key == ord('a'):
                    run_direction1 = "left"
                # 若事件类型是按下键盘→
                if event.key == ord('d'):
                    run_direction1 = "right"
        # 绘制初始化的25个食物图像(24+1=25)
        # 随着该列表中的食物被吃掉，列表应该不断pop以清除已经被吃的事物
        for item in food_list:
            draw_food(item)
        # 绘制被贪吃蛇吃掉后新增的食物图像
        draw_food(food)
        # 绘制蛇头图像
        # 在绘制蛇头之前先检查是不是已经死亡，如果已死亡，则不绘制
        # ！！不能通过die_flag判断是否死亡因为每次循环一开头die_flag都初始化为False
        # 因此最好的方法是通过snake_body是否为空判断
        if len(snake_body1) != 0:
            draw_snake(black, head1)
        if len(snake_body2) != 0:
            draw_snake(black, head2)
        # 绘制蛇身图像，蛇1是蓝色
        for item in snake_body1:
            draw_snake(blue, item)
        # 绘制蛇身图像，蛇2是绿色
        for item in snake_body2:
            draw_snake(green, item)
        # 若蛇未死亡，则插入蛇头位置到蛇身列表中
        # 即：若蛇已死亡，则保持snake_body为空不变
        if len(snake_body1) != 0:
            snake_body1.insert(0, Snake(head1.x, head1.y))
        if len(snake_body2) != 0:
            snake_body2.insert(0, Snake(head2.x, head2.y))
        # 判断贪吃蛇原运动方向(run)与玩家键盘输入的运动方向(run_direction)是否违反正常运动情况
        if run1 == "up" and not run_direction1 == "down":
            run1 = run_direction1
        if run1 == "down" and not run_direction1 == "up":
            run1 = run_direction1
        if run1 == "left" and not run_direction1 == "right":
            run1 = run_direction1
        if run1 == "right" and not run_direction1 == "left":
            run1 = run_direction1
        if run2 == "up" and not run_direction2 == "down":
            run2 = run_direction2
        if run2 == "down" and not run_direction2 == "up":
            run2 = run_direction2
        if run2 == "left" and not run_direction2 == "right":
            run2 = run_direction2
        if run2 == "right" and not run_direction2 == "left":
            run2 = run_direction2
        # 根据玩家键入方向进行蛇头坐标的更新
        if run1 == "up":
            head1.y -= 20
        if run1 == "down":
            head1.y += 20
        if run1 == "left":
            head1.x -= 20
        if run1 == "right":
            head1.x += 20
        if run2 == "up":
            head2.y -= 20
        if run2 == "down":
            head2.y += 20
        if run2 == "left":
            head2.x -= 20
        if run2 == "right":
            head2.x += 20
        # 判断两条蛇是否死亡
        # 初始化四个死亡标志为False
        die_flag1 = die_flag2 = False
        # 此时snake_body1,2中均已包含蛇头
        # snake_body1,2第一个元素是蛇头，故不能从0号元素开始比较
        # 因为该蛇蛇头必然和自己重合
        # 这里snake_body1,2均从1号元素开始
        # 所以snake_body1[1:]+snake_body2[1:]是纯粹存储蛇身的列表
        for body in snake_body1[1:]+snake_body2[1:]:
            if head1.x == body.x and head1.y == body.y:
                die_flag1 = True
            if head2.x == body.x and head2.y == body.y:
                die_flag2 = True
        if die_flag1 == True or head1.x < 0 or head1.x > 960 or head1.y < 0 or head1.y > 600:
            # 注意：这边虽然蛇身列表清空，但head1对象仍存在
            # 故必须要在上面的绘制蛇头代码前面加上if先判断蛇是否死亡
            snake_body1.clear()
        if die_flag2 == True or head2.x < 0 or head2.x > 960 or head2.y < 0 or head2.y > 600:
            die_flag2 = True
            # 注意：这边虽然蛇身列表清空，但head1对象仍存在
            # 故必须要在上面的绘制蛇头代码前面加上if先判断蛇是否死亡
            snake_body2.clear()
        # 若两条蛇都死亡
        # 同样地，只能通过snake_body是否为空判断蛇是否死亡
        if len(snake_body1) == 0 and len(snake_body2) == 0:
            show_end_double()
        # 判断蛇头和食物坐标，若相等，则加分，并生成新的食物
        # 定义标志，表明是否找到和蛇头相等的食物
        global flag1
        global flag2
        flag1 = flag2 = 0
        # 如果蛇头和食物重合
        for item in food_list:
            # 在蛇1没死且蛇头1和某一食物坐标相等的条件下
            if len(snake_body1) != 0 and (head1.x == item.x and head1.y == item.y or head1.x == food.x and head1.y == food.y):
                flag1 = 1
                score1 += 1
                # 弹出被吃掉的这个食物
                food_list.pop(food_list.index(item))
                # 再产生一个食物
                food = new_food(head1)
                # 把新食物插入food_list，下一次循环中会更新绘制食物全体
                food_list.append(food)
                break
            # 在蛇2没死的且蛇头2和某一食物坐标相等的条件下
            elif len(snake_body2) != 0 and head2.x == item.x and head2.y == item.y or head2.x == food.x and head2.y == food.y:
                flag2 = 1
                score2 += 1
                # 弹出被吃掉的这个食物
                food_list.pop(food_list.index(item))
                # 再产生一个食物
                food = new_food(head2)
                # 把新食物插入food_list，下一次循环中会更新绘制食物全体
                food_list.append(food)
                break
        # 蛇1必须没死，否则pop会引发异常
        if len(snake_body1) != 0 and flag1 == 0:
            snake_body1.pop()
        # 蛇2必须没死，否则pop会引发异常
        if len(snake_body2) != 0 and flag2 == 0:
            snake_body2.pop ()
        font = pygame.font.SysFont("simHei", 25)
        mode_title1 = mode_title2 = font.render('正常模式', False, grey)
        socre_title1 = font.render('得分: %s' % score1, False, grey)
        socre_title2 = font.render('得分: %s' % score2, False, grey)
        window.blit(mode_title1, (50, 30))
        window.blit(socre_title1, (50, 65))
        window.blit(mode_title2, (800, 30))
        window.blit(socre_title2, (800, 65))
        # 更新蛇头蛇身和食物的数据
        pygame.display.update()
        # 通过帧率设置贪吃蛇速度
        clock.tick(8)


# 双人穿墙模式主体设置
def start_kgame_double():
    # 播放音乐
    pygame.mixer.music.play(-1)
    # 定义存分数的全局变量
    global score1
    global score2
    score1 = score2 = 0
    # 初始化存放玩家键盘输入运动方向的变量
    run_direction1 = "right"
    run_direction2 = "up"
    # 初始化贪吃蛇运动方向的变量
    run1 = run_direction1
    run2 = run_direction2
    # 实例化贪吃蛇和食物对象
    head1 = Snake(randint(0, 30) * 20, randint(0, 20) * 20)
    head2 = Snake(randint(0, 30) * 20, randint(0, 20) * 20)
    # 实例化蛇身长度为2个单位
    snake_body1 = [Snake(head1.x, head1.y + 20), Snake(head1.x, head1.y + 40)]
    snake_body2 = [Snake(head2.x, head2.y + 20), Snake(head2.x, head2.y + 40)]
    # 实例化食物列表，列表随着其中食物被吃掉应该不断缩短
    food_list = [Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))]
    for i in range(1,24):
        food_list.append(Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255))))
    # 实例化单个食物，方便循环内生成单个新食物
    food = Food(randint(0, 45) * 20, randint(0, 28) * 20, (randint(10, 255), randint(10, 255), randint(10, 255)))
    while True:
        window.blit(background, (0,0))
        # 监听玩家键盘输入的运动方向值，并根据输入转为up、down、right或left，方便程序中调用
        # pygame.event.get()返回一个列表，存放本次game执行中程序遇到的一连串事件（按时间顺序依次存放）
        for event in pygame.event.get():
            # pygame.QUIT事件是指用户点击窗口右上角的"×"
            if event.type == pygame.QUIT:
                # 显示结果界面
                show_end_double()
            # 若事件类型是按下键盘，分↑ ↓ ← →四种情况讨论
            elif event.type == pygame.KEYDOWN:
                # 若事件类型是按下键盘↑
                # key是键值，表示按下去的键值是什么
                if event.key == pygame.K_UP:
                    run_direction2 = "up"
                # 若事件类型是按下键盘↓
                if event.key == pygame.K_DOWN:
                    run_direction2 = "down"
                # 若事件类型是按下键盘←
                if event.key == pygame.K_LEFT:
                    run_direction2 = "left"
                # 若事件类型是按下键盘→
                if event.key == pygame.K_RIGHT:
                    run_direction2 = "right"
                # 若事件类型是按下键盘↑
                if event.key == ord('w'):
                    run_direction1 = "up"
                # 若事件类型是按下键盘↓
                if event.key == ord('s'):
                    run_direction1 = "down"
                # 若事件类型是按下键盘←
                if event.key == ord('a'):
                    run_direction1 = "left"
                # 若事件类型是按下键盘→
                if event.key == ord('d'):
                    run_direction1 = "right"
        # 绘制初始化的25个食物图像(24+1=25)
        # 随着该列表中的食物被吃掉，列表应该不断pop以清除已经被吃的事物
        for item in food_list:
            draw_food(item)
        # 绘制被贪吃蛇吃掉后新增的食物图像
        draw_food(food)
        # 绘制蛇头图像
        # 在绘制蛇头之前先检查是不是已经死亡，如果已死亡，则不绘制
        if len(snake_body1) != 0:
            draw_snake(black, head1)
        if len(snake_body2) != 0:
            draw_snake(black, head2)
        # 绘制蛇身图像
        for item in snake_body1:
            draw_snake(blue, item)
        for item in snake_body2:
            draw_snake(green, item)
        # 插入蛇头位置到蛇身列表中
        if len(snake_body1) != 0:
            snake_body1.insert(0, Snake(head1.x, head1.y))
        if len(snake_body2) != 0:
            snake_body2.insert(0, Snake(head2.x, head2.y))
        # 判断贪吃蛇原运动方向(run)与玩家键盘输入的运动方向(run_direction)是否违反正常运动情况
        if run1 == "up" and not run_direction1 == "down":
            run1 = run_direction1
        if run1 == "down" and not run_direction1 == "up":
            run1 = run_direction1
        if run1 == "left" and not run_direction1 == "right":
            run1 = run_direction1
        if run1 == "right" and not run_direction1 == "left":
            run1 = run_direction1
        if run2 == "up" and not run_direction2 == "down":
            run2 = run_direction2
        if run2 == "down" and not run_direction2 == "up":
            run2 = run_direction2
        if run2 == "left" and not run_direction2 == "right":
            run2 = run_direction2
        if run2 == "right" and not run_direction2 == "left":
            run2 = run_direction2
        # 根据玩家键入方向进行蛇头坐标的更新
        if run1 == "up":
            head1.y -= 20
        if run1 == "down":
            head1.y += 20
        if run1 == "left":
            head1.x -= 20
        if run1 == "right":
            head1.x += 20
        if run2 == "up":
            head2.y -= 20
        if run2 == "down":
            head2.y += 20
        if run2 == "left":
            head2.x -= 20
        if run2 == "right":
            head2.x += 20
        # 实现穿墙
        # 蛇头穿出窗体共有8种情况
        if head1.x < 0:
            head1.x = 960
        if head1.x > 960:
            head1.x = 0
        if head1.y < 0:
            head1.y = 600
        if head1.y > 600:
            head1.y = 0
        if head2.x < 0:
            head2.x = 960
        if head2.x > 960:
            head2.x = 0
        if head2.y < 0:
            head2.y = 600
        if head2.y > 600:
            head2.y = 0
        # 定义死亡标志位
        die_flag1 = die_flag2 = False
        for body in snake_body1[1:]+snake_body2[1:]:
            if head1.x == body.x and head1.y == body.y:
                die_flag1 = True
            if head2.x == body.x and head2.y == body.y:
                die_flag2 = True
        if die_flag1 == True:
            snake_body1.clear()
        if die_flag2 == True:
            snake_body2.clear()
        # 若两条蛇都死亡
        if len(snake_body1) == 0 and len(snake_body2) == 0:
            show_end_double()
        # 判断蛇头和食物坐标，若相等，则加分，并生成新的食物
        # 定义标志，表明是否找到和蛇头相等的食物
        global flag1
        global flag2
        flag1 = flag2 = 0
        # 如果蛇头和食物重合
        for item in food_list:
            # 在蛇1没死且蛇头1和某一食物坐标相等的条件下
            if len(snake_body1) != 0 and (head1.x == item.x and head1.y == item.y or head1.x == food.x and head1.y == food.y):
                flag1 = 1
                score1 += 1
                # 弹出被吃掉的这个食物
                food_list.pop(food_list.index(item))
                # 再产生一个食物
                food = new_food(head1)
                # 把新食物插入food_list，下一次循环中会更新绘制食物全体
                food_list.append(food)
                break
            # 在蛇2没死的且蛇头2和某一食物坐标相等的条件下
            elif len(snake_body2) != 0 and head2.x == item.x and head2.y == item.y or head2.x == food.x and head2.y == food.y:
                flag2 = 1
                score2 += 1
                # 弹出被吃掉的这个食物
                food_list.pop(food_list.index(item))
                # 再产生一个食物
                food = new_food(head2)
                # 把新食物插入food_list，下一次循环中会更新绘制食物全体
                food_list.append(food)
                break
        # 蛇1必须没死，否则pop会引发异常
        if len(snake_body1) != 0 and flag1 == 0:
            snake_body1.pop()
        # 蛇2必须没死，否则pop会引发异常
        if len(snake_body2) != 0 and flag2 == 0:
            snake_body2.pop ()
        font = pygame.font.SysFont("simHei", 25)
        mode_title1 = mode_title2 = font.render('穿墙模式', False, grey)
        socre_title1 = font.render('得分: %s' % score1, False, grey)
        socre_title2 = font.render('得分: %s' % score2, False, grey)
        window.blit(mode_title1, (50, 30))
        window.blit(socre_title1, (50, 65))
        window.blit(mode_title2, (800, 30))
        window.blit(socre_title2, (800, 65))
        # 更新蛇头蛇身和食物的数据
        pygame.display.update()
        # 通过帧率设置贪吃蛇速度
        clock.tick(8)


# 渲染按钮函数，设置按钮颜色、位置和其中文字的格式
# 同时处理鼠标移动至按钮上的按钮变色及鼠标点击的事件响应
# msg: 按钮信息，x: 按钮的x轴，y: 按钮的y轴，w: 按钮的宽，h: 按钮的高，ic: 按钮初始颜色，ac: 按钮按下颜色，action: 按钮按下的动作
def button(msg, x, y, w, h, ic, ac, action=None):
    # 获取鼠标位置
    mouse = pygame.mouse.get_pos()
    # 获取鼠标点击情况
    click = pygame.mouse.get_pressed()
    # 如果鼠标位置落在按钮上，则绘制ac颜色按钮
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        # 如果鼠标落在按钮上且有点击动作发生，则执行相应的响应函数
        if click[0] == 1 and action != None:
            action()
    # 如果鼠标位置未落在按钮上，则绘制ic颜色按钮
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
    # 必须死循环，不断监听鼠标位置及点击情况，以便于及时渲染图像及进行事件处理
    while True:
        window.blit(init_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_end()
        # 设置字体
        font = pygame.font.SysFont("simHei", 40)
        # 初始界面显示文字
        fontsurf0 = font.render('欢迎来到贪吃蛇大冒险!', True, black)
        fontrect0 = fontsurf0.get_rect()
        # 通过文本框矩形中心设置文字位置
        fontrect0.center = (480, 100)
        window.blit(fontsurf0, fontrect0)
        # 单人模式显示文字
        font = pygame.font.SysFont("simHei", 25)
        fontsurf1 = font.render('单人模式', True, black)
        fontrect1 = fontsurf1.get_rect()
        fontrect1.center = (175, 350)
        window.blit(fontsurf1, fontrect1)
        # 双人模式显示文字
        fontsurf2 = font.render('双人模式', True, black)
        fontrect2 = fontsurf2.get_rect()
        fontrect2.center = (770, 350)
        window.blit(fontsurf2, fontrect2)
        button("正常模式", 75, 370, 200, 40, blue, brightred, start_game_single)
        button("可穿墙模式", 75, 420, 200, 40, violte, brightred, start_kgame_single)
        button("正常模式", 670, 370, 200, 40, blue, brightred, start_game_double)
        button("可穿墙模式", 670, 420, 200, 40, violte, brightred, start_kgame_double)
        button("帮助", 370, 400, 200, 40, green, blue, help)
        button("退出游戏", 370, 470, 200, 40, red, brightred, exit_end)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    # 定义用到的颜色
    white = (255, 255, 255)
    red = (200, 0, 0)
    green = (0, 128, 0)
    blue = (0, 202, 254)
    violte = (194, 8, 234)
    brightred = (255, 0, 0)
    brightgreen = (0, 255, 0)
    black = (0, 0, 0)
    grey = (129, 131, 129)
    # 设计主窗口
    window = pygame.display.set_mode((960, 600))
    # 设计标题
    pygame.display.set_caption("贪吃蛇大冒险")
    # 导入背景图片
    init_background = pygame.image.load(r"C:\Users\HP\Desktop\PythonLearning\贪吃蛇小游戏\image\init_bgimg.jpg")
    background = pygame.image.load(r"C:\Users\HP\Desktop\PythonLearning\贪吃蛇小游戏\image\bgimg.jpg")
    # 导入背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\HP\Desktop\PythonLearning\贪吃蛇小游戏\background.mp3")
    # 创建时钟
    clock = pygame.time.Clock()
    # 初始化，自检所有模块是否完整
    pygame.init()
    # 进入游戏初始界面
    into_game()