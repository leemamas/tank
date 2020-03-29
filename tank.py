import pygame, time, random
from pygame.sprite import Sprite

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
BG_COLOR = pygame.Color(255, 255, 255)
TEXT_COLOR = pygame.Color(255, 0, 0)


class BaseItem(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class MainGame():
    window = None
    my_tank = None
    reward = None
    enemyTankList = []
    enemyTankCount = 5
    myBulletList = []
    enemyBulletList = []
    explodeList = []
    wallList = []

    def __init__(self):
        pass

    # 开始游戏
    def start(self):
        # 加载主窗口
        # 初始化
        pygame.display.init()
        # 标题
        pygame.display.set_caption('Tank')
        # 设置大小
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 墙壁
        self.productWall()
        # 我方坦克
        self.productOwn()
        # 敌军
        self.productEnemy(MainGame.enemyTankCount)
        while True:
            time.sleep(0.02)
            # 背景色
            MainGame.window.fill(BG_COLOR)
            # 事件
            self.getEvent()
            # 绘制文字
            MainGame.window.blit(self.getText('敌军数:%d' % len(MainGame.enemyTankList)), (10, 10))
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
            else:
                del MainGame.my_tank
                MainGame.my_tank = None
            self.displayWall()
            self.displayEnemy()
            self.displayMyBullet()
            self.displayEnemyBullet()
            self.displyaExplode()
            if MainGame.reward:
                self.displayReward()

            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    MainGame.my_tank.hitWall()
                    MainGame.my_tank.hit()

            pygame.display.update()

    # 产生墙壁
    def productWall(self):
        for i in range(10):
            wall = Wall('iron')
            MainGame.wallList.append(wall)


    # 产生奖励
    def productReward(self):
        MainGame.reward = Reward()

    # 创建友军
    def productOwn(self):
        MainGame.my_tank = MyTank(400, 550)
        music = Music('music/add.wav')
        music.play()

    # 创建敌军
    def productEnemy(self, count):
        top = 50
        for i in range(count):
            left = random.randint(0, 800)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            MainGame.enemyTankList.append(enemy)

    # 显示墙
    def displayWall(self):
        for wall in MainGame.wallList:

            if wall.live:
                wall.display()
            else:
                MainGame.wallList.remove(wall)

    # 显示奖励
    def displayReward(self):
        MainGame.reward.display()

    # 展示敌军
    def displayEnemy(self):
        for enemy in MainGame.enemyTankList:
            if enemy.live:
                enemy.displayTank()
                enemy.ranMove()
                enemy.hitWall()
                if MainGame.my_tank and MainGame.my_tank.live:
                    enemy.hit()
                # 射击
                enemyBullet = enemy.shot()
                if enemyBullet:
                    MainGame.enemyBulletList.append(enemyBullet)
            else:
                MainGame.enemyTankList.remove(enemy)

    # 友军子弹
    def displayMyBullet(self):
        for bullet in MainGame.myBulletList:
            if bullet.status:
                bullet.display()
                bullet.move()
                bullet.hit()
                bullet.hitWall()
            else:
                MainGame.myBulletList.remove(bullet)

    # 敌军子弹
    def displayEnemyBullet(self):
        for bullet in MainGame.enemyBulletList:
            if bullet.status:
                bullet.display()
                bullet.move()
                bullet.injured()
                bullet.hitWall()
            else:
                MainGame.enemyBulletList.remove(bullet)

    # 展示爆炸
    def displyaExplode(self):
        for explode in MainGame.explodeList:
            if explode.live:
                explode.display()
            else:
                MainGame.explodeList.remove(explode)

    # 结束游戏
    def end(self):
        print('End')
        exit()

    def getText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 18)
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface

    # 获取事件
    def getEvent(self):
        # 所有事件
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.end()
            if event.type == pygame.KEYDOWN:
                if MainGame.my_tank and MainGame.my_tank.live:
                    if event.key == pygame.K_LEFT:
                        MainGame.my_tank.direction = 'L'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                    elif event.key == pygame.K_RIGHT:
                        MainGame.my_tank.direction = 'R'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                    elif event.key == pygame.K_UP:
                        MainGame.my_tank.direction = 'U'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                    elif event.key == pygame.K_DOWN:
                        MainGame.my_tank.direction = 'D'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                    # 增加敌军
                    elif event.key == pygame.K_F2:
                        self.productEnemy(1)
                    # 快捷添加奖励
                    elif event.key == pygame.K_F3:
                        self.productReward()

                    elif event.key == pygame.K_SPACE:
                        # 限制发射子弹数
                        if len(MainGame.myBulletList) < 3:
                            # 创建子弹
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)
                else:
                    # 招魂
                    if event.key == pygame.K_F1:
                        self.productOwn()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        MainGame.my_tank.stop = True


