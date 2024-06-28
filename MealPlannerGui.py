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
        # self.root.resizable(False, False)
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

        quick_food_btn = ctk.CTkButton(master=menu_buttons_frame, text="Quick Meal",
                                       command=lambda: self.switch_pages(self.show_quickmeal),
                                       font=('Arial', 20, 'bold'), fg_color='black', width=5)
        quick_food_btn.pack(side='right')

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

    def show_quickmeal(self):
        def use_quickmeal(food):
            food_id = self.Mp1.food_key(food)
            self.Mp1.decrease_nutrients(food_id)
            self.switch_pages(self.home_page)

        quickmeal_page = ctk.CTkFrame(master=self.main_frame, bg_color='black')
        quickmeal_page.pack(fill='both', expand=True)

        quick_meal = self.Mp1.available_meal()
        if not quick_meal:
            ctk.CTkLabel(master=quickmeal_page,
                         text='there is no available food with nutrients you have', font=('Times', 30, 'bold')).pack(side='top')
            back_home_button = ctk.CTkButton(master=quickmeal_page, text='Back to home',
                                             command=lambda: self.switch_pages(self.home_page))
            back_home_button.pack(side='top')
            return 0
        quickmeal_frame = ctk.CTkFrame(master=quickmeal_page, bg_color='#5A5F63', fg_color='#63520B')
        quickmeal_frame.pack(fill='y', expand=True)
        quickmeal_frame.columnconfigure(0, weight=1)
        rows = 4
        for i in quick_meal[1]:
            rows += 1
        for i in range(rows):
            quickmeal_frame.rowconfigure(i, weight=0)
        quickmeal_name = ctk.CTkLabel(master=quickmeal_frame, text=quick_meal[0], pady=15,
                                      font=('Times', 25, 'bold', 'underline'))
        quickmeal_name.grid(row=0, column=0)

        food_ingredients = ctk.CTkLabel(master=quickmeal_frame, text='food ingredients', pady=15,
                                        font=('Times', 25, 'bold'))
        food_ingredients.grid(row=1, column=0)
        rows = 2
        for i in quick_meal[1]:
            ctk.CTkLabel(master=quickmeal_frame, text=f"{i}: {quick_meal[1][i]}", font=('Helvetica', 20)).grid(row=rows,
                                                                                                               column=0)
            rows += 1
        recipie = quick_meal[2]
        food_recipe = ctk.CTkLabel(master=quickmeal_frame, text='food recipe', pady=15, font=('Times', 25, 'bold'))
        food_recipe.grid(row=rows, column=0)
        recipie_label = ctk.CTkLabel(master=quickmeal_frame, text=recipie, pady=10, font=('Arial', 15))
        recipie_label.grid(rows=rows + 1, column=0)

        # add two more rows for use and back home btn
        quickmeal_frame.rowconfigure(rows + 11, weight=0)
        quickmeal_frame.rowconfigure(rows + 10, weight=0)  # don't know why but it worked

        use_button = ctk.CTkButton(master=quickmeal_frame, text='Used this recipie', fg_color='green',
                                   command=lambda: use_quickmeal(quick_meal[0]))
        back_home_button = ctk.CTkButton(master=quickmeal_frame, text='Back to home', fg_color='black',
                                         command=lambda: self.switch_pages(self.home_page))
        use_button.grid(row=rows + 10, column=0)
        back_home_button.grid(row=rows + 11, column=0)

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
