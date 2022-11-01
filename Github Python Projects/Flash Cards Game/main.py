BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas as pd
from random import sample, choice
import time

word_set = {}



try:
    data = pd.read_csv("data/words_left.csv")
except FileNotFoundError:
    main_data = pd.read_csv("./data/french_words.csv")
    words_list = main_data.to_dict(orient="records")
else:
    words_list = data.to_dict(orient="records")

def switch_to_front():
    canvas.itemconfig(card, image=card_front)


def switch_to_back():
    canvas.itemconfig(card, image=card_back)
    global word_set
    canvas.itemconfig(lang_label, text="English")
    canvas.itemconfig(word_lab, text=word_set["English"])

def correct():
    global word_set, timer, words_list
    window.after_cancel(timer)
    if len(words_list) != 0:
        words_list.remove(word_set)
        print(len(words_list))
        with open ("words_left.csv", "w"):
            words_left_df = pd.DataFrame(words_list)
            words_left_df.to_csv("data/words_left.csv")
        next_word()



def incorrect():
    global timer
    window.after_cancel(timer)
    next_word()

def next_word():
    global word_set, timer
    try:
        word_set = choice(words_list)
        switch_to_front()
        timer = window.after(3000, switch_to_back)
        canvas.itemconfig(lang_label, text="French")

    except:
        word_set = {"French": "No words left", "English": "No words left"}
    # else:
        # if len(words_list) == 0:
        #     canvas.itemconfig(lang_label, text="You have learned")
        #     canvas.itemconfig(word_lab, text="all words from\n this dictionary!")
        #     window.after_cancel(timer)
        # else:

    finally:
        canvas.itemconfig(word_lab, text=word_set["French"], fill="black")







# --------------------------UI--------------------------------------
window = Tk()
window.config(padx=50, pady=50, bg="#B1DDC6", highlightthickness=0)
canvas = Canvas(width=800, height=526, bg="#B1DDC6", highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas.grid(column=0, row=0, columnspan=2)
card = canvas.create_image(400, 263, image=card_front)

right = PhotoImage(file="./images/right.png")
wrong = PhotoImage(file="./images/wrong.png")
r_button = Button(image=right, highlightthickness=0, command=correct)
w_button = Button(image=wrong, highlightthickness=0, command=incorrect)
r_button.grid(column=0, row=1)
w_button.grid(column=1, row=1)

lang_label = canvas.create_text(400, 100, text="", font=("Arial", 40, "italic"))
word_lab = canvas.create_text(400, 270, text="", font=("Arial", 60, "bold"))

timer = window.after(1)





next_word()

window.mainloop()
