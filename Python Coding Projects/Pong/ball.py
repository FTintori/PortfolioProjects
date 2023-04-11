from turtle import Turtle

MOVE_STEP = 10

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.reset_ball()


    def reset_ball(self):
        self.shape("square")
        self.color("white")
        self.penup()
        self.goto(0,0)
        self.new_x = 0
        self.new_y = 0
        self.y_pace = MOVE_STEP
        self.x_pace = MOVE_STEP
        self.current_speed = 0.1

    def move(self):
        self.new_x = self.xcor() + self.x_pace
        self.new_y = self.ycor() + self.y_pace
        self.goto(self.new_x, self.new_y)


    def wall_bounce(self):
        self.y_pace *= -1


    def paddle_bounce(self):
        self.x_pace *= -1
        self.current_speed *= 0.9


