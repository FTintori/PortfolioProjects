from turtle import Screen, Turtle
import time
from Snake import Snake
from Food import Food
from scoreboard import Scoreboard


screen = Screen()
screen.setup(width=650, height=670)
screen.bgcolor("black")
screen.title("Snake VI")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()


screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")


field_sides = Turtle()
field_sides.color("White")
field_sides.penup()
field_sides.goto(-310,-310)
field_sides.hideturtle()
field_sides.speed("fastest")
field_sides.pendown()
field_sides.goto(310,-310)
field_sides.goto(310,310)
field_sides.goto(-310,310)
field_sides.goto(-310,-310)

def go_on():
    pass
screen.onkey(go_on, "y")


game_on = True
while game_on:
    time.sleep(.1)
    screen.update()
    snake.move()
    if snake.head.distance(food) < 15:
        food.refresh()
        scoreboard.score += 1
        scoreboard.refresh()
        snake.extend()
    if snake.head.xcor() > 300 or snake.head.xcor() < -300 or snake.head.ycor() > 300 or snake.head.ycor() < -300:
        # game_on = False
        scoreboard.reset()

        snake.reset()

    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            scoreboard.reset()

            snake.reset()
            # game_on = False

screen.exitonclick()


