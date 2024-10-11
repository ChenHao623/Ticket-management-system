from flask import Flask, render_template, flash, redirect, url_for, session
from forms import RegistrationForm, LoginForm, TicketForm
from models import db, User, Ticket
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# 首页视图
@app.route('/')
def home():
    return "Welcome to the Ticket Management System!"

# 添加用户注册视图
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # 创建用户对象并存入数据库
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

# 添加用户登录视图
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 从数据库中查找用户
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

# 添加用户登出视图
@app.route('/logout')
def logout():
    session.clear()  # 清除会话数据，确保用户登出
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

# 添加票务视图
@app.route('/add_ticket', methods=['GET', 'POST'])
def add_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            event_name=form.event_name.data,
            date=form.date.data,
            price=form.price.data,
            available=form.available.data
        )
        db.session.add(ticket)
        db.session.commit()
        flash(f'Ticket "{form.event_name.data}" has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_ticket.html', form=form)

# 查看所有票务的视图
@app.route('/tickets')
def tickets():
    all_tickets = Ticket.query.all()
    return render_template('tickets.html', tickets=all_tickets)

if __name__ == '__main__':
    app.run(debug=True)