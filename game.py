from itertools import count
from tracemalloc import stop
import pygame as pg
import os
import random
import time
import sys
from sense_hat import SenseHat
sense=SenseHat()
#全域變數
clock=pg.time.Clock()
#子彈移動速度
speed=[random.randint(-15,15),40,-40,15]
deadline=710
id=None
life=0
score=0

#初始化
pg.init()
pg.mixer.init()
pg.mixer.music.set_volume(1.0)#音量
pg.display.set_caption('airplane game')
os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d"%(0,32)#視窗
width,height=1280,720
screen=pg.display.set_mode((width,height))#視窗大小

#載入圖片
path1=os.path.abspath('.')
ch = path1 + '/picture/'
ui_background_jpg=pg.image.load(ch+'ui.png')
background_jpg=pg.image.load(ch+'background.png')
airplane_jpg=pg.image.load(ch+"airplane2.png")
ball=pg.image.load(ch+"ball.png")
enairplane_jpg=pg.image.load(ch+"enairplane.png")
pausebtn=pg.transform.scale(pg.image.load(ch+"pause.png"),(40,40))
startbtn=pg.image.load(ch+"START.png")
bomboldbig=pg.image.load(ch+"bombold.png")
#改變圖片大小
ui_background=pg.transform.scale(ui_background_jpg,(width,height))
startbtn=pg.transform.scale(startbtn,(200,100))
airplane=pg.transform.scale(airplane_jpg,(80,90))
background=pg.transform.scale(background_jpg,(width,height))
enairplane=pg.transform.scale(enairplane_jpg,(80,90))
bombold=pg.transform.scale(bomboldbig,(90,100))

#獲得圖片的矩形資料以及設定初始座標
back_rect=background.get_rect()
ui_back_rect=ui_background.get_rect()
airplane_rect=airplane.get_rect()
airplane_rect.center=int(width/2),600


enairplane_rect=enairplane.get_rect()
enairplane_rect.bottomleft=random.randint(enairplane_rect.width,width-enairplane_rect.width),80

bombold_rect=bombold.get_rect()#爆炸特效

pause_rect=pausebtn.get_rect()
pause_rect.topright=width,0

start_rect=startbtn.get_rect()
start_rect.center=int(width/2),int(height)+150


#設定我方子彈和敵方子彈
bul=[]
bul_rect=[]
for i in range(10):
    bul.append(pg.transform.scale(pg.image.load(ch+"bullet.png"),(15,40)))
    bul_rect.append(bul[i].get_rect())
    bul_rect[i].center=width,height
bul_num=-1

bossbul=[]
bossbul_rect=[]
bossbul_num=[]
bossSpeed=[]
boss_mo=[-2,2]
bossairplane=[]
bossairplane_rect=[]
boss_bombold_rect=[]
boss_bombold_num=[]
for i in range(20):
    bossbul.append([])
    boss_bombold_num.append(0)
    boss_bombold_rect.append(bombold_rect)
    boss_bombold_rect[i].center=-1,-1
    bossbul_rect.append([])
    bossbul_num.append(-1)
    bossSpeed.append(boss_mo[random.randint(0,1)])
    bossairplane.append(pg.transform.scale(pg.image.load(ch+"enairplane.png"),(80,90)))
    bossairplane_rect.append(bossairplane[i].get_rect())
    bossairplane_rect[i].bottomleft=random.randint(enairplane_rect.width,width-enairplane_rect.width),80
    for j in range(10):
        bossbul[i].append(pg.transform.scale(pg.image.load(ch+"enbullet.png"),(15,40)))
        bossbul_rect[i].append(bossbul[i][j].get_rect())
        bossbul_rect[i][j].center=-1,-1

  


#碰撞判定
def rebound0(atop,abot,al,ar,btop,bbot,bl,br):#a:子彈  b:敵機
    if atop<=bbot and abot>=btop and al<=br and ar>=bl:
        return True
    else:
        return False
    #暫停
