import pygame,sys,random
from PIL import Image
import cv2
skier_images = ["skier_down.jpeg","skier_right1.jpeg","skier_right2.jpeg",
"skier_left2.jpeg", "skier_left1.jpeg"]

door = cv2.imread("boom.jpg")
door = cv2.resize(door,(100,100))
cv2.imwrite('boom.jpg', door)


class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("skier_down.jpeg")
        self.rect = self.image.get_rect()
        self.rect.center = [100,100]
        self.angle = 0

    def turn(self, direction, speed_lev):
        self.angle = self.angle + direction
        # print(self.angle)
        if self.angle<-2: self.angle=-2
        if self.angle> 2: self.angle= 2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, speed_lev - abs(self.angle)*2]
        # speed = [self.angle, speed_lev]
        # print(speed)
        return speed

    def move(self, speed):
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20: self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620

class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self,image_file,location,type):
        pygame.sprite.Sprite.__init__(self) 
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False

    def scroll(self,terrainPos):
        self.rect.centery = self.location[1]-terrainPos

def create_map(start,end):
    global timer
    # print('----->',start)
    # print('-------->>',end)
    obstacles = pygame.sprite.Group()
    locations = []
    # gates = pygame.sprite.Group()
    for i in range(10): 
        row = random.randint(start,end)
        col = random.randint(0,9)
        location = [col*64+20, row*64+20]
        if not (location in locations):
            locations.append(location)
            type = random.choice(["tree","flag","coin"])
            if type == "tree":img = "skier_tree.jpeg"
            elif type=="flag": img = "skier_flag.jpeg"
            elif type=="coin": img = "coin.jpg"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)
    if timer % 2 == 0:
        # print('------------------>>')
        row = random.randint(start,end)
        col = random.randint(0,9)
        location = [col*64+20, row*64+20]
        if not (location in locations):
            locations.append(location)
            type = "door"
            img = "door.jpg"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)
    return obstacles
    
def animate():
    screen.fill([255,255,255])
    pygame.display.update(obstacles.draw(screen))
    screen.blit(skier.image,skier.rect)
    screen.blit(score_text,[10,10])
    screen.blit(power_text,[300,10])
    pygame.display.flip()   

def create_map_door(start,end):
    obstacles = pygame.sprite.Group()
    locations = []
    for i in range(2): 
        row = random.randint(start,end)
        col = random.randint(0,9)
        location = [col*64+20, row*64+20]
        if not (location in locations): 
            locations.append(location)
            # type = random.choice(["monster","monster2"])
            type = "monster"
            if type == "monster":img = "monster.png"
            # elif type=="monster2": img = "monster2.png"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)
    return obstacles

def create_map_fight(start,end):
    obstacles = pygame.sprite.Group()
    return obstacles

def animate_fight(points,powers):
    global pos_x
    global pos_y
    global shoot_flag
    global fight_flag
    image_boom = pygame.image.load("boom.jpg")
    image_fight = pygame.image.load("snow.jpg")
    image_fight = pygame.transform.scale(image_fight,(640,640))
    image_mon = pygame.image.load("monster.png")
    pygame.display.update(obstacles.draw(screen))
    image_fire = pygame.image.load("fire.jpg")
    screen.blit(image_fight,(0,0))
    screen.blit(skier.image,skier.rect)
    if shoot_flag == True:
        screen.blit(image_fire,(skier.rect[0],skier.rect[1]+pos_y))
        pos_y += 5
    if pos_y > 500:
        shoot_flag = False
        pos_y = 50
    print('-->',shoot_flag)
    fire_rect = image_fire.get_rect()
    fire_rect.x = skier.rect[0]
    fire_rect.y = skier.rect[1]+pos_y
    # print(fire_rect)
    mon_rect = image_mon.get_rect()
    mon_rect.x = pos_x
    mon_rect.y = 500
    # print('--->',mon_rect)
    screen.blit(image_mon,(pos_x,500))
    screen.blit(score_text,[10,10])
    screen.blit(power_text,[300,10])
    if fire_rect.colliderect(mon_rect):
        screen.blit(image_boom,(pos_x,500))
        fight_flag = False
        shoot_flag = False
        points += 1000
        powers += 200
    pygame.display.flip()   
    return points,powers

