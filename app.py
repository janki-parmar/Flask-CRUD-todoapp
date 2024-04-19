from flask import Flask, request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime)

    def __repr__(self) -> str:
            return f"{self.sno} - {self.title}"
    

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')



@app.route("/home" , methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']

        if title.strip() and description.strip() != '':
            todo = Todo(title=title, desc=description)
            db.session.add(todo)
            db.session.commit()
    return render_template('home.html')
    

@app.route("/show")
def show():
    allTodo = Todo.query.all()
    return render_template('show.html', all= allTodo)


@app.route("/update/<int:sno>", methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']

        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = description
        
        db.session.add(todo)
        db.session.commit()
        return redirect('/show')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo= todo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/show')





if __name__ == '__main__':
    app.run( debug=True)

app = Flask(__name__, static_folder='static')