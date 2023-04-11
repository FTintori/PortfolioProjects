from turtle import Turtle
import time
FONT = ('Courier', 20,'normal')
ALIGNMENT = "center"


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.P1score = 0
        self.P2score = 0
        self.hideturtle()
        self.speed("fastest")
        self.penup()
        self.goto(0,320)
        self.write(f"P1 Score: {self.P1score}           P2 Score: {self.P2score}", font=FONT, align=ALIGNMENT)

    def refresh(self):
        self.clear()
        self.write(f"P1 Score: {self.P1score}           P2 Score: {self.P2score}", font=FONT, align=ALIGNMENT)


    def countdown(self):
        countdown = Turtle()
        countdown.color("white")
        countdown.speed("fastest")
        countdown.hideturtle()
        countdown.penup()
        countdown.write("5...", font=FONT, align=ALIGNMENT)
        time.sleep(1)
        countdown.clear()
        countdown.write("4...", font=FONT, align=ALIGNMENT)
        time.sleep(1)
        countdown.clear()
        countdown.write("3...", font=FONT, align=ALIGNMENT)
        time.sleep(1)
        countdown.clear()
        countdown.write("2...", font=FONT, align=ALIGNMENT)
        time.sleep(1)
        countdown.clear()
        countdown.write("1...", font=FONT, align=ALIGNMENT)
        time.sleep(1)
        countdown.clear()
        countdown.write("Go!", font=FONT, align=ALIGNMENT)
        time.sleep(0.5)
        countdown.clear()