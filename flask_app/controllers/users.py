from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reg_page')
def reg_page():
    return render_template('reg.html')

@app.route('/registration', methods = ['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/reg_page')

    # email= {
    #             'email':request.form['email'] 
            
    #     }
    email = {'email':request.form['email']}
    # email = request.form['email']
    email_to_check = User.get_by_email(email)
    if email_to_check:
        flash("Email Already in Use.", 'dupe')
        return redirect('/reg_page')
    

        
    

    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    print(pw_hash)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'pw': pw_hash,
        'created_at': 'NOW()',
        'updated_at': 'NOW()'
    }
    # data = request.form
    # Member.create(data)
    User.create(data)
    email = {'email':request.form['email']}
    user_id = User.get_by_email(email)



    session['user_id'] = user_id.id
    
    return redirect('/logged/in')

@app.route('/logged/in')
def login_success():
    if not session['user_id']:
        return redirect('/')
    return redirect('/home')

@app.route('/login', methods=['POST'])    
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.pw,request.form['pw']):
        flash("Invalid Username/Password",'login')
        return redirect('/')
    session['user_id'] = user_in_db.id

    return redirect('/logged/in')


@app.route('/logged/out')
def logout():
    if session['user_id']:
        session.clear()
    return redirect('/')


