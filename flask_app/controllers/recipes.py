from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import recipe,user

@app.route('/create/recipe/<int:id>')
def create_page(id):

    user_id = {'id':id}
    current_user = user.User.get_one(user_id)

    return render_template('create.html',current_user=current_user)

@app.route('/create', methods=['POST'])
def create_recipe():
    data = request.form
    if not recipe.Recipe.validate_recipe(data):
        return redirect(request.referrer)
    recipe.Recipe.save(data)

    return redirect('/home')

@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):

    data = {
        'id':id
    }

    recipe.Recipe.destroy(data)

    return redirect('/home')


@app.route('/view/<int:id>')
def view_one(id):
    if 'user_id' not in session:
        return redirect('/')


    data ={'id':id}
    one_recipe = recipe.Recipe.get_one_with_user(data)
    user_id={'id':session['user_id']}
    current_user = user.User.get_one(user_id)
    return render_template('view.html', one_recipe=one_recipe, current_user=current_user)

@app.route('/edit/<int:id>')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {'id':id}
    one_recipe = recipe.Recipe.get_one_with_user(data)
    user_id={'id':session['user_id']}
    current_user = user.User.get_one(user_id)
    return render_template('edit.html', one_recipe=one_recipe, current_user=current_user)

@app.route('/edit/recipe', methods = ['POST'])
def edit_recipe():
    
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(request.referrer)

    recipe.Recipe.update_recipe(request.form)
    recipe_id = request.form['id']

    return redirect(f'/view/{recipe_id}')


