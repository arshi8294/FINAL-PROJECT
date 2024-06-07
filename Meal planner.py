# todo : create quick food function
from datetime import date, datetime, timedelta, time
from typing import Dict, Set, Any

import mysql.connector
import random

from _decimal import Decimal


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
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()  # this command is to undo commit we had

        # Close the connection to connect again this time to mealPlanner database
        self.conn.close()

        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Luka77Magic',
            database='MealPlanner'
        )
        self.cursor = self.conn.cursor()

        # Create a table of nutrients we have
        sql = """
        CREATE TABLE IF NOT EXISTS Nutrients(
        id INT NOT NULL AUTO_INCREMENT,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Quantity INT,
        PRIMARY KEY (id)
        );
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

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
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

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
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        # Create a table to store our weekly meals
        sql = """
        CREATE TABLE IF NOT EXISTS Weekly_Meals(
        id INT NOT NULL AUTO_INCREMENT,
        Meal_day VARCHAR(10) NOT NULL,
        Meal_category VARCHAR(1) NOT NULL,
        Meal_food INT NOT NULL,
        PRIMARY KEY (id),
        CONSTRAINT Meal_food_fk FOREIGN KEY (Meal_food) REFERENCES food(id),
        # The Constraint below is required for the table to prevent same meals on each day
        CONSTRAINT Meal_unique UNIQUE (Meal_day, Meal_category)   
        );"""
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def add_nutrients(self, nutrients: dict):

        """" This function is used to add nutrients with their quantities to the nutrients table in the database and
        gets a dictionary with the nutrients names as key and the nutrients quantity as value"""

        sql = """
        INSERT INTO nutrients(name, quantity) VALUES (%s, %s)
        """
        for i in nutrients.keys():
            try:
                self.cursor.execute(sql, (i, nutrients[i]))
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
            else:
                print(f"{i} added successfully to nutrients")

    def add_food(self, food: str, recipie: str):

        """ This function is used to add food to the food table in the database and
        gets food name and food recipie and insert them into the food table in the database"""

        sql = """
        INSERT INTO food(Name, Recipie) VALUES (%s, %s);
        """
        try:
            self.cursor.execute(sql, (food, recipie))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        else:
            print(f"{food} added successfully")

    def add_food_ingredients(self, food, ingredients: dict):

        """ This function is used to add ingredients of foods to the foods_ingredients table in the database;
         It takes a food name and a dictionary of ingredients, which contains ingredients as keys and quantity as values
         and insert them into the foods_ingredients.
         In this function we defined two functions to convert food name and ingredient name to their ids in
         food table and nutrients table."""

        # with the code below we add all not existed nutrients which uses in the food to nutrients table
        self.cursor.execute("SELECT name FROM nutrients")
        nutrients = self.cursor.fetchall()
        nutrients = [i[0] for i in nutrients]
        sql = """
        INSERT INTO nutrients (Name, Quantity) VALUES (%s, 0)
        """
        for i in ingredients:
            if i not in nutrients:
                try:
                    self.cursor.execute(sql, (i, ))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()

        def food_key():
            """
            this function is used to convert food which is food name to food_id which is id of that food in food table
            """
            sql = "SELECT id FROM food WHERE Name = %s "
            try:
                self.cursor.execute(sql, (food,))
            except Exception as e:
                print(e)
            else:
                return self.cursor.fetchone()[0]

        def ingredient_key():
            """"
            this function is used to convert the dictionary which contains nutrients name as keys to ingredients_dict
            which contains nutrients id as keys and quantity as value
            """
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
                self.conn.rollback()
        print(f"{food}'s ingredients added successfully")






    def insertWeeklyMeals(self, day, meal, food):

        """This function is used to insert meals of a week to weekly_meals table in the database.
        It takes a day of the week and a meal name (like breakfast, lunch or dinner) and the food user want for that
        meal. In this function, food_key another time used to convert food name to its id.
        Although one of the most important functions of the application executed at the end of this function,
        and it's updating our nutrients storage after a meal selected completely """

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
            self.conn.rollback()
        else:
            print("your meal added successfully")

        self.decrease_nutrients(food_id)

    def decrease_nutrients(self, food_id):
        # The next query is to get how much and what ingredient selected food need
        sql = """SELECT Ingredient_quantity, food_Ingredient  FROM foods_ingredients WHERE Food_id = %s"""
        try:
            self.cursor.execute(sql, (food_id,))
        except Exception as e:
            print(e)
        else:
            food_ingredients = self.cursor.fetchall()

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
                self.conn.rollback()

    @property
    def shopping_cart(self):
        sql = """SELECT Name, abs(Quantity) FROM nutrients WHERE Quantity<0"""
        self.cursor.execute(sql)
        shopping_list = self.cursor.fetchall()
        return shopping_list

    # def quick_meal(self):
    #     self.cursor.execute("SELECT id FROM food")
    #     foods_list = self.cursor.fetchall()


if __name__ == "__main__":
    planner = MealPlanner()
    planner.add_food("sth", "nothing")
    planner.add_nutrients({"s": 1, "d": 5, "a": 4})
    planner.add_food_ingredients("sth", {"s": 2, "d": 3, "f": 4})
    planner.insertWeeklyMeals("Monday", "L", "sth")
    print(planner.shopping_cart)
