from flask import Flask, render_template, request, flash, jsonify
from werkzeug.utils import secure_filename
import cv2
import os
import numpy as np

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cwebp": 
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": 
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass

def processImage2(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "brightness": 
           newFileName = f"static/{filename}" 
           alpha=2
           beta=50
           result=cv2.addWeighted(img,alpha,np.zeros(img.shape, img.dtype),0,beta)
           cv2.imwrite(newFileName, result)
           return newFileName
        case "sharpness": 
            newFileName = f"static/{filename}"
            gaussian_blur=cv2.GaussianBlur(img,(7,7),2)
            sharpenedImage=cv2.addWeighted(img,7.5,gaussian_blur,-6.5,0)
            cv2.imwrite(newFileName, sharpenedImage)
            return newFileName
        case "blurness": 
            newFileName = f"static/{filename}"
            blurredImage=cv2.GaussianBlur(img,(35,35),0)
            cv2.imwrite(newFileName, blurredImage)
            return newFileName
    pass


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/how", methods=["GET", "POST"])
def how():
    return render_template("how.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")

@app.route("/gradients", methods=["GET", "POST"])
def gradients():
    if request.method == "POST": 
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage2(filename, operation)
            flash(f"Your image has been processed and is available <a href='{new}' target='_blank'>here</a>")
            return render_template("gradients.html")
    return render_template("gradients.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    new = "result.html"
    if request.method == "POST": 
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='{new}' target='_blank'>here</a>")
            return render_template("index.html")

    return render_template("index.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    new = "result.html"
    if request.method == "POST": 
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='{new}' target='_blank'>here</a>")
            return render_template("index.html")

    return render_template("index.html")


app.run(debug=True)