# search and implement conn.rollback & control if user changed a food in weekly meals.

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
        CONSTRAINT Meal_food_fk FOREIGN KEY (Meal_food) REFERENCES food(id),
        # This Constraint is required for the table to prevent same meals on each day
        CONSTRAINT Meal_unique UNIQUE (Meal_day, Meal_category)  
        );"""
        self.cursor.execute(sql)
        self.conn.commit()

    def add_nutrients(self, nutrients: dict):

        sql = """
        INSERT INTO nutrients(name, quantity) VALUES (%s, %s)
        """
        for i in nutrients.keys():
            try:
                self.cursor.execute(sql, (i, nutrients[i]))
            except Exception as e:
                print(e)
            else:
                self.conn.commit()
                print(f"{i} added successfully")

    def add_food(self, food, recipie):
        sql = """
        INSERT INTO food(Name, Recipie) VALUES (%s, %s);
        """
        try:
            self.cursor.execute(sql, (food, recipie))
            self.conn.commit()
        except Exception as e:
            print(e)
        else:
            print(f"{food} added successfully")

    def add_food_ingredients(self, food, ingredients: dict):
        def food_key():
            sql = "SELECT id FROM food WHERE Name = %s "
            try:
                self.cursor.execute(sql, (food,))
            except Exception as e:
                print(e)
            else:
                return self.cursor.fetchone()[0]

        def ingredient_key():
            sql = "SELECT id FROM nutrients WHERE Name = %s "
            ingredients_dict = {}
            for i in ingredients.keys():
                try:
                    self.cursor.execute(sql, (i,))
                    j = self.cursor.fetchone()[0]
                    ingredients_dict[j] = ingredients[i]
                except Exception as e:
                    print(e)
            return ingredients_dict

        food_id = food_key()
        ingredients_dict = ingredient_key()

        sql = """
        INSERT INTO foods_ingredients(Food_id, Food_Ingredient, Ingredient_quantity) VALUES (%s, %s, %s)
        """
        for i in ingredients_dict.keys():
            try:
                self.cursor.execute(sql, (food_id, i, ingredients_dict[i]))
                self.conn.commit()
            except Exception as e:
                print(e)
        print(f"{food}'s ingredients added successfully")

    def insertWeeklyMeals(self, day, meal, food):
        def food_key():
            sql = "SELECT id FROM food WHERE Name = %s "
            try:
                self.cursor.execute(sql, (food,))
            except Exception as e:
                print(e)
            else:
                return self.cursor.fetchone()[0]

        food_id = food_key()
        sql = """
        INSERT INTO weekly_meals(meal_day, meal_category, meal_food)
        VALUES (%s, %s, %s);
        """
        try:
            self.cursor.execute(sql, (day, meal, food_id))
            self.conn.commit()
        except Exception as e:
            print(e)
        else:
            print("your meal added successfully")

        # The next query is to get how much and what ingredient selected food need
        sql = """SELECT Ingredient_quantity, food_Ingredient  FROM foods_ingredients WHERE Food_id = %s"""
        try:
            self.cursor.execute(sql, (food_id,))
        except Exception as e:
            print(e)
        else:
            food_ingredients = self.cursor.fetchall()

            # This is the part of code that made me angry so much, but after I figured out how to config it
            # sent me to heaven
            # in this part of code I used data of food_ingredients,
            # which are ingredient and quantity of it that needed for food, to create a query
            # to update quantity of nutrients we have after adding food to weekly meals
            sql = """
             UPDATE nutrients SET Quantity =  Quantity-%s
             WHERE id = %s;
             """
            try:
                for i in food_ingredients:
                    self.cursor.execute(sql, i)
                    self.conn.commit()
            except Exception as e:
                print(e)


if __name__ == "__main__":
    planner = MealPlanner()
    planner.insertWeeklyMeals("Monday", "L", "Steak")
