from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "123"

db = SQLAlchemy(app)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    
class TodoForm(FlaskForm):
    task = StringField("Task")
    submit = SubmitField("Add Todo")

@app.route("/")
def index():
    all_todos = Todos.query.all()
    todos_string = ""
    return render_template("index.html", all_todos=all_todos)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todos(task=form.task.data)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html", form=form)


@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    todo = Todos.query.get(todo_id)
    todo.complete = True
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/incomplete/<int:todo_id>")
def incomplete(todo_id):
    todo = Todos.query.get(todo_id)
    todo.complete = False
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todos.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id):
    form = TodoForm()
    todo_to_be_updated = Todos.query.get(todo_id)
    if form.validate_on_submit():
        todo_to_be_updated.task = form.task.data
        db.session.commit()
        return redirect(url_for("index"))
    elif request.method == "GET":
        form.task.data = todo_to_be_updated.task
    return render_template("update.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')