def animate_door():
    screen.fill([245,245,220])
    pygame.display.update(obstacles.draw(screen))
    screen.blit(skier.image,skier.rect)
    screen.blit(score_text,[10,10])
    screen.blit(power_text,[300,10])
    pygame.display.flip()   

def updateObstacleGroup(map0,map1):
    obstacles = pygame.sprite.Group()
    for ob in map0: obstacles.add(ob)
    for ob in map1: obstacles.add(ob)
    return obstacles


pygame.init()
screen = pygame.display.set_mode([640,640])
clock = pygame.time.Clock()
skier = SkierClass()
speed = [0,6]
map_position = 0
points = 0
powers = 0
timer = 0
map0 = create_map(20,29)
map1 = create_map(10,19)
activeMap = 0
obstacles = updateObstacleGroup(map0,map1)
font = pygame.font.Font(None,50)
door_flag = False
fight_flag = False
change_flag = False
shoot_flag = False
pos_x = 10
while True:
    timer+=1
    # print(timer)
    clock.tick(30)
    if timer < 1000:
        speed_lev = 6
    elif timer >= 1000 and timer < 3000:
        speed_lev = 12
    else:
        speed_lev = 18
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit() 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT: 
                speed = skier.turn(-1,speed_lev)
            elif event.key == pygame.K_RIGHT: 
                speed = skier.turn(1,speed_lev)
            if fight_flag == True:
                if event.key == pygame.K_SPACE:
                    shoot_flag = not shoot_flag
                    powers -= 50

    skier.move(speed) 
    map_position += speed[1]

    if map_position >=640 and activeMap ==0:
        activeMap = 1
        if door_flag == True:
            if fight_flag == True:
                map0 = create_map_fight(20,29)
            else:    
                map0 = create_map_door(20,29)
        else:
            map0 = create_map(20,29)
        obstacles = updateObstacleGroup(map0,map1)
    if map_position >=1280 and activeMap == 1:
        activeMap = 0
        for ob in map0:
            ob.location[1] = ob.location[1]-1280 
        map_position = map_position - 1280
        if door_flag == True:
            if fight_flag == True:
                map1 = create_map_fight(10,19)
            else:    
                map1 = create_map_door(10,19)
        else:
            map1 = create_map(10,19)
        obstacles = updateObstacleGroup(map0,map1)

    for obstacle in obstacles:
        obstacle.scroll(map_position)
        hit = pygame.sprite.spritecollide(skier,obstacles,False)
        if hit:
            if hit[0].type == "tree" and not hit[0].passed:
                points = points-100
                skier.image = pygame.image.load("skier_crash.jpeg")
                animate()
                pygame.time.delay(1000)
                skier.image = pygame.image.load("skier_down.jpeg")
                points = 0
                door_flag = False
                skier.angle = 0
                timer = 0
                spped = [0,6]
                hit[0].passed = True
            elif hit[0].type == "flag" and not hit[0].passed:
                points += 100
                obstacles.remove(hit[0])
            elif hit[0].type == "coin" and not hit[0].passed:
                points +=30
                powers += 50
                obstacles.remove(hit[0])
            elif hit[0].type == "door" and not hit[0].passed:
                if powers >= 100:
                    door_flag = True
                    door_time = 0
                    powers -= 100
                else:
                    points -= 100
                obstacles.remove(hit[0])
            elif hit[0].type == "monster" and not hit[0].passed:
                fight_flag = True
                pos_y = 50  
                obstacles.remove(hit[0])
    score_text = font.render("Score: " + str(points),1,(0,0,0))
    power_text = font.render("Power: "+ str(powers),1,(0,0,0))
    if door_flag == True and door_time <= 2000:
        door_time += 1
        if door_time == 2000:
            door_flag = False
            fight_flag = False
            pos_x = 10
        if fight_flag == True:
            points,powers = animate_fight(points,powers)
            if change_flag == True:
                pos_x -= 5
            else:
                pos_x += 5
            if pos_x == 570:
                change_flag = True
            elif pos_x == 0:
                change_flag = False
        else:
            animate_door()
    else:
        animate()

