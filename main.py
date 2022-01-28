from flask import Flask, flash, render_template, \
    request, redirect, url_for, session
from werkzeug.utils import secure_filename
import secrets
import os
import text_to_tokens as tt


app = Flask(__name__)

LENGTH = 10

SECRET_KEY = secrets.token_urlsafe(LENGTH)
app.secret_key = SECRET_KEY

UPLOAD_EXTENSIONS = ['txt']
UPLOAD_FOLDER = os.path.join(os.getcwd(), r'Static\uploads')

# Setting which file types can be uploaded
app.config['UPLOAD_EXTENSIONS'] = UPLOAD_EXTENSIONS
# Setting path for uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_extensions(filename):
    extension = filename.split('.')
    extension = extension[-1]
    return extension in app.config['UPLOAD_EXTENSIONS']


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.files:
        doc = request.files["doc"]
        # User submitted empty file name
        if not doc:
            flash('Empty file provided', 'error')
            return redirect(url_for('index'))

        # User submitted file
        if doc:
            filename = secure_filename(doc.filename)
            # Saving filename in the server for the processing later
            session['filename'] = filename
            # File type is not supported
            if not allowed_extensions(filename):
                flash('Incompatible file extension', 'error')
                return redirect(url_for('index'))
            # Successful upload
            else:
                doc.save(os.path.join(os.path.join
                                      (app.config['UPLOAD_FOLDER'],
                                       filename)))
                flash('File saved successfully', 'success')

                return redirect(url_for('process_upload'))
    return render_template('index.html')


@app.route('/process_upload', methods=['GET'])
def process_upload():
    # A file was uploaded successfully to the server
    if 'filename' in session:
        filename = session['filename']
        path = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'],
                                         filename))
        doc = tt.load_doc(path)
        tokens = tt.clean_doc(doc)
        session['tokens'] = tokens
    return render_template('uploaded.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
