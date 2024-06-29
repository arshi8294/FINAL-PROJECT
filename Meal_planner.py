# todo: create a function to update weekly meals 
import mysql.connector
import random
import datetime as dt


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
        Quantity FLOAT,
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
                Ingredient_quantity FLOAT NOT NULL ,
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
                Meal_date DATE NOT NULL,
                Meal_category VARCHAR(1) NOT NULL,
                Meal_food INT NOT NULL,
                PRIMARY KEY (id),
                CONSTRAINT Meal_food_fk FOREIGN KEY (Meal_food) REFERENCES food(id),
                # The Constraint below is required for the table to prevent same meals on each dates
                CONSTRAINT Meal_unique UNIQUE (Meal_date, Meal_category)   
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

    def add_food(self, food: str, recipie: str, isbreakfast: bool = False):
        """ This function is used to add food to the food table in the database and
        gets food name and food recipie and insert them into the food table in the database"""

        sql = """
            INSERT INTO food(Name, Recipie, Is_Breakfast) VALUES (%s, %s, %s);
            """
        try:
            self.cursor.execute(sql, (food, recipie, isbreakfast))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            raise ValueError('This food is added before')
        else:
            print(f"{food} added successfully")

    def update_food(self, food: str, nutrients: dict, recipe: str):
        """ This function is used to update the food from foods in database """
        food_id = self.food_key(food)
        # first of all we delete food nutrients that this food took from us
        sql = """SELECT ID FROM weekly_meals WHERE Meal_food = %s"""
        self.cursor.execute(sql, (food_id,))
        food_usages = self.cursor.fetchall()
        for i in food_usages:
            self.anti_decrease_nutrients(food_id)

        # now we delete previous ingredients this food took to update it
        sql = "DELETE FROM foods_ingredients WHERE Food_id = %s"
        try:
            self.cursor.execute(sql, (food_id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
        self.add_food_ingredients(food, nutrients)

        # now we update recipie of food
        sql = 'UPDATE food SET Recipie = %s WHERE id = %s'
        self.cursor.execute(sql, (recipe, food_id))

        # at last, we decrease new amounts of nutrients the food takes
        for i in food_usages:
            self.decrease_nutrients(food_id)

    def show_food_ingredients(self, food_name):
        food_id = self.food_key(food_name)
        sql = """SELECT Name, Ingredient_quantity FROM foods_ingredients join nutrients
         ON Food_ingredient=nutrients.id
         WHERE Food_id = %s"""
        self.cursor.execute(sql, (food_id, ))
        food_ingredients = self.cursor.fetchall()
        return food_ingredients

    def show_food_recipies(self, food_name):
        sql = """SELECT Recipie FROM food where Name = %s"""
        self.cursor.execute(sql, (food_name, ))
        recipie = self.cursor.fetchone()[0]
        return recipie

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

    def ingredient_key(self, ingredients):
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

        food_id = self.food_key(food)
        ingredients_dict = self.ingredient_key(ingredients)

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

    def insertWeeklyMeals(self, date, meal, food):
        """This function is used to insert meals of a week to weekly_meals table in the database.
        It takes a day of the week and a meal name (like breakfast, lunch or dinner) and the food user want for that
        meal. In this function, food_key another time used to convert food name to its id.
        Although one of the most important functions of the application executed at the end of this function,
        and it's updating our nutrients storage after a meal selected completely """

        # first we make sure that this meal didn't plan before
        sql = "SELECT Meal_food FROM weekly_meals WHERE Meal_date = %s and Meal_category = %s"
        self.cursor.execute(sql, (date.strftime("%Y-%m-%d"), meal))
        previous_food = self.cursor.fetchone()
        food_id = self.food_key(food)

        if not previous_food:
            sql = """
                INSERT INTO weekly_meals(meal_day, meal_date, meal_category, meal_food)
                VALUES (%s, %s, %s, %s);
                """
            try:
                self.cursor.execute(sql, (date.strftime('%A'), date.strftime('%Y-%m-%d'), meal, food_id))
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
            else:
                print("your meal added successfully")

            self.decrease_nutrients(food_id)
        # now if it was planned before we need to update it
        else:
            self.anti_decrease_nutrients(previous_food[0])  # first of all return all nutrients that food took
            sql = """
            UPDATE weekly_meals SET meal_food = %s WHERE meal_date = %s AND meal_category = %s
            """
            try:
                self.cursor.execute(sql, (food_id, date.strftime('%Y-%m-%d'), meal))
                self.conn.commit()
            except Exception as e:
                print(e)
            else:
                self.decrease_nutrients(food_id)
                print("your weekly meal updated successfully")

    def decrease_nutrients(self, food_id):
        # The next query is to get how much and what ingredient selected food need
        sql = """SELECT Ingredient_quantity, food_Ingredient  FROM foods_ingredients WHERE Food_id = %s"""
        try:
            self.cursor.execute(sql, (food_id,))
        except Exception as e:
            print(e)
        else:
            food_ingredients = self.cursor.fetchall()  # it returns a tuple of (ingredient, quantity of it)

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

    def anti_decrease_nutrients(self, food_id):
        """This function is opposite of decrease_nutrients function, and it used when user want to update a food
        or update the weekly meals"""

        sql = """SELECT Ingredient_quantity, food_Ingredient  FROM foods_ingredients WHERE Food_id = %s"""
        try:
            self.cursor.execute(sql, (food_id,))
        except Exception as e:
            print(e)
        else:
            food_ingredients = self.cursor.fetchall()  # it returns a tuple of (ingredient, quantity of it)

            sql = """
                         UPDATE nutrients SET Quantity =  Quantity+%s
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
    def shopping_list(self):
        sql = """SELECT Name, abs(Quantity) FROM nutrients WHERE Quantity<0"""
        self.cursor.execute(sql)
        shopping_cart = self.cursor.fetchall()
        shopping_cart = {k: v for k, v in shopping_cart}
        return shopping_cart

    def update_nutrients_inventory(self, items: dict):
        sql = """UPDATE nutrients SET Quantity = %s WHERE Name = %s"""
        try:
            for i in items:
                self.cursor.execute(sql, (items[i], i))
                self.conn.commit()
        except Exception as e:
            print(e)

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

    def available_meal(self):
        """
        this function will return the food which its nutrients are available in our storage
        """
        available_meals = []
        self.cursor.execute("SELECT id, quantity FROM nutrients")
        nutrients = self.cursor.fetchall()
        nutrients = {k: v for k, v in nutrients}
        self.cursor.execute("SELECT id FROM food")
        foods = self.cursor.fetchall()
        sql = """SELECT food_ingredient, ingredient_quantity FROM foods_ingredients WHERE Food_id = %s"""
        for food in foods:
            self.cursor.execute(sql, food)
            food_items = self.cursor.fetchall()
            food_items = {k: v for k, v in food_items}
            for i in food_items:
                if food_items[i] > nutrients[i]:
                    break
            else:
                available_meals.append(food[0])
        return self.display_food(random.choice(available_meals)) if available_meals else 0

    def show_each_day_meals(self, date):
        meals = ['B', 'L', 'D']
        daily_meals = []
        sql = """
            SELECT Name from food inner join weekly_meals ON food.id = weekly_meals.Meal_food 
            WHERE Meal_date = %s and Meal_category = %s"""
        for i in meals:
            self.cursor.execute(sql, (date.strftime("%Y-%m-%d"), i))
            s = self.cursor.fetchone()
            if s:
                daily_meals.append(s[0])
            else:
                daily_meals.append('None')
        return daily_meals

    def show_breakfasts(self):
        sql = """SELECT Name from food where Is_Breakfast = 1"""
        self.cursor.execute(sql)
        breakfasts = self.cursor.fetchall()
        if not breakfasts:
            return []
        breakfasts = [i[0] for i in breakfasts]
        return breakfasts

    def show_lunch_and_dinner(self):
        sql = """SELECT Name from food where Is_Breakfast = 0"""
        self.cursor.execute(sql)
        dinners = self.cursor.fetchall()
        if not dinners:
            return []
        dinners = [i[0] for i in dinners]
        return dinners

    def show_all_nutrients(self):
        sql = """SELECT name, quantity FROM nutrients ORDER BY quantity DESC, Name """
        self.cursor.execute(sql)
        all_nutrients = self.cursor.fetchall()
        return all_nutrients if all_nutrients else False



if __name__ == "__main__":
    planner = MealPlanner()
    print((dt.datetime.now()+dt.timedelta(days=1)).strftime("%Y-%m-%d"))
    # planner.add_nutrients({"s": 1, "d": 5, "a": 4})
    # planner.add_food("sth24", "nothing")
    # planner.add_food("sth25", "nothing")
    # planner.add_food("sth26", "nothing")
    # planner.add_food_ingredients("sth24", {"a": 3, "d": 1})
    # planner.add_food_ingredients("sth25", {"a": 1, "f": 4})
    # planner.add_food_ingredients("sth26", {"b": 11, "c": 7})
    # print(planner.show_breakfasts())
    # print(planner.show_lunch_and_dinner())
    # # # planner.delete_food("sth26")
    # print(planner.shopping_list)
    # # print(planner.available_meal())
    # # planner.update_nutrients_inventory(planner.shopping_list)
    # planner.update_food('sth26', {'w': 1111}, 'cook it')
    # print(planner.shopping_list)
    print(planner.show_food_ingredients('qeymah'))
    print(planner.show_food_recipies('qeymah'))
    print(planner.show_all_nutrients())
    print([i[0] for i in planner.show_all_nutrients() if planner.show_all_nutrients()])