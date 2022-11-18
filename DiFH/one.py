from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from addFile import *
import os


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'html', 'css', 'js', 'jpeg', 'jpg', 'png', 'bnp', 'mp3', 'mp4', 'wav', 'ogg'}

app = Flask(__name__,
            static_folder='./static',
            template_folder='./templates')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
currentUser = {'username':'', 'password':''}

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return('<Task %r>' % self.id)

class files(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),nullable=False)
    # fileName=db.Column(db.String(200),nullable=False)
    hash=db.Column(db.String(500), nullable=False)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")



@app.route('/signup', methods=['POST', 'GET'])
def signUp():
    if request.method =='POST':
        username=request.form['username']
        password=request.form['password']
        rePassword=request.form['rePassword']
        print('\nEntered U:', username, 'P:', password, 'R:', rePassword)
        if password==rePassword:
            newUser=Todo(username=username, password=password)
        else:
            return("Password do not match")
        try:
            db.session.add(newUser)
            db.session.commit()
            print('\nValue inserted to database, redirection to home...')
            return redirect('/log')
        except:
            return 'there was an issue'

    else:
        return render_template("signUP.html")



@app.route('/login', methods=['POST', 'GET'])
def userLogin():
    if request.method =='POST':
        username=request.form['username']
        password=request.form['password']

        users = Todo.query.order_by(Todo.id).all()

        for user in users:
            if user.username == username:
                if user.password == password:
                    currentUser['username'] = username
                    currentUser['password'] = password
                    return redirect('/user')
                else:
                    return 'wrong username or password'
            else:
                continue

        return 'no username exists. Try sign up.'
    else:
        return render_template('login.html')



@app.route('/user', methods=['GET'])
def user():
    if currentUser['username'] == "":
        contentDiv="Please Login"
    else:
        contentDiv= 'You are ' + currentUser['username']
    return render_template('content.html', contentDiv=contentDiv)



@app.route('/log', methods=['POST', 'GET'])
def users():
    if request.method =='GET':
        users = Todo.query.order_by(Todo.id).all()
        filesUp = files.query.order_by(files.id).all()

        print("\n")
        for user in users:
            print(user.id, '|', user.username, '|',  user.password)
        print("\n")

        print("\n")
        for f in filesUp:
            print(f.id, '|', f.username, '|',  f.hash)
        print("\n")
        return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    currentUser['username'] = ""
    currentUser['password'] = ""
    return redirect('/')


@app.route('/dash', methods=['GET'])
def dash():
    if currentUser['username'] == "":
        contentDiv="Please Login to access the dash"
        return render_template('index.html', contentDiv=contentDiv)
    return render_template('dash.html')

@app.route('/addFile', methods=['GET', 'POST'])
def addFile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', contentDiv="no file part")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template('index.html', contentDiv="no file selected")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            hash = uploadFile(filename)

            newHash = files(username = currentUser['username'], hash = hash)
            try:
                db.session.add(newHash)
                db.session.commit()
                print("\nHash saved to the databalse")
            except:
                print("something went wrong")

            return render_template('hash.html', contentDiv=hash)
    else:
        if currentUser['username'] == "":
            contentDiv="Please Login to access the dash"
            return render_template('index.html', contentDiv=contentDiv)
        return render_template('addFile.html')

@app.route("/uploads", methods=['GET'])
def uploads():
    ups = files.query.order_by(files.id).all()
    toRender = []
    for x in ups:
        print(x.id, '|', x.username, '|', x.hash)
        if x.username == currentUser['username']:
            toRender.append(x.hash)
    print("\n")
    return render_template("uploads.html", contentDiv=toRender)

if __name__ == "__main__":
    app.run(debug=True)
