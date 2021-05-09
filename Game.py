import winsound#Biblioteca para reproduccion de pistas de audio  Metodos: Playsound
import tkinter as tk
import os
from PIL import Image, ImageTk
import tkinter.font as font
import time#Biblioteca para administracion de tiempo Metodos: time,sleep
from threading import Thread
import random
imageFolder="imagenes"
musicFolder="music"
mainWindowWidth=650
mainWindowHeight=450
LevelsHeight=650
LevelsWidth=550
movement=20
Shoot_Movement=7
shoot_pause_time=0.7
EnemyX=200
EnemyY=40
Enemy1CicleTime=3
Enemy2ShootPause=1
Enemy2TeleportPause=2
EnemyTag="Enemy"
EnemyShootTag="EnemyShoot"
NaveShootTag="Shoot"
NaveTag="Nave"
EnemyTag="Enemy"
DefaultPlayerLife=50
EnemyLevel1Life=30
EnemyLevel2Life=40
EnemyLevel3Life=50

def imagenes(nombre_imagen):
    ruta=os.path.join(imageFolder,nombre_imagen)#Asigna la ruta donde esta el archivo
    imagen=tk.PhotoImage(file=ruta)#Establece como un objeto de clase PhotoImage al archivo ubicado en la ruta establecida
    return imagen#Retorna el objeto PhotoImage
def import_image_resize(image_name,width,height):
    route=imageFolder+"/"+image_name
    Imagen=Image.open(route).resize((width,height),Image.ANTIALIAS)
    PhotoImage=ImageTk.PhotoImage(Imagen)
    return PhotoImage
def import_image(image_name,width,height):
    route=imageFolder+"/"+image_name
    Imagen=Image.open(route)
    PhotoImage=ImageTk.PhotoImage(Imagen)
    return PhotoImage
def play_song(song_name):#Cancion de la pantalla principal
    relative_route=musicFolder+"/"+song_name+".wav"
    winsound.PlaySound(relative_route,winsound.SND_ASYNC+winsound.SND_LOOP)
    
def moveObject(Canvas,Canvas_Object,X_Movement,Y_Movement):
    Canvas.move(Canvas_Object,X_Movement,Y_Movement)
def moveObjectInto(Canvas,Canvas_Object,X_Movement,Y_Movement):
    coords=Canvas.coords(Canvas_Object)
    print(coords)
    x=coords[0]
    y=coords[1]
    moveObject(Canvas,Canvas_Object,x+X_Movement,y+Y_Movement)
    
def draw_image(Canvas,imagen,X_position,Y_position):
    Image=Canvas.create_image(X_position,Y_position,image=imagen)
    return Image
def getImageSize(image_name):
    route=imageFolder+"/"+image_name
    Imagen=Image.open(route)
    PhotoImage=ImageTk.PhotoImage(Imagen)
    return (PhotoImage.width(),PhotoImage.height())
    
def aboutWindow():
    About=tk.Toplevel()#Se crea una ventana secundaria para el juego
    About.title("About")#Se le asigna un titulo a la ventana
    About.minsize(mainWindowWidth,mainWindowHeight)#Se le asigna dimensiones minimas a la ventana
    About.resizable(height=tk.NO,width=tk.NO)#Se bloquea que el usuario pueda cambiar el tamano de la pantalla
    root.withdraw()
    def exit():
        About.destroy()
        root.deiconify()
    ButtonExit=tk.Button(About,text="Exit",command=exit,bg="yellow")
    ButtonExit['font']=myFont
    ButtonExit.place(x=550,y=390)
    
def scoresWindow():
    ScoresWindow=tk.Toplevel()#Se crea una ventana secundaria para el juego
    ScoresWindow.title("High Scores")#Se le asigna un titulo a la ventana
    ScoresWindow.minsize(mainWindowWidth,mainWindowHeight)#Se le asigna dimensiones minimas a la ventana
    ScoresWindow.resizable(height=tk.NO,width=tk.NO)#Se bloquea que el usuario pueda cambiar el tamano de la pantalla
    root.withdraw()
    def exit():
        ScoresWindow.destroy()
        root.deiconify()
    ButtonExit=tk.Button(ScoresWindow,text="Exit",command=exit,bg="yellow")
    ButtonExit['font']=myFont
    ButtonExit.place(x=550,y=390)
