import pygame
import random
import os

pygame.mixer.init()

pygame.init()


white=(192,192,192)
red=(255,0,0)
black=(0,0,0)

screen_width=960
screen_height=540

gameWindow=pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('Snake Game')

bgimg = pygame.image.load('grass.jpg')
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

gimg = pygame.image.load('gameover.gif')
gimg = pygame.transform.scale(gimg,(screen_width,screen_height)).convert_alpha()

img = pygame.image.load('images.jpg')
img = pygame.transform.scale(img,(screen_width,screen_height)).convert_alpha()


clock=pygame.time.Clock()

font=pygame.font.SysFont('Agency FB',55)




def text_screen(text,color,x,y):
    screen_text= font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.circle(gameWindow,black,(x ,y),snake_size)

def welcome():
    pygame.mixer.music.load('Intro.mp3')
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(img,(0,0))
        
        text_screen('Press Space Bar To Play ',(176,176,176),240,500)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                    exit_game=True

            if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        pygame.mixer.music.load('East_of_Tunesia.mp3')
                        pygame.mixer.music.play(-1)
                        gameloop()

        pygame.display.update()
        clock.tick(60)
        

def gameloop():
    exit_game = False
    game_over = False
    snake_x=45
    snake_y=55
    velocity_x=0
    velocity_y=0
    snake_size=10
    


    if not os.path.exists('hiscore.txt'):
        with open("hiscore.txt",'w') as f:
            f.write("0")
        
    with open("hiscore.txt",'r') as f:
        hiscore=f.read()

    init_velocity=5

    food_x=random.randint(20,screen_width/2)
    food_y=random.randint(20,screen_height/2)
    score=0

    snk_list=[]
    snk_length=1


    fps=30
    while not exit_game:
        if game_over:
            with open("hiscore.txt",'w')as f:
                f.write(str(hiscore))

                

            gameWindow.fill(white)
            gameWindow.blit(gimg,(0,0))
            text_screen("Press Enter To Continue",white,270,300)
            for event in pygame.event.get():
                # print(event)
                if event.type==pygame.QUIT:
                    exit_game=True

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                # print(event)
                if event.type==pygame.QUIT:
                    exit_game=True

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key==pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0

                    if event.key==pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0

                    if event.key==pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0

                    if event.key==pygame.K_q:
                        score+=10
                        snk_length+=5

                    if event.key==pygame.K_SPACE:
                        fps+=10
                        

            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y

            if abs(snake_x-food_x)<8 and abs(snake_y-food_y)<8:
                crash_sound = pygame.mixer.Sound("Beep_Short.wav")
                pygame.mixer.Sound.play(crash_sound)  
                
                score+=10
                food_x=random.randint(5,screen_width-5)
                food_y=random.randint(5,screen_height-5)
                snk_length+=5

                if score>int(hiscore):
                    hiscore=score

            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            text_screen('Score: '+str(score)+ '\nHiscore: '+str(hiscore),red ,5,5)
            
            pygame.draw.circle(gameWindow,red,(food_x ,food_y),6)
            
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over=True
                pygame.mixer.music.load('Crash.mp3')
                pygame.mixer.music.play()      
                     

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                pygame.mixer.music.load('Crash.mp3')
                pygame.mixer.music.play()  

            plot_snake(gameWindow,black,snk_list,snake_size)
            
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()


welcome()
