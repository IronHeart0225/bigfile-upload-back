import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from pathlib import Path
import pathlib

target = '/python_uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

storage_path: Path = Path(__file__).parent / "storage"

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def fileUpload():
    #target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not storage_path.exists():
        storage_path.mkdir(exist_ok=True)
    # if not os.path.isdir(target):
    #     os.mkdir(target)

    file = request.files['file'] 
    filename = secure_filename(file.filename)
    p = pathlib.PureWindowsPath(storage_path)
    destination="/".join([str(p.as_posix()), filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response="Whatever you wish too return"
    return response

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

flask_cors.CORS(app, expose_headers='Authorization')