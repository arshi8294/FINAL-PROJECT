# Todo : create functions of buttons and maybe fix menu filling issue
import customtkinter as ctk
import Meal_planner as Mp


class FirstWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Meal Planner")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.menu_bar()
        self.frame1 = ctk.CTkFrame(master=self.root)
        self.frame1.pack(side='top', fill='both')
        self.labeltable = ctk.CTkLabel(master=self.frame1, text="place for table")
        self.labeltable.pack(fill='both')

        self.root.mainloop()

    def menu_bar(self):
        menu_items = ['Add food', 'Create and edit weekly meals plan', 'Add nutrients']
        commands_lst = []  # a list of functions for buttons
        buttons_list = []

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

            # apply buttons on menu and save them in a list, so we can configure them later
            for i in menu_items:
                btn = ctk.CTkButton(master=self.menubar_frame, text=f'{i}', bg_color='black', fg_color='black')
                btn.pack(fill='x', pady=5)
                buttons_list.append(btn)

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


if __name__ == "__main__":
    first = FirstWindow()
