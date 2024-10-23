from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def start():
    files = list_files_in_folder(app.config['UPLOAD_FOLDER'])
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "Keine Datei hochgeladen!"
    
    file = request.files['file']
    
    if file.filename == '':
        return "Keine Datei ausgewählt!"
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect("/")
    
    return "Fehler beim Hochladen der Datei!"

def list_files_in_folder(folder):
    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        return files
    except FileNotFoundError:
        return f"Der Ordner '{folder}' wurde nicht gefunden!"

if __name__ == "__main__":
    app.run(debug=True, port=5400)
