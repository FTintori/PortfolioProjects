import time
from turtle import Turtle


ALIGNMENT = "center"
FONT = ('Courier', 20,'normal')
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.goto(0, 307)
        self.hideturtle()
        self.color("white")
        self.refresh()

    def refresh(self):
        self.clear()
        with open("data.txt") as file:
            self.highscore = int(file.read())
        self.write(f"Score: {self.score}   High Score:  {self.highscore}", align=ALIGNMENT, font=FONT)

    # def game_over(self):
    #     self.goto(0,0)
    #     self.write("GAME OVER", align=ALIGNMENT, font=FONT)

    def reset(self):
        if self.score > self.highscore:
            with open("data.txt", mode="w") as file:
                file.write(f"{self.score}")
        self.score = 0
        self.refresh()
        # self.goto(0,0)
        # self.write("Get ready for next round!", align=ALIGNMENT, font=FONT)
        # time.sleep(2)
        # self.clear()
        # self.goto(0, 307)
        # self.refresh()


