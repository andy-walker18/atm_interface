import tkinter as tk
from tkinter import messagebox
import time
import sqlite3
from tkinter import END

current_balance = 1000


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Balance': tk.IntVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Registration, LoginPage, MenuPage, WithdrawPage, DepositPage, BalancePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Registration")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class Registration(tk.Frame):
    """ Register for account. Email and password saved in SQLite database."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#081729")
        self.controller = controller

        self.controller.geometry("1200x900")
        self.controller.resizable(False, False)
        self.controller.title('Millennium Trust')
        self.controller.iconphoto(False, tk.PhotoImage(file="C:\PythonMasterClass\CurrentProjects\Portfolio Projects\letter-m.png"))

        heading_label = tk.Label(self,
                                 text='Millennium ATM',
                                 font=('Britannic Bold', 65, 'bold'),
                                 foreground='white',
                                 background='#081729')
        heading_label.pack(pady=50)

        space_label = tk.Label(self, height=4, bg='#081729')
        space_label.pack()

        email_label = tk.Label(self,
                               text="Enter your email:",
                               font=("orbitron", 20),
                               foreground='white',
                               bg="#081729")
        email_label.pack()

        my_email = tk.StringVar()
        email_entry_box = tk.Entry(self,
                                   textvariable=my_email,
                                   font=('orbitron', 12),
                                   width=40,
                                   borderwidth=1)
        email_entry_box.focus_set()
        email_entry_box.pack(ipady=7, pady=10)

        password_label = tk.Label(self,
                                  text="Enter your password:",
                                  font=("orbitron", 20),
                                  foreground='white',
                                  bg="#081729")
        password_label.pack()

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self,
                                      textvariable=my_password,
                                      font=('orbitron', 12),
                                      width=40,
                                      borderwidth=1,
                                      show="*")
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7, pady=5)

        def database():
            input1 = my_email.get()
            input2 = my_password.get()

            conn = sqlite3.connect('Userinfo.db')
            with conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS Account (email TEXT, password TEXT)')
                cursor.execute('INSERT INTO Account(email, password) VALUES(?,?)', (input1, input2,))
                conn.commit()

            if len(my_email.get()) == 0 or len(my_password.get()) == 0:
                tk.messagebox.showerror('Error', 'Missing email or password')
            else:
                controller.show_frame('LoginPage')

        register_button = tk.Button(self,
                                    text='Register',
                                    relief='raised',
                                    command=database,
                                    borderwidth=3,
                                    width=50,
                                    height=3)
        register_button.pack(pady=10)

        def load_next():
            controller.show_frame('LoginPage')

        existing_user = tk.Button(self,
                                  text='Existing Member',
                                  relief='raised',
                                  command=load_next,
                                  borderwidth=3,
                                  width=50,
                                  height=3)
        existing_user.pack()

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa = tk.PhotoImage(file='C://PythonMasterClass//CurrentProjects//Portfolio Projects//visa.icon.png')
        visa_label = tk.Label(bottom_frame, image=visa)
        visa_label.pack(side='left')
        visa_label.image = visa

        american_express = tk.PhotoImage(file="C://PythonMasterClass//CurrentProjects//Portfolio Projects//amex.png")
        american_express_label = tk.Label(bottom_frame, image=american_express)
        american_express_label.pack(side='left')
        american_express_label.image = american_express

        def clock_ticker():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, clock_ticker)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        clock_ticker()


class LoginPage(tk.Frame):
    """Fetches account information to confirm log in user. If incorrect email
        or password error message box will show. If correct will load into
        main menu."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#081729")
        self.controller = controller

        self.controller.title('Millennium Trust')
        self.controller.resizable(False, False)

        heading_label = tk.Label(self,
                                 text='Millennium ATM',
                                 font=('Britannic Bold', 65, 'bold'),
                                 foreground='white',
                                 background='#081729')
        heading_label.pack(pady=50)

        space_label = tk.Label(self, height=4, bg='#081729')
        space_label.pack()

        email_label = tk.Label(self,
                               text='Email:',
                               font=('orbitron', 20),
                               bg='#081729',
                               fg='white')
        email_label.pack()

        my_email = tk.StringVar()
        email_entry_box = tk.Entry(self,
                                   textvariable=my_email,
                                   font=('orbitron', 12),
                                   width=40,
                                   borderwidth=1)
        email_entry_box.focus_set()
        email_entry_box.pack(ipady=7, pady=5)

        password_label = tk.Label(self,
                                  text='Password:',
                                  font=('orbitron', 20),
                                  bg='#081729',
                                  fg='white')
        password_label.pack()

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self,
                                      textvariable=my_password,
                                      font=('orbitron', 12),
                                      width=40,
                                      borderwidth=1)
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black', show='*')

        password_entry_box.bind('<FocusIn>', handle_focus_in)

        def check_password():
            conn = sqlite3.connect('Userinfo.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Account WHERE email=? AND password=?', (my_email.get(), my_password.get()))
            row = cursor.fetchone()

            if len(my_email.get()) == 0 or len(my_password.get()) == 0:
                tk.messagebox.showerror('Error', 'Missing email or password')
            if row == None:
                tk.messagebox.showinfo('Info', 'Wrong password or email')

            for i in row:
                if my_email.get() and my_password.get() in row:
                    email_entry_box.delete(0, END)
                    password_entry_box.delete(0, END)
                    controller.show_frame('MenuPage')

        enter_button = tk.Button(self,
                                 text='Log in',
                                 command=check_password,
                                 relief='raised',
                                 borderwidth=3,
                                 width=50,
                                 height=3)
        enter_button.pack(pady=12)

        incorrect_password_label = tk.Label(self,
                                            text='',
                                            font=('orbitron', 13),
                                            fg='white',
                                            bg='#030a12',
                                            anchor='n')
        incorrect_password_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa = tk.PhotoImage(file='C://PythonMasterClass//CurrentProjects//Portfolio Projects//visa.icon.png')
        visa_label = tk.Label(bottom_frame, image=visa)
        visa_label.pack(side='left')
        visa_label.image = visa

        american_express = tk.PhotoImage(file="C://PythonMasterClass//CurrentProjects//Portfolio Projects//amex.png")
        american_express_label = tk.Label(bottom_frame, image=american_express)
        american_express_label.pack(side='left')
        american_express_label.image = american_express

        def clock_ticker():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, clock_ticker)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        clock_ticker()


