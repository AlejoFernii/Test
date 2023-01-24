from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


from flask import flash


class Recipe:
    DB = 'recipes'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.is_under = data['is_under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.comments = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (user_id, name, description, instructions, date_made, is_under, created_at, updated_at) VALUES ( %(user_id)s, %(name)s, %(description)s, %(instructions)s, DATE_FORMAT(%(date_made)s,'%%%%W %%%%M %%%%D %%%%Y'), %(is_under)s, NOW(), NOW() );"

        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_all_with_user(cls):

        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"

        results = connectToMySQL('recipes').query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)

            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'pw': row['pw'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            author = user.User(user_data)
            one_recipe.creator = author

            all_recipes.append(one_recipe)

        return all_recipes

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"

        result = connectToMySQL(cls.DB).query_db(query, data)

        one_recipe = cls(result[0])

        user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'pw': result[0]['pw'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at'],
        }
        author = user.User(user_data)
        one_recipe.creator = author

        return one_recipe

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, is_under = %(is_under)s, updated_at = NOW() WHERE id = %(id)s;"

        return connectToMySQL(cls.DB).query_db(query,data)
        




    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        return connectToMySQL('recipes').query_db(query,data)





    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) <= 0:
            flash("Recipe Aust Have A Name.", 'recipe')
            is_valid=False
        if len(recipe['description']) <= 0:
            flash("Recipe Must Have A Description." , 'recipe')
            is_valid=False
        if len(recipe['instructions']) <= 0:
            flash("Recipe Must Have A Instructions.", 'recipe')
            is_valid=False
        if len(recipe['date_made']) <=0:
            flash("All Fields Required.", 'recipe' )
            is_valid=False
        # if recipe['is_under'] == None:
        #     flash("All Fields Required.", 'recipe' )
        #     is_valid=False
        return is_valid
        

