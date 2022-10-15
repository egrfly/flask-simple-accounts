from flask import Flask, request, flash, render_template, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

from config import SECRET_KEY

from database.users import get_user_by_id, get_user_with_credentials, email_available, add_user

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.login_message = 'Please login to view this page.'


class User(UserMixin):

    def __init__(self, user_details):
        self.id = user_details.get('id')
        self.name = user_details.get('name')
        self.email = user_details.get('email')


@login_manager.user_loader
def user_loader(user_id):
    user_details = get_user_by_id(user_id)
    if user_details is None:
        return None
    user = User(user_details)
    return user


@app.get('/')
def home():
    return render_template('home.html')


@app.get('/login')
def view_login():
    if not current_user.is_anonymous:
        return redirect('/profile')
    return render_template('login.html')


@app.post('/login')
def submit_login():
    if not current_user.is_anonymous:
        return redirect('/profile')
    email = request.form.get('email')
    password = request.form.get('password')
    user = get_user_with_credentials(email, password)
    if user is None:
        flash("Invalid credentials.", 'error')
    else:
        user = User(user)
        login_user(user)
        return redirect('/profile')
    return redirect('/login')


@app.get('/signup')
def view_signup():
    if not current_user.is_anonymous:
        return redirect('/profile')
    return render_template('signup.html')


@app.post('/signup')
def submit_signup():
    if not current_user.is_anonymous:
        return redirect('/profile')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    if len(password) < 8:
        flash("Passwords should be at least 8 characters long.", 'error')
    elif not email_available(email):
        flash("An account with that email already exists.", 'error')
    else:
        add_user(name, email, password)
        flash("New account created.", 'info')
        return redirect('/login')
    return redirect('/signup')


@app.post('/logout')
@login_required
def submit_logout():
    logout_user()
    return redirect('/login')


@app.get('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
