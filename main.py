import random
from tkinter import *
import time

def dice_roll():
    dice_number = random.randrange(1, 7, 1)
    return dice_number

def create_pawn(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = create_pawn


class matching_position():
    def find_snake_or_ladder(self, block, turn, position):
        x = 35*(turn>=3)
        y = (turn%3)*35
        if(block == 3):
           return 305+x, 150+y, 22
        elif(block == 5):
            return 545+x, 390+y, 8
        elif(block == 11):
            return 185+x, 30+y, 26
        elif(block == 20):
            return 545+x, 30+y, 29
        elif(block == 17):
           return 425+x, 510+y, 4
        elif(block == 19):
           return 665+x, 390+y, 7
        elif(block == 21):
           return 425+x, 390+y, 9
        elif(block == 27):
           return 65+x, 510+y, 1
        else:
            return position[0], position[1], block
        

class game_board(object):
    def _init_(self,master,img):

        
        board_width = 850
        board_height = 600
        self.color = ["#FFF", "#F00", "#0F0", "#00F", "#FF0", "#0FF"]
        self.canvas = Canvas(master, width = board_width, height = board_height, bg = "brown")
        self.canvas.grid(padx=0, pady=0)
        self.canvas.create_image(360,300,anchor=CENTER, image = img)

        self.x = 65
        self.y = 510
        self.m = []
        self.num_player = "Players"
        self.player = []
        self.position = []
        self.i = 0
        self.block=[]
        self.dice_number = 1
        self.turn = 0
        
        
        OPTIONS = ["Players", "2", "3", "4", "5", "6"]
        variable = StringVar(master)
        variable.set(OPTIONS[0]) 
        w = OptionMenu(self.canvas, variable, *OPTIONS, command=self.choose)
        w.pack()
        w.place(x=740, y=225)
        w.config(font=('calibri',(10)),bg='white',width=5)
        
        
        self.start_game = Button(self.canvas, text="Start", background='white', command = self.start_game, font=("Helvetica"))
        self.start_game.place(x=770, y=400)

    def start_game(self):
        if(self.num_player == "Players"):
            pass
        else:
            self.canvas.create_rectangle(810, 150, 760, 100, fill='white', outline='black')
            self.canvas.pack(fill=BOTH, expand=1)
           
            self.diceRoll = Button(self.canvas, text="Roll",background='white',command = self.play_game, font=("Helvetica"))
            self.num_player = int(self.num_player)
            self.diceRoll.place(x=770, y=165)
            self.create_peice()
            self.start_game.place(x=-30, y=-30)


    def choose(self, value):
        self.num_player = value

    def rolling_dice(self, position, turn):
        dice_number = dice_roll()
        dice_value = Label(self.canvas, text=str(dice_number),background='white', font=("Helvetica", 25))
        dice_value.pack()
        dice_value.place(x=775, y=105)
        
        
        self.x, self.y = position[0], position[1]
        if(dice_number+self.block[turn] > 30):
            return [self.x, self.y]
        
        self.dice_number = dice_number
        self.block[turn] += dice_number
        
        self.canvas.delete(self.player[turn])
        self.player_pieces(dice_number, turn)

        return [self.x, self.y]
 
    def player_pieces(self, dice_number, turn):
    
        for i in range(dice_number,0,-1):
            self.x = self.x+120*self.m[turn]

            if(self.x>665 and turn < 3):
                self.y = self.y - 120
                self.x = 665
                self.m[turn] = -1
            elif(self.x>700 and turn >=3):
                self.y = self.y - 120
                self.x = 700
                self.m[turn] = -1
            if(self.x<65 and turn < 3):
                self.x = 65
                self.y -= 120
                self.m[turn] = 1
            elif(self.x<100 and turn >=3):
                self.x = 100
                self.y -= 120
                self.m[turn] = 1 
            if(self.y<30):
                self.y=30

            self.canvas.delete(self.player[turn])
            self.player[turn] = self.canvas.create_circle(self.x, self.y, 15, fill=self.color[turn], outline=self.color[turn])
            self.canvas.update()
            time.sleep(0.25)

            
        print(self.x, self.y, self.block[turn])
        self.x, self.y, self.block[turn] = matching_position().find_snake_or_ladder(self.block[turn], turn, [self.x, self.y])
        
        if(any(self.y == ai for ai in [390, 425, 460, 150, 185, 220])):
            self.m[turn] = -1
        else:
            self.m[turn] = 1
        print(self.x,self.y, self.block[turn])
        self.canvas.delete(self.player[turn])
        self.player[turn] = self.canvas.create_circle(self.x, self.y, 15, fill=self.color[turn], outline="")


    def create_peice(self):
        for i in range(int(self.num_player)):
            if(i==3):
                self.x += 35
                self.y -= 105
            self.player.append(self.canvas.create_circle(self.x, self.y, 15, fill=self.color[i], outline=""))
            self.position.append([self.x, self.y])
            self.m.append(1)
            self.block.append(1)
            self.y += 35

    def play_game(self):
        if(self.dice_number == 6):
            turn = self.turn
        else:
            turn = self.i%self.num_player
            self.i += 1
            self.turn = turn
        self.position[turn] = self.rolling_dice(self.position[turn], turn)
        if(self.block[self.turn] >= 30):
            self.diceRoll.place(x=-30, y=-30)
            print("Won", self.turn+1)
            top = Toplevel()
            top.title("Snake and Ladder")
            message = "Player " + str(self.turn+1) + " Won" 
            msg = Message(top, text=message)
            top.geometry("%dx%d%+d%+d" % (100, 100, 250, 125))
            msg.pack()
            button = Button(top, text="Dismiss", command=top.destroy)
            button.pack()
            
     
def main():
    master = Tk()
    master.title("Snake and Ladder")
    master.geometry("850x600")
    img=PhotoImage( file = "snake.jpg")
    x = game_board(master,img)
    master.mainloop()

main()