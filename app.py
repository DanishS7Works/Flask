from flask import Flask ,request, render_template , redirect
from flask_login import login_user, logout_user , login_required , LoginManager , UserMixin , current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'd9f8a3c7e2b14f6a9d0e5c8b12345678'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


    

class UserAuth(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return  f'{self.id}- {self.email}'
    
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_auth.id'), nullable=False)
    user = db.relationship('UserAuth', backref='todos')

    def __repr__(self):
        return  f'{self.id}- {self.title}'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(UserAuth, int(user_id))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Optional: check if email already exists
        existing_user = UserAuth.query.filter_by(email=email).first()
        if existing_user:
            return " credentials exist. Please try with new one."

        new_user = UserAuth(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")
    



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = UserAuth.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect("/")
        else:
            return "Invalid credentials. Please try again."

    return render_template("login.html")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route("/" , methods=['GET','POST'])
@login_required
def hello_world():
    if request.method == "POST":
        title =  request.form['title']
        desc =  request.form['desc']
        todo = Todo(title=title,desc=desc , user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
    allTodo =  Todo.query.all()
    return render_template("index.html",allTodo=allTodo)

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    Todo = Todo.query.filter_by(id=id).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>" , methods=['GET','POST'])
@login_required
def update(id):
    if request.method == "POST":
        title =  request.form['title']
        desc =  request.form['desc']
        upd_todo = Todo.query.filter_by(id=id).first()
        upd_todo.title = title
        upd_todo.desc = desc
        db.session.add(upd_todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(id = id).first()

    return render_template("update.html",todo=todo)




if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)