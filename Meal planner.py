# todo : handle auto increment bugs

import mysql.connector
import random


class MealPlanner:
    # create database and tables and relations
    def __init__(self):
        # Create MealPlanner database and connect to it
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Luka77Magic')
        self.cursor = self.conn.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS MealPlanner"
        self.cursor.execute(sql)
        self.conn.commit()
        # Close the connection to connect again this time to mealPlanner database
        self.conn.close()

        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Luka77Magic',
            database='MealPlanner'
        )
        self.cursor = self.conn.cursor()

        # Create a table of ingredients we have
        sql = """
        CREATE TABLE IF NOT EXISTS Nutrients(
        id INT NOT NULL AUTO_INCREMENT,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Quantity INT,
        PRIMARY KEY (id)
        );
        """
        self.cursor.execute(sql)
        self.conn.commit()

        # Create a table of foods we have
        sql = """
        CREATE TABLE IF NOT EXISTS food(
        id INT NOT NULL AUTO_INCREMENT,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Is_Breakfast BOOLEAN DEFAULT TRUE,
        Is_Lunch BOOLEAN DEFAULT TRUE,
        Is_Dinner BOOLEAN DEFAULT TRUE,
        Recipie TEXT DEFAULT NULL,
        PRIMARY KEY (id)
        );
        """
        self.cursor.execute(sql)
        self.conn.commit()

        # Create a table for ingredients we need for each food
        sql = """
        CREATE TABLE IF NOT EXISTS Foods_Ingredients(
        id INT NOT NULL AUTO_INCREMENT,
        Food_id INT NOT NULL,
        Food_ingredient INT NOT NULL,
        Ingredient_quantity INT NOT NULL ,
        PRIMARY KEY (id),
        CONSTRAINT FOOD_FK FOREIGN KEY (Food_id) REFERENCES food(id),
        CONSTRAINT INGREDIENT_FK FOREIGN KEY (Food_ingredient) REFERENCES Nutrients(id)
        );"""
        self.cursor.execute(sql)
        self.conn.commit()

        # Create a table to store our weekly meals
        sql = """
        CREATE TABLE IF NOT EXISTS Weekly_Meals(
        id INT NOT NULL AUTO_INCREMENT,
        Meal_day VARCHAR(10) NOT NULL,
        Meal_category VARCHAR(1) NOT NULL,
        Meal_food INT NOT NULL,
        PRIMARY KEY (id),
        CONSTRAINT Meal_food_fk FOREIGN KEY (Meal_food) REFERENCES food(id)
        );"""
        self.cursor.execute(sql)
        self.conn.commit()

    def add_foods(self):
        foods_lst = ["Pizza", "Cheeseburger", "Steak", "Omelette", "Pepperoni", "Qeymah"]
        sql = """
        INSERT INTO food(name) VALUES (%s);
        """
        for food in foods_lst:
            self.cursor.execute(sql, (food,))
            self.conn.commit()

    def insertWeeklyMeals(self):
        self.cursor.execute("DELETE from weekly_meals")
        self.conn.commit()
        self.cursor.execute("ALTER TABLE weekly_meals AUTO_INCREMENT=1")
        self.conn.commit()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        meals = ["B", "L", "D"]
        self.cursor.execute("""SELECT id FROM Food ORDER BY id ASC """)
        foods = self.cursor.fetchall()
        foods = [j for i in foods for j in i]
        print(foods)

        sql = """
        INSERT INTO Weekly_Meals (MEAL_day, Meal_category, Meal_food)
        VALUES (%s, %s, %s);
        """

        for day in days :
            for meal in meals :
                self.cursor.execute(sql, (day, meal, random.choice(foods)))
                self.conn.commit()


if __name__ == "__main__":
    planner = MealPlanner()
    # planner.add_foods()
    planner.insertWeeklyMeals()
