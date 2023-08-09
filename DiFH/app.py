from flask import Flask, render_template, request, redirect, send_from_directory, url_for, send_file
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from addFile import *
from publistFile import *
import os
import re


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
    hash=db.Column(db.String(500), nullable=False)
    project=db.Column(db.String(500), nullable=False)
    version=db.Column(db.String(500), nullable=False)
    versionName=db.Column(db.String(500), nullable=False)
    releaseLog=db.Column(db.String(500))

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


        x = re.search("[a-zA-z]*@[a-zA-Z]*[.][a-zA-Z]*", username)

        if not x:
          return render_template('signUP.html', contentDiv="invalid email")


        print('\nEntered U:', username, 'P:', password, 'R:', rePassword)
        if password==rePassword:
            x = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$", password)
            if not x:
                return render_template('signUP.html', contentDiv="password must contain at least one number, one smaller case lesser, one upper case letter, one special character and a minimum of eight characters.")

            newUser=Todo(username=username, password=password)
        else:
            return render_template('signUP.html', contentDiv="Password do not match")
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

        x = re.search("[a-zA-z]*@[a-zA-Z]*[.][a-zA-Z]*", username)

        if not x:
          return render_template('login.html', contentDiv="invalid email")


        users = Todo.query.order_by(Todo.id).all()

        for user in users:
            if user.username == username:
                if user.password == password:
                    currentUser['username'] = username
                    currentUser['password'] = password
                    return redirect('/user')
                else:
                    return render_template('login.html', contentDiv="wrong username or password")
            else:
                continue

        return render_template('login.html', contentDiv="no user exists. Try sign up.")
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
            print("\n\nform input")
            print(request.form)


            fileExtension = file.filename.split(".")[-1]
            filename = str(hash(currentUser['username'] + secure_filename(file.filename)))+"."+fileExtension
            print("\n\nuploaded file name:\n", currentUser['username'] + secure_filename(file.filename), "\n\nhash:\n", filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fHash = filename # uploadFile(filename)

            newHash = files(username = currentUser['username'], 
                            hash = fHash,
                            project=request.form["project"],
                            version=request.form["version"],
                            versionName=request.form["versionName"],
                            releaseLog=request.form["releaseLog"]
                            )

            try:
                db.session.add(newHash)
                db.session.commit()
                print("\nHash saved to the database")
            except:
                print("something went wrong")

            return render_template('hash.html', contentDiv=fHash)
    else:
        if currentUser['username'] == "":
            contentDiv="Please Login to access the dash"
            return render_template('index.html', contentDiv=contentDiv)
        return render_template('addFile.html')


@app.route('/updateFile/<fileName>', methods=['GET', 'POST'])
def updateFile(fileName):
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
            print("\n\nform input")
            print(request.form)


            fileExtension = file.filename.split(".")[-1]
            filename = str(hash(currentUser['username'] + secure_filename(file.filename)))+"."+fileExtension
            print("\n\nuploaded file name:\n", currentUser['username'] + secure_filename(file.filename), "\n\nhash:\n", filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fHash = filename # uploadFile(filename)

            newHash = files(username = currentUser['username'], 
                            hash = fHash,
                            project=request.form["project"],
                            version=request.form["version"],
                            versionName=request.form["versionName"],
                            releaseLog=request.form["releaseLog"]
                            )

            try:
                db.session.add(newHash)
                db.session.commit()
                print("\nHash saved to the database")
            except:
                print("something went wrong")

            return render_template('hash.html', contentDiv=fHash)

    elif request.method == 'GET':
        return render_template('updateFile.html', contentDiv=fileName, project=fileName)

    

@app.route("/uploads", methods=['GET'])
def uploads():
    ups = files.query.order_by(files.id).all()
    toRender = []
    for x in ups:
        print(x.id, '|', x.username, '|', x.hash)
        if x.username == currentUser['username']:
            if x.project not in toRender:
                toRender.append(x.project)
    print("\n")
    return render_template("uploads.html", contentDiv=toRender)

@app.route("/returnFile/<fileHash>", methods=['GET'])
def returnFile(fileHash):
    print(fileHash)
    # file_content = ""
    # with open("./uploads/"+fileHash) as f:
    #     file_content = f.read()

    # response = make_response(file_content, 200)
    # return redirect(url_for('static', filename='uploads/' + fileHash), code=301)
    # return send_from_directory(path = "", directory = "/uploads", filename=fileHash, as_attachment=False)
    return send_file('./uploads/'+fileHash)


@app.route("/project/<projectName>", methods=['GET'])
def project(projectName):
    print(projectName)
    ups = files.query.order_by(files.id).all()
    toRender = []
    count = 0
    for x in ups:
        
        if x.username == currentUser['username'] and projectName == x.project:
            print(x.id, '|', x.username, '|', x.hash, '|', x.project, '|', x.version, '|', x.versionName)
            count = count+1
            toRender.append({
                "sl":count,
                "version": x.version,
                "versionName": x.versionName,
                "project": x.project,
                "releaseLog": x.releaseLog,
                "hash": x.hash
            })
    print("\nobjects sent to render", toRender)
    return render_template("projectDetails.html", contentDiv=toRender, project=projectName)


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method =='POST':
        username=request.form['username']
        password=request.form['password']

        if username == 'admin' and password == 'admin':
            users = Todo.query.order_by(Todo.id).all()
            print(users[0].username)
            return render_template('users.html', contentDiv=users)
        else:
            return render_template('adminLogin.html', contentDiv="wrong username or password")

    else:
        return render_template('adminLogin.html')

@app.route('/delete/<userId>', methods=['POST', 'GET'])
def deleteUser(userId):
    Todo.query.filter_by(id=userId).delete()
    db.session.commit()
    users = Todo.query.order_by(Todo.id).all()
    # print(users[0].username)
    return render_template('users.html', contentDiv=users)


@app.route('/adminFile', methods=['POST', 'GET'])
def adminFile():
    users = files.query.order_by().all()
    print(users[0].username)
    return render_template('files.html', contentDiv=users)
    
@app.route('/deleteFile/<id>', methods=['GET', 'POST'])
def deleteFile(id):
    files.query.filter_by(id=id).delete()
    db.session.commit()
    users = files.query.order_by().all()
    # print(users[0].username)
    return render_template('files.html', contentDiv=users)

if __name__ == "__main__":
    app.run(debug=True)
