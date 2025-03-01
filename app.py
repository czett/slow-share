from flask import Flask, render_template, request, redirect, send_file
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def start():
    files = list_files_in_folder(app.config['UPLOAD_FOLDER'])
    return render_template("index.html", files=files)

@app.route("/message/<m>")
def index_message(m):
    files = list_files_in_folder(app.config['UPLOAD_FOLDER'])
    return render_template("index.html", files=files, message=m)

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return redirect("/message/file_not_uploaded")
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect("/message/no_file_selected")
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect("/")
    
    return redirect("/message/internal_error")

@app.route("/delete/<file>")
def delete(file):
    os.remove(f"files/{file}")
    return redirect("/")

@app.route("/download/<file>")
def download(file):
    return send_file(f"files/{file}", as_attachment=True)

@app.errorhandler(Exception)
def handle_error(e):
    return redirect("/message/some_error")

def list_files_in_folder(folder):
    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        return files
    except FileNotFoundError:
        return redirect("/message/dir_not_found")

if __name__ == "__main__":
    app.run(debug=True, port=5400, host="0.0.0.0")
