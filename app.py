from flask import Flask ,request, render_template , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return  f'{self.id}- {self.title}'

@app.route("/" , methods=['GET','POST'])
def hello_world():
    if request.method == "POST":
        title =  request.form['title']
        desc =  request.form['desc']
        todo = User(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo =  User.query.all()
    return render_template("index.html",allTodo=allTodo)

@app.route("/delete/<int:id>")
def delete(id):
    Todo = User.query.filter_by(id=id).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>" , methods=['GET','POST'])
def update(id):
    if request.method == "POST":
        title =  request.form['title']
        desc =  request.form['desc']
        upd_todo = User.query.filter_by(id=id).first()
        upd_todo.title = title
        upd_todo.desc = desc
        db.session.add(upd_todo)
        db.session.commit()
        return redirect("/")
    todo = User.query.filter_by(id = id).first()
    print(todo.desc,"-------")
    return render_template("update.html",todo=todo)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)