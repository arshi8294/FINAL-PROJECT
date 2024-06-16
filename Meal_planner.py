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
            Is_Breakfast BOOLEAN DEFAULT FALSE,
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
                CONSTRAINT INGREDIENT_FK FOREIGN KEY (Food_ingredient) REFERENCES Nutrients(id),
                CONSTRAINT UNQ_FOOD_INGREDIENTS UNIQUE (Food_id, Food_ingredient)
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

    def food_key(self, food):
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

    def add_food_ingredients(self, food, ingredients: dict):
        """ This function is used to add ingredients of foods to the foods_ingredients table in the database;
         It takes a food name and a dictionary of ingredients, which contains ingredients as keys and quantity as values
         and insert them into the foods_ingredients."""

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
                    self.cursor.execute(sql, (i,))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()

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

        food_id = self.food_key(food)
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

        food_id = self.food_key(food)
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

    def display_food(self, food_id):
        sql = """SELECT Name, Ingredient_quantity FROM foods_ingredients JOIN nutrients
             ON foods_ingredients.Food_ingredient = nutrients.id WHERE Food_id = %s"""
        try:
            self.cursor.execute(sql, (food_id,))
            food_ingredients = self.cursor.fetchall()
            dict_ingredients = {i[0]: i[1] for i in food_ingredients}
            self.cursor.execute("""SELECT Name, Recipie FROM FOOD WHERE id = %s""", (food_id,))
            food_name = self.cursor.fetchall()
            return food_name[0][0], dict_ingredients, food_name[0][1]
        except Exception as e:
            print(e)

    @property
    def shopping_cart(self):
        sql = """SELECT Name, abs(Quantity) FROM nutrients WHERE Quantity<0"""
        self.cursor.execute(sql)
        shopping_list = self.cursor.fetchall()
        return shopping_list

    def delete_food(self, food: str):
        """This method deletes the food user wants to delete from all 3 tables: food, foods_ingredients & weekly_meals
        and if food were chosen by user in weekly_meals it will return ingredients it took to nutrients table."""
        food_id = self.food_key(food)
        sql = "SELECT count(*) as count_food FROM weekly_meals WHERE Meal_food = %s"
        self.cursor.execute(sql, (food_id,))
        result = self.cursor.fetchone()
        if result[0]:
            for j in range(result[0]):
                sql = """SELECT Ingredient_quantity, food_Ingredient  FROM foods_ingredients WHERE Food_id = %s"""
                try:
                    self.cursor.execute(sql, (food_id,))
                except Exception as e:
                    print(e)
                else:
                    food_ingredients = self.cursor.fetchall()
                    sql = """
                         UPDATE nutrients SET Quantity =  Quantity + %s
                         WHERE id = %s;
                         """
                    try:
                        for i in food_ingredients:
                            self.cursor.execute(sql, i)
                            self.conn.commit()
                    except Exception as e:
                        print(e)
                        self.conn.rollback()

        try:
            self.cursor.execute("DELETE FROM weekly_meals WHERE Meal_food = %s", (food_id,))
            self.conn.commit()
            self.cursor.execute("DELETE FROM foods_ingredients WHERE Food_id = %s", (food_id,))
            self.conn.commit()
            self.cursor.execute("DELETE FROM food WHERE id = %s", (food_id,))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def quick_meal(self):
        """ IN THIS FUNCTION BY USING AN INNER JOIN QUERY WE CAN HAVE ACCESS TO THE AVAILABLE FOODS BASED ON
         REMAIN NUTRIENTS IN NUTRIENTS TABLE IN DATABASE"""
        # this query will give us available foods based on quantity of ingredients remain for user
        sql = """
                SELECT DISTINCT food.id FROM ((foods_ingredients INNER JOIN food
                ON foods_ingredients.Food_id = food.id)
                INNER JOIN nutrients ON Foods_ingredients.Food_ingredient = nutrients.id) 
                WHERE nutrients.Quantity > foods_ingredients.Ingredient_quantity
                """
        try:
            self.cursor.execute(sql)
            available_foods = self.cursor.fetchall()
            food_id = random.choice(available_foods)[0]
            return self.display_food(food_id)
        except Exception as e:
            return e


if __name__ == "__main__":
    planner = MealPlanner()
    # planner.add_nutrients({"s": 1, "d": 5, "a": 4})
    # planner.add_food("sth24", "nothing")
    # planner.add_food("sth25", "nothing")
    # planner.add_food("sth26", "nothing")
    # planner.add_food_ingredients("sth24", {"a": 3, "d": 1})
    # planner.add_food_ingredients("sth25", {"a": 1, "f": 4})
    # planner.add_food_ingredients("sth26", {"b": 11, "c": 7})
    # planner.insertWeeklyMeals("Monday", "L", "sth26")
    # print(planner.quick_meal())
    planner.delete_food("sth26")
    print(planner.shopping_cart)
