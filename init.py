import os
from flask import Flask, flash, request, redirect, url_for, session, jsonify, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

storage_path: Path = Path(__file__).parent / "storage"

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    if not storage_path.exists():
        storage_path.mkdir(exist_ok=True)
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([str(storage_path.as_posix()), filename])
    current_chunk = int(request.form['chunkindex'])
    if os.path.exists(destination) and current_chunk == 0:
        return make_response(('File already exists', 400))
    try:
        with open(destination, 'ab') as f:
            f.seek(int(request.form['chunkbyteoffset']))
            f.write(file.stream.read())
    except OSError:
        logging.exception('Could not write to file')
        return make_response(("Not sure why," "but we couldn't write the file to disk", 500))
    total_chunks = int(request.form['totalchunkcount'])
    if current_chunk == total_chunks:
        if os.path.getsize(destination) != int(request.form['totalfilesize']):
            logging.error(f"File {file.filename} was completed, "
                      f"but has a size mismatch."
                      f"Was {os.path.getsize(destination)} but we"
                      f" expected {request.form['totalfilesize']} ")
            return make_response(('Size mismatch', 500))
        else:
            logging.info(f'File {file.filename} has been uploaded successfully')
    else:
        logging.debug(f'Chunk {current_chunk} of {total_chunks} '
                  f'for file {file.filename} complete')
    return make_response(("Chunk upload successful", 200))

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0", port=5001, use_reloader=False)

flask_cors.CORS(app, expose_headers='Authorization')