import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW, BOTTOM, Button


WIDTH = 700
HEIGHT = 700
waiting = 100
sizeOfSeg = 20
maxCountOfSeg = WIDTH * HEIGHT / (sizeOfSeg * sizeOfSeg)
randApple = 30
x = [0] * int(maxCountOfSeg)
y = [0] * int(maxCountOfSeg)

root = Tk()

class Board(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, background="black", highlightthickness=0)
        self.parent = parent
        self.CreateGame()
        self.pack()

    def CreateGame(self):
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.inGame = True
        self.segments = 3
        self.appleX = 100
        self.appleY = 190

        for i in range(self.segments):
            x[i] = 100 - i * sizeOfSeg
            y[i] = 100

        try:
            self.isegments = Image.open("seg.png")
            self.segments = ImageTk.PhotoImage(self.isegments)
            self.Rhead = Image.open("headR.png")
            self.head = ImageTk.PhotoImage(self.Rhead)
            self.iapple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.iapple)
        except FileNotFoundError:
            print("Can't open image")
            sys.exit(1)

        self.focus_get()
        self.createObjects()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(waiting, self.onTimer)

    def createObjects(self):

        self.create_image(self.appleX, self.appleY, image=self.apple, anchor=NW, tag="apple")
        self.create_image(100, 100, image=self.head, anchor=NW, tag="head")
        self.create_image(70, 100, image=self.segments, anchor=NW, tag="seg")
        self.create_image(40, 100, image=self.segments, anchor=NW, tag="seg")

    def locateApple(self):

        apple = self.find_withtag("apple")
        self.delete(apple[0])

        randNum = random.randint(0, randApple)
        self.appleX = randNum * sizeOfSeg
        r = random.randint(0, randApple)
        self.appleY = randNum * sizeOfSeg

        self.create_image(self.appleX, self.appleY, anchor=NW, image=self.apple, tag="apple")

    def checkApple(self):

        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:

            if apple[0] == ovr:
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.segments, anchor=NW, tag="seg")
                self.locateApple()

    def doMove(self):

        segments = self.find_withtag("seg")
        head = self.find_withtag("head")

        body = segments + head

        k = 0
        while k < len(body) - 1:
            c1 = self.coords(body[k])
            c2 = self.coords(body[k + 1])
            self.move(body[k], c2[0] - c1[0], c2[1] - c1[1])
            k += 1

        if self.left:
            self.move(head, -sizeOfSeg, 0)

        if self.right:
            self.move(head, sizeOfSeg, 0)

        if self.up:
            self.move(head, 0, -sizeOfSeg)

        if self.down:
            self.move(head, 0, sizeOfSeg)

    def onKeyPressed(self, pressKey):

        key = pressKey.keysym

        if key == "Left" and not self.right:
            self.left = True
            self.up = False
            self.down = False

        if key == "Right" and not self.left:
            self.right = True
            self.up = False
            self.down = False

        if key == "Up" and not self.down:
            self.up = True
            self.right = False
            self.left = False

        if key == "Down" and not self.up:
            self.down = True
            self.right = False
            self.left = False

    def checkCollisions(self):

        segments = self.find_withtag("seg")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for seg in segments:
            for over in overlap:
                if over == seg:
                    self.inGame = False

        if x1 < 0:
            self.inGame = False

        if x1 > WIDTH - sizeOfSeg:
            self.inGame = False

        if y1 < 0:
            self.inGame = False

        if y1 > HEIGHT - sizeOfSeg:
            self.inGame = False

    def onTimer(self):

        if self.inGame:
            self.checkCollisions()
            self.checkApple()
            self.doMove()
            self.after(waiting, self.onTimer)
        else:
            self.gameOver()

    def gameOver(self):

        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text="Game Over", fill="white")

class SnakeGame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title('Snake')
        self.board = Board(parent)
        self.pack()



class Menu(Frame, Canvas):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Canvas.__init__(self, width=950, height=530,
                        background="black", highlightthickness=0)
        self.parent = parent

        parent.title('Snake')
        try:
            self.iimage = Image.open("background.png")
            self.image = ImageTk.PhotoImage(self.iimage)
        except FileNotFoundError:
            print("Can't open image")
        self.focus_get()
        self.create_image(1, 1, image=self.image, anchor=NW, tag="menu")
        self.pack()



def click_button1():
    root.destroy()
    rootGame=Tk()
    snake = SnakeGame(rootGame)
    rootGame.mainloop()



menu = Menu(root)
button1 = Button(root, height=1, width=12, text="Quit", command=root.quit)
button1.pack(side=BOTTOM)
button = Button(height=1, width=12, text="Start", command=click_button1)
button.pack(side=BOTTOM)

root.mainloop()