def GameWindow():
    
    Fondo=imagenes("space.png")
    Nave_Image=imagenes("aliado.png")
    AlleyShoot=imagenes("disparoaliado.png")
    EnemyShoot=imagenes("disparoenemigo.png")
    EnemyImage1=imagenes("enemigo1.png")
    EnemyImage2=imagenes("enemigo2.png")
    EnemyImage3=imagenes("enemigo3.png")
    global PlayerLife,EnemyLife,DirectContactCondition,TimeElapsed,Points
    EnemyLife=0
    PlayerLife=DefaultPlayerLife
    Points=0
    DirectContactCondition=True
    PlayerShootDamage=1
    EnemyShootDamage=3
    EnemyContactDamage=10
    TimeElapsed=0
    
    GameWindow=tk.Toplevel()#Se crea una ventana secundaria para el juego
    GameWindow.title("Game")#Se le asigna un titulo a la ventana
    GameWindow.minsize(LevelsWidth,LevelsHeight)#Se le asigna dimensiones minimas a la ventana
    GameWindow.resizable(height=tk.NO,width=tk.NO)#Se bloquea que el usuario pueda cambiar el tamano de la pantalla
    root.resizable(height=tk.NO,width=tk.NO)#Establece que el usuario no sea capaz de alterar el largo ni el ancho de la ventana
    GameCanvas = tk.Canvas(GameWindow, bg="green", height=LevelsHeight, width=LevelsWidth)
    GameCanvas.place(x=0,y=0)
    ScoreLabel=tk.Label(GameWindow,text="puntaje=100",anchor=tk.CENTER,font=("Arial",13),height=1,width=10)
    ScoreLabel.place(x=0,y=LevelsHeight-30)
    TimeLabel=tk.Label(GameWindow,text="Tiempo=40",anchor=tk.CENTER,font=("Arial",13),height=1,width=11)
    TimeLabel.place(x=100,y=LevelsHeight-30)
    VidaLabel=tk.Label(GameWindow,text="Vida=40",anchor=tk.CENTER,font=("Arial",13),height=1,width=7)
    VidaLabel.place(x=210,y=LevelsHeight-30)
    EnemigoLabel=tk.Label(GameWindow,text="Enemigo=40",anchor=tk.CENTER,font=("Arial",13),height=1,width=11)
    EnemigoLabel.place(x=284,y=LevelsHeight-30)
    NameLabel=tk.Label(GameWindow,text="Nombre=Andrey",anchor=tk.CENTER,font=("Arial",13),height=1,width=16)
    NameLabel.place(x=395,y=LevelsHeight-30)
    draw_image(GameCanvas,Fondo,270,250)
    Nave=draw_image(GameCanvas,Nave_Image,400,600)
    NaveSizes=getImageSize("aliado.png")
    GameCanvas.addtag_withtag(NaveTag,Nave)
    print(NaveSizes)
    NaveWidth=NaveSizes[0]
    NaveHeight=NaveSizes[1]

    root.withdraw()
    
    def teclaPresionada(Evento):
        TeclaPresionada=Evento.keysym#Se decodifica la tecla presionada
        TeclaPresionadaLowerCase=TeclaPresionada.lower()
        
        if(TeclaPresionadaLowerCase=="w"):
             moveNaveUp()
          
        if(TeclaPresionadaLowerCase=="s"):
            moveNaveDown()
           
        if(TeclaPresionadaLowerCase=="a") :
            moveNaveLeft()
          
        if(TeclaPresionadaLowerCase=="d"):
            moveNaveRight()
        '''
        coordenadas=C_ventanaJuego.coords(Nave)#Se crea un tupla de dos elementos correspondiente la posicion en x y y de la nave
        x=coordenadas[0]#Se crea una variable correspondiente a la posicion en x
        y=coordenadas[1]#Se crea una variable correspondiente a l aposicion en y
        '''
    def moveNaveUp():
        moveObject(GameCanvas,Nave,0,-movement)
    def moveNaveDown():
        moveObject(GameCanvas,Nave,0,movement)
    def moveNaveRight():
        moveObject(GameCanvas,Nave,movement,0)
    def moveNaveLeft():
        moveObject(GameCanvas,Nave,-movement,0)
    def shoot(event):
        pauseThread=Thread(target=makePauseToShoot,args=())
        pauseThread.start()
        ShootImage=imagenes("disparoaliado.png")
        Coords=GameCanvas.coords(Nave)
        x=Coords[0]
        y=Coords[1]
        Shoot=draw_image(GameCanvas,AlleyShoot,x-2,y-70)
        GameCanvas.addtag_withtag(NaveShootTag,Shoot)
        MovingThread=Thread(target=move_shoot,args=(Shoot,-Shoot_Movement))
        MovingThread.start()
    def makePauseToShoot():
        GameWindow.unbind("<Button-1>")
        time.sleep(shoot_pause_time)
        GameWindow.bind("<Button-1>",shoot)
    def move_shoot(shoot,Move):
        try:
            if(stageEnded() or matchEnded()):
                GameCanvas.delete(shoot)
                return None
            bbox=GameCanvas.bbox(shoot)
            ContactTags=GameCanvas.find("overlapping",bbox[0],bbox[1],bbox[2],bbox[3])
            if(verifyCollission(shoot,ContactTags)):
               return None
            Coords=GameCanvas.coords(shoot)
            y_coord=Coords[1]
            if(Move<0 and y_coord+Move>0):
                moveObject(GameCanvas,shoot,0,Move)
                y_coord+=Move
                time.sleep(0.001)
                move_shoot(shoot,Move)
            if(Move>=0 and y_coord+Move<LevelsHeight):
                moveObject(GameCanvas,shoot,0,Move)
                y_coord+=Move
                time.sleep(0.001)
                move_shoot(shoot,Move)
                
            else:
                GameCanvas.delete(shoot)
        except:
            return None
   
    def enemyLevel1():
        global PlayerLife,EnemyLife
        PlayerLife=DefaultPlayerLife
        EnemyLife=EnemyLevel1Life
        Enemy=draw_image(GameCanvas,EnemyImage1,250,40)
        GameCanvas.addtag_withtag(EnemyTag,Enemy)
        MovementThread=Thread(target=enemyLevel1Cicle,args=(Enemy,Enemy1CicleTime,movement))
        MovementThread.start()
        ContactThread=Thread(target=detectCollisionWithEnemy,args=(Enemy,))
        ContactThread.start()
        
    def enemyLevel1Cicle(Enemy,TimeLeft,Move):
        if(matchEnded()):
                GameCanvas.delete(Enemy)
                return None
        if(TimeLeft<=0):
            RandomNumber=random.randint(1,10)
            if(RandomNumber%3==0):
                tackle(Enemy,2*movement,40,700)
                enemyLevel1Cicle(Enemy,Enemy1CicleTime,movement)
            else:
                enemyLevel1Cicle(Enemy,Enemy1CicleTime,Move)
                
                
        else:
            Move=horizontalEnemyMovement(Enemy,Move)
            time.sleep(0.1)
            enemyLevel1Cicle(Enemy,TimeLeft-0.1,Move)
            
    def enemyLevel2():
        global PlayerLife,EnemyLife
        PlayerLife=DefaultPlayerLife
        EnemyLife=EnemyLevel2Life
        Enemy=draw_image(GameCanvas,EnemyImage2,250,40)
        GameCanvas.addtag_withtag(EnemyTag,Enemy)
        EnemySizes=getImageSize("enemigo2.png")
        EnemyWidth=EnemySizes[0]
        MovingThread=Thread(target=enemyLevel2Cicle,args=(Enemy,Enemy2ShootPause,Enemy2TeleportPause,EnemyWidth/2))
        MovingThread.start()
    def enemyLevel2Cicle(Enemy,ShootTimeLeft,TeleportTimeLeft,EnemySize):
        if(TeleportTimeLeft<=0):
            teleport(Enemy,0+EnemySize,LevelsWidth-EnemySize)
            TeleportTimeLeft=Enemy2TeleportPause
        if(ShootTimeLeft<=0):
            print("Disparo")
            enemyShoot(Enemy,0,0)
            time.sleep(0.2)
            enemyShoot(Enemy,0,0)
            time.sleep(0.2)
            enemyShoot(Enemy,0,0)
            ShootTimeLeft=Enemy2ShootPause
        time.sleep(0.1)
        enemyLevel2Cicle(Enemy,ShootTimeLeft-0.1,TeleportTimeLeft-0.1,EnemySize)
        
    def teleport(Enemy,Min,Max):
        Coords=GameCanvas.coords(Enemy)
        x_pos=Coords[0]
        RandomPos=random.randint(0,LevelsWidth)
        Difference=RandomPos-x_pos
        moveObject(GameCanvas,Enemy,Difference,0)
        
        
    def horizontalEnemyMovement(Enemy,Move):
        Coords=GameCanvas.coords(Enemy)
        x_pos=Coords[0]
        if(Move>0 and x_pos+Move<LevelsWidth):
            moveObject(GameCanvas,Enemy,Move,0)
            #time.sleep(0.1)
            #horizontalEnemyMovement(Enemy,Move)
            return Move
        elif(Move<0 and x_pos+Move>0):
            moveObject(GameCanvas,Enemy,Move,0)
            #time.sleep(0.1)
            #horizontalEnemyMovement(Enemy,Move)
            return Move
        else:
            horizontalEnemyMovement(Enemy,-Move)
            return -Move
    def tackle(Enemy,Move,StartPos,EndPos):
        Coords=GameCanvas.coords(Enemy)
        y_pos=Coords[1]
        if(Move<0 and y_pos<=StartPos ):
            return None
        else:
            if(y_pos+Move>=EndPos):
                tackle(Enemy,-Move,StartPos,EndPos)
            else:
                moveObject(GameCanvas,Enemy,0,Move)
                time.sleep(0.1)
                tackle(Enemy,Move,StartPos,EndPos)
    def enemyShoot(Enemy,width,heigth):
        Coords=GameCanvas.coords(Enemy)
        x_pos=Coords[0]
        y_pos=Coords[1]
        Shoot=draw_image(GameCanvas,EnemyShoot,x_pos,y_pos)
        GameCanvas.addtag_withtag(EnemyShootTag,Shoot)
        MovingThread=Thread(target=move_shoot,args=(Shoot,Shoot_Movement))
        MovingThread.start()
    def verifyCollission(Object,EnclosedObjects):
        if(len(EnclosedObjects)==0):
            return False
        else:
            Tag=GameCanvas.gettags(Object)[0]
            CurrentElement=EnclosedObjects[0]
            LeftOver=EnclosedObjects[1:]
            CurrentElementTags=GameCanvas.gettags(CurrentElement)
            if(len(CurrentElementTags)==0):
                return verifyCollission(Object,LeftOver)
            else:
                CurrentTag=CurrentElementTags[0]
                if(DestructionRelation(Tag,CurrentTag,Object,CurrentElement)):
                    return True
                return verifyCollission(Object,LeftOver)
            
            
    def DestructionRelation(Tag1,Tag2,Object1,Object2):
        if(Tag1==EnemyShootTag and Tag2==NaveTag):
            global PlayerLife
            GameCanvas.delete(Object1)
            PlayerLife-=EnemyShootDamage
            print("hice contacto")
            return True
        if(Tag1==EnemyShootTag and Tag2==NaveShootTag):
            GameCanvas.delete(Object1)
            GameCanvas.delete(Object2)
            print("hice contacto")
            return True
        if(Tag1==NaveShootTag and Tag2==EnemyShootTag):
            GameCanvas.delete(Object1)
            GameCanvas.delete(Object2)
            print("hice contacto")
            return True
        if(Tag1==NaveShootTag and Tag2==EnemyTag):
            global EnemyLife,Points
            GameCanvas.delete(Object1)
            EnemyLife-=PlayerShootDamage
            Points+=1
            print("hice contacto")
            return True
        if(Tag1==EnemyTag and Tag2==NaveTag):
            if(DirectContactCondition):
                PlayerLife-=EnemyContactDamage
                print("hice contacto")
            
        return False
            
    def makeAbleToTouch():
        DirectContactCondition=False
        time.sleep(0.6)
        DirectContactCondition=True
    def detectCollisionWithEnemy(Enemy):
        if(matchEnded()):
            return None
        bbox=GameCanvas.bbox(Enemy)
        ContactTags=GameCanvas.find("overlapping",bbox[0],bbox[1],bbox[2],bbox[3])
        verifyCollission(Enemy,ContactTags)
        makeAbleToTouch()
        detectCollisionWithEnemy(Enemy)
    def cronometer():
        global TimeElapsed
        if(matchEnded()):
            return None
        try:
            time.sleep(1)
            TimeElapsed+=1
            cronometer()
        except RecursionError:
            cronometer()
    def updateLabels():
        
        try:
            TimeText="Tiempo="+str(TimeElapsed)
            TimeLabel["text"]=TimeText
            LifeText="Vida="+str(PlayerLife)
            VidaLabel["text"]=LifeText
            ScoreText="Puntaje="+str(Points)
            ScoreLabel["text"]=ScoreText
            EnemyText="Enemigo="+str(EnemyLife)
            EnemigoLabel["text"]=EnemyText
            time.sleep(0.1)
            updateLabels()
        except RecursionError:
            updateLabels()
        except:
            print("fin")
            if(matchEnded()):
                return None
        
    def stageEnded():
        return EnemyLife<=0
    def matchEnded():
        return PlayerLife<=0
    def exit():
        GameWindow.destroy()
        root.deiconify()
        
    '''
EnemyTag="Enemy"
EnemyShootTag="EnemyShoot"
NaveShootTag="Shoot"
NaveTag="Nave"
'''
        
    #enemyLevel1()
    CronometerThread=Thread(target=cronometer,args=())
    LabelsThread=Thread(target=updateLabels,args=())
    CronometerThread.start()
    LabelsThread.start()
    enemyLevel1()
    GameWindow.bind("<KeyPress>",teclaPresionada)
    GameWindow.bind("<Button-1>",shoot)
    GameWindow.mainloop()

  
    
    
