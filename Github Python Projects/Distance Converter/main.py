from tkinter import *

window = Tk()
window.title("Distance Converter")
window.minsize(width=300, height=100)


def convert():
    global km
    miles = float(miles_field.get())
    km = round(1.609*miles, 2)
    solution.config(text=f"Distance in km is:   {km}")

km = ""
label = Label(text="Enter distance in mi:  ", font=("Arial", 15))
label.grid(column=0, row=0)

button = Button(text="Convert", command=convert)
button.grid(column=1, row=1)

miles_field = Entry(width=10)
miles_field.grid(column=1, row=0)

solution = Label(text=f"Distance in km is:   {km}", font=("Arial", 15))
solution.grid(column=0, row=4)

window.mainloop()
