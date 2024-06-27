# Todo : create functions of buttons and maybe fix menu filling issue
import customtkinter as ctk
import Meal_planner as Mp
import datetime as dt


class FirstWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.Mp1 = Mp.MealPlanner()
        self.root.title("Meal Planner")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.menu_bar()
        self.main_frame = ctk.CTkFrame(self.root, bg_color='white', fg_color='white')
        self.main_frame.pack(fill='both', expand=True)
        self.home_page()
        self.root.mainloop()

    def menu_bar(self):
        menu_buttons = {"Home Page": self.home_page, "Food_Page": self.food_page}

        def menu_frame():
            def collapse_menu():
                """this function collapses the menu after click on the menu btn when menu is opened"""
                menubar_frame.destroy()
                menu_btn.configure(text='≡', command=menu_frame)

            height = self.root.winfo_screenheight()
            menubar_frame = ctk.CTkFrame(master=self.root, height=height, width=200, fg_color='black', bg_color='black')
            menubar_frame.place(x=0, y=40)  # better to be placed
            menu_btn.configure(text='X', command=collapse_menu)

            btn1 = ctk.CTkButton(master=menubar_frame, text='Home page', bg_color='black',
                                 fg_color='black', command=lambda: self.switch_pages(self.home_page))
            btn1.pack(fill='x', pady=5)
            btn2 = ctk.CTkButton(master=menubar_frame, text='Food page', bg_color='black',
                                 fg_color='black', command=lambda: self.switch_pages(self.food_page))
            btn2.pack(fill='x', pady=5)

        menu_buttons_frame = ctk.CTkFrame(master=self.root, fg_color='black', bg_color='black')
        menu_buttons_frame.pack(side='top', fill='x')
        menu_buttons_frame.pack_propagate(False)  # used it to force the frame to have height 40
        menu_buttons_frame.configure(height=40)

        menu_btn = ctk.CTkButton(master=menu_buttons_frame, text="≡", font=('Arial', 20, 'bold'),
                                 fg_color='black', width=10, command=menu_frame)
        menu_btn.pack(side='left')

        label1 = ctk.CTkLabel(master=menu_buttons_frame, text="Meal Planner application",
                              font=('Arial', 15, 'bold'), padx=5)
        label1.pack(side='left')

        contactus_btn = ctk.CTkButton(master=menu_buttons_frame, text="contact us",
                                      font=('Arial', 15), fg_color='black', width=5)
        contactus_btn.pack(side='right')

    def home_page(self):
        """at the homepage a frame is displayed inside main frame which includes planned meals for next seven days
        by using datetime we send date of next seven days to database and get each date's meals"""

        now = dt.datetime.now()
        meals = ['Breakfast', 'Lunch', 'Dinner']
        home_page = ctk.CTkFrame(master=self.main_frame, bg_color='black')
        home_page.pack(fill='both', expand=True)
        for i in range(8):
            home_page.rowconfigure(i, weight=1)
        for i in range(4):
            home_page.columnconfigure(i, weight=1)
        empty_label = ctk.CTkLabel(master=home_page, text='', width=20, height=10)
        empty_label.grid(row=0, column=0)
        for i in range(1, 8):
            label = ctk.CTkLabel(master=home_page,
                                 text=f'{(now + dt.timedelta(days=i)).strftime('%A')}\n{(now + dt.timedelta(days=i)).strftime('%m-%d')}',
                                 font=('Arial', 15, 'bold', 'underline'),
                                 width=20, height=10)
            label.grid(row=i, column=0)
        for i in range(1, 4):
            label = ctk.CTkLabel(master=home_page, text=meals[i - 1], font=('Arial', 15, 'bold', 'underline'),
                                 width=20,
                                 height=10)
            label.grid(row=0, column=i)
        for i in range(1, 8):
            daily_meals = self.Mp1.show_each_day_meals(now + dt.timedelta(days=i))
            for j in range(1, 4):
                label = ctk.CTkLabel(master=home_page, text=daily_meals[j - 1], font=('Arial', 15),
                                     width=20, height=10)
                label.grid(row=i, column=j)

    def food_page(self):
        food_page = ctk.CTkFrame(master=self.main_frame)
        foodpage_label = ctk.CTkLabel(master=food_page, text="Food Page", font=('Arial', 20), pady=50)
        food_page.pack(fill='both', expand=True)
        foodpage_label.pack(fill='both', expand=True)

    def switch_pages(self, page):
        for frame in self.main_frame.winfo_children():
            frame.destroy()
            self.root.update()
        page()


if __name__ == "__main__":
    first = FirstWindow()
