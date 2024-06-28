# Todo : create functions of buttons and maybe fix menu filling issue
import customtkinter as ctk
import Meal_planner as Mp
import datetime as dt


class FirstWindow:
    def __init__(self):
        self.root = ctk.CTk()
        # this date used in set_meals function and in nxt func inside of it
        self.date = dt.datetime.now() + dt.timedelta(days=1)
        # this variable is useful in showing foods
        self.current_food = ''
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
        def menu_frame():
            def collapse_menu():
                """this function collapses the menu after click on the menu btn when menu is opened"""
                menubar_frame.destroy()
                menu_btn.configure(text='≡', command=menu_frame)

            height = self.root.winfo_screenheight()
            menubar_frame = ctk.CTkFrame(master=self.root, height=height, width=200, fg_color='black', bg_color='black')
            menubar_frame.place(x=0, y=40)  # better to be placed
            menu_btn.configure(text='X', command=collapse_menu)

            homePagebtn = ctk.CTkButton(master=menubar_frame, text='Home page', bg_color='black',
                                        fg_color='black', command=lambda: self.switch_pages(self.home_page))
            homePagebtn.pack(fill='x', pady=5)
            setMealsbtn = ctk.CTkButton(master=menubar_frame, text='Set meals', bg_color='black',
                                        fg_color='black', command=lambda: self.switch_pages(self.set_meals))
            setMealsbtn.pack(fill='x', pady=5)
            foods_btn = ctk.CTkButton(master=menubar_frame, text='Foods', bg_color='black',
                                      fg_color='black', command=lambda: self.switch_pages(self.foods_page))
            foods_btn.pack(fill='x', pady=5)

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
                         text='there is no available food with nutrients you have', font=('Times', 30, 'bold')).pack(
                side='top')
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

    def set_meals(self):
        def submit(date, combo1, combo2, combo3):
            if combo1.get():
                self.Mp1.insertWeeklyMeals(date, 'B', combo1.get())
            if combo2.get():
                self.Mp1.insertWeeklyMeals(date, 'L', combo2.get())
            if combo3.get():
                self.Mp1.insertWeeklyMeals(date, 'D', combo3.get())

        def nxt():
            self.date = self.date + dt.timedelta(days=1)
            self.switch_pages(self.set_meals)

        date = self.date
        date_str = date.strftime('%A \n%Y-%m-%d')
        lunch_dinners = self.Mp1.show_lunch_and_dinner()
        breakfasts = self.Mp1.show_breakfasts()
        meals = ['Breakfast', 'Lunch', 'Dinner']

        set_meals_frame = ctk.CTkFrame(master=self.main_frame, fg_color='#1A1A24', bg_color='#1A1A24')
        set_meals_frame.pack(fill='both', expand=True)
        date_frame = ctk.CTkFrame(master=set_meals_frame, width=400, height=100, fg_color='#1A1A24')
        date_label = ctk.CTkLabel(master=date_frame, text=date_str, font=('Arial', 25, 'bold'), width=400, height=100,
                                  fg_color='#1A1A24')
        date_label.pack(side='top', fill='both')
        date_frame.pack(side='top', pady=20)

        meal_selection_frame = ctk.CTkFrame(master=set_meals_frame)
        meal_selection_frame.pack(fill='both')
        for i in range(3):
            meal_selection_frame.rowconfigure(i, weight=1)
        for i in range(2):
            meal_selection_frame.columnconfigure(i, weight=1)

        for i in range(len(meals)):
            ctk.CTkLabel(master=meal_selection_frame, text=meals[i], pady=15,
                         font=('Times New Roman', 20, 'bold')).grid(row=i, column=0)

        breakfast_btn = ctk.CTkComboBox(master=meal_selection_frame, values=[''] + breakfasts, width=100)
        breakfast_btn.grid(row=0, column=1)
        lunch_btn = ctk.CTkComboBox(master=meal_selection_frame, values=[''] + lunch_dinners, width=100)
        lunch_btn.grid(row=1, column=1)
        dinner_btn = ctk.CTkComboBox(master=meal_selection_frame, values=[''] + lunch_dinners, width=100)
        dinner_btn.grid(row=2, column=1)

        buttons_frame = ctk.CTkFrame(master=set_meals_frame, height=200, bg_color='#1A1A24', fg_color='#1A1A24')
        buttons_frame.pack(side='bottom', fill='x', pady=10)
        submit_btn = ctk.CTkButton(master=buttons_frame, text='Submit', fg_color='green',
                                   command=lambda: submit(date, breakfast_btn, lunch_btn, dinner_btn))
        submit_btn.pack(side='left')
        next_day_btn = ctk.CTkButton(master=buttons_frame, text='Next', command=nxt)
        next_day_btn.pack(side='left')

    def foods_page(self):
        def show_food(food_name):
            self.current_food = food_name
            self.switch_pages(self.foods_details)

        all_foods = self.Mp1.show_breakfasts() + self.Mp1.show_lunch_and_dinner()
        foods_page_main = ctk.CTkFrame(master=self.main_frame, fg_color='#1A1A24', bg_color='#1A1A24')
        foods_page_main.pack(fill='both', expand=True)

        foods_title_frame = ctk.CTkFrame(master=foods_page_main, height=100, fg_color='#1A1A24', bg_color='#1A1A24')
        foods_title_frame.pack(side='top', fill='x', pady=5)
        food_page_title = ctk.CTkLabel(master=foods_title_frame, text='Your Foods & Recipies',
                                       font=('Times', 25, 'bold'), fg_color='#1A1A24', bg_color='#1A1A24')
        food_page_title.pack(side='top', fill='both')

        foods_names_frame = ctk.CTkScrollableFrame(master=foods_page_main, fg_color='white', bg_color='#1A1A24', height=10)
        foods_names_frame.pack(side='top', fill='x', pady=20)
        foods_names_frame.columnconfigure(0, weight=1)
        for i in range(len(all_foods)):
            foods_names_frame.rowconfigure(i, weight=0)
        btns_lst = []
        for i in range(len(all_foods)):
            btn = ctk.CTkButton(master=foods_names_frame, text=all_foods[i], hover_color='gray', anchor='center',
                                font=('Arial', 15), bg_color='#1A1A24', fg_color='#1A1A24',
                                command=lambda i=i: show_food(all_foods[i]), border_width=1, border_color='white')
            btns_lst.append(btn)
        for i in range(len(btns_lst)):
            btns_lst[i].grid(row=i, column=0)
    def foods_details(self):
        foods_details_main = ctk.CTkFrame(master=self.main_frame, fg_color='#1A1A24', bg_color='#1A1A24')
        foods_details_main.pack(fill='both', expand=True)
        foods_details_label = ctk.CTkLabel(master=foods_details_main, text=self.current_food)
        foods_details_label.pack()

    def switch_pages(self, page):
        # this code must be applied on every page switches except set_meals switches to get back date
        if page != self.set_meals:
            self.date = dt.datetime.now() + dt.timedelta(days=1)
        for frame in self.main_frame.winfo_children():
            frame.destroy()
            self.root.update()
        page()


if __name__ == "__main__":
    first = FirstWindow()
