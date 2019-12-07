from tkinter import *
from PIL import Image, ImageTk
import math
import random
import time

class Window(Frame):
    def __init__(self, Master=None):
        self.Started=False
        Frame.__init__(self, Master)
        self.Master=Master
        self.InitWindow()

    def  InitWindow(self):
        self.Moving=[True]
        self.SnakeTick=0
        Root.configure(background='light grey')
        self.Master.title("GUI")
        self.Canvas = Canvas(Root, width = 600, height = 400)
        self.Canvas.pack()
        self.Turn=0
        self.Die=Button(Root, text = "Click me \n to roll", command=self.Role)
        self.Die.place(x=470, y=170, width= 60, height = 60)
        self.Regen=Button(Root, text = "Regenerate", command=self.Regenerate)
        self.Regen.place(x=465, y=20, width= 70, height = 60)
        self.AnimateSnakes=IntVar(Root)
        self.AnimateSnakeCheck=Checkbutton(Root,text = "Animate snakes?", variable = self.AnimateSnakes)
        self.AnimateSnakeCheck.place(x=420, y=240)
        self.AnimateLadders=IntVar(Root)
        self.AnimateLadderCheck=Checkbutton(Root,text = "Animate ladders?", variable = self.AnimateLadders)
        self.AnimateLadderCheck.place(x=420, y=260)
        self.AllowRollSeven=IntVar(Root)
        self.AllowRollSevenCheck=Checkbutton(Root,text = "Allow roll 7 \n (1/21 chance to place \n ladders or snakes)?", variable = self.AllowRollSeven)
        self.AllowRollSevenCheck.place(x=420, y=350)
        self.WiggleFactorSlide=Scale(Root, from_=0, to=100, orient="horizontal", label="Wiggle factor:")
        self.WiggleFactorSlide.place(x=420, y=285)
        self.WiggleFactorSlide.set(40)
        self.AnimateSnakeCheck.select()
        self.AllowRollSevenCheck.select()
        self.StatusText=Label(Root, text = str("Player "+str(self.Turn+1)+"'s turn"))
        self.StatusText.place(x=460, y=120)
        self.PlayerImages=[]
        for PlayerNum in range(0,4):
            self.PlayerImages.append(ImageTk.PhotoImage(Image.open("P"+str(PlayerNum+1)+".png").resize((20,20))))
        self.TileImg=ImageTk.PhotoImage(Image.open("Tile.png").resize((40,40)))
        self.SnakeImages=[]
        self.SnakeImages.append(Image.open("SnakeTail.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeBody.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead1.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead2.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead3.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead4.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead5.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead4.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead3.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead2.png").resize((40,40)))
        self.SnakeImages.append(Image.open("SnakeHead.png").resize((40,40)))
        self.LadderImage=Image.open("Ladder.png").resize((35,35))
        self.PlayerPositions=[1,1,1,1]
        self.Regenerate()
        self.UpdateDisplay()
        while True:
            Time=time.time()
            Root.update()
            self.UpdateDisplay()
            if time.time()-Time<0.016:
                time.sleep(0.016-(time.time()-Time))
        
    def Regenerate(self):
        self.LadderSnakes=[]
        self.SnakeTick=90
        for LadderSnakeNum in range(0,random.randint(4,6)):
            Invalid=True
            while Invalid:
                Start=random.randint(2,99)
                Invalid=False
                for LadderSnake in self.LadderSnakes:
                    if Start in LadderSnake:
                        Invalid=True
            Invalid=True
            while Invalid:
                End=random.randint(2,99)
                Invalid=False
                for LadderSnake in self.LadderSnakes:
                    if End in LadderSnake:
                        Invalid=True
                if End==Start:
                    Invalid=True
                elif End>Start:
                    if End-10<Start:
                        Invalid=True
                else:
                    if End+10>Start:
                        Invalid=True
            self.LadderSnakes.append([Start,End])

    def Role(self):
        self.Die.destroy()
        if self.AllowRollSeven.get():
            self.Result=random.randint(1,7)
            if self.Result==7 and not(random.randint(0,2)==0):
                self.Result=random.randint(1,6)
        else:
            self.Result=random.randint(1,6)
        if not self.Result == 7:
            self.Moving=[True,self.PlayerPositions[self.Turn]]
            self.PlayerPositions[self.Turn]+=self.Result
        if self.PlayerPositions[self.Turn]>=100:
            self.PlayerPositions[self.Turn]=100
            self.UpdateDisplay()
            self.Die=Button(Root, text = self.Result, command=self.Role)
            self.Die.place(x=100000, y=170, width= 60, height = 60)
            self.Regen.place(x=100000, y=170, width= 60, height = 60)
            self.StatusText=Label(Root, text = str("Player "+str(self.Turn+1)+" has won!"))
            self.StatusText.place(x=460, y=120)
            while True:
                Root.update()
        for LadderSnake in self.LadderSnakes:
            if self.PlayerPositions[self.Turn]==LadderSnake[0]:
                self.PlayerPositions[self.Turn]=LadderSnake[1]
        self.Turn+=1
        if self.Turn>3:
            self.Turn=0
        self.UpdateDisplay()
        if not self.Result==7:
            self.Die=Button(Root, text = self.Result, command=self.Role)
            self.Die.place(x=470, y=170, width= 60, height = 60)
            self.StatusText=Label(Root, text = str("Player "+str(self.Turn+1)+"'s turn"))
            self.StatusText.place(x=460, y=120)
        else:
            self.Die.destroy()
            self.StatusText=Label(Root, text = str("Place a ladder/snake by \n clicking on two locations \n on the board!"))
            self.StatusText.place(x=430, y=120)
            self.NotPlaced=True
            self.SnakeToAdd=[]
            self.Canvas.bind("<Button-1>", self.Click)
            while self.NotPlaced:
                self.UpdateDisplay()
                Root.update()
                time.sleep(0.016)
            self.StatusText.destroy()
            self.StatusText=Label(Root, text = str("Player "+str(self.Turn+1)+"'s turn"))
            self.StatusText.place(x=460, y=120)
            self.Die=Button(Root, text = "Click me \n to role", command=self.Role)
            self.Die.place(x=470, y=170, width= 60, height = 60)
            
    def Click(self, event):
        if self.NotPlaced:
            MousePos=[event.x,event.y]
            MousePos[0]=round((MousePos[0]-20)/40)
            MousePos[1]=round((MousePos[1]-20)/40)
            New=True
            for LadderSnake in self.LadderSnakes:
                if LadderSnake[0]==100-(MousePos[1]*10+ abs((MousePos[1]%2)*9-MousePos[0])) or LadderSnake[1]==100-(MousePos[1]*10+ abs((MousePos[1]%2)*9-MousePos[0])):
                    New=False
            if not (MousePos[0]>9 or 100-(MousePos[1]*10+ abs((MousePos[1]%2)*9-MousePos[0]))== 100 or 100-(MousePos[1]*10+ abs((MousePos[1]%2)*9-MousePos[0]))== 1 or
                    100-(MousePos[1]*10+ abs((MousePos[1]%2)*9-MousePos[0])) in self.SnakeToAdd or 100-(MousePos[1]*10+ abs((MousePos[1]%2)*9-MousePos[0])) in self.LadderSnakes) and New:
                self.SnakeToAdd.append(100-(MousePos[1]*10+ abs((MousePos[1]%2)*9-MousePos[0])))
                if len(self.SnakeToAdd)==2:
                    self.LadderSnakes.append(self.SnakeToAdd)
                    self.NotPlaced=False
        
    def UpdateDisplay(self):
        self.WiggleFactor=self.WiggleFactorSlide.get()/100
        if self.AnimateSnakes.get():
            self.SnakeTick-=10
        else:
            if (self.SnakeTick)%360==0:
                self.SnakeTick=0
            else:
                if abs(self.SnakeTick)<=360:
                    self.SnakeTick+=((0-self.SnakeTick)/4)
                else:
                    self.SnakeTick=-180
        self.Canvas.delete("all")
        self.Tiles=[]
        for YVar in range (0,10):
            for XVar in range (0,10):
                TempTile=self.Canvas.create_image(XVar*40, YVar*40, anchor=NW, image=self.TileImg)
                TempTileText=self.Canvas.create_text(XVar*40+20,YVar*40+20,fill="white",font="Times 15 bold",
                        text=str(100-(YVar*10+ abs((YVar%2)*9-XVar))))
                self.Tiles.append([TempTile,TempTileText])
        self.LadderSnakeImages=[]
        self.ImageSaver=[]
        HeadOffset=1
        for LadderSnake in self.LadderSnakes:
            TempLadderSnake=[]
            if LadderSnake[0]>LadderSnake[1]:
                Angle=math.degrees(math.atan2((self.ConvertToX(LadderSnake[1])-self.ConvertToX(LadderSnake[0])),(((100-LadderSnake[1])//10)*40-((100-LadderSnake[0])//10)*40)))
                Distance=math.sqrt((self.ConvertToX(LadderSnake[1])-self.ConvertToX(LadderSnake[0]))**2+(((100-LadderSnake[1])//10)*40-((100-LadderSnake[0])//10)*40)**2)
                StartDist=math.sqrt((self.ConvertToX(LadderSnake[1])-self.ConvertToX(LadderSnake[0]))**2+(((100-LadderSnake[1])//10)*40-((100-LadderSnake[0])//10)*40)**2)
                TwistAngle=Angle+math.degrees(math.atan(math.cos(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))))*self.WiggleFactor*(StartDist/400)
                self.ImageSaver.append(ImageTk.PhotoImage(self.SnakeImages[0].rotate(TwistAngle, expand=True, center=(self.SnakeImages[0].width/2,self.SnakeImages[0].height/2))))
                TempLadderSnake.append(self.Canvas.create_image(self.ConvertToX(LadderSnake[0])+math.sin(math.radians(Angle))*Distance+
                                                                math.sin(math.radians(Angle+90))*math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*40*self.WiggleFactor*(StartDist/400)*HeadOffset
                    ,((100-LadderSnake[0])//10)*40+math.cos(math.radians(Angle))*Distance+
                                                                 math.cos(math.radians(Angle+90))*math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*40*self.WiggleFactor*(StartDist/400)*HeadOffset
                    ,anchor=NW, image=self.ImageSaver[-1]))
                while Distance>38:
                    Distance-=30/(1+abs(math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*self.WiggleFactor*(StartDist/400)))
                    TwistAngle=Angle+math.degrees(math.atan(math.cos(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))))*self.WiggleFactor*(StartDist/400)
                    self.ImageSaver.append(ImageTk.PhotoImage(self.SnakeImages[1].rotate(TwistAngle, expand=True, center=(self.SnakeImages[1].width/2,self.SnakeImages[1].height/2))))
                    TempLadderSnake.append(self.Canvas.create_image(self.ConvertToX(LadderSnake[0])+math.sin(math.radians(Angle))*Distance+
                                                                    math.sin(math.radians(Angle+90))*math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*40*self.WiggleFactor*(StartDist/400)
                        ,((100-LadderSnake[0])//10)*40+math.cos(math.radians(Angle))*Distance+
                                                                     math.cos(math.radians(Angle+90))*math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*40*self.WiggleFactor*(StartDist/400)
                        ,anchor=NW, image=self.ImageSaver[-1]))
                if Distance>30:
                    Distance-=Distance/2
                    TwistAngle=Angle+math.degrees(math.atan(math.cos(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))))*self.WiggleFactor*(StartDist/400)
                    self.ImageSaver.append(ImageTk.PhotoImage(self.SnakeImages[1].rotate(TwistAngle, expand=True, center=(self.SnakeImages[1].width/2,self.SnakeImages[1].height/2))))
                    TempLadderSnake.append(self.Canvas.create_image(self.ConvertToX(LadderSnake[0])+math.sin(math.radians(Angle))*Distance+
                                                                    math.sin(math.radians(Angle+90))*math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*40*self.WiggleFactor*(StartDist/400)
                        ,((100-LadderSnake[0])//10)*40+math.cos(math.radians(Angle))*Distance+
                                                                     math.cos(math.radians(Angle+90))*math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*40*self.WiggleFactor*(StartDist/400)
                        ,anchor=NW, image=self.ImageSaver[-1]))
                Distance=0
                TwistAngle=Angle+math.degrees(math.atan(math.cos(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))))*self.WiggleFactor*(StartDist/400)
                self.ImageSaver.append(ImageTk.PhotoImage(self.SnakeImages[2+round(abs(self.SnakeTick)/10)%10].rotate(TwistAngle, expand=True, center=(self.SnakeImages[2].width/2,self.SnakeImages[2].height/2))))
                TempLadderSnake.append(self.Canvas.create_image(self.ConvertToX(LadderSnake[0])+math.sin(math.radians(Angle))*Distance+
                                                                math.sin(math.radians(Angle+90))*math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*40*self.WiggleFactor*(StartDist/400)*HeadOffset
                    ,((100-LadderSnake[0])//10)*40+math.cos(math.radians(Angle))*Distance+
                                                                 math.cos(math.radians(Angle+90))*math.sin(math.radians((Distance-StartDist+self.SnakeTick)/((1/360)*StartDist)))*40*self.WiggleFactor*(StartDist/400)*HeadOffset
                    , anchor=NW, image=self.ImageSaver[-1]))
            else:
                LadderRattle=round(self.WiggleFactor*200*self.AnimateLadders.get())
                Angle=math.degrees(math.atan2((self.ConvertToX(LadderSnake[1])-self.ConvertToX(LadderSnake[0])),(((100-LadderSnake[1])//10)*40-((100-LadderSnake[0])//10)*40)))
                self.ImageSaver.append(ImageTk.PhotoImage(self.LadderImage.rotate(Angle, expand=True)))
                TempLadderSnake.append(self.Canvas.create_image(self.ConvertToX(LadderSnake[0])+random.randint(-LadderRattle,LadderRattle)/100, ((100-LadderSnake[0])//10)*40+random.randint(-LadderRattle,LadderRattle)/100, anchor=NW, image=self.ImageSaver[-1]))
                Distance=math.sqrt((self.ConvertToX(LadderSnake[1])-self.ConvertToX(LadderSnake[0]))**2+(((100-LadderSnake[1])//10)*40-((100-LadderSnake[0])//10)*40)**2)
                while Distance>0:
                    TempLadderSnake.append(self.Canvas.create_image(self.ConvertToX(LadderSnake[0])+math.sin(math.radians(Angle))*Distance+random.randint(-LadderRattle,LadderRattle)/100,((100-LadderSnake[0])//10)*40+math.cos(
                        math.radians(Angle))*Distance+random.randint(-LadderRattle,LadderRattle)/100, anchor=NW, image=self.ImageSaver[-1]))
                    Distance-=34
            self.LadderSnakeImages.append(TempLadderSnake)
        self.PlayerCounters=[]
        for PlayerNum in range(0,len(self.PlayerPositions)):
            self.PlayerCounters.append(self.Canvas.create_image(self.ConvertToX(self.PlayerPositions[PlayerNum])+10,
                                      ((100-self.PlayerPositions[PlayerNum])//10)*40+10,anchor=NW, image=self.PlayerImages[PlayerNum]))
    
    def ConvertToX(self,PositionNum):
        return(((9*(1-int((100-PositionNum)//20==(((100-PositionNum)//10)/2))))+
                                       (((100-PositionNum)%10)*(int((100-PositionNum)//20==(((100-PositionNum)//10)/2))*2-1)))
                                      *40)

Root=Tk()
Root.geometry("600x400")
App=Window(Root)
Root.mainloop()
