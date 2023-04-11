from tkinter import *
import time
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#367E18"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
timer = None
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps
    global tiks
    global timer
    window.after_cancel(timer)
    reps = 1
    tiks = ""
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    tickmark_label.config(text=tiks)


# ---------------------------- TIMER MECHANISM ------------------------------- # 
tiks = ""
def start_timer():
    global reps
    work_time = WORK_MIN*60
    sh_br_time = SHORT_BREAK_MIN*60
    long_br_time = LONG_BREAK_MIN*60
    if reps%2==0 and reps != 8:
        time_set = sh_br_time
    elif reps%2==1:
        time_set = work_time
    elif reps==8:
        time_set = long_br_time

    count_down(time_set)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def count_down(count):
    secs = count % 60
    global reps
    global tiks
    if secs < 10:
        secs = f"0{secs}"
    mins = math.floor(count / 60)
    if mins < 10:
        mins = f"0{mins}"
    canvas.itemconfig(timer_text, text=f"{mins}:{secs}")
    if reps % 2 != 0:
        timer_label.config(text="WORK!")
    if reps % 2 == 0:
        timer_label.config(text="Chill!")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    if count == 0 and reps < 8:
        if reps%2!=0:
            tiks +=  "✓"
            tickmark_label.config(text=tiks)
        reps += 1
        start_timer()
    if count == 0 and reps == 8:
            timer_label.config(text="Restart?!")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Pomodoro')
window.config(padx=50, pady=50, bg=YELLOW)




canvas = Canvas(width=230, height=240, bg=YELLOW, highlightthickness=0)
image = PhotoImage(file="tomato.png")
canvas.create_image(110, 115, image=image)
timer_text= canvas.create_text(110, 135, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1,row=1)

timer_label = Label(text="Timer", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=GREEN, highlightthickness=0)
timer_label.grid(column=1,row=0)
tickmark_label = Label(text=tiks, font=(FONT_NAME, 25, "bold"), fg=GREEN, bg=YELLOW, highlightthickness=0 )
tickmark_label.grid(column=1, row=2)
stat_butt = Button(text="Start", width=10, command=start_timer)
stat_butt.grid(column=0, row=2)
res_butt = Button(text="Reset", width=10, command=reset_timer)
res_butt.grid(column=2, row=2)






window.mainloop()