root=tk.Tk()#Asigna a root como la ventana principal
root.title("my Game")#Asigna un titulo a la ventana
root.minsize(mainWindowWidth,mainWindowHeight)#Establece dimensiones minimas para la ventana principal
root.resizable(height=tk.NO,width=tk.NO)#Establece que el usuario no sea capaz de alterar el largo ni el ancho de la ventana
myCanvas = tk.Canvas(root, bg="green", height=mainWindowHeight, width=mainWindowWidth)
myCanvas.place(x=0,y=0)
imagenFondo=import_image("inicio.png",mainWindowWidth,mainWindowHeight)
draw_image(myCanvas,imagenFondo,320,230)
myFont = font.Font(size=20)
ButtonAbout=tk.Button(root,text="About",command=aboutWindow,bg="yellow")
ButtonAbout['font']=myFont
ButtonAbout.place(x=550,y=390)
ButtonMaxScores=tk.Button(root,text="Scores",command=scoresWindow,bg="yellow")
ButtonMaxScores['font']=myFont
ButtonMaxScores.place(x=535,y=10)
ButtonPlay=tk.Button(root,text="Play",command=GameWindow,bg="yellow")
ButtonPlay['font']=myFont
ButtonPlay.place(x=40,y=390)
root.mainloop()

        
    
        
    