def pause(a):
    scoretext = font2.render("Pause",True,(0,200,0))
    score_rect=scoretext.get_rect()
    score_rect.center=width/2,height/4
    start_png=pg.image.load(ch+'START.png')
    start=pg.transform.scale(start_png,(400,200))
    start2_png=pg.image.load(ch+'START2.png')
    start2=pg.transform.scale(start2_png,(400,200))
    start_rect=start.get_rect()
    start_rect.center=width/4,height/2+150
    start_print=start
    main_png=pg.image.load(ch+'MAIN.png')
    main=pg.transform.scale(main_png,(400,200))
    main2_png=pg.image.load(ch+'MAIN2.png')
    main2=pg.transform.scale(main2_png,(400,200))
    main_print=main
    main_rect=main.get_rect()
    main_rect.center=width*3/4,height/2+150
    while a:
        clock.tick(30)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type==pg.MOUSEMOTION:
                x,y=pg.mouse.get_pos()
                if y>=start_rect.top and y<=start_rect.bottom and x>=start_rect.left and x<=start_rect.right:
                    start_print=start2
                else:
                    start_print=start
                if y>=main_rect.top and y<=main_rect.bottom and x>=main_rect.left and x<=main_rect.right:
                    main_print=main2
                else:
                    main_print=main
            if event.type==pg.MOUSEBUTTONDOWN:
                x,y=pg.mouse.get_pos()
                if y>=start_rect.top and y<=start_rect.bottom and x>=start_rect.left and x<=start_rect.right :
                    return 1
                if y>=main_rect.top and y<=main_rect.bottom and x>=main_rect.left and x<=main_rect.right :
                    return 0
        screen.blit(background,back_rect)
        screen.blit(lifetext,life_rect)
        screen.blit(airplane,airplane_rect)
        screen.blit(start_print,start_rect)
        screen.blit(main_print,main_rect)
        screen.blit(scoretext,score_rect)
        pg.display.update()
        
    #飛機移動
def vector(object,dex,x,dey,y):
    if dex==True:
        object.centerx-=20
    if x==True:
        object.centerx+=20
    if dey==True:
        object.centery-=10
    if y==True:
        object.centery+=10
    if object.centerx<0:
        object.centerx=0
    if object.left<0:
        object.left=0
    elif object.centerx>=1280:
        object.centerx=1280
    if object.centery<450:
        object.centery=450
    elif object.centery>600:
        object.centery=600

def game_over():
    scoretext = font2.render("GAME OVER",True,(255,0,0))
    score_rect=scoretext.get_rect()
    score_rect.center=int(width/2),int(height/4)
    if not pg.mixer.music.get_busy():
        pg.mixer.music.load(ch+'No Hope.mp3')
        pg.mixer.music.play()
    i=0
    while i<256:
        for event in pg.event.get():
            #正常關閉
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        scoretext.set_alpha(i)
        time.sleep(0.05078125)
        screen.blit(scoretext,score_rect)
        pg.display.update()
        i+=1

    #偵測關閉事件
