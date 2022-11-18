from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from model import *


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'mp3', 'wav', 'ogg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/upload')
# def returnHTML():
#    return render_template('index.html')
	
# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return toText(filename)
    return '''
    <!doctype html>
    <title>Natural Language Processing</title>
    <h1>Speech to Text</h1>
    <h3>Upload a audio file</h3>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/api', methods = ['GET'])
def returnAscii():
    d = {}
    return  { 'output': ord(str(request.args['query'])) }

if __name__ == "__main__":
    app.run(debug = True)