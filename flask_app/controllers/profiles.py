from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe, user

@app.route('/profile/<int:id>')
def show_profile(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {'id': id}
    profile = user.User.get_one(data)

    sesh_data = {'id':session['user_id']}
    current_user = user.User.get_one(sesh_data)

    all_recipes = user.User.get_user_with_recipes(data)

    return render_template('profile.html',profile=profile, current_user=current_user, all_recipes=all_recipes)