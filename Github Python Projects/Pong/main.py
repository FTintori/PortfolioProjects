from turtle import Turtle, Screen
from scoreboard import Scoreboard
from paddles import Paddle
from game_area import Borders
from ball import Ball
import time



screen = Screen()
screen.screensize(800,700)
screen.setup(1200, 800)
screen.bgcolor("black")
screen.tracer(0)

borders = Borders()
scoreboard = Scoreboard()
P1paddle = Paddle(1)
P2paddle = Paddle(2)
ball = Ball()

screen.listen()
screen.onkey(P1paddle.up, "w")
screen.onkey(P1paddle.down, "s")
screen.onkey(P2paddle.up, "Up")
screen.onkey(P2paddle.down, "Down")


game_on = True
while game_on:
    time.sleep(ball.current_speed)
    ball.move()
    screen.update()
    if ball.ycor() == 290 or ball.ycor() == -290:
        ball.wall_bounce()
    if ball.distance(P2paddle) < 62.3 and ball.xcor() == +480 or ball.distance(P1paddle) < 62.3 and ball.xcor() == -480:
        ball.paddle_bounce()
    if ball.xcor() > 500:
        scoreboard.P1score += 1
        scoreboard.refresh()
        scoreboard.countdown()
        ball.reset_ball()

    if ball.xcor() < -500:
        scoreboard.P2score += 1
        scoreboard.refresh()
        scoreboard.countdown()
        ball.reset_ball()



screen.exitonclick()