def restart_game(a):
    global number
    start_png=pg.image.load(ch+'START.png')
    start=pg.transform.scale(start_png,(400,200))
    start2_png=pg.image.load(ch+'START2.png')
    start2=pg.transform.scale(start2_png,(400,200))
    start_rect=start.get_rect()
    start_rect.center=int(width/4-100),int(height/2+150)
    start_print=start
    main_png=pg.image.load(ch+'MAIN.png')
    main=pg.transform.scale(main_png,(400,200))
    main2_png=pg.image.load(ch+'MAIN2.png')
    main2=pg.transform.scale(main2_png,(400,200))
    main_print=main
    main_rect=main.get_rect()
    main_rect.center=int(width/2),int(height/2+150)
    exit_png=pg.image.load(ch+'EXIT.png')
    exit=pg.transform.scale(exit_png,(400,200))
    exit2_png=pg.image.load(ch+'EXIT2.png')
    exit2=pg.transform.scale(exit2_png,(400,200))
    exit_print=exit
    exit_rect=exit.get_rect()
    exit_rect.center=int(width*3/4+100),int(height/2+150)

    scoretext = font2.render("Again?",True,(0,255,0))
    score_rect=scoretext.get_rect()
    score_rect.center=int(width/2),int(height/4)
  
    numbertext = font2.render(f"score:{number}",True,(100,200,0))
    number_rect=numbertext.get_rect()
    number_rect.center=int(width/2),int(height/4-100)
    while a:
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(ch+'lo-fi_fall.mp3')
            pg.mixer.music.play(-1)
        clock.tick(30)
        
        #pygame 事件處理
        for event in pg.event.get():
            #正常關閉
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type==pg.MOUSEMOTION:
                x,y=pg.mouse.get_pos()
                if y>=start_rect.top and y<=start_rect.bottom and x>=start_rect.left and x<=start_rect.right:
                    start_print=start2
                else:
                    start_print=start
                if y>=main_rect.top and y<=main_rect.bottom and x>=main_rect.left and x<=main_rect.right:
                    main_print=main2
                else:
                    main_print=main
                if y>=exit_rect.top and y<=exit_rect.bottom and x>=exit_rect.left and x<=exit_rect.right:
                    exit_print=exit2
                else:
                    exit_print=exit
            if event.type == pg.MOUSEBUTTONDOWN:
                x,y = pg.mouse.get_pos()
                if y>=start_rect.top and y<=start_rect.bottom and x>=start_rect.left and x<=start_rect.right:
                    pg.mixer.music.stop()
                elif y>=main_rect.top and y<=main_rect.bottom and x>=main_rect.left and x<=main_rect.right:
                    pg.mixer.music.stop()
                    return 1
                elif y>=exit_rect.top and y<=exit_rect.bottom and x>=exit_rect.left and x<=exit_rect.right:
                    pg.quit()
                    sys.exit()
        screen.blit(background,back_rect)
        screen.blit(start_print,start_rect)
        screen.blit(main_print,main_rect)
        screen.blit(exit_print,exit_rect)
        screen.blit(scoretext,score_rect)
        screen.blit(numbertext,number_rect)
        pg.display.update()



