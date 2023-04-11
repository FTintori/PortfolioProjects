from turtle import Screen, Turtle

class Borders(Turtle):
    def __init__(self):
        super().__init__()
        self = Turtle()
        self.penup()
        self.hideturtle()
        self.speed("fastest")
        self.goto(-1000,300)
        self.color("white")
        self.pendown()
        self.goto(1000,300)
        self.goto(1000,-300)
        self.goto(-1000,-300)
