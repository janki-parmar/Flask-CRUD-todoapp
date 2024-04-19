from flask import Flask, request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    dateofbirth = db.Column(db.String(10), nullable=False)  # Adjust as per your requirements

    def __repr__(self):
        return f"<User {self.id} - {self.username}>"

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime)

    def __repr__(self) -> str:
            return f"{self.sno} - {self.title}"
    

@app.route("/", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']

            data = User.query.all()
            for i in data:
                if i.email == email and i.password == password:
                    return redirect('/home')

    return render_template('login.html')


@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        dateofbirth = request.form['dateofbirth']

        if username.strip() and email.strip() and password.strip() and dateofbirth.strip() != '':
            userdata = User(username=username, email=email, password=password, dateofbirth=dateofbirth)
            db.session.add(userdata)
            db.session.commit()
            return redirect('/')
    return render_template('signup.html')



@app.route("/home", methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']

        if title.strip() and description.strip() != '':
            todo = Todo(title=title, desc=description)
            db.session.add(todo)
            db.session.commit()
            return redirect('/home')
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
    with app.app_context():
        db.create_all()
    app.run( debug=True)

app = Flask(__name__, static_folder='static')