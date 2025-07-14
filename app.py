 from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import LoginForm

app = Flask(_name_)
app.secret_key = 'mysecret'  # Important for sessions & forms

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy user class
class User(UserMixin):
    def _init_(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Dummy database
users = {
    "admin": User(id=1, username="admin", password="password")
}

# Load user function
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == str(user_id):
            return user
    return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.get(form.username.data)
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Invalid Credentials"
    return render_template('login.html', form=form)

# Home route (protected)
@app.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.username)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if _name_ == '_main_':
    app.run(debug=True)
