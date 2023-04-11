from tkinter import *
from tkinter import messagebox
DEFAULT_USERNAME = "francesco.tintori93@gmail.com"
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
def gen_pw():
    pw_field.delete(0, END)
    length = int(askstring('Length', 'Enter password lenght\nMinimum length is 6'))
    if length < 6:
        messagebox.showwarning(title="Empty field", message="Minimum length is 6 characters")
        return
    nr_letters = random.randint(2, length-4)
    nr_numbers = random.randint(2, length - nr_letters - 2)
    nr_symbols = length - nr_letters - nr_numbers
    password_list = []
    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    random.shuffle(password_list)
    pw_field.insert(0, "".join(password_list))
    pyperclip.copy("".join(password_list))
    messagebox.showinfo(title="Password copied", message="Password copied to clipboard")
    password_list.clear()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_pw():
    website = website_field.get().lower()
    username = user_field.get()
    password = pw_field.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password)==0 or len(username) ==0:
        messagebox.showwarning(title="Empty field", message="Please fill in all required entries")
        return

    is_ok = messagebox.askokcancel(title=website,
                                   message=f"You entered\n    Username: {username} \n    Password: {password}\n    for {website}\nClick OK to confirm")
    if is_ok:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except:
            data = new_data
        finally:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

            website_field.delete(0, END)
            pw_field.delete(0, END)
            user_field.delete(0, END)
            user_field.insert(0, DEFAULT_USERNAME)
    # if is_ok:
    #     with open("data.txt", "a") as data_file:
    #         data_file.write(f"{website} | {username} | {password}\n")
    #         website_field.delete(0, END)
    #         pw_field.delete(0, END)
    #         user_field.delete(0, END)
    #         user_field.insert(0, DEFAULT_USERNAME)
# -----------------------------Password Search-------------------------#
def search():
    search = website_field.get().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
            messagebox.showinfo(title="No data", message="No data in database")
    else:
        if search in data:
            print(data[search]["username"], data[search]["password"])
            messagebox.showinfo(message=f"For the website:  {search}\n\n"
                                        f"Username:         {data[search]['username']}\n"
                                        f"Password:         {data[search]['password']}", title=search)
        if search not in data:
            messagebox.showinfo(title="No match", message="No matching website was found.")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=20, pady=20, bg="#fff", highlightthickness=0)
canvas = Canvas(width=200, height=200, bg="#fff", highlightthickness=0)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

website_lab = Label(text="Website:   ", font=("Arial", 12), bg="#fff")
website_lab.grid(column=0, row=1)
user_lab = Label(text="Email/username: ", font=("Arial", 12), bg="#fff")
user_lab.grid(column=0, row=2)
pw_lab = Label(text="Password:   ", font=("Arial", 12), bg="#fff")
pw_lab.grid(column=0, row=3)

website_field = Entry(width=34)
website_field.grid(column=1, row=1, sticky=W, columnspan=1)
website_field.focus()
user_field = Entry(width=52)
user_field.grid(column=1, row=2, sticky=W, columnspan=2)
user_field.insert(0, DEFAULT_USERNAME)
pw_field = Entry(width=34)
pw_field.grid(column=1, row=3, sticky=W)

gen_pw_button = Button(text="Generate password", command=gen_pw, width=14)
gen_pw_button.grid(column=2, row=3, sticky=W)
add_pw_button = Button(text="Add", command=add_pw, width=44)
add_pw_button.grid(column=1, row=4, sticky=W, columnspan=2)
search_button = Button(text="Search", command=search, width=14)
search_button.grid(column=2, row=1, sticky=W)

window.mainloop()
