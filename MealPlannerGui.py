# Todo : create functions of buttons and maybe fix menu filling issue
import customtkinter as ctk
import Meal_planner as Mp


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

        def menuframe():
            def collapse_menu():
                """this function collapses the menu after click on the menu btn when menu is opened"""
                self.menubar_frame.destroy()
                self.menu_btn.configure(text='≡', command=menuframe)

            height = self.root.winfo_screenheight()
            self.menubar_frame = ctk.CTkFrame(master=self.root, height=height, width=200, fg_color='black',
                                              bg_color='black')
            self.menubar_frame.place(x=0, y=40)  # better to be placed
            self.menu_btn.configure(text='X', command=collapse_menu)

            btn1 = ctk.CTkButton(master=self.menubar_frame, text='Home page', bg_color='black',
                                 fg_color='black', command=lambda: self.switch_pages(self.home_page))
            btn1.pack(fill='x', pady=5)
            btn2 = ctk.CTkButton(master=self.menubar_frame, text='Food page', bg_color='black',
                                 fg_color='black', command=lambda: self.switch_pages(self.food_page))
            btn2.pack(fill='x', pady=5)

        self.menubtn_frame = ctk.CTkFrame(master=self.root, fg_color='black', bg_color='black')
        self.menubtn_frame.pack(side='top', fill='x')
        self.menubtn_frame.pack_propagate(False)  # used it to force the frame to have height 40
        self.menubtn_frame.configure(height=40)

        self.menu_btn = ctk.CTkButton(master=self.menubtn_frame, text="≡", font=('Arial', 20, 'bold'),
                                      fg_color='black', width=10, command=menuframe)
        self.menu_btn.pack(side='left')

        self.label1 = ctk.CTkLabel(master=self.menubtn_frame, text="Meal Planner application",
                                   font=('Arial', 15, 'bold'), padx=5)
        self.label1.pack(side='left')

        self.contactus_btn = ctk.CTkButton(master=self.menubtn_frame, text="contact us",
                                           font=('Arial', 15), fg_color='black', width=5)
        self.contactus_btn.pack(side='right')

    def home_page(self):
        days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
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
            label = ctk.CTkLabel(master=home_page, text=days[i - 1], font=('Arial', 15, 'bold', 'underline'),
                                 width=20,
                                 height=10)
            label.grid(row=i, column=0)
        for i in range(1, 4):
            label = ctk.CTkLabel(master=home_page, text=meals[i - 1], font=('Arial', 15, 'bold', 'underline'),
                                 width=20,
                                 height=10)
            label.grid(row=0, column=i)
        for i in range(1, 8):
            daily_meals = self.Mp1.show_each_day_meals(days[i - 1])
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
