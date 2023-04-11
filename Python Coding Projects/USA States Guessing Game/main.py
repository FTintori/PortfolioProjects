import turtle
import pandas
screen = turtle.Screen()
screen.title("US States Guessing Game")

screen.addshape("blank_states_img.gif")
turtle.shape("blank_states_img.gif")

# def click_coordinate(x, y):
#     print(x, y)
# turtle.onscreenclick(click_coordinate)


data = pandas.read_csv("50_states.csv")
game_on = True
states = list(data["state"])
answer_state_turtle = turtle.Turtle()
answer_state_turtle.hideturtle()
answer_state_turtle.penup()
score = 0
correct_guesses = []
while len(correct_guesses) < 50:
    answer_state = screen.textinput(title=f"Score: {score}/50", prompt= "What is the name of a state?").title()
    if answer_state == "Exit":
        break
    if answer_state in states and answer_state not in correct_guesses:
        score += 1
        state_row = data[data["state"] == answer_state]
        x_cor = (int(state_row.x))
        y_cor = (int(state_row.y))
        answer_state_turtle.goto(x_cor, y_cor)
        answer_state_turtle.write(f"{answer_state}")
        correct_guesses.append(answer_state)

# missed_states = []
# for state in states:
#     if state not in correct_guesses:
#         missed_states.append(state)
missed_states = [stat for stat in states if stat not in correct_guesses]

dict = {"Missed_States": missed_states }
miss_st = pandas.DataFrame(dict)
miss_st.to_csv("Missed States.csv")