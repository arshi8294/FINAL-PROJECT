import Meal_planner
import tkinter as tk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MealPlanner")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.goto_

        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()