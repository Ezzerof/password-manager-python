import base64
import random
import string
import datetime
from tkinter import *
from tkinter import messagebox

# Update existent credential

def check():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    encoded_pass = encode_password(password)

    with open("data.txt", "r+") as credentials_file:
        lines = credentials_file.readlines()

        for idx, line in enumerate(lines):
            text = line.strip().split(" | ")
            if len(text) >= 3:
                saved_website = text[0]
                saved_email = text[1]
                if saved_website == website and saved_email == email:
                    if messagebox.askyesno("Update", "Do you want to update an existing credential?"):
                        lines[idx] = f"{saved_website} | {saved_email} | {encoded_pass}\n"
                        credentials_file.truncate(0)
                        credentials_file.seek(0)
                        credentials_file.writelines(lines)
                        return
                    else:
                        return

        return True


# Encode and Decode password
def encode_password(password):
    encoded_password = base64.b64encode(password.encode('utf-8'))
    return encoded_password.decode('utf-8')

def decode_password(encoded_password):
    decoded_password = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_password.decode('utf-8')

def create_credentials_file():
    file = open("data.txt", "a")
    file.close()

# Save user to file

def save():
    website = website_input.get().capitalize()
    email = email_input.get().lower()
    temp_pass = password_input.get()
    password = encode_password(temp_pass)
    today_datetime = datetime.datetime.today()

    if not website or not email or not password:
        print("All fields must be filled!")
        messagebox.showerror("Error", "All fields must be filled!")
        return
    create_credentials_file()

    if check():

        with open("data.txt", "a+") as credentials_file:
            credentials_file.write(f"{website} | {email} | {password} | {today_datetime}\n")
            website_input.delete(0, END)
            password_input.delete(0, END)
            messagebox.showinfo("Confirmation", "Credentials were saved!")

# Generate a random password

def generate():
    text = password_input.get()
    if text:
        password_input.delete(0, END)

    nums = string.digits
    symbols = string.punctuation
    letters = string.ascii_letters

    password_numbers = ''.join(random.choices(nums, k=3))
    password_symbols = ''.join(random.choices(symbols, k=2))
    password_letters = ''.join(random.choices(letters, k=10))

    password = password_numbers + password_letters + password_symbols
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    password_input.insert(1, password)

def search():
    searched_website = website_input.get()

    if not searched_website:
        messagebox.showerror("Error", "The Website field cannot be empty!")
        return

    with open("data.txt", "r") as websites_file:
        lines = websites_file.readlines()

        for idx, line in enumerate(lines):
            text = line.strip().split(" | ")
            website = text[0]
            email = text[1]
            password = decode_password(text[2])

            if website == searched_website:
                messagebox.showinfo("Credentials", f"Email: {email}\nPassword: {password}")
                return

        messagebox.showerror("Error", f"The following: {searched_website} doesn't exist")
        return


# UI
window = Tk()

window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(window, text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(window, text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(window, text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_input = Entry(window, width=21)
website_input.focus()
website_input.grid(row=1, column=1, sticky="EW")
email_input = Entry(window, width=55)
email_input.insert(0, "email@gmail.com")
email_input.grid(row=2, column=1, columnspan=2)
password_input = Entry(window, width=21)
password_input.grid(row=3, column=1, sticky="EW")

# Buttons
generate_password_button = Button(window, text="Generate Password", width=14, command=generate)
generate_password_button.grid(row=3, column=2, sticky="EW")
add_button = Button(window, text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")
search_button = Button(window, text="Search", width=14, command=search)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()
