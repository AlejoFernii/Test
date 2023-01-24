from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = 'recipes'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_admin = False
        self.recipes = []

    @classmethod
    def create(cls, data):
        query = """ INSERT INTO users (first_name, last_name, email, pw, created_at, updated_at)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s, NOW(),NOW()); """

        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"

        result = connectToMySQL('recipes').query_db(query, data)

        return cls(result[0])

    @classmethod
    def get_user_with_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id=recipes.user_id WHERE users.id = %(id)s;"

        results = connectToMySQL(cls.DB).query_db(query, data)

        
        all_recipes = []
        for row in results:

        #     user_data = {
        #     'id': row['id'],
        #     'first_name': row['first_name'],
        #     'last_name': row['last_name'],
        #     'email': row['email'],
        #     'pw': row['pw'],
        #     'created_at': row['created_at'],
        #     'updated_at': row['updated_at'],
        # }
        #     one_user = cls(user_data)

            recipe_data = {
                "id": row['recipes.id'],
                "user_id": row['user_id'],
                "name": row['name'],
                "description": row['description'],
                "instructions": row['instructions'],
                "date_made": row['date_made'],
                "is_under": row['is_under'],
                "created_at": row['recipes.created_at'],
                "updated_at": row['recipes.updated_at']
            }
            one_recipe = recipe.Recipe(recipe_data)
            # one_user.recipes.append(one_recipe)

            all_recipes.append(one_recipe)


        return all_recipes

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL('recipes').query_db(query)

    # @classmethod
    # def get_by_username(cls,data):
    #     query = "SELECT * FROM users WHERE username = %(username)s;"
    #     result = connectToMySQL('wall').query_db(query,data)
    #     if len(result) < 1:
    #         return False
    #     return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(member):
        is_valid = True
        if len(member['first_name']) <= 0:
            flash("First Name Required.", 'reg')
            is_valid = False
        if len(member['last_name']) <= 0:
            flash("Last Name Required.", 'reg')
            is_valid = False
        if len(member['pw']) < 8:
            flash("Password Must Be At Least 8 Characters.", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(member['email']):
            flash("Invalid Email Format.", 'reg')
            is_valid = False
        if member['conpw'] != member['pw']:
            flash("Password Must Match.", 'reg')
            is_valid = False
        return is_valid