class MenuPage(tk.Frame):
    """Provides buttons of menu uptions to withdraw, deposit,
        check balance, and log out."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#081729")
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='Millennium ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background="#081729")
        heading_label.pack(pady=25)

        self.controller.title('Millennium ATM')

        main_menu_label = tk.Label(self,
                                   text='Main Menu',
                                   font=('orbitron', 20),
                                   fg='white',
                                   bg="#081729")
        main_menu_label.pack()

        selection_label = tk.Label(self,
                                   text='Please make a selection',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg="#081729",
                                   anchor='w')
        selection_label.pack(fill='x')

        button_frame = tk.Frame(self, bg="#030a12")
        button_frame.pack(fill='both', expand=True)

        def withdraw():
            controller.show_frame("WithdrawPage")

        withdraw_button = tk.Button(button_frame,
                                    text="Withdraw",
                                    command=withdraw,
                                    relief="raised",
                                    borderwidth=3,
                                    width=50,
                                    height=5)
        withdraw_button.grid(row=0, column=0, pady=5)

        def deposit():
            controller.show_frame("DepositPage")

        deposit_button = tk.Button(button_frame,
                                   text="Deposit",
                                   command=deposit,
                                   relief="raised",
                                   borderwidth=3,
                                   width=50,
                                   height=5)
        deposit_button.grid(row=1, column=0, pady=5)

        def check_balance():
            controller.show_frame("BalancePage")

        check_balance_button = tk.Button(button_frame,
                                         text="View Balance",
                                         command=check_balance,
                                         relief="raised",
                                         borderwidth=3,
                                         width=50,
                                         height=5)
        check_balance_button.grid(row=2, column=0, pady=5)

        def exit1():
            controller.show_frame("LoginPage")

        exit_button = tk.Button(button_frame,
                                text="Exit",
                                command=exit1,
                                relief="raised",
                                borderwidth=3,
                                width=50,
                                height=5)
        exit_button.grid(row=3, column=0, pady=5)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='C://PythonMasterClass//CurrentProjects//Portfolio Projects//visa.icon.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        american_express_photo = tk.PhotoImage(file="C://PythonMasterClass/"
                                                    "/CurrentProjects//Portfolio Projects//amex.png")
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def clock_ticker():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, clock_ticker)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        clock_ticker()


class WithdrawPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#081729")
        self.controller = controller

        self.controller.title("Millennium Trust")

        heading_label = tk.Label(self,
                                 text='Millennium ATM',
                                 font=('Britannic Bold', 65, 'bold'),
                                 foreground='white',
                                 background='#081729')
        heading_label.pack(pady=50)

        space_label = tk.Label(self, height=4, bg='#081729')
        space_label.pack()

        withdraw_label = tk.Label(self,
                                  text='Choose the amount to withdraw',
                                  font=('orbitron', 20),
                                  bg='#081729',
                                  fg='white')
        withdraw_label.pack(pady=10)

        button_frame = tk.Frame(self,bg="#030a12")
        button_frame.pack(fill='both', expand=True)

        def withdraw1(amount):
            global current_balance

            if current_balance < amount:
                tk.messagebox.showerror('Error', 'Account balance insufficient')
            else:
                current_balance -= amount
                controller.shared_data['Balance'].set(current_balance)
                withdraw_amount.set('')
                controller.show_frame('MenuPage')

        b1 = tk.Button(button_frame,
                       text="$20",
                       relief="raised",
                       width=50,
                       height=5,
                       borderwidth=3,
                       command=lambda: withdraw1(20))
        b1.grid(row=0, column=0, pady=5, padx=10)

        b2 = tk.Button(button_frame,
                       text="$40",
                       relief="raised",
                       width=50,
                       height=5,
                       borderwidth=3,
                       command=lambda: withdraw1(40))
        b2.grid(row=1, column=0)

        b3 = tk.Button(button_frame,
                       text="$80",
                       relief="raised",
                       width=50,
                       height=5,
                       borderwidth=3,
                       command=lambda: withdraw1(80))
        b3.grid(row=2, column=0, pady=5)

        b4 = tk.Button(button_frame,
                       text="$100",
                       relief="raised",
                       width=50,
                       height=5,
                       borderwidth=3,
                       command=lambda: withdraw1(100))
        b4.grid(row=0, column=1, pady=5, padx=450)

        b5 = tk.Button(button_frame,
                       text="$200",
                       relief="raised",
                       width=50,
                       height=5,
                       borderwidth=3,
                       command=lambda: withdraw1(200))
        b5.grid(row=1, column=1, pady=5)

        withdraw_amount = tk.StringVar()
        withdraw_entry = tk.Entry(button_frame,
                                  textvariable=withdraw_amount,
                                  font=('Britannica Bold', 12),
                                  width=40,
                                  borderwidth=1,
                                  justify="center")
        withdraw_entry.focus_set()
        withdraw_entry.grid(row=2, column=1, pady=5, ipady=30)

        custom_label = tk.Label(button_frame,
                                text="Other Amount",
                                font=("Britannica Bold", 15),
                                bg="#030a12",
                                fg='white')
        custom_label.grid(row=4, column=1)

        def exit1():
            controller.show_frame("MenuPage")

        b6 = tk.Button(button_frame,
                       text="Exit",
                       command=exit1,
                       relief="raised",
                       borderwidth=3,
                       width=50,
                       height=5)
        b6.place(x=975, y=600, anchor="s")

        def custom_amount(x):
            global current_balance

            if current_balance < int(withdraw_amount.get()):
                tk.messagebox.showerror('Error', 'Account balance insufficient')
            else:
                current_balance -= int(withdraw_amount.get())
                controller.shared_data['Balance'].set(current_balance)
                withdraw_amount.set('')
                controller.show_frame('MenuPage')

        withdraw_entry.bind('<Return>', custom_amount)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='C://PythonMasterClass//CurrentProjects//Portfolio Projects//visa.icon.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        american_express_photo = tk.PhotoImage(file="C://PythonMasterClass//"
                                                    "CurrentProjects//Portfolio Projects//amex.png")
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def clock_ticker():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, clock_ticker)

        time_label = tk.Label(bottom_frame, font=('Britannica Bold', 12))
        time_label.pack(side='right')

        clock_ticker()


class DepositPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#081729")
        self.controller = controller

        self.controller.title("Millennium Trust")

        heading_label = tk.Label(self,
                                 text='Millennium ATM',
                                 font=('Britannica Bold', 65, 'bold'),
                                 foreground='white',
                                 background='#081729')
        heading_label.pack(pady=50)

        space_label = tk.Label(self, height=4, bg='#081729')
        space_label.pack()

        deposit_label = tk.Label(self,
                                 text='Enter Deposit Amount',
                                 font=('Britannica Bold', 20),
                                 bg='#081729',
                                 fg='white')
        deposit_label.pack()

        deposit_amount = tk.StringVar()
        deposit_entry = tk.Entry(self,
                                 textvariable=deposit_amount,
                                 font=('Britannica Bold', 12),
                                 width=40,
                                 borderwidth=1)
        deposit_entry.focus_set()
        deposit_entry.pack(pady=5, ipady=7)

        def custom_amount():
            global current_balance
            current_balance += int(deposit_amount.get())
            controller.shared_data['Balance'].set(current_balance)
            deposit_amount.set('')
            controller.show_frame('MenuPage')

        enter_button = tk.Button(self,
                                 text='Confirm Deposit',
                                 relief='raised',
                                 borderwidth=3,
                                 width=50,
                                 height=3,
                                 command=custom_amount)
        enter_button.pack(pady=5)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='C://PythonMasterClass//CurrentProjects//Portfolio Projects//visa.icon.png')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        american_express = tk.PhotoImage(file="C://PythonMasterClass//CurrentProjects//Portfolio Projects//amex.png")
        american_express_label = tk.Label(bottom_frame, image=american_express)
        american_express_label.pack(side='left')
        american_express_label.image = american_express

        def clock_ticker():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, clock_ticker)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        clock_ticker()


class BalancePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#081729")
        self.controller = controller

        self.controller.title("Millennium Trust")

        heading_label = tk.Label(self,
                                 text='Millennium ATM',
                                 font=('Britannic Bold', 65, 'bold'),
                                 foreground='white',
                                 background='#081729')
        heading_label.pack(pady=50)

        global current_balance
        controller.shared_data["Balance"].set(current_balance)
        balance_label = tk.Label(self,
                                 textvariable=controller.shared_data["Balance"],
                                 font=("Britannica Bold", 15),
                                 fg="white",
                                 bg="#081729",
                                 anchor="w")

        balance_label.pack(fill="x")

        button_frame = tk.Frame(self, bg="#030a12")
        button_frame.pack(fill="both", expand=True)

        def menu():
            controller.show_frame("MenuPage")

        main_menu = tk.Button(button_frame,
                              text="Main Menu",
                              relief="raised",
                              borderwidth=3,
                              width=50,
                              height=5,
                              command=menu)

        main_menu.pack(pady=5, anchor="w")

        def exit2():
            controller.show_frame("Registration")

        main_menu = tk.Button(button_frame,
                              text="Exit",
                              relief="raised",
                              borderwidth=3,
                              width=50,
                              height=5,
                              command=exit2)

        main_menu.pack(anchor="w")

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa = tk.PhotoImage(file='C://PythonMasterClass//CurrentProjects//Portfolio Projects//visa.icon.png')
        visa_label = tk.Label(bottom_frame, image=visa)
        visa_label.pack(side='left')
        visa_label.image = visa

        american_express = tk.PhotoImage(file="C://PythonMasterClass//CurrentProjects//Portfolio Projects//amex.png")
        american_express_label = tk.Label(bottom_frame, image=american_express)
        american_express_label.pack(side='left')
        american_express_label.image = american_express

        def clock_ticker():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, clock_ticker)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        clock_ticker()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()