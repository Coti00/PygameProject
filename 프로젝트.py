#############################################################
# 해야할 것
# 1. 시작 화면 배경에 시작 버튼 & 메뉴얼 버튼 & 제목 이벤트
# 2. 시작 버튼 누른 후 캐릭터 세명이 나오고 선택하는 이벤트
# 2. restart 버튼 눌렀을 때 재실행
#############################################################
import pygame
import random
import sys
############################################################
# 기본 초기화   
pygame.init()
# 시작화면 만들기
def game_start():
    start_screen = pygame.display.set_mode((626,352))

    pygame.font.init()
    start_font = pygame.font.SysFont('arial', 40, True)
    start_message = "Press the space key to Start!"
    start_message_object =  start_font.render(start_message, True, (255,255,0))
    start_message_rect = start_message_object.get_rect()
    start_message_rect.center = (626/2,352/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return 
        start_background = pygame.image.load("background.png")
        start_screen.blit(start_background,(0,0))
        start_screen.blit(start_message_object, start_message_rect)
        pygame.display.update()

# 게임 재시작 함수
def game_restart(_score):
    restart_screen = pygame.display.set_mode((626,352))

    pygame.font.init()
    game_restart_font = pygame.font.SysFont('arial',40,True)
    small_game_font = pygame.font.SysFont('arial', 30, True)
    game_restart_message = "Press the Space Key to Restart!"
    game_restart_object = game_restart_font.render(game_restart_message,True,(255,255,0))

    game_score_message = "score : " + str(int(_score)) + '.'
    game_score_object = small_game_font.render(game_score_message, True, (255,0,0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_play()
    
        gameover_background = pygame.image.load("gameover.png")
        restart_screen.blit(gameover_background,(0,0))
        restart_screen.blit(game_restart_object,(85,150))
        restart_screen.blit(game_score_object,(250,190))

        pygame.display.update()

game_start()

# 게임 시작 함수
def game_play():
#화면 크기 설정
    screen_width = 626
    screen_height = 352
    screen = pygame.display.set_mode((screen_width,screen_height))

    pygame.init()
    # 화면 타이틀 설정
    pygame.display.set_caption("하음식")

    # FPS
    clock = pygame.time.Clock()
    ##############################################################

    ############## 1. 사용자 게임 초기화( 배경 화면, 게임 이미지, 좌표, 이동속도, 폰트 등)

    # 배경 이미지 불러오기
    background = pygame.image.load("background.png")
    # 배경 음악
    bgm = pygame.mixer.Sound("bgm.mp3")
    bgm.play()

    ## 스프라이트(캐릭터) 불러오기
    character = pygame.image.load("character.png")
    character_size =  character.get_rect().size #이미지 크기 구해옴
    character_width = character_size[0] # 캐릭터의 가로 크기
    character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로의 절반 크기에 해당하는 곳에 위치
    character_y_pos = screen_height - 58 # 캐릭터 높이 만큼 빼기

    # 폰트 정의
    game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)

    # 스코어
    score = 0

    # 이동할 좌표
    to_x = 0
   
    # 이동 속도
    character_speed = 7
    enemy_speed = 5

    ## 적 enemy 캐릭터
    enemy = pygame.image.load("enemy.png")
    enemy_size =  enemy.get_rect().size #이미지 크기 구해옴
    enemy_x_pos = random.randint(0,screen_width-character_width) # 화면에서 생성되는 x축 값 랜덤
    enemy_y_pos = 0 # 적이 떨어지는 높이는 일정

    # 이벤트 루프 

    while True: #게임이 진행 중인가?
        dt = clock.tick(60) # FPS 설정, 게임화면의 초당 프레임 수를 설정
        print("fps : " + str(clock.get_fps()))
    
    ############### 2. 이벤트 처리( 키보드 , 마우스 등)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #창의 X부분 누르면 게임 종료 / 창이 닫히는 이벤트
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: #캐릭터 왼쪽
                    to_x -= character_speed
                elif event.key == pygame.K_RIGHT:
                    to_x += character_speed
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    to_x = 0


    #############3. 게임 캐릭터 위치 정의     
        character_x_pos += to_x 

    # 가로 경계값 처리
        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width
    # 적 캐릭터가 바닥에 닿으면
        enemy_y_pos += enemy_speed

        if enemy_y_pos > screen_height:
            score += 1
            if (score > 0) and (score % 10 == 0): # 스코어가 10의 배수일 때 속도 상승
                enemy_speed += 1
            enemy_y_pos = 0
            enemy_x_pos = random.randint(0,screen_width-character_width)

    ###########4. 충돌 처리
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos

    # 충돌 체크
        if character_rect.colliderect(enemy_rect):
            bgm.stop()
            game_restart(score)

    #5. 화면에 그리기
    # 배경 그리기
        screen.blit(background, (0,0))

    # 캐릭터 그리기  & 적캐릭터 점수별로 바꾸기
        if score < 15:
            screen.blit(character, (character_x_pos,character_y_pos))
            screen.blit(enemy, (enemy_x_pos,enemy_y_pos))

        elif score >= 15 and score < 35:
            character = pygame.image.load("character2.png")
            screen.blit(character, (character_x_pos,character_y_pos))
            enemy = pygame.image.load("enemy2.jpg")
            screen.blit(enemy, (enemy_x_pos,enemy_y_pos))

        elif score >= 35  :
            character = pygame.image.load("character3.png")
            screen.blit(character, (character_x_pos,character_y_pos))
            enemy = pygame.image.load("enemy3.png")
            screen.blit(enemy, (enemy_x_pos,enemy_y_pos))




    # 스코어 넣기
    # 스코어 계산
        myscore = game_font.render("score: " + str(int(score)),True,(0, 0, 0))
        # (출력할 글자, True, 글자 색상)
        screen.blit(myscore, (10,10))
        myspeed = game_font.render("speed: "+ str(int(enemy_speed)),True,(0, 0, 0))
        screen.blit(myspeed,(10,35))   
        pygame.display.update() # 게임화면 다시 그리기

game_play()