def main_ui():
    start_png=pg.image.load(ch+'START.png')
    start=pg.transform.scale(start_png,(400,200))
    start_rect=start.get_rect()
    start_rect.center=int(width/4+300),int(height/2)+150
    
    pra_png=pg.image.load(ch+'practise.png')
    pra_p=pg.transform.scale(pra_png,(400,200))
    pra_png2=pg.image.load(ch+'practise2.png')
    pra_p2=pg.transform.scale(pra_png2,(400,200))
    print_pra=pra_p



    change_background_jpg=pg.image.load(ch+'background.png')
    change_background=pg.transform.scale(change_background_jpg,(width,height))
    change_back_rect=change_background.get_rect()
    font=pg.font.SysFont("Microsoft Jhenghei",60)
    totaltext=font.render(f"Airplane Game",True,(255,255,255))
    total_rect=totaltext.get_rect()
    total_rect.center=int(width/2),int(height/4)
    
    running = True

    # Font
    font = pg.font.SysFont("微軟正黑體",50)
    # Run
    while running:
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(ch+'Space Sprinkles.mp3')
            pg.mixer.music.play(-1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x,y=pg.mouse.get_pos()
                if y>=start_rect.top and y<=start_rect.bottom and x>=start_rect.left and x<=start_rect.right :
                    pg.mixer.music.stop()
                    return 2
                if y>=start2_rect.top and y<=start2_rect.bottom and x>=start2_rect.left and x<=start2_rect.right :
                    pg.mixer.music.stop()
                    return 2
            if event.type==pg.MOUSEMOTION:
                x,y=pg.mouse.get_pos()
                if y>=start_rect.top and y<=start_rect.bottom and x>=start_rect.left and x<=start_rect.right:
                    print_pra=pra_p2
                else:
                    print_pra=pra_p

        # Updates
        screen.blit(change_background,change_back_rect)
        screen.blit(totaltext, total_rect)
        screen.blit(print_pra, start_rect)
        pg.display.flip()


par=False
game_start=False
while True:
    switch=main_ui()
    par=True
    while par: 
        
        #字串字體和大小
        font=pg.font.SysFont("微軟正黑體",36)
        font2 = pg.font.SysFont("Microsoft Jhenghei",60)
        #倒數計時
        COUNT=pg.USEREVENT+1
        pg.time.set_timer(COUNT,1000)
        runtime=60
        life=20
        bnbnoin=True
        boss_bnbnoin=[True,True,True,True,True,True,True,True,True,True]
        bnbspeed=[0,0]
        debomb_num=100
        mo=[-20,-30,20,30]
        number=0
        eneSpeed=mo[random.randint(0,3)]
        logic_x,logic_dex,logic_y,logic_dey=False,False,False,False
        pitch,roll,yaw=sense.get_orientation().values()
        pv,rv,yv=sense.get_orientation().values()
        for i in range(10):
            bul_rect[i].center=width,height
        bul_num=-1
        operation=True#game start
        fps=30
        count=0
        while operation:
            count+=1
            if not pg.mixer.music.get_busy():
                    pg.mixer.music.load(ch+'CleytonRX - Battle RPG Theme.mp3')
                    pg.mixer.music.play(-1)
            clock.tick(fps)#fps
            lifetext=font.render(f"life:{life}",True,(0,0,0))
            life_rect=lifetext.get_rect()
            life_rect.top=airplane_rect.bottom
            life_rect.centerx=airplane_rect.centerx

            #偵測使用者觸發的事件
            for event in pg.event.get():
                # if event.type==pg.QUIT:
                #     pg.quit()
                #     sys.exit()
                #if event.type==COUNT:
                    #fps+=1
                    #number+=1
                if event.type==pg.MOUSEMOTION:
                    x,y=pg.mouse.get_pos()
                    if y<450:
                        y=450
                    elif y>600:
                        y=600
                    airplane_rect.center=x,y
                if event.type==pg.KEYDOWN :
                    if event.key==pg.K_a or event.key==pg.K_LEFT :
                        logic_dex=True
                    elif event.key==pg.K_d or event.key==pg.K_RIGHT:
                        logic_x=True
                    elif event.key==pg.K_w or event.key==pg.K_UP:
                        logic_dey=True
                    elif event.key==pg.K_s or event.key==pg.K_DOWN:
                        logic_y=True
                    if event.key==pg.K_SPACE:
                        bul_num_after=bul_num
                        bul_num=(bul_num+1)%5
                        if bul_rect[bul_num].centerx==width:
                            bul_rect[bul_num].center=airplane_rect.center
                        else:
                            bul_num=bul_num_after
                if event.type==pg.KEYUP:
                    if event.key==pg.K_a or event.key==pg.K_LEFT:
                        logic_dex=False
                    if event.key==pg.K_d or event.key==pg.K_RIGHT:
                        logic_x=False
                    if event.key==pg.K_w or event.key==pg.K_UP:
                        logic_dey=False
                    if event.key==pg.K_s or event.key==pg.K_DOWN:
                        logic_y=False
                pitch,roll,yaw=sense.get_orientation().values()
                if (abs(int(pv-pitch))>300):
                    #我方子彈發射
                    bul_num_after=bul_num
                    bul_num=(bul_num+1)%10
                    if bul_rect[bul_num].centerx==width:
                        bul_rect[bul_num].center=airplane_rect.center
                    else:
                        bul_num=bul_num_after
                print(int(yv-yaw))
                if(int(yv-yaw)>10):
                    logic_dex=True
                    logic_x=False
                elif(int(yv-yaw)<=-10):
                    logic_x=True
                    logic_dex=False
                else:
                    logic_x=False
                    logic_dex=False
                if event.type==pg.MOUSEBUTTONDOWN:
                    x,y=pg.mouse.get_pos()
                    if y>=pause_rect.top and y<=pause_rect.bottom and x>=pause_rect.left and x<=pause_rect.right :
                        a=True
                        pause_b=pause(a)
                        if pause_b==0:
                            operation=False
                            par=False
                            pg.mixer.music.stop()
                    #我方子彈發射
                    bul_num_after=bul_num
                    bul_num=(bul_num+1)%10
                    if bul_rect[bul_num].centerx==width:
                        bul_rect[bul_num].center=airplane_rect.center
                    else:
                        bul_num=bul_num_after
            vector(airplane_rect,logic_dex,logic_x,logic_dey,logic_y)

            for j in range(10):
                logic=random.randint(0,10)
                if logic==1:#敵人子彈發射
                    bossbul_num[j]=(bossbul_num[j]+1)%5
                    if bossbul_rect[j][bossbul_num[j]].centerx==-1:
                        bossbul_rect[j][bossbul_num[j]].center=bossairplane_rect[j].center
                for i in range(10):
                    bossbul_rect[j][i]=bossbul_rect[j][i].move(0,speed[3])#子彈移動
                    if bossbul_rect[j][i].top>=height:#是否到達視窗底部
                        bossbul_rect[j][i].center=-1,-1
                if bul_rect[j].centerx!=width:#是否是射出的子彈
                    bul_rect[j]=bul_rect[j].move(0,speed[2])
                if bul_rect[j].top<=0:#將子彈重置
                    bul_rect[j].center=width,height



            
            #碰撞判定
            for i in range(5):
                for j in range(10):
                    for k in range(10):
                        if rebound0(bul_rect[i].top,bul_rect[i].bottom,bul_rect[i].left,bul_rect[i].right,bossbul_rect[j][k].top,bossbul_rect[j][k].bottom,bossbul_rect[j][k].left,bossbul_rect[j][k].right):
                            bul_rect[i].center=width,height
                            bossbul_rect[j][k].center=-1,-1
                        
                        if rebound0(bul_rect[i].top,bul_rect[i].bottom,bul_rect[i].left,bul_rect[i].right,bossairplane_rect[j].top,bossairplane_rect[j].bottom,bossairplane_rect[j].left,bossairplane_rect[j].right): 
                            number+=1
                            boss_bombold_num[j]=30
                            boss_bombold_rect[j].center=bossairplane_rect[j].center
                            bossSpeed[j]=mo[random.randint(0,1)]
                            bossairplane_rect[j].bottomleft=random.randint(enairplane_rect.width,width-enairplane_rect.width),80
                            bul_rect[i].center=width,height
            for i in range(10):
                for j in range(10):
                    if rebound0(airplane_rect.top,airplane_rect.bottom,airplane_rect.left,airplane_rect.right,bossbul_rect[i][j].top,bossbul_rect[i][j].bottom,bossbul_rect[i][j].left,bossbul_rect[i][j].right):
                            if bossbul_rect[i][j].centerx>0:
                                bossbul_rect[i][j].center=-1,-1
                                life-=1
            
            if life <=0:
                pg.mixer.music.stop()
                game_over()
                a=True
                control_choose=restart_game(a)
                life=20
                score=0
                fps=20
                if control_choose==1: 
                    par=False
                    break
                

            #敵機左右移動
            for i in range(10):
                bossairplane_rect[i]=bossairplane_rect[i].move(bossSpeed[i],0)
                if bossairplane_rect[i].centerx>=pause_rect.centerx:
                    bossairplane_rect[i].centerx=pause_rect.centerx
                    bossSpeed[i]=-20
                elif bossairplane_rect[i].left<=0:
                    bossairplane_rect[i].left=1
                    bossSpeed[i]=20
            #圖片更新
            screen.blit(background,back_rect)
            for i in range(10):
                if bul_rect[i].centerx>=0:
                    screen.blit(bul[i],bul_rect[i])
                if boss_bombold_num[i]>0:
                    screen.blit(bombold,boss_bombold_rect[i])
                    boss_bombold_num[i]-=5
                screen.blit(bossairplane[i],bossairplane_rect[i])
                for j in range(10):
                    if bossbul_rect[i][j].centerx>=0:
                        screen.blit(bossbul[i][j],bossbul_rect[i][j])

            screen.blit(airplane,airplane_rect)
            screen.blit(lifetext,life_rect)
            screen.blit(pausebtn,pause_rect)
            pg.display.update()
    restart=True