class Tank(BaseItem):
    myTankImage = r"images/tank_T1_0.png"

    def __init__(self, left, top):

        self.mytank = pygame.image.load(self.myTankImage).convert_alpha()

        self.images = {
            'U': self.mytank.subsurface((0, 0), (48, 48)),
            'D': self.mytank.subsurface((48, 48), (48, 48)),
            'L': self.mytank.subsurface((48, 96), (48, 48)),
            'R': self.mytank.subsurface((48, 144), (48, 48))
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5
        self.stop = True
        self.live = True
        # 记录碰撞坐标
        self.sLeft = self.rect.left
        self.sTop = self.rect.top

    def move(self):

        self.sLeft = self.rect.left
        self.sTop = self.rect.top

        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed

    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall, self):
                self.stay()

    def stay(self):
        self.rect.left = self.sLeft
        self.rect.top = self.sTop

    def shot(self):
        return Bullet(self)

    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


# 友军
class MyTank(Tank):

    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)

    def hit(self):
        for enemy in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemy, self):
                enemy.stay()


# 敌军
class EnemyTank(Tank):
    enemyImage = r"images/enemy_1_0.png"

    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        self.enemy = pygame.image.load(self.enemyImage).convert_alpha()

        self.images = {
            'U': self.enemy.subsurface((0, 0), (48, 48)),
            'D': self.enemy.subsurface((48, 48), (48, 48)),
            'L': self.enemy.subsurface((48, 96), (48, 48)),
            'R': self.enemy.subsurface((48, 144), (48, 48))
        }
        self.direction = self.ranDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5
        self.stop = True
        self.step = 20

    def ranDirection(self):
        ran = random.randint(1, 4)
        if ran == 1:
            return 'U'
        elif ran == 2:
            return 'D'
        elif ran == 3:
            return 'L'
        elif ran == 4:
            return 'R'

    def ranMove(self):
        if self.step <= 0:
            self.direction = self.ranDirection()
            self.step = 20
        else:
            self.move()
            self.step -= 1

    def shot(self):
        ran = random.randint(1, 100)
        if ran < 10:
            return Bullet(self)

    def hit(self):
        if pygame.sprite.collide_rect(MainGame.my_tank, self):
            self.stay()


class Bullet(BaseItem):
    def __init__(self, tank):
        self.images = {
            'U': pygame.image.load('images/b_u.png'),
            'D': pygame.image.load('images/b_d.png'),
            'L': pygame.image.load('images/b_l.png'),
            'R': pygame.image.load('images/b_r.png')
        }
        self.direction = tank.direction
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()

        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2

        self.speed = 10
        self.status = True

    def move(self):
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.status = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.status = False
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.status = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.status = False

    def display(self):
        MainGame.window.blit(self.image, self.rect)

    # 碰撞(攻击）
    def hit(self):
        for enemy in MainGame.enemyTankList:
            # 发生碰撞
            if pygame.sprite.collide_rect(enemy, self):
                enemy.live = False
                self.status = False
                # 爆炸
                explode = Explode(enemy)
                MainGame.explodeList.append(explode)

    # 碰撞（中弹）
    def injured(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                explode = Explode(MainGame.my_tank)
                MainGame.explodeList.append(explode)
                self.status = False
                MainGame.my_tank.live = False

    # 撞墙
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall, self):
                self.status = False
                # 攻击墙壁是否消失
                # wall.live=False


class Wall():
    brickImage = r"images\brick.png"
    ironImage = r"images\iron.png"

    # def __init__(self, left, top, type):
    def __init__(self, type):
        if type == 'brick':
            self.image = pygame.image.load(self.brickImage)
        elif type == 'iron':
            self.image = pygame.image.load(self.ironImage)
        self.rect = self.image.get_rect()

        self.rect.left=random.randint(1,20)*24
        self.rect.top = random.randint(1,4)*100


        # self.rect.left = left
        # self.rect.top = top
        self.live = True

    def display(self):
        MainGame.window.blit(self.image, self.rect)


class Explode():
    def __init__(self, tank):
        self.rect = tank.rect
        self.images = [
            pygame.image.load('images/e0.png'),
            pygame.image.load('images/e1.png'),
            pygame.image.load('images/e2.png'),
            pygame.image.load('images/e3.png'),
            pygame.image.load('images/e4.png')
        ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True

    def display(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            self.step += 1
            MainGame.window.blit(self.image, self.rect)
        else:
            self.live = False
            self.step = 0


# 奖励
class Reward():
    boomImage = r'images/reward_boom.png'
    levelImage = r'images/reward_level.png'
    lifeImage = r'images/reward_life.png'

    def __init__(self):
        self.boom = pygame.image.load(self.boomImage).convert_alpha()
        self.level = pygame.image.load(self.levelImage).convert_alpha()
        self.life = pygame.image.load(self.lifeImage).convert_alpha()

        self.kind = random.choice([1, 2, 3])
        if self.kind == 1:
            self.image = self.boom
        elif self.kind == 2:
            self.image = self.level
        elif self.kind == 3:
            self.image = self.life

        self.rect = self.image.get_rect()
        self.rect.left = self.rect.top = random.randint(100, 500)

    def display(self):
        MainGame.window.blit(self.image, self.rect)


class Music():
    def __init__(self, filename):
        self.filename = filename
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)

    def play(self):
        pygame.mixer.music.play()


if __name__ == '__main__':
    a = MainGame()
    a.start()
