from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, player_num):
        super().__init__()
        self.color("white")
        self.penup()
        self.shape("square")
        self.speed("fastest")
        if player_num == 1:
            self.goto(-500, 0)
        elif player_num == 2:
            self.goto(+500, 0)
        self.shapesize(stretch_wid=5, stretch_len=1)

    def up(self):
        new_pos = self.ycor() +20
        self.goto(self.xcor(), new_pos)

    def down(self):
        new_pos = self.ycor() - 20
        self.goto(self.xcor(), new_pos)