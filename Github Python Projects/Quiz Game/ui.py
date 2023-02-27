THEME_COLOR = "#375362"
from tkinter import *

from quiz_brain import QuizBrain

class QuizInterface:


    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg="#375362", highlightthickness=0)
        self.canvas = Canvas(width=300, height=250,bg="#fff", highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20, padx=20)
        self.true = PhotoImage(file="./images/true.png")
        self.false = PhotoImage(file="./images/false.png")
        self.r_button = Button(image=self.true, highlightthickness=0, command=self.true_pressed)
        self.w_button = Button(image=self.false, highlightthickness=0, command=self.false_pressed)
        self.r_button.grid(column=0, row=2, pady=20, padx=20)
        self.w_button.grid(column=1, row=2, pady=20, padx=20)
        self.question_text = self.canvas.create_text(150, 125, text="", font=("Arial", 20), width=290, fill="#375362")
        self.score_lab = Label(text="Score: 0", font=("Arial", 20, "bold"),
                               bg="#375362", highlightthickness=0, anchor="center", fg="#fff")
        self.score_lab.grid(row=0, column=1, pady=10)

        self.get_next_q()

        self.window.mainloop()

    def get_next_q(self):
        self.butt_act()
        self.canvas.configure(bg="#fff")
        if self.quiz.still_has_questions():
                q_text = self.quiz.next_question()
                self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.butt_deact()
            self.canvas.itemconfig(self.question_text, text="There are no more questions, close or restart the game")

    def true_pressed(self):
        self.feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.feedback(self.quiz.check_answer("False"))

    def feedback(self, is_correct):
        if is_correct:
            self.canvas.configure(bg="Green")

        elif not is_correct:
            self.canvas.configure(bg="Red")
        self.score_lab.configure(text=f"Score: {self.quiz.score}")
        self.butt_deact()
        self.window.after(1000, self.get_next_q)

    def butt_act(self):
        self.r_button.config(state="active")
        self.w_button.config(state="active")

    def butt_deact(self):
        self.r_button.config(state="disabled")
        self.w_button.config(state="disabled")